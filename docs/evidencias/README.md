# Índice de evidências

## Complemento documental - testes de Nicolas - 09/11/2026

Nicolas Ferreira relatou a execucao de 21 cenarios manuais:
15 do perfil ADMIN e 6 do perfil RESPONSAVEL, em 09/11/2026.
Segundo o executor, nenhum problema foi encontrado nos passos
descritos. O trecho de terminal apresentado nao contem erros 500
nem traceback.

Consulte o [relato funcional de Nicolas](../entrega/revisao-nicolas.md) para os resultados,
a identificacao informada e as pendencias de rastreabilidade.
O commit informado como testado e f3f2061; sua correspondencia
com o ambiente executado ainda precisa de confirmacao.

O registro nao inclui validacao completa de aprovacao e rejeicao,
retirada, devolucao ou nao comparecimento de materiais.
A revisao integral do codigo e a confirmacao coletiva permanecem
pendentes. A participacao de Robert nao e atestada por este relato.

Este complemento e posterior a rc3 e nao modifica sua tag.
As indicacoes anteriores de pendencia devem ser lidas considerando
este novo relato, dentro do escopo e dos limites aqui registrados.
O envio ao professor deve ser confirmado pelo comprovante do formulario.


## Preparacao da candidata v1.0.0-rc3

Atualizacao: 08/11/2026.

A rc3 reunira a documentacao consolidada pelos PRs #4 e #5.
A publicacao depende da integracao desta preparacao, CI aprovada
no commit escolhido, criacao da tag anotada e preservacao dos
relatorios correspondentes.

A identidade definitiva do commit, os links das execucoes e os
anexos serao registrados nas notas da release rc3:
[Release rc3](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc3).
Esse endereco somente estara disponivel depois da publicacao.

Os resultados da rc2 abaixo continuam associados a rc2.
Nao sao apresentados como novas medicoes da rc3.
Os testes parciais dos integrantes continuam com versao presumida;
a revisao do codigo, a confirmacao coletiva e o aceite dos riscos
permanecem pendentes.

## Registro anterior a preparacao da rc3

O conteudo abaixo preserva o estado anterior. As referencias a
"candidata publicada", a rc2 e as pendencias de consolidacao
representam esse registro historico.

Atualização: 08/11/2026.

## Versão candidata publicada

- Tag: v1.0.0-rc2.
- Commit: 12fae657686f2179da3feae561031ff3622c937e.
- [Código da candidata](https://github.com/Arthurmrsilva/organizacao-recursos/tree/v1.0.0-rc2).
- [Release e arquivos anexados](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc2).

A tag permanece fixa. Documentos acrescentados depois da publicação
não fazem parte do conteúdo original da rc2.

## CI e relatórios da rc2

As execuções abaixo correspondem ao commit da tag:

| Verificação | Execução | Resultado |
| --- | --- | --- |
| Testes automatizados na tag | [#208](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42432889313) | Aprovado |
| Testcontainers na tag | [#46](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42432889203) | Aprovado |
| Testes automatizados na main, no mesmo commit | [#207](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42432684085) | Aprovado |
| Testcontainers na main, no mesmo commit | [#45](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42432684089) | Aprovado |

Relatórios preservados:

- [Cobertura em JSON, XML e HTML](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc2/relatorios-cobertura.2.zip).
- [Log do Testcontainers](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc2/resultado-testcontainers.2.zip).

Resultados dos relatórios:

- Cobertura de linhas: 97,46%.
- Cobertura de ramificações: 94,83%.
- Escopo: sete módulos Python.
- Suíte no container: 292 testes aprovados em 19,614 segundos.
- Teste externo do Testcontainers: aprovado.
- Concorrência por HTTP e fluxo no Chromium: aprovados na CI.

A cobertura é calculada pelo Coverage.py. Não corresponde à
cobertura sobre código novo do Sonar nem abrange todos os arquivos.

A análise Sonar é configurada nos pull requests e pushes da main.
A execução #207 é a referência da main para o commit da rc2;
a execução da tag não substitui essa análise.

## Complemento documental posterior à rc2

O [PR #4](https://github.com/Arthurmrsilva/organizacao-recursos/pull/4)
acrescentou o relato de testes funcionais parciais dos integrantes.

Commit de integração:
d937c1e9a8c7f90d38b240b728a8d24515414dad.

CI desse commit:

- [Testes automatizados #211](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42500698008): aprovado.
- [Testcontainers #49](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42500698004): aprovado.

A comparação entre rc2 e esse commit contém somente três documentos,
sem alteração no código da aplicação.

[Registro dos testes parciais relatados](../entrega/validacao-parcial-integrantes.md).

Esse relato está na main e não integra a tag rc2.
A versão utilizada pelos participantes é presumida como rc1,
ainda sem confirmação do identificador.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [README](../../README.md) | Instalação, execução e rotas HTTP |
| [RTM](../rtm.md) | Rastreabilidade dos requisitos |
| [Arquitetura](../../ARQUITETURA.md) | Organização e diagramas |
| [Plano de testes](../../PLANO_TESTES.md) | Estratégia e cenários |
| [Relatório de qualidade](../relatorio-qualidade.md) | Resultados e limitações |
| [Defeitos](../defeitos/README.md) | Problemas e correções |
| [Segurança](../../SEGURANCA.md) | Controles e auditorias |
| [Checklist](../entrega/checklist.md) | Estado da entrega |
| [Decisão de qualidade](../decisao-qualidade.md) | Proposta, riscos e confirmações |
| [Changelog](../../CHANGELOG.md) | Histórico das alterações |

Os links relativos desta seção acompanham a versão do repositório
em que este índice é consultado. Para consultar o conteúdo original
da candidata, utilize o link do código da rc2 acima.

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

## Pendências reais

- Consolidar a documentação para distinguir estado atual e histórico.
- Confirmar versão e cenários executados por cada integrante.
- Concluir a revisão do código e as confirmações do grupo.
- Registrar responsáveis e aceite dos riscos.
- Conferir o atendimento dos requisitos obrigatórios da especificação.
- Confirmar o envio no formulário e preservar o comprovante.

O relato de testes parciais não representa aprovação coletiva.
CI aprovada não comprova, isoladamente, atendimento integral à especificação.