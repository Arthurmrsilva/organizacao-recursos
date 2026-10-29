import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select, update

import app as aplicativo
from banco import (
    auditoria_reservas,
    metadata,
    recursos,
    reservas,
    usuarios,
)


class TestNaoComparecimentoHTTP(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        agora = datetime.now()

        with self.engine.begin() as conexao:
            for usuario_id, perfil, ativo in (
                (1, "ADMIN", True),
                (2, "RESPONSAVEL", True),
                (3, "RESPONSAVEL", True),
                (4, "SOLICITANTE", True),
                (5, "ADMIN", False),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {usuario_id}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=ativo,
                    )
                )

            conexao.execute(
                insert(recursos).values(
                    id=1,
                    nome="Projetor para não comparecimento",
                    tipo="MATERIAL",
                    localizacao="Bloco A",
                    restrito=False,
                    ativo=True,
                    responsavel_id=2,
                )
            )

            conexao.execute(
                insert(reservas).values(
                    id=1,
                    recurso_id=1,
                    usuario_id=4,
                    inicio=agora - timedelta(days=2),
                    fim=agora - timedelta(days=1),
                    finalidade="Apresentação de trabalho",
                    status="APROVADA",
                )
            )

        substituicao = patch.object(
            aplicativo,
            "engine",
            self.engine,
        )
        substituicao.start()
        self.addCleanup(substituicao.stop)

        self.cliente = aplicativo.app.test_client()

    def autenticar(self, usuario_id):
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["usuario_id"] = usuario_id
            sessao["csrf_token"] = "token-teste"

    def enviar(self, reserva_id=1):
        return self.cliente.post(
            f"/materiais/{reserva_id}/movimentar",
            data={
                "csrf_token": "token-teste",
                "acao": "NAO_COMPARECEU",
            },
        )

    def alterar_reserva(self, **valores):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == 1)
                .values(**valores)
            )

    def consultar_status(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(reservas.c.status).where(
                    reservas.c.id == 1
                )
            ).scalar_one()

    def consultar_eventos(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(auditoria_reservas).order_by(
                    auditoria_reservas.c.id
                )
            ).mappings().all()

    def conferir_redirecionamento(self, resposta, destino):
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith(destino))

    def conferir_sem_alteracao(self, status="APROVADA"):
        self.assertEqual(self.consultar_status(), status)
        self.assertEqual(self.consultar_eventos(), [])

    def conferir_sucesso(self, usuario_id):
        self.assertEqual(
            self.consultar_status(),
            "NAO_COMPARECEU",
        )

        eventos = self.consultar_eventos()

        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["reserva_id"], 1)
        self.assertEqual(
            eventos[0]["usuario_id"],
            usuario_id,
        )
        self.assertEqual(
            eventos[0]["acao"],
            "NAO_COMPARECEU",
        )
        self.assertEqual(
            eventos[0]["status_anterior"],
            "APROVADA",
        )
        self.assertEqual(
            eventos[0]["status_novo"],
            "NAO_COMPARECEU",
        )

    def test_operacao_exige_login(self):
        with self.cliente.session_transaction() as sessao:
            sessao["csrf_token"] = "token-teste"

        resposta = self.enviar()

        self.conferir_redirecionamento(resposta, "/login")
        self.conferir_sem_alteracao()

    def test_solicitante_nao_registra(self):
        self.autenticar(4)

        resposta = self.enviar()

        self.assertEqual(resposta.status_code, 403)
        self.conferir_sem_alteracao()

    def test_usuario_inativo_nao_registra(self):
        self.autenticar(5)

        resposta = self.enviar()

        self.conferir_redirecionamento(resposta, "/login")
        self.conferir_sem_alteracao()

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

    def test_admin_registra_e_apresenta_mensagem(self):
        self.autenticar(1)

        resposta = self.enviar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sucesso(1)

        resposta = self.cliente.get("/materiais")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "Não comparecimento da reserva nº 1 registrado!",
            pagina,
        )
        self.assertNotIn(
            "Projetor para não comparecimento",
            pagina,
        )

    def test_responsavel_vinculado_registra(self):
        self.autenticar(2)

        resposta = self.enviar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sucesso(2)

    def test_responsavel_alheio_nao_registra(self):
        self.autenticar(3)

        resposta = self.enviar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sem_alteracao()

        with self.cliente.session_transaction() as sessao:
            self.assertTrue(sessao.get("erro_material"))
            self.assertNotIn("mensagem_material", sessao)

    def test_csrf_ausente_ou_incorreto_bloqueia(self):
        for token in (None, "incorreto"):
            with self.subTest(token=token):
                self.autenticar(1)
                dados = {"acao": "NAO_COMPARECEU"}

                if token is not None:
                    dados["csrf_token"] = token

                resposta = self.cliente.post(
                    "/materiais/1/movimentar",
                    data=dados,
                )

                self.assertEqual(resposta.status_code, 400)
                self.conferir_sem_alteracao()

    def test_antes_do_termino_recusa_e_oculta_botao(self):
        self.alterar_reserva(
            fim=datetime.now() + timedelta(days=1)
        )
        self.autenticar(1)

        pagina = self.cliente.get(
            "/materiais"
        ).get_data(as_text=True)

        self.assertNotIn('value="NAO_COMPARECEU"', pagina)

        resposta = self.enviar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sem_alteracao()

        pagina = self.cliente.get(
            "/materiais"
        ).get_data(as_text=True)

        self.assertIn(
            "O não comparecimento só pode ser registrado "
            "após o encerramento do período da reserva.",
            pagina,
        )

    def test_em_uso_nao_permite_nao_comparecimento(self):
        self.alterar_reserva(status="EM_USO")
        self.autenticar(1)

        pagina = self.cliente.get(
            "/materiais"
        ).get_data(as_text=True)

        self.assertIn('value="DEVOLUCAO"', pagina)
        self.assertNotIn('value="NAO_COMPARECEU"', pagina)

        resposta = self.enviar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sem_alteracao(status="EM_USO")

    def test_botao_disponivel_mesmo_com_material_inativo(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        self.autenticar(2)

        resposta = self.cliente.get("/materiais")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "Registrar não comparecimento",
            pagina,
        )
        self.assertIn('value="NAO_COMPARECEU"', pagina)
        self.assertIn('name="csrf_token"', pagina)

        resposta = self.enviar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sucesso(2)

    def test_repeticao_nao_duplica_evento(self):
        self.autenticar(1)

        primeira = self.enviar()
        segunda = self.enviar()

        self.conferir_redirecionamento(
            primeira,
            "/materiais",
        )
        self.conferir_redirecionamento(
            segunda,
            "/materiais",
        )
        self.conferir_sucesso(1)

        with self.cliente.session_transaction() as sessao:
            self.assertTrue(sessao.get("erro_material"))

    def test_reserva_inexistente_nao_altera_dados(self):
        self.autenticar(1)

        resposta = self.enviar(reserva_id=999)

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.conferir_sem_alteracao()

        pagina = self.cliente.get(
            "/materiais"
        ).get_data(as_text=True)

        self.assertIn("Reserva não encontrada.", pagina)


if __name__ == "__main__":
    unittest.main()