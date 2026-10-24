import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine, insert

import app as aplicativo
from banco import metadata, recursos


class TestConsultaRecursos(unittest.TestCase):
    def setUp(self):
        # Cada teste começa com um banco temporário novo.
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        exemplos = [
            ("Sala Teste", "SALA", True),
            ("Professor Teste", "PROFESSOR", True),
            ("Projetor Teste", "MATERIAL", True),
            ("Sala Inativa", "SALA", False),
        ]

        with self.engine.begin() as conexao:
            for nome, tipo, ativo in exemplos:
                conexao.execute(
                    insert(recursos).values(
                        nome=nome,
                        tipo=tipo,
                        localizacao="Bloco Teste",
                        restrito=False,
                        ativo=ativo,
                    )
                )

        # Faz a página consultar o banco de teste.
        self.engine_original = aplicativo.engine
        aplicativo.engine = self.engine
        self.cliente = aplicativo.app.test_client()

    def tearDown(self):
        aplicativo.engine = self.engine_original
        self.engine.dispose()
        self.pasta.cleanup()

    def test_listar_recursos_ativos(self):
        resposta = self.cliente.get("/")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sala Teste", pagina)
        self.assertIn("Professor Teste", pagina)
        self.assertIn("Projetor Teste", pagina)
        self.assertNotIn("Sala Inativa", pagina)

    def test_filtrar_por_tipo(self):
        casos = {
            "SALA": "Sala Teste",
            "PROFESSOR": "Professor Teste",
            "MATERIAL": "Projetor Teste",
        }

        for tipo, nome_esperado in casos.items():
            with self.subTest(tipo=tipo):
                resposta = self.cliente.get(f"/?tipo={tipo}")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(nome_esperado, pagina)
                self.assertNotIn("Sala Inativa", pagina)

                for outro_tipo, outro_nome in casos.items():
                    if outro_tipo != tipo:
                        self.assertNotIn(outro_nome, pagina)

    def test_tipo_invalido_mostra_todos_os_ativos(self):
        resposta = self.cliente.get("/?tipo=INVALIDO")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sala Teste", pagina)
        self.assertIn("Professor Teste", pagina)
        self.assertIn("Projetor Teste", pagina)
        self.assertNotIn("Sala Inativa", pagina)


if __name__ == "__main__":
    unittest.main()