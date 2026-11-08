# Checklist da entrega

## Atualização do fechamento — 07/11/2026

A candidata v1.0.0-rc1 foi publicada no commit 3a1ef85, com os relatórios anexados e os workflows da main e da tag aprovados.

Consulte o [registro de fechamento](fechamento.md) para o SHA completo, links das execuções, relatórios e pendências.

A revisão por outro integrante, a confirmação coletiva e o aceite nominal dos riscos continuam pendentes. O envio ainda não foi confirmado.

As seções anteriores a esta atualização mantêm o estado registrado em suas respectivas datas; menções à tag ainda em preparação referem-se ao período anterior à publicação.

Atualização: 03/11/2026.
Branch de fechamento: fechamento/entrega.

Este documento registra o andamento da entrega.
As confirmações dos integrantes devem refletir atividades realmente realizadas.

## O que já foi feito

- [x] Aplicação desenvolvida em Python, Flask e SQLite.
- [x] Instruções de instalação e execução no README.
- [x] Documentação das 17 rotas HTTP.
- [x] Matriz de rastreabilidade em RTM.md.
- [x] Diagramas e explicação da arquitetura em ARQUITETURA.md.
- [x] Plano de testes em PLANO_TESTES.md.
- [x] Relatório de qualidade em RELATORIO_QUALIDADE.md.
- [x] Registro de defeitos em DEFEITOS.md.
- [x] Documentação de segurança em SEGURANCA.md.
- [x] Caminhos documentais docs/rtm.md e docs/relatorio-qualidade.md.
- [x] Índice de defeitos em docs/defeitos/README.md.
- [x] Nomes dos integrantes corrigidos nos documentos e templates.
- [x] Instalação das dependências em ambiente virtual novo.
- [x] Execução local de 292 testes em clone limpo: todos aprovados.
- [x] Teste manual de login e consulta dos recursos.
- [x] Teste manual de criação de reserva.
- [x] Teste manual de bloqueio de reserva no mesmo horário.
- [x] Teste manual de cancelamento e consulta no histórico.
- [x] Registro da validação em docs/entrega/validacao-2026-11-03.md.
- [x] Duas execuções planejadas do teste de carga registradas.
- [x] Verificação de backup e restauração documentada.
- [x] Repositório público.
- [x] Pull request #1 integrado na main.
- [x] Workflow Testes automatizados aprovado na main após a integração.
- [x] Workflow Testes com Testcontainers aprovado na main após a integração.
- [x] Branch separada criada para o fechamento documental.

## Versões e resultados

A validação em clone limpo foi realizada no commit:

b55f1ef87ea97bb5fee3bf076a57cf0555656e74

Resultado local: 292 testes aprovados em 86,353 segundos.

A validação foi feita por Arthur, no mesmo computador, utilizando
um clone separado e um ambiente virtual novo. Ela não representa
revisão por outro integrante nem teste em outro computador.

Após a integração do pull request #1, a main ficou no commit
f22d2c9. Os workflows aprovados foram:

- Testes automatizados #200.
- Testes com Testcontainers #38.

A comparação entre b55f1ef e a main integrada mostrou apenas
a inclusão do documento de validação, sem alterações no código.

Esses registros ainda não identificam a futura tag de entrega.

## Evidências históricas

- Cobertura no commit da93d49: 97,46% de linhas e 94,83%
  de ramificações, considerando sete módulos.
- Quality Gate aprovado no commit 3a76227, com 84,1%
  de cobertura sobre código novo.
- Carga: duas execuções com 565 amostras cada, zero erros
  e p95 de 23 ms e 19 ms.
- Resultados e limites da carga: docs/performance/resultado-01.md.

Os números históricos pertencem às versões registradas.
Eles não devem ser apresentados como novas medições da tag final.

## O que ainda falta

- [ ] Conferir os links e a correspondência entre os documentos finais.
- [ ] Atualizar o README para orientar o acesso à versão de entrega.
- [ ] Atualizar docs/evidencias/README.md com os registros atuais.
- [ ] Atualizar CHANGELOG.md.
- [ ] Finalizar docs/decisao-qualidade.md com a decisão real.
- [ ] Registrar as contribuições reais de cada integrante.
- [ ] Registrar revisão por outro integrante.
- [ ] Definir responsáveis pelos riscos que o grupo aceitar.
- [ ] Integrar as alterações finais e conferir a CI do commit avaliado.
- [ ] Preservar os relatórios de cobertura da execução final.
- [ ] Criar e publicar a tag anotada v1.0.0-rc1.
- [ ] Conferir os links públicos do repositório e da tag.
- [ ] Fazer um único envio pelo grupo e guardar o comprovante.

## Linguagem e ferramentas

Conforme informado por Arthur, o professor permitiu utilizar
qualquer linguagem de programação.

O projeto utiliza:

- Python e Flask para a aplicação.
- SQLite para o banco de dados.
- pip e arquivos de lock para instalar dependências.
- unittest para testes automatizados.
- Playwright e Chromium para o teste de navegador.
- Coverage.py para medir cobertura.
- GitHub Actions para automatizar as verificações.
- SonarQube Cloud para análise estática e Quality Gate.
- JMeter para o teste de carga.
- Testcontainers para executar a suíte em container Linux com SQLite.

Não se declara execução de Maven nem geração de relatório JaCoCo.
A autorização relatada foi sobre a linguagem, sem presumir
aprovação específica de cada ferramenta.

## Regras do fechamento

- Não registrar revisão, contribuição ou aprovação que não aconteceu.
- Relacionar cada resultado à versão realmente testada.
- Se houver alteração de código, avaliar quais testes repetir.
- Conferir a CI do commit escolhido antes de publicar a tag.
- Não mover a tag depois de publicada.
- Usar outra versão candidata caso sejam necessárias novas correções.
- A entrega acadêmica não representa liberação para produção.bo