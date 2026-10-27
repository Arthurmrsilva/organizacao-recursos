import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select, update

from banco import (
    auditoria_reservas,
    manutencoes,
    metadata,
    recursos,
    reservas,
    usuarios,
)
from servico_reservas import alterar_reserva, criar_reserva


class TestEdicaoReservas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(hour=14, minute=0, second=0, microsecond=0)

        self.fim = self.inicio + timedelta(hours=1)

        with self.engine.begin() as conexao:
            for usuario_id in (1, 2):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {usuario_id}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil="SOLICITANTE",
                        ativo=True,
                    )
                )

            for recurso_id, tipo, restrito in (
                (1, "SALA", False),
                (2, "SALA", False),
                (3, "SALA", True),
                (4, "PROFESSOR", False),
            ):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Recurso {recurso_id}",
                        tipo=tipo,
                        localizacao="Bloco A",
                        capacidade=30 if tipo == "SALA" else None,
                        competencia="Python" if tipo == "PROFESSOR" else None,
                        restrito=restrito,
                        ativo=True,
                    )
                )

        self.reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(),
        )

    def tearDown(self):
        self.engine.dispose()
        self.pasta.cleanup()

    def dados(self, **alteracoes):
        dados = {
            "recurso_id": "1",
            "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Finalidade original",
        }
        dados.update(alteracoes)
        return dados

    def buscar_reserva(self):
        with self.engine.connect() as conexao:
            return dict(
                conexao.execute(
                    select(reservas).where(
                        reservas.c.id == self.reserva_id
                    )
                ).mappings().one()
            )

    def listar_eventos(self):
        with self.engine.connect() as conexao:
            return [
                dict(evento)
                for evento in conexao.execute(
                    select(auditoria_reservas)
                    .where(
                        auditoria_reservas.c.reserva_id
                        == self.reserva_id
                    )
                    .order_by(auditoria_reservas.c.id)
                ).mappings().all()
            ]

    def conferir_recusa(
        self,
        dados,
        usuario_id=1,
        reserva_id=None,
    ):
        reserva_antes = self.buscar_reserva()
        eventos_antes = self.listar_eventos()

        with self.assertRaises(ValueError):
            alterar_reserva(
                self.engine,
                usuario_id,
                self.reserva_id if reserva_id is None else reserva_id,
                dados,
            )

        self.assertEqual(self.buscar_reserva(), reserva_antes)
        self.assertEqual(self.listar_eventos(), eventos_antes)

    def cadastrar_manutencao(self, inicio, fim, ativo=True):
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(manutencoes).values(
                    recurso_id=2,
                    usuario_id=1,
                    inicio=inicio,
                    fim=fim,
                    motivo="Manutenção de teste",
                    criado_em=datetime.now(),
                    ativo=ativo,
                )
            )

    def test_alterar_finalidade_e_registrar_antes_depois(self):
        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(finalidade="Finalidade atualizada"),
        )

        reserva = self.buscar_reserva()
        eventos = self.listar_eventos()

        self.assertEqual(
            reserva["finalidade"],
            "Finalidade atualizada",
        )
        self.assertEqual(reserva["status"], "APROVADA")
        self.assertEqual(reserva["inicio"], self.inicio)
        self.assertEqual(reserva["fim"], self.fim)
        self.assertEqual(len(eventos), 2)

        evento = eventos[-1]

        self.assertEqual(evento["acao"], "ALTERACAO")
        self.assertEqual(evento["usuario_id"], 1)
        self.assertEqual(evento["status_anterior"], "APROVADA")
        self.assertEqual(evento["status_novo"], "APROVADA")

        detalhes = json.loads(evento["detalhes"])

        self.assertEqual(
            detalhes["antes"]["finalidade"],
            "Finalidade original",
        )
        self.assertEqual(
            detalhes["depois"]["finalidade"],
            "Finalidade atualizada",
        )
        self.assertEqual(detalhes["antes"]["recurso_id"], 1)
        self.assertEqual(detalhes["depois"]["recurso_id"], 1)
        self.assertEqual(
            detalhes["depois"]["inicio"],
            self.inicio.isoformat(),
        )

    def test_alterar_periodo_da_propria_reserva(self):
        novo_inicio = self.inicio + timedelta(minutes=15)
        novo_fim = self.fim + timedelta(minutes=15)

        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(
                inicio=novo_inicio.strftime("%Y-%m-%dT%H:%M"),
                fim=novo_fim.strftime("%Y-%m-%dT%H:%M"),
            ),
        )

        reserva = self.buscar_reserva()

        self.assertEqual(reserva["inicio"], novo_inicio)
        self.assertEqual(reserva["fim"], novo_fim)

    def test_trocar_recurso_libera_recurso_anterior(self):
        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(recurso_id="2"),
        )

        nova_id = criar_reserva(
            self.engine,
            2,
            self.dados(),
        )

        self.assertEqual(self.buscar_reserva()["recurso_id"], 2)
        self.assertNotEqual(nova_id, self.reserva_id)

    def test_recurso_restrito_exige_nova_aprovacao(self):
        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(recurso_id="3"),
        )

        self.assertEqual(
            self.buscar_reserva()["status"],
            "SOLICITADA",
        )
        self.assertEqual(
            self.listar_eventos()[-1]["status_novo"],
            "SOLICITADA",
        )

    def test_professor_exige_aprovacao(self):
        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(recurso_id="4"),
        )

        self.assertEqual(
            self.buscar_reserva()["status"],
            "SOLICITADA",
        )

    def test_editar_restrito_aprovado_volta_para_solicitada(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == self.reserva_id)
                .values(recurso_id=3, status="APROVADA")
            )

        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(
                recurso_id="3",
                finalidade="Finalidade revisada",
            ),
        )

        self.assertEqual(
            self.buscar_reserva()["status"],
            "SOLICITADA",
        )

    def test_outro_usuario_nao_pode_editar(self):
        self.conferir_recusa(
            self.dados(finalidade="Alteração indevida"),
            usuario_id=2,
        )

    def test_usuario_inativo_nao_pode_editar(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(ativo=False)
            )

        self.conferir_recusa(
            self.dados(finalidade="Tentativa de alteração"),
        )

    def test_reserva_inexistente(self):
        self.conferir_recusa(
            self.dados(finalidade="Tentativa de alteração"),
            reserva_id=999,
        )

    def test_situacoes_que_nao_permitem_edicao(self):
        for status in (
            "EM_USO",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
            with self.subTest(status=status):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(reservas)
                        .where(reservas.c.id == self.reserva_id)
                        .values(status=status)
                    )

                self.conferir_recusa(
                    self.dados(finalidade="Tentativa de alteração"),
                )

    def test_reserva_que_ja_comecou_nao_pode_ser_editada(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == self.reserva_id)
                .values(
                    inicio=datetime.now() - timedelta(minutes=30),
                    fim=datetime.now() + timedelta(minutes=30),
                )
            )

        self.conferir_recusa(
            self.dados(finalidade="Tentativa de alteração"),
        )

    def test_finalidade_invalida(self):
        for finalidade in ("", "   ", "a" * 201):
            with self.subTest(finalidade=finalidade):
                self.conferir_recusa(
                    self.dados(finalidade=finalidade),
                )

    def test_recurso_invalido_ou_inexistente(self):
        for recurso_id in ("", "abc", "999"):
            with self.subTest(recurso_id=recurso_id):
                self.conferir_recusa(
                    self.dados(recurso_id=recurso_id),
                )

    def test_recurso_inativo(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 2)
                .values(ativo=False)
            )

        self.conferir_recusa(
            self.dados(recurso_id="2"),
        )

    def test_datas_invalidas(self):
        for campo in ("inicio", "fim"):
            with self.subTest(campo=campo):
                self.conferir_recusa(
                    self.dados(**{campo: "data-invalida"}),
                )

    def test_termino_igual_ou_anterior_ao_inicio(self):
        for fim in (
            self.inicio,
            self.inicio - timedelta(minutes=1),
        ):
            with self.subTest(fim=fim):
                self.conferir_recusa(
                    self.dados(
                        fim=fim.strftime("%Y-%m-%dT%H:%M"),
                    ),
                )

    def test_novo_periodo_no_passado(self):
        inicio = datetime.now() - timedelta(days=2)
        fim = inicio + timedelta(hours=1)

        self.conferir_recusa(
            self.dados(
                inicio=inicio.strftime("%Y-%m-%dT%H:%M"),
                fim=fim.strftime("%Y-%m-%dT%H:%M"),
            ),
        )

    def test_sem_alteracoes_nao_gera_evento(self):
        self.conferir_recusa(self.dados())

    def test_conflito_com_outra_reserva(self):
        criar_reserva(
            self.engine,
            2,
            self.dados(recurso_id="2"),
        )

        self.conferir_recusa(
            self.dados(recurso_id="2"),
        )

    def test_permitir_horario_consecutivo_a_outra_reserva(self):
        criar_reserva(
            self.engine,
            2,
            self.dados(recurso_id="2"),
        )

        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(
                recurso_id="2",
                inicio=self.fim.strftime("%Y-%m-%dT%H:%M"),
                fim=(
                    self.fim + timedelta(hours=1)
                ).strftime("%Y-%m-%dT%H:%M"),
            ),
        )

        reserva = self.buscar_reserva()

        self.assertEqual(reserva["recurso_id"], 2)
        self.assertEqual(reserva["inicio"], self.fim)

    def test_manutencao_bloqueia_edicao(self):
        self.cadastrar_manutencao(self.inicio, self.fim)

        self.conferir_recusa(
            self.dados(recurso_id="2"),
        )

    def test_manutencao_inativa_nao_bloqueia(self):
        self.cadastrar_manutencao(
            self.inicio,
            self.fim,
            ativo=False,
        )

        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(recurso_id="2"),
        )

        self.assertEqual(self.buscar_reserva()["recurso_id"], 2)

    def test_permitir_inicio_no_fim_da_manutencao(self):
        self.cadastrar_manutencao(
            self.inicio - timedelta(hours=1),
            self.inicio,
        )

        alterar_reserva(
            self.engine,
            1,
            self.reserva_id,
            self.dados(recurso_id="2"),
        )

        self.assertEqual(self.buscar_reserva()["recurso_id"], 2)

    def test_falha_na_auditoria_desfaz_alteracao(self):
        reserva_antes = self.buscar_reserva()
        eventos_antes = self.listar_eventos()

        with patch(
            "servico_reservas.registrar_auditoria",
            side_effect=RuntimeError("Falha simulada na auditoria"),
        ):
            with self.assertRaises(RuntimeError):
                alterar_reserva(
                    self.engine,
                    1,
                    self.reserva_id,
                    self.dados(finalidade="Não deve ser salva"),
                )

        self.assertEqual(self.buscar_reserva(), reserva_antes)
        self.assertEqual(self.listar_eventos(), eventos_antes)


if __name__ == "__main__":
    unittest.main()