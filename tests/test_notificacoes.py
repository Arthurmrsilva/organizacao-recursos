import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select

import app as aplicativo
from banco import (
    auditoria_reservas,
    metadata,
    notificacoes,
    recursos,
    reservas,
    usuarios,
)
from servico_reservas import (
    alterar_reserva,
    avaliar_reserva,
    cancelar_reserva,
    criar_reserva,
)


class TestNotificacoes(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)

        metadata.create_all(self.engine)

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(hour=14, minute=0, second=0, microsecond=0)
        self.fim = self.inicio + timedelta(hours=1)
        self.token = "token-csrf-notificacoes"

        with self.engine.begin() as conexao:
            for usuario_id, perfil in (
                (1, "SOLICITANTE"),
                (2, "SOLICITANTE"),
                (3, "RESPONSAVEL"),
                (4, "ADMIN"),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {usuario_id}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=True,
                    )
                )

            for recurso_id, restrito in ((1, False), (2, True)):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Sala {recurso_id}",
                        tipo="SALA",
                        localizacao="Bloco A",
                        capacidade=30,
                        restrito=restrito,
                        responsavel_id=3 if restrito else None,
                        ativo=True,
                    )
                )

        troca_engine = patch.object(
            aplicativo,
            "engine",
            self.engine,
        )
        troca_engine.start()
        self.addCleanup(troca_engine.stop)

        self.cliente = aplicativo.app.test_client()

    def dados(self, **alteracoes):
        dados = {
            "recurso_id": "1",
            "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Teste de notificações",
        }
        dados.update(alteracoes)
        return dados

    def autenticar(self, usuario_id=1):
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["csrf_token"] = self.token

            if usuario_id is not None:
                sessao["usuario_id"] = usuario_id

    def listar(self, tabela):
        with self.engine.connect() as conexao:
            return [
                dict(registro)
                for registro in conexao.execute(
                    select(tabela).order_by(tabela.c.id)
                ).mappings().all()
            ]

    def criar_aviso(
        self,
        usuario_id=1,
        mensagem="Aviso exclusivo do usuário 1",
        criado_em=None,
    ):
        with self.engine.begin() as conexao:
            resultado = conexao.execute(
                insert(reservas).values(
                    recurso_id=1,
                    usuario_id=usuario_id,
                    inicio=self.inicio,
                    fim=self.fim,
                    finalidade="Reserva para teste de aviso",
                    status="APROVADA",
                )
            )
            reserva_id = resultado.inserted_primary_key[0]

            resultado = conexao.execute(
                insert(notificacoes).values(
                    usuario_id=usuario_id,
                    reserva_id=reserva_id,
                    mensagem=mensagem,
                    criado_em=criado_em or datetime.now(),
                    lida=False,
                )
            )

            return resultado.inserted_primary_key[0]

    def test_criacao_comum_gera_aviso_nao_lido(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(),
        )

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]["usuario_id"], 1)
        self.assertEqual(avisos[0]["reserva_id"], reserva_id)
        self.assertFalse(avisos[0]["lida"])
        self.assertIn(
            "aprovada automaticamente",
            avisos[0]["mensagem"],
        )

    def test_criacao_restrita_informa_aguardo(self):
        criar_reserva(
            self.engine,
            1,
            self.dados(recurso_id="2"),
        )

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]["usuario_id"], 1)
        self.assertIn(
            "aguardando aprovação",
            avisos[0]["mensagem"],
        )

    def test_edicao_gera_novo_aviso(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(),
        )

        alterar_reserva(
            self.engine,
            1,
            reserva_id,
            self.dados(finalidade="Finalidade revisada"),
        )

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 2)
        self.assertEqual(avisos[-1]["usuario_id"], 1)
        self.assertEqual(avisos[-1]["reserva_id"], reserva_id)
        self.assertIn("alterada", avisos[-1]["mensagem"])
        self.assertIn("está aprovada", avisos[-1]["mensagem"])

    def test_edicao_restrita_informa_nova_aprovacao(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(recurso_id="2"),
        )

        alterar_reserva(
            self.engine,
            1,
            reserva_id,
            self.dados(
                recurso_id="2",
                finalidade="Finalidade revisada",
            ),
        )

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 2)
        self.assertIn(
            "aguardando nova aprovação",
            avisos[-1]["mensagem"],
        )

    def test_cancelamento_gera_aviso(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(),
        )

        cancelar_reserva(self.engine, 1, reserva_id)

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 2)
        self.assertEqual(avisos[-1]["usuario_id"], 1)
        self.assertEqual(
            avisos[-1]["mensagem"],
            f"Reserva nº {reserva_id} cancelada.",
        )

    def test_aprovacao_notifica_solicitante(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(recurso_id="2"),
        )

        avaliar_reserva(
            self.engine,
            3,
            reserva_id,
            "APROVADA",
        )

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 2)
        self.assertEqual(avisos[-1]["usuario_id"], 1)
        self.assertIn(
            "aprovada pelo responsável",
            avisos[-1]["mensagem"],
        )
        self.assertTrue(
            all(aviso["usuario_id"] != 3 for aviso in avisos)
        )

    def test_rejeicao_notifica_solicitante(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(recurso_id="2"),
        )

        avaliar_reserva(
            self.engine,
            3,
            reserva_id,
            "REJEITADA",
        )

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 2)
        self.assertEqual(avisos[-1]["usuario_id"], 1)
        self.assertIn(
            "rejeitada pelo responsável",
            avisos[-1]["mensagem"],
        )

    def test_conflito_nao_gera_aviso_extra(self):
        criar_reserva(self.engine, 1, self.dados())

        antes = self.listar(notificacoes)

        with self.assertRaises(ValueError):
            criar_reserva(self.engine, 2, self.dados())

        self.assertEqual(self.listar(notificacoes), antes)
        self.assertEqual(len(self.listar(reservas)), 1)
        self.assertEqual(len(self.listar(auditoria_reservas)), 1)

    def test_falha_no_aviso_desfaz_criacao_e_auditoria(self):
        with patch(
            "servico_reservas.registrar_notificacao",
            side_effect=RuntimeError("Falha simulada no aviso"),
        ):
            with self.assertRaises(RuntimeError):
                criar_reserva(self.engine, 1, self.dados())

        self.assertEqual(self.listar(reservas), [])
        self.assertEqual(self.listar(auditoria_reservas), [])
        self.assertEqual(self.listar(notificacoes), [])

    def test_falha_no_aviso_desfaz_edicao_e_auditoria(self):
        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados(),
        )

        reservas_antes = self.listar(reservas)
        eventos_antes = self.listar(auditoria_reservas)
        avisos_antes = self.listar(notificacoes)

        with patch(
            "servico_reservas.registrar_notificacao",
            side_effect=RuntimeError("Falha simulada no aviso"),
        ):
            with self.assertRaises(RuntimeError):
                alterar_reserva(
                    self.engine,
                    1,
                    reserva_id,
                    self.dados(finalidade="Não deve ser salva"),
                )

        self.assertEqual(self.listar(reservas), reservas_antes)
        self.assertEqual(
            self.listar(auditoria_reservas),
            eventos_antes,
        )
        self.assertEqual(
            self.listar(notificacoes),
            avisos_antes,
        )

    def test_falha_no_aviso_desfaz_cancelamento_e_avaliacao(self):
        casos = (
            ("CANCELAMENTO", "1"),
            ("APROVADA", "2"),
            ("REJEITADA", "2"),
        )

        for indice, (acao, recurso_id) in enumerate(casos):
            with self.subTest(acao=acao):
                inicio = self.inicio + timedelta(days=indice)
                fim = inicio + timedelta(hours=1)

                reserva_id = criar_reserva(
                    self.engine,
                    1,
                    self.dados(
                        recurso_id=recurso_id,
                        inicio=inicio.strftime("%Y-%m-%dT%H:%M"),
                        fim=fim.strftime("%Y-%m-%dT%H:%M"),
                    ),
                )

                reservas_antes = self.listar(reservas)
                eventos_antes = self.listar(auditoria_reservas)
                avisos_antes = self.listar(notificacoes)

                with patch(
                    "servico_reservas.registrar_notificacao",
                    side_effect=RuntimeError("Falha simulada"),
                ):
                    with self.assertRaises(RuntimeError):
                        if acao == "CANCELAMENTO":
                            cancelar_reserva(
                                self.engine,
                                1,
                                reserva_id,
                            )
                        else:
                            avaliar_reserva(
                                self.engine,
                                3,
                                reserva_id,
                                acao,
                            )

                self.assertEqual(
                    self.listar(reservas),
                    reservas_antes,
                )
                self.assertEqual(
                    self.listar(auditoria_reservas),
                    eventos_antes,
                )
                self.assertEqual(
                    self.listar(notificacoes),
                    avisos_antes,
                )

    def test_consulta_exige_login(self):
        resposta = self.cliente.get("/notificacoes")

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_marcacao_exige_login(self):
        aviso_id = self.criar_aviso()
        self.autenticar(usuario_id=None)

        resposta = self.cliente.post(
            f"/notificacoes/{aviso_id}/ler",
            data={"csrf_token": self.token},
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))
        self.assertFalse(self.listar(notificacoes)[0]["lida"])

    def test_usuario_consulta_somente_proprios_avisos(self):
        self.criar_aviso(
            usuario_id=1,
            mensagem="Mensagem privada da pessoa um",
        )
        self.criar_aviso(
            usuario_id=2,
            mensagem="Mensagem privada da pessoa dois",
        )

        for usuario_id, propria, outra in (
            (1, "Mensagem privada da pessoa um",
             "Mensagem privada da pessoa dois"),
            (2, "Mensagem privada da pessoa dois",
             "Mensagem privada da pessoa um"),
        ):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.get("/notificacoes")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(propria, pagina)
                self.assertNotIn(outra, pagina)

    def test_lista_vazia(self):
        self.autenticar(1)

        resposta = self.cliente.get("/notificacoes")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "Você ainda não possui notificações.",
            resposta.get_data(as_text=True),
        )

    def test_marcar_proprio_aviso_e_persistir_leitura(self):
        aviso_id = self.criar_aviso()
        self.autenticar(1)

        resposta = self.cliente.post(
            f"/notificacoes/{aviso_id}/ler",
            data={"csrf_token": self.token},
            follow_redirects=True,
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Notificação marcada como lida.", pagina)
        self.assertIn("Notificação lida", pagina)
        self.assertNotIn("Marcar como lida", pagina)
        self.assertTrue(self.listar(notificacoes)[0]["lida"])

        atualizacao = self.cliente.get("/notificacoes")
        pagina = atualizacao.get_data(as_text=True)

        self.assertIn("Notificação lida", pagina)
        self.assertNotIn("Marcar como lida", pagina)
        self.assertEqual(len(self.listar(notificacoes)), 1)

    def test_outro_usuario_e_admin_nao_marcam_aviso_alheio(self):
        aviso_id = self.criar_aviso(usuario_id=1)

        for usuario_id in (2, 3, 4):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.post(
                    f"/notificacoes/{aviso_id}/ler",
                    data={"csrf_token": self.token},
                )

                self.assertEqual(resposta.status_code, 404)
                self.assertFalse(
                    self.listar(notificacoes)[0]["lida"]
                )

    def test_aviso_inexistente_retorna_404(self):
        self.autenticar(1)

        resposta = self.cliente.post(
            "/notificacoes/999/ler",
            data={"csrf_token": self.token},
        )

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(self.listar(notificacoes), [])

    def test_csrf_ausente_ou_incorreto_nao_marca(self):
        aviso_id = self.criar_aviso()
        self.autenticar(1)

        for dados in ({}, {"csrf_token": "incorreto"}):
            with self.subTest(dados=dados):
                resposta = self.cliente.post(
                    f"/notificacoes/{aviso_id}/ler",
                    data=dados,
                )

                self.assertEqual(resposta.status_code, 400)
                self.assertFalse(
                    self.listar(notificacoes)[0]["lida"]
                )

    def test_get_nao_pode_marcar_como_lida(self):
        aviso_id = self.criar_aviso()
        self.autenticar(1)

        resposta = self.cliente.get(
            f"/notificacoes/{aviso_id}/ler"
        )

        self.assertEqual(resposta.status_code, 405)
        self.assertFalse(self.listar(notificacoes)[0]["lida"])

    def test_marcar_duas_vezes_nao_duplica_aviso(self):
        aviso_id = self.criar_aviso()
        self.autenticar(1)

        for _ in range(2):
            resposta = self.cliente.post(
                f"/notificacoes/{aviso_id}/ler",
                data={"csrf_token": self.token},
            )

            self.assertEqual(resposta.status_code, 302)

        avisos = self.listar(notificacoes)

        self.assertEqual(len(avisos), 1)
        self.assertTrue(avisos[0]["lida"])

    def test_ordenacao_por_data_e_id_decrescentes(self):
        momento = datetime.now()

        self.criar_aviso(
            mensagem="Aviso-antigo-teste",
            criado_em=momento - timedelta(days=1),
        )
        self.criar_aviso(
            mensagem="Aviso-recente-primeiro-teste",
            criado_em=momento,
        )
        self.criar_aviso(
            mensagem="Aviso-recente-segundo-teste",
            criado_em=momento,
        )
        self.autenticar(1)

        resposta = self.cliente.get("/notificacoes")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertLess(
            pagina.index("Aviso-recente-segundo-teste"),
            pagina.index("Aviso-recente-primeiro-teste"),
        )
        self.assertLess(
            pagina.index("Aviso-recente-primeiro-teste"),
            pagina.index("Aviso-antigo-teste"),
        )

    def test_mensagem_html_e_exibida_com_escape(self):
        self.criar_aviso(
            mensagem="<script>alert('teste')</script>",
        )
        self.autenticar(1)

        resposta = self.cliente.get("/notificacoes")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn("<script>alert(", pagina)
        self.assertIn("&lt;script&gt;", pagina)

    def test_botao_notificacoes_disponivel_para_todos_os_perfis(self):
        for usuario_id in (1, 3, 4):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.get("/")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn('href="/notificacoes"', pagina)


if __name__ == "__main__":
    unittest.main()