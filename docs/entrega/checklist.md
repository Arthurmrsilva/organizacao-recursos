# Checklist da entrega

Data da verificacao: 02/11/2026.
Branch: funcionalidade/login.
Referencia desta verificacao: commit 49f9268.

Este checklist registra o estado da preparacao da entrega.
Nao representa aprovacao do grupo nem liberacao para producao.

## Entregaveis

| Item | Existe | Atualizado | Caminho ou evidencia |
| --- | --- | --- | --- |
| Aplicacao Flask e SQLite | Sim | Validacao final pendente | app.py, banco.py e servico_*.py |
| Instrucoes de instalacao e execucao | Sim | Revisao final pendente | README.md |
| Validacao em clone separado | Sim | Executada no commit c84dac2; repetir na versao candidata | VALIDACAO_INSTALACAO.md |
| Matriz de rastreabilidade | Sim | Consolidacao final pendente | RTM.md |
| Diagramas de contexto, componentes e sequencias | Sim | Conferencia final pendente | ARQUITETURA.md |
| Documentacao das rotas HTTP | A conferir | Pendente | Conferir README.md e app.py |
| Plano de testes | Sim | Consolidacao final pendente | PLANO_TESTES.md |
| Relatorio de qualidade | Sim | Consolidacao final pendente | RELATORIO_QUALIDADE.md |
| Registro de defeitos | Sim | Conferencia final pendente | DEFEITOS.md |
| Controles e auditorias de seguranca | Sim | Consolidacao final pendente | SEGURANCA.md e auditoria_dependencias*.json |
| Suite Python | Sim | 292 testes aprovados nas execucoes registradas | tests/ |
| Concorrencia por HTTP | Sim | Aprovada nas execucoes registradas | teste_concorrencia_http.py |
| Teste de navegador Chromium | Sim | Aprovado nas execucoes registradas | e2e/test_fluxo_reserva.py |
| Testcontainers | Sim | Execucao verde informada no commit 1e42442 | teste_testcontainers.py e .github/workflows/testcontainers.yml |
| Pipeline de testes e cobertura | Sim | Vincular execucao da versao candidata | .github/workflows/testes.yml |
| Analise Sonar e Quality Gate | Sim | Vincular analise da versao candidata | sonar-project.properties e check do Sonar |
| Relatorios de cobertura | Sim, publicados pela CI | Preservar os da versao candidata | Artefato relatorios-cobertura |
| Plano de carga | Sim | Executado em duas repeticoes planejadas | performance/consulta_login_10usuarios_60s.jmx |
| Resultado do teste de carga | Sim | Registrado no commit 49f9268 | docs/performance/resultado-01.md e arquivos JTL vinculados |
| Verificacao de backup e restauracao SQLite | Sim | Validacao final pendente | validar_backup.py e tests/test_validar_backup.py |
| Repositorio publico | Nao | Pendente | Configuracao de visibilidade do GitHub |
| Revisao por outro integrante | Pendente | Pendente | Pull request #1 |
| Indice de evidencias | Nao nesta verificacao | Pendente | docs/evidencias/README.md |
| Changelog | Nao nesta verificacao | Pendente | CHANGELOG.md |
| Decisao de qualidade do grupo | Nao nesta verificacao | Pendente | docs/decisao-qualidade.md |
| CI verde na main avaliada | Pendente | Pendente | Execucao apos integracao revisada |
| Tag anotada da release candidata | Pendente | Pendente | v1.0.0-rc1 |
| Envio no formulario | Pendente | Pendente | Comprovante do integrante que enviar |

## Diferencas em relacao as orientacoes

A implementacao utiliza Python, Flask, unittest e Coverage.py.
As orientacoes mencionam Maven e JaCoCo.

A correspondencia proposta e:

- Execucao de testes: unittest.
- Medicao de cobertura: Coverage.py.
- Relatorios: JSON, XML e HTML publicados na CI.
- Analise estatica e Quality Gate: SonarQube Cloud.

A aceitacao dessa adaptacao pelo professor ainda deve ser confirmada.
Nao se declara execucao de Maven ou geracao de relatorio JaCoCo.

O Testcontainers executa a suite com SQLite dentro de um container Linux.
Nao foi implementado um servidor PostgreSQL ou MySQL separado.

## Pendencias em ordem de fechamento

1. Confirmar a aceitacao da stack Python e das ferramentas equivalentes.
2. Conferir documentacao das rotas e consolidar os documentos existentes.
3. Criar o indice de evidencias e o changelog.
4. Obter revisao real de outro integrante e registrar as contribuicoes.
5. Conferir o conteudo versionado antes de tornar o repositorio publico.
6. Integrar o pull request revisado e verificar a CI na main.
7. Repetir a validacao em clone limpo da versao candidata.
8. Registrar a decisao real do grupo, incluindo riscos e responsaveis.
9. Criar a tag anotada no commit avaliado e conferir os links das evidencias.
10. Realizar um unico envio pelo grupo e guardar o comprovante.

## Condicoes para finalizar

- Cada evidencia deve identificar a versao efetivamente avaliada.
- Evidencias historicas devem permanecer identificadas como historicas.
- A tag nao deve ser movida depois de publicada.
- Correcoes posteriores exigem uma nova release candidata.
- Nenhuma assinatura, revisao ou contribuicao deve ser presumida.
- Resultados locais nao comprovam prontidao para producao.