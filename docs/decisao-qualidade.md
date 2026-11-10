# Decisão de qualidade

## Complemento documental - testes de Nicolas - 09/11/2026

Nicolas Ferreira relatou a execucao de 21 cenarios manuais:
15 do perfil ADMIN e 6 do perfil RESPONSAVEL, em 09/11/2026.
Segundo o executor, nenhum problema foi encontrado nos passos
descritos. O trecho de terminal apresentado nao contem erros 500
nem traceback.

Consulte o [relato funcional de Nicolas](entrega/revisao-nicolas.md) para os resultados,
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
Projeto: Organização de Recursos.
Disciplina: Qualidade de Software.

Estado: proposta de entrega acadêmica com ressalvas.
Proponente: Arthur Mendes Ramos da Silva.
Confirmação coletiva: pendente.

## 1. Integrantes

- Arthur Mendes Ramos da Silva.
- Nicolas Ferreira.
- Robert Oliveira.

As contribuições registradas abaixo são distintas da aprovação
individual da decisão de qualidade.

## 2. Versao candidata e complementos documentais

Candidata publicada de referencia: v1.0.0-rc3.

Commit da tag:
b2949306587d37801be304101d36bf6974bcb6f0.

[Release rc3 e relatorios](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc3).

A release identifica as execucoes automatizadas da candidata
e os relatorios correspondentes.

Os resultados da rc2 na secao 4 sao historicos e permanecem
associados ao commit 12fae657686f2179da3feae561031ff3622c937e.
Nao representam novas medicoes da rc3.

O aceite individual de Arthur e o relato funcional de Nicolas
sao complementos posteriores a publicacao da rc3.
O relato de Nicolas e seus resumos foram integrados pelo PR #9;
a situacao dos integrantes foi atualizada pelo PR #10.
Esses complementos nao modificam o conteudo da tag publicada.

## 3. Proposta de decisão

Arthur propõe a entrega acadêmica com ressalvas, considerando:

- As execuções de CI aprovadas para a candidata.
- Os relatórios de cobertura e do container preservados.
- A validação histórica em clone separado e ambiente virtual novo.
- Os testes manuais realizados por Arthur.
- O relato dos testes funcionais parciais de Nicolas e Robert.
- A documentação dos limites das verificações.

A proposta ainda não constitui decisão coletiva assinada pelo grupo.
A revisão do código e o aceite nominal dos riscos permanecem pendentes.

Não se declara prontidão para produção nem atendimento integral
a requisitos cuja conferência ainda está pendente.

## 4. Critérios e evidências

| Critério | Evidência | Resultado e limite |
| --- | --- | --- |
| Instalação em ambiente novo | Validação de 03/11/2026 | Clone separado no computador de Arthur, no commit b55f1ef |
| Suíte no clone limpo | Registro histórico | 292 testes aprovados em 86,353 segundos |
| Fluxo manual por Arthur | Registro de validação | Criação, conflito, cancelamento e histórico verificados |
| CI da candidata | Testes automatizados #208 e Testcontainers #46 | Aprovados no commit da rc2 |
| Cobertura da candidata | Relatórios anexados à rc2 | 97,46% de linhas e 94,83% de ramificações, em sete módulos |
| Suíte no container | Log anexado à rc2 | 292 testes aprovados em 19,614 segundos |
| Concorrência HTTP e Chromium | CI #208 | Cenários automatizados aprovados |
| Análise estática | Workflow #207 da main no commit da rc2 | Referência da análise Sonar; a execução da tag não a substitui |
| Complemento documental | CI #211 e #49 | Aprovada no commit d937c1e |
| Testes dos integrantes | Relato registrado por Arthur | Validação funcional parcial, sem falhas relatadas nos cenários listados |
| Desempenho | Duas execuções históricas documentadas | Cenário limitado a GET /login no mesmo computador |
| Recuperação | Verificador e testes de backup | Restauração temporária, sem comprovação de recuperação operacional completa |
| Requisitos obrigatórios | RTM e especificação da disciplina | Conferência final pendente |

[Índice de evidências e links das execuções](evidencias/README.md).

[Validação histórica em clone limpo](entrega/validacao-2026-11-03.md).

## 5. Testes funcionais parciais dos integrantes

Conforme relato recebido por Arthur, Nicolas Ferreira e Robert Oliveira
participaram de testes manuais na sexta-feira anterior à publicação
da rc2, nos seguintes fluxos:

- Login.
- Criação de reserva.
- Aprovação de reserva.
- Recusa de reserva.
- Bloqueio de tentativa de reserva conflitante.
- Consulta ao histórico.

Não foram relatadas falhas nesses cenários.

A versão utilizada é presumida como rc1 pela cronologia,
ainda sem confirmação da tag ou do commit.

