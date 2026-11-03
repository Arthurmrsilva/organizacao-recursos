# Checklist da entrega

Data da atualização: 02/11/2026.
Branch de preparação: funcionalidade/login.
Referência documental: commit e75f65f.

Este checklist registra a preparação da entrega.
Não representa aprovação do grupo nem liberação para produção.

## Entregáveis

| Item | Existe | Estado | Caminho ou evidência |
| --- | --- | --- | --- |
| Aplicação Flask e SQLite | Sim | Validação final da candidata pendente | app.py, banco.py e servico_*.py |
| Instruções de instalação e execução | Sim | Atualizadas; repetir em clone limpo da candidata | README.md |
| Validação em clone separado | Sim | Executada no commit c84dac2; repetir na candidata | VALIDACAO_INSTALACAO.md |
| Matriz de rastreabilidade | Sim | Consolidada; revisão final pendente | RTM.md |
| Diagramas de contexto, componentes e sequências | Sim | Conferência final pendente | ARQUITETURA.md |
| Documentação das rotas HTTP | Sim | 17 rotas conferidas com app.py; atualização no commit 0cf5154 | README.md, seção Interface HTTP |
| Plano de testes | Sim | Consolidado no commit 5ffea52 | PLANO_TESTES.md |
| Relatório de qualidade | Sim | Consolidado no commit 3a76227 | RELATORIO_QUALIDADE.md |
| Registro de defeitos | Sim | Conferência final pendente | DEFEITOS.md |
| Controles e auditorias de segurança | Sim | Documento consolidado; auditorias históricas identificadas | SEGURANCA.md e auditoria_dependencias*.json |
| Suíte Python | Sim | 292 testes aprovados nas execuções registradas | tests/ e RELATORIO_QUALIDADE.md |
| Concorrência por HTTP | Sim | Aprovada nas execuções registradas | teste_concorrencia_http.py |
| Teste de navegador Chromium | Sim | Aprovado nas execuções registradas | e2e/test_fluxo_reserva.py |
| Testcontainers | Sim | Execuções aprovadas registradas; repetir na candidata | teste_testcontainers.py e .github/workflows/testcontainers.yml |
| Pipeline de testes e cobertura | Sim | Vincular execução da candidata | .github/workflows/testes.yml |
| Análise Sonar e Quality Gate | Sim | Gate aprovado no commit 3a76227; conferir candidata | sonar-project.properties e check do Sonar |
| Relatórios de cobertura | Sim, publicados pela CI | Preservar os da candidata | Artefato relatorios-cobertura |
| Plano de carga | Sim | Executado em duas repetições planejadas | performance/consulta_login_10usuarios_60s.jmx |
| Resultado do teste de carga | Sim | Registrado no commit 49f9268 | docs/performance/resultado-01.md e JTL vinculados |
| Verificação de backup e restauração SQLite | Sim | Execução e testes registrados; validação final pendente | validar_backup.py e tests/test_validar_backup.py |
| Integrantes | Sim | README e quatro arquivos corrigidos; conferir os demais documentos | Commits 0cf5154 e e75f65f |
| Repositório público | A conferir | Último estado registrado: privado | Configuração de visibilidade do GitHub |
| Revisão por outro integrante | Pendente | Registrar revisão real | Pull request #1 |
| Índice de evidências | Sim | Criado no commit b990407; vínculos finais pendentes | docs/evidencias/README.md |
| Changelog | Sim | Criado no commit 04f2d2c; fechamento da versão pendente | CHANGELOG.md |
| Decisão de qualidade do grupo | Pendente | Elaborar e confirmar com os integrantes | docs/decisao-qualidade.md |
| CI verde na main avaliada | Pendente | Verificar após integração revisada | Execução vinculada ao commit avaliado |
| Tag anotada da release candidata | Pendente | Criar após validação | v1.0.0-rc1 |
| Envio no formulário | Pendente | Um único envio pelo grupo | Comprovante do integrante que enviar |

## Linguagem e ferramentas

Conforme informado por Arthur, o professor autorizou o uso de qualquer
linguagem de programação. O projeto utiliza Python e Flask.

O roteiro apresenta comandos e ferramentas do ecossistema Java.
Neste projeto, os papéis correspondentes são:

- Instalação de dependências: pip com arquivos de lock.
- Execução de testes: unittest e Playwright.
- Medição de cobertura: Coverage.py.
- Relatórios de cobertura: JSON, XML e HTML publicados pela CI.
- Automação das verificações: GitHub Actions.
- Análise estática e Quality Gate: SonarQube Cloud.

A autorização relatada refere-se à linguagem. Este registro explica
a adaptação técnica; não atribui ao professor uma aprovação específica
de cada ferramenta.

Não se declara execução de Maven nem geração de relatório JaCoCo.

O Testcontainers executa a suíte com SQLite dentro de um container Linux.
Não foi implementado um servidor PostgreSQL ou MySQL separado.

## Evidências já registradas

- Suíte Python: 292 testes.
- Cobertura registrada no commit da93d49: 97,46% de linhas
  e 94,83% de ramificações, no escopo de sete módulos.
- Quality Gate aprovado no commit 3a76227, com 84,1% de cobertura
  sobre código novo.
- Duas execuções planejadas de carga: 565 amostras em cada,
  zero erros e p95 de 23 ms e 19 ms.
- Instalação em clone separado validada no commit c84dac2.
- Verificação de backup e restauração em diretório temporário.
- Documentação das 17 rotas HTTP atualizada no commit 0cf5154.

Esses resultados pertencem às versões e execuções identificadas.
Não equivalem automaticamente à validação da futura tag.

## Pendências em ordem de fechamento

1. Conferir os demais nomes, diagramas, registro de defeitos e
   correspondência dos caminhos documentais com o roteiro.
2. Obter revisão real de outro integrante e registrar as contribuições.
3. Conferir o conteúdo versionado antes de tornar o repositório público.
4. Integrar o pull request revisado e verificar a CI e o Sonar na main.
5. Repetir a instalação e as verificações em clone limpo da candidata,
   seguindo somente o README, e registrar o commit e os resultados.
6. Registrar a decisão real do grupo, com critérios, evidências,
   riscos, justificativas e responsáveis.
7. Finalizar o changelog e o índice de evidências.
8. Avaliar o commit final e criar a tag anotada, conferindo a CI
   e os vínculos de evidência correspondentes.
9. Realizar um único envio pelo grupo e guardar o comprovante.

Se houver alteração após uma validação, avaliar quais verificações
precisam ser repetidas no novo commit antes de criar a tag.

## Condições para finalizar

- Cada evidência deve identificar a versão efetivamente avaliada.
- Evidências históricas devem permanecer identificadas como históricas.
- O índice deve apresentar links válidos e permitir localizar os relatórios.
- O repositório deve estar público para a entrega, conforme o roteiro.
- A revisão e a decisão precisam ser confirmadas pelos integrantes.
- Os riscos aceitos precisam ter impacto, justificativa e responsável.
- A execução de CI citada deve corresponder ao commit da tag.
- A tag não deve ser movida depois de publicada.
- Correções posteriores exigem uma nova release candidata.
- Nenhuma assinatura, revisão ou contribuição deve ser presumida.
- Resultados locais não comprovam prontidão para produção.