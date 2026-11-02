# Indice de evidencias

## Estado do pacote

Pacote em preparacao para a entrega academica.

A tag da release candidata ainda nao foi criada.
As evidencias abaixo identificam arquivos e resultados existentes.
A validacao final devera vincular CI, cobertura e Sonar ao commit
avaliado para a release.

Repositorio:
https://github.com/Arthurmrsilva/organizacao-recursos

Pull request:
https://github.com/Arthurmrsilva/organizacao-recursos/pull/1

## Documentacao

| Evidencia | Caminho |
| --- | --- |
| Instalacao e execucao | [README](../../README.md) |
| Rastreabilidade dos requisitos | [RTM](../../RTM.md) |
| Arquitetura e diagramas | [Arquitetura](../../ARQUITETURA.md) |
| Plano de testes | [Plano de testes](../../PLANO_TESTES.md) |
| Relatorio de qualidade | [Relatorio](../../RELATORIO_QUALIDADE.md) |
| Registro de defeitos | [Defeitos](../../DEFEITOS.md) |
| Controles de seguranca | [Seguranca](../../SEGURANCA.md) |
| Validacao de instalacao limpa | [Validacao](../../VALIDACAO_INSTALACAO.md) |
| Checklist de entrega | [Checklist](../entrega/checklist.md) |

Os documentos existentes ainda precisam da consolidacao final indicada
no checklist.

## Testes e integracao continua

| Evidencia | Caminho |
| --- | --- |
| Suite Python | [Testes](../../tests/) |
| Concorrencia por HTTP | [Teste HTTP](../../teste_concorrencia_http.py) |
| Concorrencia entre manutencao e reserva | [Teste de concorrencia](../../tests/test_concorrencia_manutencao.py) |
| Fluxo de navegador | [Teste Chromium](../../e2e/test_fluxo_reserva.py) |
| Execucao via Testcontainers | [Teste do container](../../teste_testcontainers.py) |
| Imagem dos testes | [Dockerfile](../../Dockerfile.testes) |
| Pipeline de cobertura e navegador | [Workflow](../../.github/workflows/testes.yml) |
| Pipeline Testcontainers | [Workflow](../../.github/workflows/testcontainers.yml) |
| Configuracao Sonar | [Configuracao](../../sonar-project.properties) |

As execucoes podem ser consultadas em:
https://github.com/Arthurmrsilva/organizacao-recursos/actions

O workflow principal publica o artefato relatorios-cobertura,
com coverage.json, coverage.xml e htmlcov.

O workflow Testcontainers publica o artefato resultado-testcontainers.

## Resultados anteriores a release

Estes resultados sao referencias historicas. Nao substituem a
validacao final do commit da release candidata.

| Referencia | Resultado registrado |
| --- | --- |
| da93d49 | 292 testes aprovados localmente; CI de testes automatizados aprovada |
| da93d49 | CI: cobertura de linhas de 97,46% e ramificacoes de 94,83% |
| b1b308a | Testcontainers aprovado na CI; Quality Gate reprovado por instalacao sem exigir pacotes binarios |
| 047995b | Quality Gate aprovado; correcao posterior necessaria na sintaxe YAML do workflow |
| 1e42442 | Correcao YAML; execucao Testcontainers verde informada pelo executor |

A cobertura do Sonar sobre codigo novo e uma metrica distinta da
cobertura de linhas e ramificacoes calculada pelo Coverage.py.

## Desempenho

- [Relatorio das duas execucoes planejadas](../performance/resultado-01.md)
- [Plano JMeter](../../performance/consulta_login_10usuarios_60s.jmx)
- [JTL da execucao 1](../../performance/login_planejado_20261102-192309_01.jtl)
- [JTL da execucao 2](../../performance/login_planejado_20261102-192309_02.jtl)

Resultados registrados no commit 49f9268:

| Execucao | Amostras | Erros | Media (ms) | p95 (ms) |
| --- | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 |
| 2 | 565 | 0 | 8,11 | 19 |

Escopo: GET da pagina de login, 10 usuarios virtuais, 60 segundos,
pausa de 1 segundo, aplicacao e JMeter no mesmo computador.

Nao representa avaliacao de carga dos fluxos autenticados.

## Dependencias e recuperacao de dados

- [Auditoria das dependencias principais](../../auditoria_dependencias.json)
- [Auditoria das dependencias do navegador](../../auditoria_dependencias_e2e.json)
- [Verificador de backup e restauracao](../../validar_backup.py)
- [Testes do verificador](../../tests/test_validar_backup.py)

As auditorias registram o resultado no momento da execucao.
Nao abrangem automaticamente o sistema operacional da imagem Docker,
o binario Chromium ou as dependencias do ambiente Testcontainers.

## Fechamento da release — pendente

Antes do envio, registrar neste indice:

- Tag anotada e SHA completo do commit avaliado.
- Link da CI aprovada na main para esse commit.
- Links das execucoes e dos artefatos de cobertura e Testcontainers.
- Link e resultado da analise Sonar correspondente.
- Resultado da validacao em clone limpo da versao candidata.
- Revisao real do pull request por outro integrante.
- Link da decisao de qualidade, com contribuicoes e riscos assumidos.

O relatorio de carga identifica uma execucao anterior a release.
Caso o codigo avaliado mude de forma relevante para esse cenario,
a necessidade de repetir a medicao deve ser avaliada e registrada.