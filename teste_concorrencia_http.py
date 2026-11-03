import importlib
import re
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from http.cookiejar import CookieJar
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import (
    HTTPCookieProcessor,
    HTTPRedirectHandler,
    Request,
    build_opener,
)

from sqlalchemy import create_engine, insert, select
from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server

import banco


class SemRedirecionamento(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def requisitar(cliente, url, dados=None):
    corpo = None
    if dados is not None:
        corpo = urlencode(dados).encode("utf-8")

    pedido = Request(url, data=corpo)

    try:
        resposta = cliente.open(pedido, timeout=20)
    except HTTPError as erro:
        resposta = erro

    with resposta:
        return resposta.code, resposta.read().decode("utf-8")


def extrair_token(html):
    resultado = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        html,
    )
    if resultado is None:
        raise AssertionError("Token CSRF não encontrado.")
    return resultado.group(1)


class TestConcorrenciaHTTP(unittest.TestCase):
    def test_duas_requisicoes_aceitam_apenas_uma_reserva(self):
        self.assertNotIn(
            "app",
            sys.modules,
            "Execute este arquivo em um processo separado.",
        )

        with tempfile.TemporaryDirectory(
            prefix="concorrencia_http_"
        ) as pasta:
            caminho = Path(pasta) / "teste.db"
            engine = create_engine(
                f"sqlite:///{caminho.as_posix()}",
                connect_args={
                    "check_same_thread": False,
                    "timeout": 20,
                },
            )

            try:
                banco.metadata.create_all(engine)
                senha = "Senha-Teste-HTTP-123!"
                senha_hash = generate_password_hash(senha)

                with engine.begin() as conexao:
                    for numero in (1, 2):
                        conexao.execute(
                            insert(banco.usuarios).values(
                                id=numero,
                                nome=f"Usuário HTTP {numero}",
                                login=f"http{numero}",
                                senha_hash=senha_hash,
                                perfil="SOLICITANTE",
                                ativo=True,
                            )
                        )

                    conexao.execute(
                        insert(banco.recursos).values(
                            id=1,
                            nome="Sala de teste HTTP",
                            tipo="SALA",
                            localizacao="Teste temporário",
                            capacidade=20,
                            restrito=False,
                            ativo=True,
                        )
                    )

                # A importação também usará o banco temporário.
                with patch.object(banco, "engine", engine):
                    modulo = importlib.import_module("app")
                    self.assertIs(modulo.engine, engine)

                    modulo.app.config.update(
                        SECRET_KEY="chave-exclusiva-teste-http",
                        DEBUG=False,
                        TESTING=False,
                    )

                    servidor = make_server(
                        "127.0.0.1",
                        0,
                        modulo.app,
                        threaded=True,
                    )
                    thread = threading.Thread(
                        target=servidor.serve_forever,
                        daemon=True,
                    )
                    thread.start()

                    try:
                        endereco = (
                            f"http://127.0.0.1:"
                            f"{servidor.server_port}"
                        )
                        self.verificar_disputa(
                            endereco, engine, senha
                        )
                    finally:
                        servidor.shutdown()
                        thread.join(timeout=10)
                        servidor.server_close()
            finally:
                engine.dispose()

    def verificar_disputa(self, endereco, engine, senha):
        clientes = []
        tokens = []

        # Cada usuário autentica por HTTP com cookies próprios.
        for numero in (1, 2):
            cliente = build_opener(
                HTTPCookieProcessor(CookieJar()),
                SemRedirecionamento(),
            )

            codigo, html = requisitar(
                cliente, f"{endereco}/login"
            )
            self.assertEqual(codigo, 200)

            codigo, _ = requisitar(
                cliente,
                f"{endereco}/login",
                {
                    "login": f"http{numero}",
                    "senha": senha,
                    "csrf_token": extrair_token(html),
                },
            )
            self.assertEqual(codigo, 302)

            codigo, html = requisitar(
                cliente, f"{endereco}/reservas/nova"
            )
            self.assertEqual(codigo, 200)

            clientes.append(cliente)
            tokens.append(extrair_token(html))

        inicio = (
            datetime.now() + timedelta(days=2)
        ).replace(hour=14, minute=0, second=0, microsecond=0)
        fim = inicio + timedelta(hours=1)
        barreira = threading.Barrier(2, timeout=15)

        def enviar(indice):
            dados = {
                "recurso_id": "1",
                "inicio": inicio.strftime("%Y-%m-%dT%H:%M"),
                "fim": fim.strftime("%Y-%m-%dT%H:%M"),
                "finalidade": f"Disputa HTTP {indice + 1}",
                "csrf_token": tokens[indice],
            }
            barreira.wait()
            codigo, html = requisitar(
                clientes[indice],
                f"{endereco}/reservas/nova",
                dados,
            )
            return indice + 1, codigo, html

        with ThreadPoolExecutor(max_workers=2) as executor:
            futuros = [
                executor.submit(enviar, indice)
                for indice in (0, 1)
            ]
            resultados = [
                futuro.result(timeout=30)
                for futuro in futuros
            ]

        self.assertEqual(
            sorted(item[1] for item in resultados),
            [302, 400],
        )

        vencedor = next(
            item[0] for item in resultados if item[1] == 302
        )
        perdedor, _, html_erro = next(
            item for item in resultados if item[1] == 400
        )

        self.assertIn(
            "Já existe uma reserva para esse recurso",
            html_erro,
        )

        with engine.connect() as conexao:
            reservas = conexao.execute(
                select(banco.reservas)
            ).mappings().all()
            eventos = conexao.execute(
                select(banco.auditoria_reservas)
            ).mappings().all()
            avisos = conexao.execute(
                select(banco.notificacoes)
            ).mappings().all()
            conflitos = conexao.execute(
                select(banco.conflitos_reservas)
            ).mappings().all()

        self.assertEqual(len(reservas), 1)
        reserva = reservas[0]
        self.assertEqual(reserva["usuario_id"], vencedor)
        self.assertEqual(reserva["recurso_id"], 1)
        self.assertEqual(reserva["inicio"], inicio)
        self.assertEqual(reserva["fim"], fim)
        self.assertEqual(reserva["status"], "APROVADA")
        self.assertEqual(
            reserva["finalidade"], f"Disputa HTTP {vencedor}"
        )

        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["acao"], "CRIACAO")
        self.assertEqual(eventos[0]["usuario_id"], vencedor)
        self.assertEqual(eventos[0]["reserva_id"], reserva["id"])

        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]["usuario_id"], vencedor)
        self.assertEqual(avisos[0]["reserva_id"], reserva["id"])

        self.assertEqual(len(conflitos), 1)
        self.assertEqual(conflitos[0]["usuario_id"], perdedor)
        self.assertEqual(conflitos[0]["recurso_id"], 1)
        self.assertEqual(conflitos[0]["operacao"], "CRIACAO")
        self.assertEqual(
            conflitos[0]["reserva_conflitante_id"],
            reserva["id"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)