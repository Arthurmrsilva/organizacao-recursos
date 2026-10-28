import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert

import app as aplicativo
from banco import metadata, recursos, reservas, usuarios


class TestMinhasReservas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)

        metadata.create_all(self.engine)

        # Relógio fixo para testar o instante exato do término.
        self.agora = datetime(2030, 6, 10, 12, 0)

        relogio = patch.object(aplicativo, "datetime")
        self.relogio = relogio.start()
        self.relogio.now.return_value = self.agora
        self.addCleanup(relogio.stop)

        inicio = self.agora + timedelta(days=7)

        with self.engine.begin() as conexao:
            for usuario_id in (1, 2, 3):
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

            conexao.execute(
                insert(recursos).values(
                    id=1,
                    nome="Sala de teste",
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
                    nome="Projetor de teste",
                    tipo="MATERIAL",
                    localizacao="Almoxarifado",
                    restrito=False,
                    ativo=True,
                )
            )

            for usuario_id in (1, 2):
                horario = inicio + timedelta(hours=usuario_id)

                conexao.execute(
                    insert(reservas).values(
                        recurso_id=1,
                        usuario_id=usuario_id,
                        inicio=horario,
                        fim=horario + timedelta(hours=1),
                        finalidade=f"Finalidade exclusiva {usuario_id}",
                        status="APROVADA",
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

    def autenticar(self, usuario_id):
        # Simula uma sessão autenticada para testar a listagem.
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["usuario_id"] = usuario_id

    def cadastrar_reserva(
        self,
        finalidade,
        status,
        inicio,
        fim,
        usuario_id=3,
        recurso_id=2,
    ):
        with self.engine.begin() as conexao:
            resultado = conexao.execute(
                insert(reservas).values(
                    recurso_id=recurso_id,
                    usuario_id=usuario_id,
                    inicio=inicio,
                    fim=fim,
                    finalidade=finalidade,
                    status=status,
                )
            )

            return resultado.inserted_primary_key[0]

    def consultar(self, filtro):
        resposta = self.cliente.get(
            "/reservas",
            query_string={"filtro": filtro},
        )

        self.assertEqual(resposta.status_code, 200)
        return resposta.get_data(as_text=True)

    def test_listagem_exige_login(self):
        resposta = self.cliente.get("/reservas")

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_usuario_ve_apenas_suas_reservas(self):
        for usuario_id, outro_id in ((1, 2), (2, 1)):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                for filtro in ("ativas", "historico", "todas"):
                    with self.subTest(filtro=filtro):
                        pagina = self.consultar(filtro)

                        self.assertNotIn(
                            f"Finalidade exclusiva {outro_id}",
                            pagina,
                        )

                        if filtro == "historico":
                            self.assertNotIn(
                                f"Finalidade exclusiva {usuario_id}",
                                pagina,
                            )
                        else:
                            self.assertIn(
                                f"Finalidade exclusiva {usuario_id}",
                                pagina,
                            )

    def test_usuario_sem_reservas_ve_mensagem(self):
        self.autenticar(3)

        casos = (
            ("ativas", "Nenhuma reserva ativa no momento."),
            ("historico", "Nenhuma reserva no histórico."),
            ("todas", "Você ainda não possui reservas."),
        )

        for filtro, mensagem in casos:
            with self.subTest(filtro=filtro):
                pagina = self.consultar(filtro)

                self.assertIn(mensagem, pagina)
                self.assertNotIn("Finalidade exclusiva", pagina)

    def test_em_uso_vencida_permanece_ativa_com_aviso(self):
        self.cadastrar_reserva(
            finalidade="Material com devolução pendente",
            status="EM_USO",
            inicio=self.agora - timedelta(hours=2),
            fim=self.agora - timedelta(hours=1),
        )
        self.autenticar(3)

        pagina_ativas = self.consultar("ativas")
        pagina_historico = self.consultar("historico")
        pagina_todas = self.consultar("todas")

        self.assertIn(
            "Material com devolução pendente",
            pagina_ativas,
        )
        self.assertIn(
            "Prazo de utilização encerrado.",
            pagina_ativas,
        )
        self.assertIn(
            "A devolução ainda não foi registrada.",
            pagina_ativas,
        )
        self.assertNotIn(
            "Material com devolução pendente",
            pagina_historico,
        )
        self.assertIn(
            "Material com devolução pendente",
            pagina_todas,
        )
        self.assertNotIn("Editar reserva", pagina_ativas)
        self.assertNotIn("Cancelar reserva", pagina_ativas)

    def test_em_uso_dentro_do_prazo_sem_aviso_de_atraso(self):
        self.cadastrar_reserva(
            finalidade="Material em utilização no prazo",
            status="EM_USO",
            inicio=self.agora - timedelta(minutes=30),
            fim=self.agora + timedelta(minutes=30),
        )
        self.autenticar(3)

        pagina = self.consultar("ativas")

        self.assertIn(
            "Material em utilização no prazo",
            pagina,
        )
        self.assertNotIn(
            "Prazo de utilização encerrado.",
            pagina,
        )

    def test_distribuicao_por_status_e_prazo(self):
        casos = []

        for status in ("SOLICITADA", "APROVADA", "EM_USO"):
            for periodo, inicio, fim in (
                (
                    "futuro",
                    self.agora + timedelta(hours=1),
                    self.agora + timedelta(hours=2),
                ),
                (
                    "vencido",
                    self.agora - timedelta(hours=2),
                    self.agora - timedelta(hours=1),
                ),
            ):
                finalidade = f"Cenario-{status}-{periodo}-fim"

                self.cadastrar_reserva(
                    finalidade=finalidade,
                    status=status,
                    inicio=inicio,
                    fim=fim,
                )

                deve_ser_ativa = (
                    status == "EM_USO" or periodo == "futuro"
                )
                casos.append((finalidade, deve_ser_ativa))

        for status in (
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
            finalidade = f"Cenario-{status}-encerrado-fim"

            self.cadastrar_reserva(
                finalidade=finalidade,
                status=status,
                inicio=self.agora + timedelta(hours=3),
                fim=self.agora + timedelta(hours=4),
            )
            casos.append((finalidade, False))

        self.autenticar(3)

        ativas = self.consultar("ativas")
        historico = self.consultar("historico")
        todas = self.consultar("todas")

        for finalidade, deve_ser_ativa in casos:
            with self.subTest(finalidade=finalidade):
                self.assertIn(finalidade, todas)

                if deve_ser_ativa:
                    self.assertIn(finalidade, ativas)
                    self.assertNotIn(finalidade, historico)
                else:
                    self.assertNotIn(finalidade, ativas)
                    self.assertIn(finalidade, historico)

    def test_instante_exato_do_termino(self):
        for status in ("SOLICITADA", "APROVADA", "EM_USO"):
            self.cadastrar_reserva(
                finalidade=f"Limite-{status}-fim",
                status=status,
                inicio=self.agora - timedelta(hours=1),
                fim=self.agora,
            )

        self.autenticar(3)

        ativas = self.consultar("ativas")
        historico = self.consultar("historico")

        self.assertIn("Limite-EM_USO-fim", ativas)
        self.assertNotIn("Limite-EM_USO-fim", historico)
        self.assertIn("Prazo de utilização encerrado.", ativas)

        for status in ("SOLICITADA", "APROVADA"):
            with self.subTest(status=status):
                finalidade = f"Limite-{status}-fim"

                self.assertNotIn(finalidade, ativas)
                self.assertIn(finalidade, historico)

    def test_filtro_invalido_usa_ativas(self):
        self.cadastrar_reserva(
            finalidade="Registro ativo para filtro",
            status="EM_USO",
            inicio=self.agora - timedelta(hours=2),
            fim=self.agora - timedelta(hours=1),
        )
        self.cadastrar_reserva(
            finalidade="Registro encerrado para filtro",
            status="CONCLUIDA",
            inicio=self.agora - timedelta(hours=4),
            fim=self.agora - timedelta(hours=3),
        )
        self.autenticar(3)

        for filtro in ("inexistente", "", " ATIVAS "):
            with self.subTest(filtro=filtro):
                pagina = self.consultar(filtro)

                self.assertIn(
                    "Registro ativo para filtro",
                    pagina,
                )
                self.assertNotIn(
                    "Registro encerrado para filtro",
                    pagina,
                )

    def test_ativas_ordenadas_por_inicio_e_id(self):
        inicio_mais_tarde = self.agora + timedelta(days=2)
        inicio_mais_cedo = self.agora + timedelta(days=1)

        self.cadastrar_reserva(
            finalidade="Ordem-ativa-tardia",
            status="APROVADA",
            inicio=inicio_mais_tarde,
            fim=inicio_mais_tarde + timedelta(hours=1),
        )
        self.cadastrar_reserva(
            finalidade="Ordem-ativa-cedo-primeira",
            status="APROVADA",
            inicio=inicio_mais_cedo,
            fim=inicio_mais_cedo + timedelta(hours=1),
        )
        self.cadastrar_reserva(
            finalidade="Ordem-ativa-cedo-segunda",
            status="APROVADA",
            inicio=inicio_mais_cedo,
            fim=inicio_mais_cedo + timedelta(hours=1),
        )
        self.autenticar(3)

        pagina = self.consultar("ativas")

        primeira = pagina.index("Ordem-ativa-cedo-primeira")
        segunda = pagina.index("Ordem-ativa-cedo-segunda")
        tardia = pagina.index("Ordem-ativa-tardia")

        self.assertLess(primeira, segunda)
        self.assertLess(segunda, tardia)

    def test_historico_e_todas_ordenados_por_inicio_e_id_desc(self):
        inicio_antigo = self.agora - timedelta(days=2)
        inicio_recente = self.agora - timedelta(days=1)

        self.cadastrar_reserva(
            finalidade="Ordem-historico-antiga",
            status="CONCLUIDA",
            inicio=inicio_antigo,
            fim=inicio_antigo + timedelta(hours=1),
        )
        self.cadastrar_reserva(
            finalidade="Ordem-historico-recente-primeira",
            status="CONCLUIDA",
            inicio=inicio_recente,
            fim=inicio_recente + timedelta(hours=1),
        )
        self.cadastrar_reserva(
            finalidade="Ordem-historico-recente-segunda",
            status="CONCLUIDA",
            inicio=inicio_recente,
            fim=inicio_recente + timedelta(hours=1),
        )
        self.autenticar(3)

        for filtro in ("historico", "todas"):
            with self.subTest(filtro=filtro):
                pagina = self.consultar(filtro)

                segunda = pagina.index(
                    "Ordem-historico-recente-segunda"
                )
                primeira = pagina.index(
                    "Ordem-historico-recente-primeira"
                )
                antiga = pagina.index(
                    "Ordem-historico-antiga"
                )

                self.assertLess(segunda, primeira)
                self.assertLess(primeira, antiga)


if __name__ == "__main__":
    unittest.main()