Não há, neste registro, identificação dos cenários executados
individualmente por cada participante ou evidências de cada execução.
Por isso, não se atribui percentual de conclusão.

O bloqueio esperado é de sobreposição de horários para o mesmo recurso.
Reservas no mesmo dia podem ser permitidas quando não houver sobreposição.

[Registro completo e limitações](entrega/validacao-parcial-integrantes.md).

## 6. Riscos e limitações

Arthur Mendes Ramos da Silva registrou seu aceite individual
em 08/11/2026 e assumiu o acompanhamento dos tratamentos abaixo.
As confirmacoes individuais de Nicolas e Robert permanecem pendentes.
A coluna de tratamento descreve propostas, não aprovações já concedidas.

| Limitação | Impacto | Tratamento proposto e justificativa | Responsável e aceite |
| --- | --- | --- | --- |
| Gestão completa de usuários e edição/desativação de recursos incompletas na interface | Parte da administração depende de procedimentos externos | Conferir a especificação e implementar o que for obrigatório; não presumir dispensa | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| Carga limitada a GET /login no mesmo computador | Não mede desempenho dos fluxos autenticados | Restringir as conclusões ao cenário medido e ampliar o ensaio se exigido | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| Execução com servidor de desenvolvimento | Não comprova implantação apropriada para produção | Restringir o uso à demonstração acadêmica | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| Cobertura calculada em sete módulos | Os percentuais não abrangem todos os arquivos | Informar o escopo junto das métricas | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| SQLite dentro do container | Não verifica servidor de banco separado | Explicar a arquitetura e conferir sua adequação à especificação | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| Ambiente externo do Testcontainers sem lock completo com hashes | Menor reprodutibilidade das dependências transitivas | Preservar logs e documentar a configuração utilizada | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| Restauração em diretório temporário | Não demonstra recuperação operacional completa | Apresentar o resultado como verificação de integridade e restauração no escopo testado | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |
| Testes dos integrantes registrados por relato indireto e versão presumida | Rastreabilidade limitada da validação manual | Obter confirmação dos participantes sobre versão, cenários e resultados | Arthur Mendes Ramos da Silva; aceite individual em 08/11/2026; acompanhamento assumido |

Aceitar um risco exige confirmação do responsável nominal.
Uma ressalva não substitui o atendimento de requisito obrigatório
nem a autorização do professor para mudança de escopo.

## 7. Contribuições individuais

| Integrante | Participação registrada | Base do registro |
| --- | --- | --- |
| Arthur Mendes Ramos da Silva | Implementação, ajustes, testes, documentação e integração no GitHub | Histórico de commits e registros de validação |
| Nicolas Ferreira | Validacao funcional manual de 21 cenarios dos perfis ADMIN e RESPONSAVEL | [Relato do executor](entrega/revisao-nicolas.md), integrado pelo PR #9; versao informada f3f2061, correspondencia com o ambiente a confirmar |
| Robert Oliveira | Participação em testes funcionais parciais | Relato recebido por Arthur; cenários individuais e versão a confirmar |

Esta seção atualiza o registro anterior, de 03/11/2026,
que ainda não incluía a participação funcional posteriormente relatada.

## 8. Revisao e confirmacao

Situacao atualizada em 09/11/2026.

| Integrante | Situacao |
| --- | --- |
| Arthur Mendes Ramos da Silva | Aprova a entrega academica com ressalvas da rc3. Aceite individual dos riscos e responsabilidade de acompanhamento registrados em 08/11/2026, conforme confirmacao ao final deste documento. |
| Nicolas Ferreira | Relato de 21 cenarios integrado pelo PR #9. Arthur informou em 10/11/2026 que Nicolas confirmou os dados do relato, a revisao realizada e a concordancia com a entrega academica com ressalvas. Ver registro de confirmacao ao final. |
| Robert Oliveira | Testes parciais anteriormente relatados por Arthur. Versao e cenarios individuais a confirmar; revisao do codigo e decisao individual final pendentes. |

O [relato de Nicolas](entrega/revisao-nicolas.md) registra resultados
e limites da validacao funcional. Os testes manuais nao equivalem
a revisao integral do codigo.

A integracao dos pull requests e a aprovacao da CI nao substituem
a revisao humana ou a confirmacao da decisao pelos integrantes.

## 9. Pendencias e acompanhamento

Concluido:
- Integracao do relato de Nicolas e dos resumos documentais pelo PR #9.
- CI da main apos o PR #9: testes automatizados #225 e Testcontainers #63 aprovados.
- Registro do aceite individual de Arthur e de sua responsabilidade
  pelo acompanhamento dos riscos, conforme confirmacao de 08/11/2026.

