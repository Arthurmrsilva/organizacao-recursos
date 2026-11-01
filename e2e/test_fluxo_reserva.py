import importlib
import re
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from playwright.sync_api import expect, sync_playwright
from sqlalchemy import create_engine, insert, select
from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server


PASTA_PROJETO = Path(__file__).resolve().parents[1]

if str(PASTA_PROJETO) not in sys.path:
    sys.path.insert(0, str(PASTA_PROJETO))

import banco


class TestFluxoReservaNavegador(unittest.TestCase):
    def test_login_criacao_conflito_e_cancelamento(self):
        # Execute este arquivo em um processo separado.
        # O app precisa ser importado somente após trocar o engine.
        self.assertNotIn(
            "app",
            sys.modules,
            "Execute somente a suíte da pasta e2e neste processo.",
        )

        with tempfile.TemporaryDirectory(
            prefix="organizacao_e2e_"
        ) as pasta:
            caminho = Path(pasta) / "teste.db"

            engine_teste = create_engine(
                f"sqlite:///{caminho.as_posix()}",
                connect_args={"check_same_thread": False},
            )
            self.addCleanup(engine_teste.dispose)

            try:
                banco.metadata.create_all(engine_teste)

                with engine_teste.begin() as conexao:
                    resultado = conexao.execute(
                        insert(banco.usuarios).values(
                            nome="Solicitante E2E",
                            login="solicitante_e2e",
                            senha_hash=generate_password_hash(
                                "Senha-E2E-123!"
                            ),
                            perfil="SOLICITANTE",
                            ativo=True,
                        )
                    )
                    usuario_id = resultado.inserted_primary_key[0]

                    resultado = conexao.execute(
                        insert(banco.recursos).values(
                            nome="Sala E2E",
                            tipo="SALA",
                            localizacao="Ambiente de testes",
                            capacidade=20,
                            restrito=False,
                            ativo=True,
                        )
                    )
                    recurso_id = resultado.inserted_primary_key[0]

                # criar_tabelas(), chamado ao importar app.py,
                # também utilizará o banco temporário.
                with patch.object(banco, "engine", engine_teste):
                    modulo_app = importlib.import_module("app")

                    self.assertIs(
                        modulo_app.engine,
                        engine_teste,
                    )

                    modulo_app.app.config.update(
                        SECRET_KEY="chave-exclusiva-do-teste-e2e",
                        TESTING=False,
                        DEBUG=False,
                    )

                    servidor = make_server(
                        "127.0.0.1",
                        0,
                        modulo_app.app,
                        threaded=True,
                    )

                    thread = threading.Thread(
                        target=servidor.serve_forever,
                        daemon=True,
                    )
                    thread.start()

                    endereco = (
                        f"http://127.0.0.1:{servidor.server_port}"
                    )

                    try:
                        self._executar_fluxo(
                            endereco,
                            recurso_id,
                        )

                        self._conferir_persistencia(
                            engine_teste,
                            usuario_id,
                            recurso_id,
                        )
                    finally:
                        servidor.shutdown()
                        thread.join()
                        servidor.server_close()
            finally:
                # Fecha as conexões antes de remover a pasta,
                # inclusive no Windows.
                engine_teste.dispose()

    def _executar_fluxo(self, endereco, recurso_id):
        inicio = (
            datetime.now() + timedelta(days=2)
        ).replace(hour=14, minute=0, second=0, microsecond=0)

        fim = inicio + timedelta(hours=1)

        with sync_playwright() as playwright:
            navegador = playwright.chromium.launch(
                headless=False,
                slow_mo=150,
            )

            try:
                contexto = navegador.new_context(
                    viewport={
                        "width": 1280,
                        "height": 900,
                    }
                )
                pagina = contexto.new_page()
                pagina.set_default_timeout(10000)

                # Acesso sem sessão deve levar ao login.
                pagina.goto(f"{endereco}/reservas")

                expect(pagina).to_have_url(
                    f"{endereco}/login"
                )

                # Login inválido deve exibir uma mensagem.
                pagina.get_by_label(
                    "Login",
                    exact=True,
                ).fill("solicitante_e2e")

                pagina.get_by_label(
                    "Senha",
                    exact=True,
                ).fill("senha-incorreta")

                pagina.get_by_role(
                    "button",
                    name="Entrar",
                    exact=True,
                ).click()

                expect(
                    pagina.get_by_role("alert")
                ).to_have_text(
                    "Login ou senha inválidos."
                )

                # Login correto.
                pagina.get_by_label(
                    "Login",
                    exact=True,
                ).fill("solicitante_e2e")

                pagina.get_by_label(
                    "Senha",
                    exact=True,
                ).fill("Senha-E2E-123!")

                pagina.get_by_role(
                    "button",
                    name="Entrar",
                    exact=True,
                ).click()

                expect(pagina).to_have_url(
                    f"{endereco}/"
                )

                # Criação pelo formulário real.
                pagina.goto(
                    f"{endereco}/reservas/nova"
                )

                self._preencher_reserva(
                    pagina,
                    recurso_id,
                    inicio,
                    fim,
                    "Reserva criada pelo teste de navegador",
                )

                pagina.get_by_role(
                    "button",
                    name="Reservar",
                    exact=True,
                ).click()

                expect(
                    pagina.get_by_role("status")
                ).to_contain_text(
                    "registrada com sucesso!"
                )

                # A reserva precisa aparecer em Minhas reservas.
                pagina.goto(f"{endereco}/reservas")

                cartao = pagina.locator(
                    "article.recurso"
                ).filter(
                    has=pagina.get_by_role(
                        "heading",
                        name="Sala E2E",
                        exact=True,
                    )
                )

                expect(cartao).to_have_count(1)
                expect(cartao).to_contain_text(
                    "Reserva criada pelo teste de navegador"
                )
                expect(cartao).to_contain_text(
                    "Aprovada"
                )

                # Segunda tentativa sobreposta deve ser recusada.
                pagina.get_by_role(
                    "link",
                    name="+ Fazer reserva",
                    exact=True,
                ).click()

                self._preencher_reserva(
                    pagina,
                    recurso_id,
                    inicio,
                    fim,
                    "Tentativa de reserva sobreposta",
                )

                pagina.get_by_role(
                    "button",
                    name="Reservar",
                    exact=True,
                ).click()

                expect(
                    pagina.get_by_role("alert")
                ).to_contain_text(
                    "Já existe uma reserva para esse recurso "
                    "no período informado."
                )

                # Volta à listagem para cancelar a reserva original.
                pagina.goto(f"{endereco}/reservas")

                cartao = pagina.locator(
                    "article.recurso"
                ).filter(
                    has=pagina.get_by_role(
                        "heading",
                        name="Sala E2E",
                        exact=True,
                    )
                )

                # Confere e aceita o confirm() do navegador.
                def confirmar_cancelamento(dialogo):
                    self.assertEqual(
                        dialogo.type,
                        "confirm",
                    )
                    self.assertEqual(
                        dialogo.message,
                        "Deseja cancelar esta reserva?",
                    )
                    dialogo.accept()

                pagina.once(
                    "dialog",
                    confirmar_cancelamento,
                )

                cartao.get_by_role(
                    "button",
                    name="Cancelar reserva",
                    exact=True,
                ).click()

                expect(
                    pagina.get_by_role("status")
                ).to_contain_text(
                    "cancelada com sucesso!"
                )

                expect(
                    pagina.locator("article.recurso")
                ).to_have_count(0)

                # Cancelamento deve preservar a reserva no histórico.
                pagina.get_by_role(
                    "link",
                    name="Histórico",
                    exact=True,
                ).click()

                expect(pagina).to_have_url(
                    re.compile(
                        r"/reservas\?filtro=historico$"
                    )
                )

                historico = pagina.locator(
                    "article.recurso"
                )

                expect(historico).to_have_count(1)
                expect(historico).to_contain_text(
                    "Sala E2E"
                )
                expect(historico).to_contain_text(
                    "Cancelada"
                )

                expect(
                    historico.get_by_role(
                        "button",
                        name="Cancelar reserva",
                        exact=True,
                    )
                ).to_have_count(0)
            finally:
                navegador.close()

    @staticmethod
    def _preencher_reserva(
        pagina,
        recurso_id,
        inicio,
        fim,
        finalidade,
    ):
        pagina.get_by_label(
            "Recurso",
            exact=True,
        ).select_option(str(recurso_id))

        pagina.get_by_label(
            "Data e horário de início",
            exact=True,
        ).fill(
            inicio.strftime("%Y-%m-%dT%H:%M")
        )

        pagina.get_by_label(
            "Data e horário de término",
            exact=True,
        ).fill(
            fim.strftime("%Y-%m-%dT%H:%M")
        )

        pagina.get_by_label(
            "Finalidade da reserva",
            exact=True,
        ).fill(finalidade)

    def _conferir_persistencia(
        self,
        engine_teste,
        usuario_id,
        recurso_id,
    ):
        # Complementa o fluxo visual com a conferência dos registros.
        with engine_teste.connect() as conexao:
            lista_reservas = conexao.execute(
                select(banco.reservas)
            ).mappings().all()

            eventos = conexao.execute(
                select(banco.auditoria_reservas)
                .order_by(banco.auditoria_reservas.c.id)
            ).mappings().all()

            avisos = conexao.execute(
                select(banco.notificacoes)
            ).mappings().all()

            conflitos = conexao.execute(
                select(banco.conflitos_reservas)
            ).mappings().all()

        self.assertEqual(len(lista_reservas), 1)

        reserva = lista_reservas[0]

        self.assertEqual(
            reserva["usuario_id"],
            usuario_id,
        )
        self.assertEqual(
            reserva["recurso_id"],
            recurso_id,
        )
        self.assertEqual(
            reserva["status"],
            "CANCELADA",
        )
        self.assertEqual(
            reserva["finalidade"],
            "Reserva criada pelo teste de navegador",
        )

        self.assertEqual(
            [evento["acao"] for evento in eventos],
            ["CRIACAO", "CANCELAMENTO"],
        )

        self.assertEqual(len(avisos), 2)

        for aviso in avisos:
            self.assertEqual(
                aviso["usuario_id"],
                usuario_id,
            )
            self.assertEqual(
                aviso["reserva_id"],
                reserva["id"],
            )

        self.assertEqual(len(conflitos), 1)
        self.assertEqual(
            conflitos[0]["operacao"],
            "CRIACAO",
        )
        self.assertEqual(
            conflitos[0]["reserva_conflitante_id"],
            reserva["id"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)