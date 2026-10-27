import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert

import app as aplicativo
from banco import metadata, manutencoes, recursos, reservas, usuarios


class TestDisponibilidade(unittest.TestCase):
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
            conexao.execute(
                insert(usuarios).values(
                    id=1,
                    nome="Usuário de teste",
                    login="teste_disponibilidade",
                    senha_hash="nao-utilizado-neste-teste",
                    perfil="SOLICITANTE",
                    ativo=True,
                )
            )

            tipos = ("SALA", "PROFESSOR", "MATERIAL")

            for recurso_id, tipo in enumerate(tipos, start=1):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Recurso de teste {recurso_id}",
                        tipo=tipo,
                        localizacao="Bloco de teste",
                        capacidade=30 if tipo == "SALA" else None,
                        competencia="Python" if tipo == "PROFESSOR" else None,
                        restrito=False,
                        ativo=True,
                    )
                )

            conexao.execute(
                insert(recursos).values(
                    id=4,
                    nome="Recurso inativo de teste",
                    tipo="SALA",
                    localizacao="Bloco de teste",
                    capacidade=20,
                    restrito=False,
                    ativo=False,
                )
            )

        self.engine_anterior = aplicativo.engine
        aplicativo.engine = self.engine
        self.cliente = aplicativo.app.test_client()

        with self.cliente.session_transaction() as sessao:
            sessao["usuario_id"] = 1

    def tearDown(self):
        aplicativo.engine = self.engine_anterior
        self.engine.dispose()
        self.pasta.cleanup()

    def consultar(self, inicio=None, fim=None, **filtros):
        parametros = dict(filtros)

        if inicio is not None:
            parametros["inicio"] = inicio.strftime("%Y-%m-%dT%H:%M")

        if fim is not None:
            parametros["fim"] = fim.strftime("%Y-%m-%dT%H:%M")

        return self.cliente.get("/", query_string=parametros)

    def adicionar_reserva(self, recurso_id=1, status="APROVADA"):
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(reservas).values(
                    recurso_id=recurso_id,
                    usuario_id=1,
                    inicio=self.inicio,
                    fim=self.fim,
                    finalidade="Teste de disponibilidade",
                    status=status,
                )
            )

    def adicionar_manutencao(self, ativo=True):
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(manutencoes).values(
                    recurso_id=1,
                    usuario_id=1,
                    inicio=self.inicio,
                    fim=self.fim,
                    motivo="Manutenção de teste",
                    criado_em=datetime.now(),
                    ativo=ativo,
                )
            )

    def verificar_recurso(self, resposta, recurso_id, presente):
        self.assertEqual(resposta.status_code, 200)

        pagina = resposta.get_data(as_text=True)
        nome = f"Recurso de teste {recurso_id}"

        if presente:
            self.assertIn(nome, pagina)
        else:
            self.assertNotIn(nome, pagina)

    def test_consulta_exige_login(self):
        with self.cliente.session_transaction() as sessao:
            sessao.clear()

        resposta = self.consultar(self.inicio, self.fim)

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_sem_periodo_lista_recursos_ativos(self):
        self.adicionar_reserva()

        resposta = self.consultar()

        for recurso_id in (1, 2, 3):
            self.verificar_recurso(resposta, recurso_id, True)

        self.assertNotIn(
            "Recurso inativo de teste",
            resposta.get_data(as_text=True),
        )

    def test_periodo_livre_lista_recursos(self):
        resposta = self.consultar(self.inicio, self.fim)

        for recurso_id in (1, 2, 3):
            self.verificar_recurso(resposta, recurso_id, True)

        self.assertNotIn(
            "Recurso inativo de teste",
            resposta.get_data(as_text=True),
        )

    def test_reservas_bloqueiam_todos_os_tipos(self):
        for recurso_id in (1, 2, 3):
            self.adicionar_reserva(recurso_id=recurso_id)

        resposta = self.consultar(self.inicio, self.fim)

        for recurso_id in (1, 2, 3):
            with self.subTest(recurso_id=recurso_id):
                self.verificar_recurso(resposta, recurso_id, False)

    def test_status_que_bloqueiam_disponibilidade(self):
        for recurso_id, status in enumerate(
            ("SOLICITADA", "APROVADA", "EM_USO"),
            start=1,
        ):
            self.adicionar_reserva(recurso_id, status)

        resposta = self.consultar(self.inicio, self.fim)

        for recurso_id in (1, 2, 3):
            self.verificar_recurso(resposta, recurso_id, False)

    def test_status_encerrados_nao_bloqueiam(self):
        for status in (
            "CANCELADA",
            "REJEITADA",
            "CONCLUIDA",
            "NAO_COMPARECEU",
        ):
            self.adicionar_reserva(status=status)

        resposta = self.consultar(self.inicio, self.fim)

        self.verificar_recurso(resposta, 1, True)

    def test_diferentes_sobreposicoes_bloqueiam(self):
        self.adicionar_reserva()

        periodos = (
            (self.inicio, self.fim),
            (
                self.inicio + timedelta(minutes=10),
                self.fim - timedelta(minutes=10),
            ),
            (
                self.inicio - timedelta(minutes=30),
                self.inicio + timedelta(minutes=30),
            ),
            (
                self.fim - timedelta(minutes=30),
                self.fim + timedelta(minutes=30),
            ),
            (
                self.inicio - timedelta(hours=1),
                self.fim + timedelta(hours=1),
            ),
        )

        for inicio, fim in periodos:
            with self.subTest(inicio=inicio, fim=fim):
                resposta = self.consultar(inicio, fim)

                self.verificar_recurso(resposta, 1, False)
                self.verificar_recurso(resposta, 2, True)

    def test_horarios_consecutivos_sao_permitidos(self):
        self.adicionar_reserva()

        periodos = (
            (
                self.inicio - timedelta(hours=1),
                self.inicio,
            ),
            (
                self.fim,
                self.fim + timedelta(hours=1),
            ),
        )

        for inicio, fim in periodos:
            with self.subTest(inicio=inicio, fim=fim):
                resposta = self.consultar(inicio, fim)
                self.verificar_recurso(resposta, 1, True)

    def test_manutencao_ativa_bloqueia(self):
        self.adicionar_manutencao()

        resposta = self.consultar(
            self.inicio + timedelta(minutes=10),
            self.fim - timedelta(minutes=10),
        )

        self.verificar_recurso(resposta, 1, False)
        self.verificar_recurso(resposta, 2, True)

    def test_manutencao_inativa_nao_bloqueia(self):
        self.adicionar_manutencao(ativo=False)

        resposta = self.consultar(self.inicio, self.fim)

        self.verificar_recurso(resposta, 1, True)

    def test_horarios_consecutivos_a_manutencao(self):
        self.adicionar_manutencao()

        periodos = (
            (
                self.inicio - timedelta(hours=1),
                self.inicio,
            ),
            (
                self.fim,
                self.fim + timedelta(hours=1),
            ),
        )

        for inicio, fim in periodos:
            with self.subTest(inicio=inicio, fim=fim):
                resposta = self.consultar(inicio, fim)
                self.verificar_recurso(resposta, 1, True)

    def test_periodo_incompleto_exibe_erro(self):
        consultas = (
            {"inicio": self.inicio},
            {"fim": self.fim},
        )

        for parametros in consultas:
            with self.subTest(parametros=parametros):
                resposta = self.consultar(**parametros)
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 400)
                self.assertIn(
                    "Informe o início e o término",
                    pagina,
                )
                self.assertNotIn("Recurso de teste 1", pagina)

    def test_datas_invalidas_exibem_erro(self):
        consultas = (
            {
                "inicio": "data-invalida",
                "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
            },
            {
                "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
                "fim": "2026-02-30T15:00",
            },
        )

        for parametros in consultas:
            with self.subTest(parametros=parametros):
                resposta = self.cliente.get(
                    "/",
                    query_string=parametros,
                )
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 400)
                self.assertIn(
                    "Informe datas e horários válidos.",
                    pagina,
                )
                self.assertNotIn("Recurso de teste 1", pagina)

    def test_termino_igual_ou_anterior_exibe_erro(self):
        for fim in (
            self.inicio,
            self.inicio - timedelta(hours=1),
        ):
            with self.subTest(fim=fim):
                resposta = self.consultar(self.inicio, fim)
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 400)
                self.assertIn(
                    "O término deve ser posterior ao início.",
                    pagina,
                )
                self.assertNotIn("Recurso de teste 1", pagina)

    def test_disponibilidade_com_outros_filtros(self):
        resposta = self.consultar(
            self.inicio,
            self.fim,
            tipo="SALA",
            localizacao="Bloco",
            capacidade="25",
        )

        self.verificar_recurso(resposta, 1, True)
        self.verificar_recurso(resposta, 2, False)
        self.verificar_recurso(resposta, 3, False)


if __name__ == "__main__":
    unittest.main()