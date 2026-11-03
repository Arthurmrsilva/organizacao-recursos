import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert

import app as aplicativo
from banco import metadata, recursos, usuarios


class TestSegurancaXSS(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)

        caminho = Path(pasta.name) / "xss.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        self.nome = "<script>alert(123)</script>"

        with self.engine.begin() as conexao:
            conexao.execute(
                insert(usuarios).values(
                    id=1,
                    nome="Usuário de teste",
                    login="teste_xss",
                    senha_hash="nao-utilizado-neste-teste",
                    perfil="SOLICITANTE",
                    ativo=True,
                )
            )
            conexao.execute(
                insert(recursos).values(
                    id=1,
                    nome=self.nome,
                    tipo="SALA",
                    localizacao="Bloco A",
                    capacidade=20,
                    restrito=False,
                    ativo=True,
                )
            )

        troca = patch.object(
            aplicativo, "engine", self.engine
        )
        troca.start()
        self.addCleanup(troca.stop)

        self.cliente = aplicativo.app.test_client()

        # O login possui testes próprios.
        with self.cliente.session_transaction() as sessao:
            sessao["usuario_id"] = 1
            sessao["csrf_token"] = "token-de-teste"

    def test_nome_do_recurso_e_escapado_nas_paginas(self):
        for endereco in ("/", "/reservas/nova"):
            with self.subTest(endereco=endereco):
                resposta = self.cliente.get(endereco)
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertNotIn(self.nome, pagina)
                self.assertIn(
                    "&lt;script&gt;alert(123)&lt;/script&gt;",
                    pagina,
                )


if __name__ == "__main__":
    unittest.main()