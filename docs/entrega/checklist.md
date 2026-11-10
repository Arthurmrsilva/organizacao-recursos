# Checklist da entrega

## Estado da entrega — 10/11/2026

Decisão do grupo: **entrega acadêmica com ressalvas**.
Arthur registrou seu aceite; Nicolas e Robert confirmaram a concordância
com a entrega e as ressalvas, conforme comunicação de Arthur em 10/11/2026.

A última candidata publicada é a **v1.0.0-rc4**, commit
`ca08ea6132c462fec7228d22892f50ad8ae82926`.
Sua CI e seus relatórios estão na [release rc4](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc4).

Esta consolidação corrige referências documentais posteriores à rc4 e
prepara a **rc5**. A rc5 somente estará publicada após integração,
CI aprovada, criação da nova tag anotada e publicação da release.
As tags anteriores permanecem fixas.

Para avaliar uma candidata, use o commit e as execuções identificados
nas notas da respectiva release. Resultados anteriores mantêm sua versão
de origem. O envio pelo formulário ainda não tem comprovante neste registro.


## Entregáveis e caminhos

| Item | Existe | Estado registrado | Caminho |
| --- | --- | --- | --- |
| Aplicação executável | Sim | Python, Flask e SQLite; CI da rc4 aprovada | [README](../../README.md), [app.py](../../app.py) |
| Instalação e rotas HTTP | Sim | Instruções e métodos documentados | [README](../../README.md) |
| Rastreabilidade | Sim | Conferir limitações frente à especificação | [RTM](../rtm.md) |
| Diagramas | Sim | Arquitetura documentada | [Arquitetura](../../ARQUITETURA.md) |
| Plano e relatório de testes | Sim | Cenários, resultados e limites registrados | [Plano](../../PLANO_TESTES.md), [relatório](../relatorio-qualidade.md) |
| CI e cobertura | Sim | rc4 aprovada; rc5 depende de nova execução | [Índice](../evidencias/README.md) |
| Análise estática | Sim | Sonar na main da rc4 aprovado | [CI #244](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42919624873) |
| Carga | Sim | Medições históricas, limitadas a GET /login | [Resultado](../performance/resultado-01.md) |
| Defeitos | Sim | Registro e limitações disponíveis | [Defeitos](../defeitos/README.md) |
| Decisão e riscos | Sim | Entrega com ressalvas; acompanhamento por Arthur | [Decisão](../decisao-qualidade.md) |
| Contribuições e revisões | Sim | Nicolas e Robert registrados; concordância dos três | [Decisão, seções 7 e 8](../decisao-qualidade.md) |
| Testes de Nicolas | Sim | 21 cenários ADMIN e RESPONSAVEL | [Relato](revisao-nicolas.md) |

## Verificações concluídas

- [x] Repositório público e nomes dos três integrantes registrados.
- [x] Instruções de instalação, testes e execução no README.
- [x] Validação histórica em clone separado e ambiente virtual novo por Arthur.
- [x] CI da rc4 aprovada no commit ca08ea6132c462fec7228d22892f50ad8ae82926.
- [x] Testes automatizados #245 e Testcontainers #83 aprovados na tag rc4.
- [x] Relatórios da rc4 anexados à release.
- [x] Relato dos 21 cenários de Nicolas integrado.
- [x] Contribuições de Nicolas em programação, cores do CSS, testes e revisão registradas.
- [x] Colaboração de Robert nos diagramas e na revisão registrada.
- [x] Concordância de Arthur, Nicolas e Robert com a entrega e as ressalvas registrada.
- [x] Responsabilidade de Arthur pelo acompanhamento dos riscos registrada.

## Fechamento da consolidação seguinte

- [ ] Integrar a consolidação documental e conferir a CI da main.
- [ ] Criar a tag anotada rc5 no commit conferido, sem mover tags anteriores.
- [ ] Conferir a CI da rc5 e publicar a release com os relatórios dessa execução.
- [ ] Conferir correspondência entre tag, SHA, CI e anexos na release da rc5.
- [ ] Conferir requisitos obrigatórios ainda associados a limitações conhecidas.
- [ ] Confirmar nomes completos e envio pelo formulário.
- [ ] Guardar comprovante de recebimento.

Esses itens descrevem o trabalho posterior à edição deste arquivo. A
publicação e a CI definitivas devem ser conferidas na release correspondente.

## Limites preservados

A validação de 03/11 ocorreu no computador de Arthur, em clone separado,
no commit b55f1ef87ea97bb5fee3bf076a57cf0555656e74. Não é uma nova
instalação da rc4 ou rc5 em outro computador.

Os 21 testes manuais de Nicolas não cobrem todos os fluxos do sistema.
O relato anterior de testes parciais dos integrantes não individualiza
todos os cenários nem identifica de modo confirmado sua versão.
As contribuições e confirmações posteriores não ampliam esse escopo.

O projeto usa unittest e Coverage.py em Python; não executa Maven nem
gera JaCoCo. A cobertura considera sete módulos. A carga mede GET /login
no mesmo computador, e Testcontainers utiliza SQLite dentro do container.
A demonstração usa o servidor de desenvolvimento Flask.
Gestão completa de usuários e edição/desativação de recursos pela interface
permanecem limitações, sujeitas à conferência dos requisitos obrigatórios.

O envio não está comprovado neste registro. A concordância com a entrega
acadêmica com ressalvas não representa liberação para produção.
