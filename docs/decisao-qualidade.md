# Decisão de qualidade

Projeto: Organização de Recursos.
Disciplina: Qualidade de Software.
Data de preparação: 02/11/2026.

Estado: RASCUNHO — aguardando avaliação final e confirmação do grupo.

## 1. Integrantes

- Arthur Mendes Ramos da Silva.
- Nicolas Ferreira.
- Robert Oliveira.

A presença dos nomes neste documento não representa assinatura,
aprovação ou confirmação de contribuições.

## 2. Versão avaliada

Preencher após a validação final:

- Commit completo da versão avaliada: PENDENTE.
- Branch de entrega: main.
- Tag da release candidata: PENDENTE.
- Link da execução de CI desse commit: PENDENTE.
- Link da análise Sonar correspondente: PENDENTE.
- Registro da validação em clone limpo: PENDENTE.
- Revisão por outro integrante: PENDENTE.

A futura tag deve apontar para o commit efetivamente avaliado.
Resultados históricos não substituem a verificação dessa versão.

## 3. Decisão

Decisão final do grupo: PENDENTE.

Após avaliar as evidências, registrar uma das opções:

- Liberar para entrega acadêmica.
- Liberar para entrega acadêmica com ressalvas.
- Bloquear a entrega até corrigir os problemas identificados.

A versão ainda não está liberada por este documento.
Não se declara prontidão para produção.

## 4. Critérios e evidências

| Critério | Evidência disponível | Estado para a versão final |
| --- | --- | --- |
| Instalação reproduzível seguindo o README | README e validação histórica em clone separado | Repetir e registrar no commit avaliado |
| Suíte Python aprovada | 292 testes nas execuções registradas | Conferir execução final |
| Cobertura mínima de 80% de linhas e 70% de ramificações | Relatórios publicados pela CI | Conferir e preservar artefatos finais |
| Concorrência por HTTP | Teste com duas sessões e SQLite temporário | Conferir execução final |
| Fluxo de navegador | Teste automatizado com Chromium | Conferir execução final |
| Execução em container | Workflow de Testcontainers | Conferir execução final |
| Quality Gate aprovado | Análises históricas aprovadas | Vincular análise do commit avaliado |
| Teste de carga documentado | Duas execuções planejadas de GET /login | Conferir vínculo com a versão e registrar limites |
| Backup e restauração verificados | Script e testes automatizados | Conferir execução final |
| Requisitos rastreáveis e limitações declaradas | RTM, plano de testes e relatório de qualidade | Revisar itens parciais e pendentes |
| Revisão por pares | Pull request #1 | Revisão real pendente |
| Pacote de evidências acessível | Índice de evidências | Conferir links e referências finais |
| Repositório público e tag identificada | GitHub | Conferência final pendente |

### Documentos de apoio

- [README](../README.md).
- [Checklist da entrega](entrega/checklist.md).
- [Índice de evidências](evidencias/README.md).
- [Matriz de rastreabilidade](rtm.md).
- [Relatório de qualidade](relatorio-qualidade.md).
- [Registro de defeitos](defeitos/README.md).
- [Plano de testes](../PLANO_TESTES.md).
- [Arquitetura](../ARQUITETURA.md).
- [Segurança](../SEGURANCA.md).
- [Resultado do teste de carga](performance/resultado-01.md).
- [Validação histórica da instalação](../VALIDACAO_INSTALACAO.md).

## 5. Resultados históricos de referência

Os resultados abaixo pertencem às execuções documentadas,
não constituindo aprovação automática da versão final:

- 292 testes Python nas execuções registradas.
- Cobertura no commit da93d49: 97,46% de linhas e
  94,83% de ramificações, no escopo de sete módulos.
- Quality Gate aprovado no commit 3a76227, com 84,1%
  de cobertura sobre código novo.
- Duas execuções planejadas de GET /login com 565 amostras
  em cada, zero erros e p95 de 23 ms e 19 ms.
- Instalação em clone separado validada no commit c84dac2.
- Verificação de backup e restauração SQLite em diretório temporário.

Consultar os documentos vinculados para ambiente, procedimentos,
versões, critérios e limitações.

