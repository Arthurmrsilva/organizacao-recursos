import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select

import app as aplicativo
from banco import metadata, recursos, reservas, usuarios


class TestRelatoriosHTTP(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)

        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            for usuario_id, perfil, ativo in (
                (1, "ADMIN", True),
                (2, "SOLICITANTE", True),
                (3, "RESPONSAVEL", True),
                (4, "ADMIN", False),
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
                    nome="Sala exclusiva de junho",
                    tipo="SALA",
                    localizacao="Bloco A",
                    capacidade=30,
                    restrito=False,
                    ativo=True,
                )
            )

            conexao.execute(
                insert(recursos).values(
                    id=2,
                    nome="Projetor exclusivo de julho",
                    tipo="MATERIAL",
                    localizacao="Almoxarifado",
                    restrito=False,
                    ativo=True,
                )
            )

            conexao.execute(
                insert(reservas).values(
                    recurso_id=1,
                    usuario_id=2,
                    inicio=datetime(2030, 6, 10, 10, 0),
                    fim=datetime(2030, 6, 10, 11, 30),
                    finalidade="Reserva de junho",
                    status="APROVADA",
                )
            )

            conexao.execute(
                insert(reservas).values(
                    recurso_id=2,
                    usuario_id=2,
                    inicio=datetime(2030, 7, 10, 14, 0),
                    fim=datetime(2030, 7, 10, 16, 0),
                    finalidade="Reserva de julho",
                    status="CONCLUIDA",
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

    def autenticar(self, usuario_id=1):
        # Simula a sessão; login e senha têm testes próprios.
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["usuario_id"] = usuario_id
            sessao["csrf_token"] = "token-relatorios"

    def consultar(self, dados=None):
        return self.cliente.get(
            "/relatorios",
            query_string=dados or {},
        )

    def conferir_erro(self, dados, mensagem):
        resposta = self.consultar(dados)
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn(mensagem, pagina)
        self.assertIn('role="alert"', pagina)

        # Consulta inválida não deve apresentar indicadores.
        self.assertNotIn("Resumo geral", pagina)
        self.assertNotIn("Reservas por situação", pagina)
        self.assertNotIn("Resumo por recurso", pagina)

        return pagina

    def test_consulta_exige_login(self):
        resposta = self.consultar()

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_outros_perfis_recebem_403(self):
        for usuario_id in (2, 3):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.consultar()
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 403)
                self.assertIn("Acesso negado", pagina)
                self.assertNotIn(
                    "Sala exclusiva de junho",
                    pagina,
                )
                self.assertNotIn("Resumo geral", pagina)

    def test_administrador_inativo_perde_acesso(self):
        self.autenticar(4)

        resposta = self.consultar()

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

    def test_administrador_consulta_historico_completo(self):
        self.autenticar()

        resposta = self.consultar()
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Resumo geral", pagina)
        self.assertIn("Reservas por situação", pagina)
        self.assertIn("Sala exclusiva de junho", pagina)
        self.assertIn("Projetor exclusivo de julho", pagina)
        self.assertIn("3,50 h", pagina)
        self.assertIn("1,50 h", pagina)
        self.assertIn("2,00 h", pagina)

    def test_filtro_mostra_apenas_recurso_do_periodo(self):
        self.autenticar()

        resposta = self.consultar(
            {
                "inicio": "2030-06-10",
                "fim": "2030-06-10",
            }
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sala exclusiva de junho", pagina)
        self.assertNotIn(
            "Projetor exclusivo de julho",
            pagina,
        )
        self.assertIn("1,50 h", pagina)
        self.assertNotIn("3,50 h", pagina)
        self.assertIn('value="2030-06-10"', pagina)

    def test_periodo_sem_reservas_mostra_lista_vazia(self):
        self.autenticar()

        resposta = self.consultar(
            {
                "inicio": "2031-01-01",
                "fim": "2031-01-01",
            }
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("0,00 h", pagina)
        self.assertIn(
            "Nenhum recurso com reservas",
            pagina,
        )
        self.assertNotIn("Sala exclusiva de junho", pagina)
        self.assertNotIn(
            "Projetor exclusivo de julho",
            pagina,
        )

    def test_data_final_anterior_mostra_erro_e_preserva_campos(self):
        self.autenticar()

        pagina = self.conferir_erro(
            {
                "inicio": "2030-06-11",
                "fim": "2030-06-10",
            },
            "A data final não pode ser anterior à data inicial.",
        )

        self.assertIn('value="2030-06-11"', pagina)
        self.assertIn('value="2030-06-10"', pagina)

    def test_periodo_incompleto_mostra_erro(self):
        self.autenticar()

        for dados in (
            {"inicio": "2030-06-10"},
            {"fim": "2030-06-10"},
        ):
            with self.subTest(dados=dados):
                self.conferir_erro(
                    dados,
                    "Informe a data inicial e a data final.",
                )

    def test_datas_invalidas_mostram_erro(self):
        self.autenticar()

        for dados in (
            {"inicio": "invalida", "fim": "2030-06-10"},
            {"inicio": "2030-06-10", "fim": "2030-02-30"},
        ):
            with self.subTest(dados=dados):
                self.conferir_erro(
                    dados,
                    "Informe datas válidas para o relatório.",
                )

    def test_conflitos_aparecem_como_indisponiveis(self):
        self.autenticar()

        resposta = self.consultar()
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Conflitos evitados", pagina)
        self.assertIn(
            "Indicador ainda indisponível.",
            pagina,
        )

    def test_consulta_nao_altera_reservas(self):
        self.autenticar()

        with self.engine.connect() as conexao:
            antes = conexao.execute(
                select(reservas).order_by(reservas.c.id)
            ).mappings().all()

        resposta = self.consultar()

        self.assertEqual(resposta.status_code, 200)

        with self.engine.connect() as conexao:
            depois = conexao.execute(
                select(reservas).order_by(reservas.c.id)
            ).mappings().all()

        self.assertEqual(antes, depois)

    def test_datas_vazias_consultam_historico_completo(self):
        self.autenticar()

        resposta = self.consultar(
            {"inicio": "", "fim": ""}
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sala exclusiva de junho", pagina)
        self.assertIn("Projetor exclusivo de julho", pagina)
        self.assertIn("3,50 h", pagina)


if __name__ == "__main__":
    unittest.main()