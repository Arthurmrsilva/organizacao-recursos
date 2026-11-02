import unittest

from testcontainers.core.container import DockerContainer


class TestExecucaoEmContainer(unittest.TestCase):
    def test_suite_do_projeto_no_container(self):
        with DockerContainer("organizacao-recursos-testes:latest") as container:
            docker_container = container.get_wrapped_container()

            try:
                resultado = docker_container.wait(timeout=600)
            finally:
                saida = docker_container.logs(
                    stdout=True,
                    stderr=True,
                ).decode("utf-8", errors="replace")
                print(saida, flush=True)

            self.assertEqual(
                resultado["StatusCode"],
                0,
                "A suite do projeto falhou dentro do container.",
            )
            self.assertIn(
                "Ran 292 tests",
                saida,
                "A imagem precisa conter os 292 testes esperados.",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)