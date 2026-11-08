# Decisão de qualidade

## Atualização do fechamento — 07/11/2026

A candidata v1.0.0-rc1 foi publicada no commit 3a1ef85, com os relatórios anexados e os workflows da main e da tag aprovados.

Consulte o [registro de fechamento](entrega/fechamento.md) para o SHA completo, links das execuções, relatórios e pendências.

A revisão por outro integrante, a confirmação coletiva e o aceite nominal dos riscos continuam pendentes. O envio ainda não foi confirmado.

As seções anteriores a esta atualização mantêm o estado registrado em suas respectivas datas; menções à tag ainda em preparação referem-se ao período anterior à publicação.

Projeto: Organização de Recursos.
Disciplina: Qualidade de Software.
Atualização: 03/11/2026.

Estado: proposta de liberação para entrega acadêmica com ressalvas.
Confirmação final do grupo: pendente.

## 1. Integrantes

- Arthur Mendes Ramos da Silva.
- Nicolas Ferreira.
- Robert Oliveira.

A inclusão dos nomes identifica os integrantes.
Não representa aprovação ou participação em atividades não realizadas.

## 2. Versão verificada

Validação em clone limpo:

- Commit: b55f1ef87ea97bb5fee3bf076a57cf0555656e74.
- Executor: Arthur Mendes Ramos da Silva.
- Ambiente: clone separado e ambiente virtual novo no mesmo computador.
- Resultado: 292 testes aprovados em 86,353 segundos.

[Registro completo da validação](entrega/validacao-2026-11-03.md)

Integração posterior:

- Pull request #1 integrado na main.
- Commit de integração: f22d2c9.
- Testes automatizados #200: aprovado.
- Testes com Testcontainers #38: aprovado.

A comparação entre o commit testado e a integração mostrou somente
a inclusão do documento de validação, sem alteração no código.

O fechamento documental está sendo preparado em fechamento/entrega.
A tag v1.0.0-rc1 ainda não foi criada.

## 3. Proposta de decisão

Arthur propõe liberar a versão para entrega acadêmica com ressalvas,
após concluir as verificações finais e identificar a versão pela tag.

A proposta considera:

- Os testes automatizados aprovados.
- A instalação em clone limpo.
- O fluxo manual de reserva verificado.
- Os workflows aprovados após a integração na main.
- A documentação dos resultados e das limitações.

A proposta não representa decisão unânime do grupo.
A revisão por outro integrante e as confirmações continuam pendentes.

Também não representa liberação para produção.

Requisitos obrigatórios não atendidos precisam ser corrigidos ou ter
a mudança de escopo autorizada pelo professor. A existência de testes
aprovados não elimina essa necessidade.

## 4. Critérios e evidências

| Critério | Evidência | Situação |
| --- | --- | --- |
| Instalação em ambiente novo | Validação de 03/11/2026 | Executada no commit b55f1ef |
| Suíte Python | 292 testes em 86,353 segundos | Aprovada no clone limpo |
| Fluxo manual de reserva | Criação, conflito, cancelamento e histórico | Verificado por Arthur |
| Testes automatizados na main | Workflow #200 | Aprovado no commit f22d2c9 |
| Testcontainers na main | Workflow #38 | Aprovado no commit f22d2c9 |
| Cobertura mínima | Metas de 80% de linhas e 70% de ramificações na CI | Preservar os relatórios finais |
| Quality Gate | Verificação configurada no workflow principal | Vincular a análise da versão final |
| Teste de carga | Duas execuções planejadas documentadas | Resultado limitado a GET /login |
| Backup e restauração | Verificador e testes automatizados | Evidências disponíveis |
| Rastreabilidade | RTM e documentos vinculados | Conferência final pendente |
| Repositório público | Visibilidade conferida no GitHub | Concluído |
| Revisão por outro integrante | Ainda não realizada | Pendente |
| Tag da entrega | v1.0.0-rc1 | Ainda não criada |

## 5. Documentos de apoio

- [Instalação e execução](../README.md).
- [Checklist](entrega/checklist.md).
- [Índice de evidências](evidencias/README.md).
- [Rastreabilidade](rtm.md).
- [Relatório de qualidade](relatorio-qualidade.md).
- [Defeitos](defeitos/README.md).
- [Plano de testes](../PLANO_TESTES.md).
- [Arquitetura e diagramas](../ARQUITETURA.md).
- [Segurança](../SEGURANCA.md).
- [Desempenho](performance/resultado-01.md).
- [Changelog](../CHANGELOG.md).

## 6. Resultados históricos

Os resultados abaixo pertencem às versões indicadas:

- Commit da93d49: cobertura de 97,46% de linhas e 94,83%
  de ramificações, considerando sete módulos.
