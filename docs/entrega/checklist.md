# Checklist da entrega

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
Projeto: Organização de Recursos.

## Versões de referência

- Candidata publicada: v1.0.0-rc2.
- Commit da candidata: 12fae657686f2179da3feae561031ff3622c937e.
- Complemento documental do PR #4: d937c1e9a8c7f90d38b240b728a8d24515414dad.

A rc2 permanece fixa. O complemento do PR #4 está na main
e não integra o conteúdo original da tag.

[Índice de evidências](../evidencias/README.md).

## Aplicação e documentação disponíveis

- [x] Aplicação em Python, Flask e SQLite.
- [x] Instruções de instalação e execução no README.
- [x] Documentação das rotas HTTP.
- [x] Matriz de rastreabilidade.
- [x] Arquitetura e diagramas.
- [x] Plano de testes.
- [x] Relatório de qualidade.
- [x] Registro de defeitos.
- [x] Documentação de segurança.
- [x] Relatórios históricos de carga.
- [x] Verificador e testes de backup e restauração.
- [x] Repositório público.

A existência dos documentos não representa aprovação de todos
os requisitos. As limitações funcionais continuam sujeitas à
conferência com a especificação da disciplina.

## Verificações realizadas

- [x] Instalação em clone separado e ambiente virtual novo por Arthur.
- [x] Registro histórico de 292 testes aprovados no clone limpo.
- [x] Fluxo manual de criação, conflito, cancelamento e histórico por Arthur.
- [x] CI da rc2 aprovada: Testes automatizados #208.
- [x] CI da rc2 aprovada: Testcontainers #46.
- [x] Concorrência por HTTP e Chromium aprovados na CI da rc2.
- [x] Relatórios da rc2 preservados na release.
- [x] Cobertura da rc2: 97,46% de linhas e 94,83% de ramificações.
- [x] Escopo da cobertura identificado: sete módulos Python.
- [x] Log da rc2 com 292 testes aprovados no container.
- [x] CI do complemento documental aprovada: #211 e #49.

A instalação em clone limpo foi realizada no commit
b55f1ef87ea97bb5fee3bf076a57cf0555656e74,
em um clone separado no mesmo computador de Arthur.

[Registro da instalação e testes](validacao-2026-11-03.md).

Essa execução histórica não é apresentada como nova validação
da rc2 em outro computador.

## Publicação e rastreabilidade

- [x] Tag v1.0.0-rc1 publicada e preservada.
- [x] Tag v1.0.0-rc2 publicada e preservada.
- [x] Release rc2 publicada como pre-release.
- [x] Arquivos de cobertura e Testcontainers da rc2 anexados.
- [x] PR #4 integrado com o relato de testes parciais.
- [ ] Concluir e integrar esta consolidação documental.
- [ ] Conferir a CI do commit desta consolidação.
- [ ] Conferir a correspondência final entre versão entregue,
      documentos e evidências.

Documentos posteriores à rc2 devem ser identificados como complementos.
Caso outra candidata seja publicada, ela deve receber uma nova tag;
as tags existentes não devem ser movidas.

## Participação e revisão

- [x] Atividades técnicas de Arthur documentadas.
- [x] Relato recebido por Arthur sobre testes parciais de Nicolas e Robert registrado.
- [ ] Confirmar a versão utilizada pelos participantes.
- [ ] Identificar quais cenários cada participante executou.
- [ ] Complementar os cenários ainda não verificados.
- [ ] Registrar revisão do código por outro integrante.
- [ ] Obter a confirmação individual da decisão de qualidade.

[Registro dos testes parciais](validacao-parcial-integrantes.md).

Os cenários relatados incluem login, criação de reserva, aprovação,
recusa, bloqueio de conflito de horários e consulta ao histórico.

A versão é presumida como rc1 pela cronologia, ainda sem confirmação.
Não é atribuído percentual de conclusão aos testes manuais.

## Decisão de qualidade

- [x] Proposta de entrega acadêmica com ressalvas registrada por Arthur.
- [x] Limitações e seus impactos documentados.
- [ ] Confirmar responsáveis nominais pelo acompanhamento dos riscos.
- [ ] Registrar o aceite dos riscos e a decisão final dos integrantes.
- [ ] Conferir os requisitos obrigatórios ainda apontados como incompletos.

[Decisão de qualidade](../decisao-qualidade.md).

A proposta individual não representa aprovação coletiva.
Uma ressalva não substitui o atendimento de requisito obrigatório
nem a autorização do professor para alteração de escopo.

## Envio

- [ ] Confirmar os nomes completos dos integrantes no formulário.
- [ ] Realizar um único envio pelo grupo.
- [ ] Guardar o comprovante de recebimento.

Não há comprovante de envio associado a este checklist.

## Ferramentas e limites

Conforme informado por Arthur, o professor permitiu utilizar
qualquer linguagem de programação.

O projeto utiliza Python, Flask, SQLite, unittest, Coverage.py,
Playwright, GitHub Actions, SonarQube Cloud, JMeter e Testcontainers.

Não se declara execução de Maven ou geração de relatório JaCoCo.
A autorização relatada sobre linguagem não é tratada como
aprovação específica de todas as substituições de ferramentas.

Os testes de carga são limitados ao cenário GET /login.
O container utiliza SQLite, sem servidor de banco separado.
A demonstração utiliza servidor de desenvolvimento Flask.

A entrega acadêmica não representa liberação para produção.