## 6. Riscos e limitações para avaliação

Os itens abaixo são propostas de avaliação.
Nenhum risco está declarado como aceito pelo grupo neste rascunho.

| Risco ou limitação | Impacto | Justificativa proposta para eventual aceitação acadêmica | Responsável | Aceite |
| --- | --- | --- | --- | --- |
| Gestão de usuários e edição/desativação de recursos incompletas na interface | Parte da administração depende de procedimentos externos à interface | Somente aceitar se compatível com o escopo exigido; caso contrário, corrigir antes da entrega | A definir pelo grupo | Pendente |
| Carga restrita a GET /login no mesmo computador | Não comprova desempenho de autenticação, reservas ou ambiente de produção | Evidência limitada ao cenário documentado, sem extrapolar capacidade | A definir pelo grupo | Pendente |
| Servidor de desenvolvimento e configuração local | Não oferece evidência de implantação adequada para produção | Entrega restrita à demonstração acadêmica local | A definir pelo grupo | Pendente |
| Cobertura medida em sete módulos Python | Percentuais não abrangem todos os scripts e arquivos da aplicação | Escopo de medição explicitamente identificado nos relatórios | A definir pelo grupo | Pendente |
| Testcontainers com SQLite dentro do container | Não verifica integração com um servidor de banco separado | Cenário corresponde ao banco utilizado pela aplicação; conferir exigências do trabalho | A definir pelo grupo | Pendente |
| Dependências externas do Testcontainers sem lock completo com hashes | Reprodutibilidade inferior à instalação principal com lock | Versões diretas fixadas e limitação documentada | A definir pelo grupo | Pendente |
| Restauração verificada em diretório temporário | Não demonstra recuperação operacional completa após desastre | Ensaio verifica integridade e equivalência dos dados dentro do escopo descrito | A definir pelo grupo | Pendente |

Antes do aceite final, cada risco aceito deve ter responsável nominal,
impacto e justificativa confirmados.

Requisitos obrigatórios não atendidos devem ser tratados como
bloqueadores, salvo alteração de escopo autorizada pelo professor.

## 7. Bloqueadores de fechamento

- Revisão real por outro integrante ainda não registrada.
- Validação final em clone limpo ainda não registrada.
- CI e análise Sonar do commit final ainda não vinculadas.
- Conferência da visibilidade pública ainda pendente.
- Contribuições individuais ainda não confirmadas.
- Decisão e responsáveis pelos riscos ainda não confirmados.
- Tag final e índice de evidências ainda não finalizados.

Atualizar esta lista conforme as verificações forem concluídas.

## 8. Contribuições individuais

Cada integrante deve declarar somente atividades que efetivamente realizou.

| Integrante | Atividades realizadas | Evidências | Confirmação |
| --- | --- | --- | --- |
| Arthur Mendes Ramos da Silva | A preencher pelo integrante | Commits, documentos ou verificações correspondentes | Pendente |
| Nicolas Ferreira | A preencher pelo integrante | Commits, documentos ou verificações correspondentes | Pendente |
| Robert Oliveira | A preencher pelo integrante | Commits, documentos ou verificações correspondentes | Pendente |

## 9. Confirmação da decisão

Preencher após a leitura do pacote de evidências e a avaliação dos riscos.

| Integrante | Concordância com a decisão e os riscos | Data | Registro da confirmação |
| --- | --- | --- | --- |
| Arthur Mendes Ramos da Silva | Pendente | Pendente | Pendente |
| Nicolas Ferreira | Pendente | Pendente | Pendente |
| Robert Oliveira | Pendente | Pendente | Pendente |

Uma confirmação deve ser registrada pelo próprio integrante,
por exemplo em revisão ou comentário identificado no pull request.

## 10. Envio

- Integrante responsável pelo envio: PENDENTE.
- Link público do repositório: https://github.com/Arthurmrsilva/organizacao-recursos
- Tag avaliada: PENDENTE.
- Data do envio: PENDENTE.
- Comprovante do formulário: PENDENTE.

O endereço acima identifica o repositório; não comprova sua
visibilidade pública.

Um único integrante deve realizar o envio pelo grupo e guardar
o comprovante.