- Commit 3a76227: Quality Gate aprovado e cobertura sobre
  código novo de 84,1%.
- Carga registrada no commit 49f9268: duas execuções com
  565 amostras cada, zero erros e p95 de 23 ms e 19 ms.

As métricas do Coverage.py e do Sonar medem escopos diferentes.
Esses valores não devem ser apresentados como novas medições
da futura tag.

## 7. Riscos e limitações

Nenhum aceite coletivo dos riscos está registrado neste documento.
Os responsáveis pelo acompanhamento ainda precisam ser confirmados.

| Limitação | Impacto | Tratamento proposto | Responsável e aceite |
| --- | --- | --- | --- |
| Gestão de usuários e edição/desativação de recursos incompletas na interface | Parte da administração depende de procedimentos externos | Conferir os requisitos; corrigir se obrigatório | Pendente |
| Carga limitada a GET /login no mesmo computador | Não mede desempenho dos fluxos autenticados | Apresentar o resultado somente para o cenário testado | Pendente |
| Execução local com servidor de desenvolvimento | Não comprova implantação adequada para produção | Restringir a demonstração ao contexto acadêmico | Pendente |
| Cobertura calculada em sete módulos | Percentuais não abrangem todos os arquivos | Informar o escopo junto dos resultados | Pendente |
| SQLite dentro do container | Não verifica um servidor de banco separado | Explicar a configuração e conferir as exigências do trabalho | Pendente |
| Ambiente Testcontainers sem lock completo com hashes | Reprodutibilidade inferior à instalação principal | Documentar a limitação e preservar o log da execução | Pendente |
| Restauração em diretório temporário | Não demonstra recuperação operacional completa | Apresentar como verificação de integridade e restauração no escopo testado | Pendente |

Para aceitar um risco, registrar responsável nominal, impacto,
justificativa e confirmação. Uma ressalva não substitui o atendimento
de um requisito obrigatório.

## 8. Contribuições individuais

Registro baseado nas informações fornecidas por Arthur em 03/11/2026.

| Integrante | Participação neste projeto | Evidência ou situação |
| --- | --- | --- |
| Arthur Mendes Ramos da Silva | Implementação, ajustes, testes, documentação e integração no GitHub | Histórico de commits, documentos e registros de validação |
| Nicolas Ferreira | Nenhuma atividade realizada até este registro, conforme informado por Arthur | Participação e confirmação próprias pendentes |
| Robert Oliveira | Nenhuma atividade realizada até este registro, conforme informado por Arthur | Participação e confirmação próprias pendentes |

Atividades posteriores devem ser acrescentadas somente depois
de realizadas. A participação em outras disciplinas não é contabilizada
como contribuição neste projeto.

## 9. Revisão e confirmação

A integração do pull request não substitui revisão por outro integrante.

| Integrante | Situação |
| --- | --- |
| Arthur Mendes Ramos da Silva | Concordou com o registro desta proposta de liberação acadêmica com ressalvas |
| Nicolas Ferreira | Revisão e confirmação pendentes |
| Robert Oliveira | Revisão e confirmação pendentes |

As confirmações de Nicolas e Robert devem ser feitas pelos próprios
integrantes, após lerem os documentos e verificarem o sistema.

Este registro não atribui a eles aprovação antecipada.

## 10. Pendências de fechamento

- Conferir os documentos e os links finais.
- Conferir o atendimento dos requisitos obrigatórios.
- Registrar revisão por outro integrante.
- Obter as confirmações reais do grupo.
- Definir responsáveis e registrar o aceite dos riscos.
- Integrar o fechamento documental.
- Conferir a CI do commit escolhido.
- Preservar os relatórios finais.
- Criar a tag anotada v1.0.0-rc1.
- Registrar o SHA completo e os links das execuções finais.
- Realizar o envio e guardar o comprovante.

## 11. Envio

Repositório público:

https://github.com/Arthurmrsilva/organizacao-recursos

- Responsável pelo envio: a definir.
- Tag: pendente.
- Data do envio: pendente.
- Comprovante: pendente.

Um único integrante deve enviar o trabalho pelo grupo.
## Complemento — testes funcionais parciais relatados em 08/11/2026

Arthur informou que Nicolas Ferreira e Robert Oliveira participaram
de testes manuais parciais, sem falhas relatadas nos cenários listados.
A versão é presumida como rc1 pela cronologia, ainda a confirmar.

[Registro dos testes e suas limitações](entrega/validacao-parcial-integrantes.md).

Este complemento atualiza o registro anterior de participação.
A revisão do código, a confirmação coletiva e o aceite dos riscos
continuam pendentes.
