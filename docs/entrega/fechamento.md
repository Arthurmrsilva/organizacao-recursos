# Registro histórico de fechamento da rc1

Este documento preserva o fechamento registrado em 07/11/2026,
referente à rc1. Seus resultados e pendências representam aquela data.

Para o estado posterior, consulte:

- [Índice de evidências](../evidencias/README.md).
- [Checklist](checklist.md).
- [Decisão de qualidade](../decisao-qualidade.md).
- [Testes parciais relatados](validacao-parcial-integrantes.md).
- [Release rc2](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc2).

---

Data: 07/11/2026.
Projeto: Organização de Recursos.
Responsável por este registro: Arthur Mendes Ramos da Silva.

## 1. Integrantes

- Arthur Mendes Ramos da Silva.
- Nicolas Ferreira.
- Robert Oliveira.

A lista identifica os integrantes do grupo.
As atividades e confirmações individuais estão registradas
em docs/decisao-qualidade.md.

## 2. Versão candidata publicada

Tag: v1.0.0-rc1.

Commit completo:

3a1ef853a3db907d4f0113949916792660a5d940

[Release e relatórios anexados](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc1)

[Código da candidata](https://github.com/Arthurmrsilva/organizacao-recursos/tree/v1.0.0-rc1)

Este registro foi preparado depois da publicação da candidata.
Ele não faz parte do conteúdo original da tag.

A tag publicada deve permanecer no mesmo commit.

## 3. Integração e testes

O pull request #1 integrou a implementação na main.
O pull request #2 integrou as atualizações documentais.

- [Pull request #1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [Pull request #2](https://github.com/Arthurmrsilva/organizacao-recursos/pull/2)

Execuções aprovadas no commit da candidata:

| Evento | Workflow | Execução | Resultado |
| --- | --- | --- | --- |
| Push na main | Testes automatizados | #203 | Aprovado |
| Push na main | Testes com Testcontainers | #41 | Aprovado |
| Push da tag | Testes automatizados | #204 | Aprovado |
| Push da tag | Testes com Testcontainers | #42 | Aprovado |

Links das execuções:

- [Testes automatizados #203](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/41751208567)
- [Testes automatizados da tag #204](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/41751510522)
- [Testcontainers da tag #42](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/41751510215)

Os testes automatizados incluem verificações da suíte Python,
concorrência por HTTP e navegador Chromium.

A análise Sonar é configurada para pull requests e pushes na main.
A execução disparada pela tag não substitui a análise da main.

## 4. Relatórios preservados

Os anexos da release foram obtidos nas execuções da main
#203 e #41, referentes ao mesmo commit da tag.

- [Cobertura em JSON, XML e HTML](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc1/relatorios-cobertura.1.zip)
- [Log Testcontainers](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc1/resultado-testcontainers.zip)

Resultados conferidos nesses arquivos:

| Verificação | Resultado |
| --- | --- |
| Cobertura de linhas | 97,46% |
| Cobertura de ramificações | 94,83% |
| Escopo da cobertura | Sete módulos Python |
| Suíte dentro do container | 292 testes aprovados |
| Tempo da suíte dentro do container | 14,529 segundos |
| Teste externo que controla o container | Aprovado |

As porcentagens não abrangem todos os arquivos do projeto.
A cobertura sobre código novo do Sonar é uma métrica diferente.

## 5. Validação local

Arthur realizou instalação em clone separado,
com ambiente virtual novo, no mesmo computador.

Commit validado:

b55f1ef87ea97bb5fee3bf076a57cf0555656e74

Resultado: 292 testes aprovados em 86,353 segundos.

Também foram verificados manualmente:

- Login.
- Consulta dos recursos.
- Criação de reserva.
- Bloqueio de reserva sobreposta.
- Cancelamento.
- Consulta da reserva cancelada no histórico.

[Procedimentos e limites da validação](validacao-2026-11-03.md)

Essa execução não representa revisão por outro integrante
nem validação em outro computador.

## 6. Documentação

- [Instalação e execução](../../README.md)
- [Checklist](checklist.md)
- [Índice de evidências](../evidencias/README.md)
- [Decisão de qualidade](../decisao-qualidade.md)
- [Rastreabilidade](../rtm.md)
- [Arquitetura](../../ARQUITETURA.md)
- [Plano de testes](../../PLANO_TESTES.md)
- [Relatório de qualidade](../relatorio-qualidade.md)
- [Defeitos](../defeitos/README.md)
- [Segurança](../../SEGURANCA.md)
- [Desempenho](../performance/resultado-01.md)
- [Changelog](../../CHANGELOG.md)

## 7. Situação e ressalvas

Existe uma candidata publicada com testes aprovados
e evidências preservadas.

A proposta de Arthur é de entrega acadêmica com ressalvas,
conforme docs/decisao-qualidade.md.

Continuam pendentes neste registro:

- Resultado completo da revisão por outro integrante.
- Confirmação coletiva da decisão.
- Definição nominal dos responsáveis e aceite dos riscos.
- Conferência final dos requisitos obrigatórios.
- Envio no formulário e comprovante.

A tentativa de instalação de um colega encontrou ausência
de Python acessível no terminal. Não foi apresentado,
até este registro, resultado de conclusão dos testes dele.

Não se declara revisão por pares concluída,
aprovação unânime ou atendimento integral do roteiro.

As limitações técnicas permanecem descritas nos documentos.
A candidata não representa liberação para produção.

## 8. Dados para o envio

Repositório público:

https://github.com/Arthurmrsilva/organizacao-recursos

Versão candidata publicada:

https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc1

Situação do envio: ainda não confirmado.
Comprovante: pendente.

Somente um integrante deve realizar o envio pelo grupo.