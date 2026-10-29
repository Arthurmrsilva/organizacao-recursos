from datetime import datetime

from sqlalchemy import select, update

from banco import recursos, reservas, usuarios
from servico_reservas import (
    registrar_auditoria,
    verificar_manutencao,
)


def registrar_retirada(engine, usuario_id, reserva_id):
    movimentar_material(
        engine,
        usuario_id,
        reserva_id,
        "RETIRADA",
    )


def registrar_devolucao(engine, usuario_id, reserva_id):
    movimentar_material(
        engine,
        usuario_id,
        reserva_id,
        "DEVOLUCAO",
    )


def registrar_nao_comparecimento(engine, usuario_id, reserva_id):
    movimentar_material(
        engine,
        usuario_id,
        reserva_id,
        "NAO_COMPARECEU",
    )


def movimentar_material(engine, usuario_id, reserva_id, acao):
    if acao not in (
        "RETIRADA",
        "DEVOLUCAO",
        "NAO_COMPARECEU",
    ):
        raise ValueError("Selecione uma operação válida.")

    with engine.connect() as conexao:
        try:
            # Serializa as gravações no SQLite.
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            usuario = conexao.execute(
                select(usuarios).where(
                    usuarios.c.id == usuario_id,
                    usuarios.c.ativo.is_(True),
                )
            ).mappings().first()

            if (
                usuario is None
                or usuario["perfil"] not in ("ADMIN", "RESPONSAVEL")
            ):
                raise ValueError(
                    "Somente administradores ou responsáveis "
                    "podem registrar retirada e devolução."
                )

            reserva = conexao.execute(
                select(reservas).where(
                    reservas.c.id == reserva_id
                )
            ).mappings().first()

            if reserva is None:
                raise ValueError("Reserva não encontrada.")

            recurso = conexao.execute(
                select(recursos).where(
                    recursos.c.id == reserva["recurso_id"]
                )
            ).mappings().first()

            if recurso is None or recurso["tipo"] != "MATERIAL":
                raise ValueError(
                    "Esta operação é exclusiva para materiais."
                )

            if (
                usuario["perfil"] == "RESPONSAVEL"
                and recurso["responsavel_id"] != usuario_id
            ):
                raise ValueError(
                    "Você não é o responsável por este recurso."
                )

            agora = datetime.now()

            if acao == "RETIRADA":
                if reserva["status"] != "APROVADA":
                    raise ValueError(
                        "Somente reservas aprovadas permitem retirada."
                    )

                if not recurso["ativo"]:
                    raise ValueError(
                        "Não é possível retirar um material inativo."
                    )

                if agora < reserva["inicio"]:
                    raise ValueError(
                        "A retirada só pode ocorrer a partir "
                        "do início da reserva."
                    )

                if agora >= reserva["fim"]:
                    raise ValueError(
                        "O período para retirada já terminou."
                    )

                verificar_manutencao(
                    conexao,
                    recurso["id"],
                    agora,
                    reserva["fim"],
                )

                # Impede nova retirada se o material ainda estiver
                # com outro usuário, mesmo após o prazo de devolução.
                outro_uso = conexao.execute(
                    select(reservas.c.id).where(
                        reservas.c.recurso_id == recurso["id"],
                        reservas.c.id != reserva_id,
                        reservas.c.status == "EM_USO",
                    ).limit(1)
                ).first()

                if outro_uso is not None:
                    raise ValueError(
                        "O material ainda está em uso em outra reserva. "
                        "Registre a devolução antes de uma nova retirada."
                    )

                status_novo = "EM_USO"

            elif acao == "DEVOLUCAO":
                if reserva["status"] != "EM_USO":
                    raise ValueError(
                        "Somente materiais em uso podem ser devolvidos."
                    )

                # Permite a devolução mesmo após o prazo ou
                # se o recurso tiver sido desativado.
                status_novo = "CONCLUIDA"

            else:
                if reserva["status"] != "APROVADA":
                    raise ValueError(
                        "Somente reservas aprovadas permitem "
                        "registrar não comparecimento."
                    )

                if agora < reserva["fim"]:
                    raise ValueError(
                        "O não comparecimento só pode ser registrado "
                        "após o encerramento do período da reserva."
                    )

                # Não altera reservas EM_USO: nesses casos,
                # é necessário registrar a devolução.
                # Recurso inativo não impede o registro histórico.
                status_novo = "NAO_COMPARECEU"

            conexao.execute(
                update(reservas)
                .where(reservas.c.id == reserva_id)
                .values(status=status_novo)
            )

            registrar_auditoria(
                conexao=conexao,
                reserva_id=reserva_id,
                usuario_id=usuario_id,
                acao=acao,
                status_anterior=reserva["status"],
                status_novo=status_novo,
            )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise