# Índice de evidências

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


## Pacote verificado da rc4

Todas as referências desta seção pertencem ao commit
`ca08ea6132c462fec7228d22892f50ad8ae82926`.

| Verificação | Evidência | Resultado |
| --- | --- | --- |
| Testes na tag rc4 | [#245](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42920846716) | Aprovado |
| Testcontainers na tag rc4 | [#83](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42920846792) | Aprovado |
| Testes e Sonar na main, mesmo commit | [#244](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42919624873) | Aprovado |
| Testcontainers na main, mesmo commit | [#82](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42919624812) | Aprovado |
| Cobertura JSON, XML e HTML | [ZIP da rc4](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc4/relatorios-cobertura.3.zip) | Preservado na release |
| Log do Testcontainers | [ZIP da rc4](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc4/resultado-testcontainers.3.zip) | Preservado na release |

A CI registra 97,46% de linhas e 94,83% de ramificações em sete módulos,
292 testes Python no container, concorrência HTTP e fluxo no Chromium.
A cobertura é do Coverage.py e não abrange todos os arquivos.
Sonar é executado nos PRs e pushes da main; o workflow da tag não o substitui.

## Consolidação para a rc5

A rc5 está em preparação e não recebe resultados antecipados.
Após a integração e a criação da tag, as notas da nova release deverão
identificar o SHA marcado, os links da CI da tag e da main no mesmo commit,
a referência ao Quality Gate e os dois relatórios dessa nova execução.

A [lista de releases](https://github.com/Arthurmrsilva/organizacao-recursos/releases) permite consultar a candidata
publicada e seus anexos. Os resultados da rc4 acima permanecem evidências
da rc4; não são apresentados como uma medição nova da rc5.

## Documentos e revisões

| Documento | Conteúdo |
| --- | --- |
| [README](../../README.md) | Instalação, execução, testes e rotas HTTP |
| [RTM](../rtm.md) | Requisitos e rastreabilidade |
| [Arquitetura](../../ARQUITETURA.md) | Diagramas e decisões |
| [Plano de testes](../../PLANO_TESTES.md) | Estratégia e cenários |
| [Relatório de qualidade](../relatorio-qualidade.md) | Resultados e limitações |
| [Defeitos](../defeitos/README.md) | Problemas e correções |
| [Checklist](../entrega/checklist.md) | Entregáveis, caminhos e fechamento |
| [Decisão de qualidade](../decisao-qualidade.md) | Riscos, responsáveis, contribuições, revisões e concordância |
| [Relato de Nicolas](../entrega/revisao-nicolas.md) | 21 cenários manuais ADMIN e RESPONSAVEL |
| [Testes parciais anteriores](../entrega/validacao-parcial-integrantes.md) | Relato histórico com limites de rastreabilidade |
| [Segurança](../../SEGURANCA.md) | Controles e auditorias |
| [Changelog](../../CHANGELOG.md) | Histórico das candidatas |

Arthur registrou o aceite dos riscos e o acompanhamento de seus tratamentos.
As confirmações de Nicolas e Robert foram comunicadas por Arthur em
10/11/2026. O relato de Nicolas identifica 21 cenários; as revisões não
são apresentadas como exame integral de todo o código.

## Evidências históricas com escopo identificado

### Instalação e fluxo manual

[Validação de 03/11/2026](../entrega/validacao-2026-11-03.md).

- Executor: Arthur Mendes Ramos da Silva.
- Commit: b55f1ef87ea97bb5fee3bf076a57cf0555656e74.
- Clone separado e ambiente virtual novo no mesmo computador.
- 292 testes aprovados em 86,353 segundos.
- Login, consulta, criação de reserva, conflito, cancelamento e histórico.

Essa execução é histórica e não deve ser apresentada como
uma nova instalação da rc2 por outro integrante.

### Desempenho

- [Relatório das duas execuções](../performance/resultado-01.md).
- [Plano JMeter](../../performance/consulta_login_10usuarios_60s.jmx).
- [Resultado 1](../../performance/login_planejado_20261102-192309_01.jtl).
- [Resultado 2](../../performance/login_planejado_20261102-192309_02.jtl).

Resultados registrados no commit 49f9268:

| Execução | Amostras | Erros | Média em ms | p95 em ms |
| --- | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 |
| 2 | 565 | 0 | 8,11 | 19 |

Escopo: GET /login, dez usuários virtuais, 60 segundos,
aplicação e JMeter no mesmo computador.

Não são medições novas da rc2 e não abrangem operações autenticadas
ou capacidade de produção.

### Dependências e recuperação

- [Auditoria principal](../../auditoria_dependencias.json).
- [Auditoria E2E](../../auditoria_dependencias_e2e.json).
- [Verificador de backup](../../validar_backup.py).
- [Testes do verificador](../../tests/test_validar_backup.py).

As auditorias representam suas respectivas datas de execução.
A restauração em diretório temporário não equivale a um plano
operacional completo de recuperação.



## Limites e envio

Resultados históricos mantêm o commit e o escopo de origem. A existência
dos documentos e a CI verde não demonstram atendimento integral a todos
os requisitos. As limitações funcionais e técnicas estão na decisão de qualidade.
O recebimento pelo formulário do professor ainda depende de comprovante.
