# Índice de evidências

Atualização: 03/11/2026.

## Situação da entrega

O repositório está público e o pull request #1 foi integrado na main.
Os dois workflows da main foram aprovados após a integração.

O fechamento documental está sendo preparado na branch fechamento/entrega.
A tag v1.0.0-rc1 ainda não foi criada.

- [Repositório público](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull request #1 integrado](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [Execuções do GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [README](../../README.md) | Instalação, execução e rotas HTTP |
| [Matriz de rastreabilidade](../rtm.md) | Ligação entre requisitos, implementação e testes |
| [Arquitetura](../../ARQUITETURA.md) | Organização do sistema e diagramas |
| [Plano de testes](../../PLANO_TESTES.md) | Cenários, critérios e estratégia de testes |
| [Relatório de qualidade](../relatorio-qualidade.md) | Resultados e limites das verificações |
| [Registro de defeitos](../defeitos/README.md) | Defeitos e correções documentadas |
| [Segurança](../../SEGURANCA.md) | Controles e auditorias |
| [Checklist](../entrega/checklist.md) | Itens concluídos e pendências |
| [Decisão de qualidade](../decisao-qualidade.md) | Rascunho; decisão e confirmações ainda pendentes |
| [Changelog](../../CHANGELOG.md) | Histórico das alterações |

Os arquivos docs/rtm.md, docs/relatorio-qualidade.md e
docs/defeitos/README.md direcionam aos documentos completos mantidos
na raiz do repositório.

## Validação em clone limpo

[Registro da validação de 03/11/2026](../entrega/validacao-2026-11-03.md)

Responsável pela execução: Arthur Mendes Ramos da Silva.

Commit testado:

b55f1ef87ea97bb5fee3bf076a57cf0555656e74

Resultados:

- Dependências instaladas em ambiente virtual novo.
- 292 testes aprovados em 86,353 segundos.
- Login e consulta dos recursos funcionando.
- Criação de reserva funcionando.
- Tentativa de reserva no mesmo recurso e horário bloqueada.
- Cancelamento funcionando.
- Reserva cancelada apresentada no histórico.

A execução utilizou um clone separado no mesmo computador.
Não representa revisão por outro integrante nem teste em outro computador.

[Registro anterior de instalação](../../VALIDACAO_INSTALACAO.md)

## Integração na main

Commit de integração do pull request #1: f22d2c9.

| Workflow | Execução | Resultado |
| --- | --- | --- |
| Testes automatizados | #200 | Aprovado |
| Testes com Testcontainers | #38 | Aprovado |

A comparação entre o commit b55f1ef e a main integrada mostrou
somente a inclusão do documento de validação, sem alterações no código.

Essas execuções comprovam o estado da integração identificada.
O fechamento documental posterior deverá ter sua própria CI conferida
antes da criação da tag.

## Código dos testes e pipelines

| Evidência | Caminho |
| --- | --- |
| Suíte Python | [tests](../../tests/) |
| Concorrência por HTTP | [Teste HTTP](../../teste_concorrencia_http.py) |
| Concorrência entre manutenção e reserva | [Teste de concorrência](../../tests/test_concorrencia_manutencao.py) |
| Fluxo no navegador Chromium | [Teste de navegador](../../e2e/test_fluxo_reserva.py) |
| Execução com Testcontainers | [Teste do container](../../teste_testcontainers.py) |
| Imagem dos testes | [Dockerfile](../../Dockerfile.testes) |
| Pipeline principal | [Workflow de testes](../../.github/workflows/testes.yml) |
| Pipeline Testcontainers | [Workflow do container](../../.github/workflows/testcontainers.yml) |
| Configuração Sonar | [sonar-project.properties](../../sonar-project.properties) |

## Relatórios publicados pela CI

O workflow principal publica o artefato relatorios-cobertura,
com os relatórios JSON, XML e HTML.

O workflow Testcontainers publica o artefato resultado-testcontainers,
com o registro da execução.

Para localizar os arquivos:

1. Abrir o GitHub Actions.
2. Selecionar a execução do commit desejado.
3. Abrir a seção Artifacts.
4. Baixar o relatório correspondente.

Os relatórios da versão final ainda precisam ser preservados
e vinculados à tag de entrega.

## Cobertura e análise estática: referências históricas

| Referência | Resultado registrado |
| --- | --- |
| da93d49 | 292 testes aprovados |
| da93d49 | Cobertura de linhas: 97,46% |
| da93d49 | Cobertura de ramificações: 94,83% |
| 3a76227 | Quality Gate aprovado |
| 3a76227 | Cobertura sobre código novo no Sonar: 84,1% |

A cobertura do Coverage.py considera sete módulos Python.
A cobertura sobre código novo do Sonar é uma medida diferente.

Esses números são históricos. Não devem ser apresentados como
novas medições da futura tag.

## Desempenho

- [Relatório das duas execuções planejadas](../performance/resultado-01.md)
- [Plano JMeter](../../performance/consulta_login_10usuarios_60s.jmx)
- [Resultado da execução 1](../../performance/login_planejado_20261102-192309_01.jtl)
- [Resultado da execução 2](../../performance/login_planejado_20261102-192309_02.jtl)

Resultados registrados no commit 49f9268:

| Execução | Amostras | Erros | Média em ms | p95 em ms |
| --- | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 |
| 2 | 565 | 0 | 8,11 | 19 |

Cenário: consulta GET da página de login, dez usuários virtuais,
60 segundos e pausa de um segundo entre requisições.

A aplicação e o JMeter foram executados no mesmo computador.
O resultado não abrange os fluxos autenticados nem comprova
capacidade de produção.

## Dependências e recuperação de dados

- [Auditoria das dependências principais](../../auditoria_dependencias.json)
- [Auditoria das dependências do navegador](../../auditoria_dependencias_e2e.json)
- [Verificador de backup e restauração](../../validar_backup.py)
- [Testes do verificador](../../tests/test_validar_backup.py)

As auditorias representam o momento de cada execução.
Não abrangem automaticamente o sistema operacional da imagem,
o binário Chromium ou as dependências do Testcontainers.

A restauração é verificada em ambiente temporário.
Ela não representa um plano completo de recuperação de produção.

## Pendências para fechar a entrega

- Registrar as contribuições reais dos três integrantes.
- Registrar revisão por outro integrante.
- Finalizar a decisão de qualidade e os responsáveis pelos riscos.
- Atualizar os documentos finais e integrar as alterações.
- Conferir a CI do commit escolhido para entrega.
- Preservar os relatórios dessa execução.
- Publicar a tag anotada v1.0.0-rc1.
- Registrar o SHA completo e os links das execuções finais.
- Realizar o envio pelo grupo e guardar o comprovante.

Nenhuma revisão, contribuição ou aprovação deve ser presumida.