Pendente:
- Confirmar a correspondencia entre a versao informada por Nicolas
  (f3f2061) e o ambiente efetivamente executado.
- Completar a identificacao do recurso vinculado ao responsavel
  e esclarecer os horarios e o ambiente descritos no relato.
- Confirmar a versao e os cenarios individuais de Robert.
- Concluir e registrar a revisao do codigo por outro integrante.
- Conferir o atendimento dos requisitos obrigatorios da especificacao.
- Obter as decisoes individuais de Nicolas e Robert sobre a entrega
  e as ressalvas, para registrar a confirmacao coletiva.
- Conferir a correspondencia entre a candidata publicada,
  os complementos posteriores e as evidencias.
- Confirmar o envio no formulario e preservar o comprovante.

## 10. Documentos de apoio

- [README](../README.md).
- [Checklist](entrega/checklist.md).
- [Índice de evidências](evidencias/README.md).
- [RTM](rtm.md).
- [Relatório de qualidade](relatorio-qualidade.md).
- [Defeitos](defeitos/README.md).
- [Plano de testes](../PLANO_TESTES.md).
- [Arquitetura](../ARQUITETURA.md).
- [Segurança](../SEGURANCA.md).
- [Desempenho](performance/resultado-01.md).
- [Changelog](../CHANGELOG.md).

## 11. Envio

Repositório:
https://github.com/Arthurmrsilva/organizacao-recursos

Candidata publicada de referencia: v1.0.0-rc3.
Os complementos documentais posteriores estao na main.
Responsável pelo envio: a confirmar.
Data de envio: não confirmada.
Comprovante: não apresentado neste registro.

Um integrante envia pelo grupo. O envio não deve ser declarado
concluído antes da confirmação de recebimento do formulário.

## Confirmacao individual de Arthur - 08/11/2026

Arthur Mendes Ramos da Silva confirmou expressamente a aprovacao
da entrega academica com ressalvas da candidata v1.0.0-rc3,
commit b2949306587d37801be304101d36bf6974bcb6f0.

Arthur aceita os riscos tecnicos descritos na secao de riscos
e limitacoes deste documento e assume a responsabilidade pelo
acompanhamento dos tratamentos propostos:

- Conferencia das limitacoes administrativas com a especificacao.
- Limites dos testes de carga e do servidor de desenvolvimento.
- Escopo da cobertura de sete modulos Python.
- Uso de SQLite dentro do container.
- Reprodutibilidade das dependencias externas do Testcontainers.
- Limites da verificacao de backup e restauracao.
- Obtencao das confirmacoes de versao, cenarios e resultados dos
  testes parciais relatados pelos integrantes.

O aceite considera a finalidade de demonstracao e entrega academica
e as evidencias publicadas na release rc3. As limitacoes e seus
impactos permanecem reconhecidos; o acompanhamento nao significa
que as correcoes propostas ja foram realizadas.

Requisitos obrigatorios eventualmente nao atendidos precisam ser
corrigidos ou ter a alteracao de escopo autorizada pelo professor.
Este aceite nao declara prontidao para producao.

Este registro atualiza, para Arthur, as indicacoes anteriores de
aceite nominal pendente. A responsabilidade de acompanhamento dos
riscos passa a ser de Arthur Mendes Ramos da Silva.

A confirmacao coletiva e a revisao do codigo por outro integrante
continuam pendentes. Nenhuma aprovacao e atribuida a Nicolas Ferreira
ou Robert Oliveira por este registro.

Este complemento e posterior a publicacao da rc3 e nao modifica
o conteudo da tag. O envio no formulario continua sem comprovacao
neste documento.

## Confirmacao de Nicolas informada por Arthur - 10/11/2026

Arthur Mendes Ramos da Silva informou que Nicolas Ferreira confirmou:
- Os dados da validacao funcional relatada.
- A realizacao da revisao do codigo no escopo que examinou.
- A concordancia com a entrega academica com as ressalvas documentadas.

Fonte deste complemento: confirmacao comunicada por Arthur.
O relato identifica 21 cenarios: A1 a A15 e R1 a R6.
Nao se declara cobertura manual integral nem revisao de 100% do codigo.

As indicacoes anteriores de revisao e decisao individual de Nicolas
pendentes ficam atualizadas por esta confirmacao.
A confirmacao de Robert permanece sem registro.

O commit informado no relato permanece f3f2061.
Os detalhes exatos do recurso vinculado, dos horarios corrigidos
e dos arquivos examinados nao foram transcritos neste complemento.
Esses detalhes documentais nao sao preenchidos por suposicao.

Este complemento e posterior a rc3 e nao modifica sua tag.
O envio ao professor continua sujeito ao comprovante do formulario.
