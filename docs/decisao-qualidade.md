# Decisão de qualidade

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

## 1. Integrantes

- Arthur Mendes Ramos da Silva.
- Nicolas Ferreira.
- Robert Oliveira.

As contribuições registradas abaixo são distintas da aprovação
individual da decisão de qualidade.

## 2. Versão candidata e rastreabilidade

A rc4 publicada é a referência automatizada identificada no estado acima.
A rc5 será sua sucessora documental; a release da rc5 deverá registrar o
commit efetivamente marcado e suas próprias execuções aprovadas.

A concordância com a entrega e os riscos documentados permanece registrada.
Esta consolidação atualiza a apresentação das evidências e das pendências,
sem ampliar o escopo das revisões ou dos testes manuais.

## 3. Proposta de decisão

Arthur propõe a entrega acadêmica com ressalvas, considerando:

- As execuções de CI aprovadas para a candidata.
- Os relatórios de cobertura e do container preservados.
- A validação histórica em clone separado e ambiente virtual novo.
- Os testes manuais realizados por Arthur.
- O relato dos testes funcionais parciais de Nicolas e Robert.
- A documentação dos limites das verificações.

A concordância dos três integrantes com a entrega acadêmica com ressalvas
está registrada neste documento. As confirmações de Nicolas e Robert foram
comunicadas por Arthur em 10/11/2026. As revisões estão nas seções 7 e 8;
os registros individuais estão ao final.

Não se declara prontidão para produção nem atendimento integral
a requisitos cuja conferência ainda está pendente.

## 4. Critérios e evidências

| Critério | Evidência | Resultado e limite |
| --- | --- | --- |
| Reprodutibilidade | [Validação de 03/11](entrega/validacao-2026-11-03.md) | Clone separado e ambiente novo no computador de Arthur, commit b55f1ef; histórico |
| Testes da rc4 | [CI #245](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42920846716) | Aprovada; suíte Python, concorrência HTTP e Chromium |
| Container da rc4 | [CI #83](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42920846792) | Aprovada; suíte de 292 testes em container Linux com SQLite |
| Cobertura da rc4 | [Relatórios](https://github.com/Arthurmrsilva/organizacao-recursos/releases/download/v1.0.0-rc4/relatorios-cobertura.3.zip) | 97,46% de linhas e 94,83% de ramificações, sete módulos |
| Sonar no commit da rc4 | [CI da main #244](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/42919624873) | Aprovada no mesmo commit ca08ea6; a execução da tag não executa Sonar |
| Testes de Nicolas | [Relato funcional](entrega/revisao-nicolas.md) | 21 cenários descritos; nenhum problema relatado nesse escopo |
| Revisões e concordância | Seções 7 e 8 e confirmações ao final | Participação registrada; não equivale a revisão integral de todo o código |
| Carga | [Relatório](performance/resultado-01.md) | Duas medições históricas de GET /login, no mesmo computador |
| Recuperação | Verificador e testes de backup | Restauração temporária, sem recuperação operacional completa |
| Requisitos obrigatórios | [RTM](rtm.md) e especificação | Limitações conhecidas ainda exigem conferência; ressalvas não dispensam requisitos |

As execuções acima pertencem à rc4. Para a rc5, conferir a CI do commit
efetivamente marcado e registrar os links nas notas da nova release.
O [índice de evidências](evidencias/README.md) separa essas referências
dos ensaios históricos.

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
As confirmações de Nicolas e Robert sobre a entrega com ressalvas
estão registradas ao final deste documento.
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
| Nicolas Ferreira | Colaborou com ideias para a programação e com a definição visual da interface, incluindo as cores do CSS. Executou e documentou 21 cenários de testes funcionais dos perfis ADMIN e RESPONSAVEL, publicou o relatório por commit e pull request e participou da revisão do código. | Contribuições informadas por Arthur em 10/11/2026; [relato funcional](entrega/revisao-nicolas.md) integrado pelo PR #9 e confirmação registrada pelo PR #12 |
| Robert Oliveira | Colaborou na elaboração dos diagramas e participou da revisão do projeto e do código. Participação em testes funcionais parciais anteriormente relatada. | Contribuições informadas por Arthur em 10/11/2026; [registro dos testes parciais](entrega/validacao-parcial-integrantes.md) |

Esta seção consolida as contribuições adicionais informadas por Arthur em
10/11/2026 e atualiza os registros anteriores de participação dos integrantes.

## 8. Revisao e confirmacao

Situacao atualizada em 10/11/2026.

| Integrante | Situacao |
| --- | --- |
| Arthur Mendes Ramos da Silva | Aprova a entrega academica com ressalvas da rc3. Aceite individual dos riscos e responsabilidade de acompanhamento registrados em 08/11/2026, conforme confirmacao ao final deste documento. |
| Nicolas Ferreira | Relato de 21 cenarios integrado pelo PR #9. Arthur informou em 10/11/2026 que Nicolas confirmou os dados do relato, a revisao realizada e a concordancia com a entrega academica com ressalvas. Ver registro de confirmacao ao final. |
| Robert Oliveira | Colaboração nos diagramas e participação na revisão do projeto e do código informadas por Arthur em 10/11/2026. Testes parciais anteriormente relatados; versão e cenários individuais a confirmar. Arthur informou em 10/11/2026 que Robert confirmou sua concordância com a entrega acadêmica e as ressalvas documentadas. |

O [relato de Nicolas](entrega/revisao-nicolas.md) registra resultados
e limites da validacao funcional. Os testes manuais nao equivalem
a revisao integral do codigo.

A integracao dos pull requests e a aprovacao da CI nao substituem
a revisao humana ou a confirmacao da decisao pelos integrantes.

## 9. Pendencias e acompanhamento

Concluido:
- Publicação da rc4, CI da tag #245 e #83 aprovada e relatórios preservados.
- Registro da concordância de Robert com a entrega e as ressalvas, comunicada por Arthur em 10/11/2026; confirmação coletiva registrada.
- Registro das contribuições de Nicolas em ideias para programação, cores do CSS e revisão.
- Registro da colaboração de Robert nos diagramas e na revisão do projeto e do código.
- Confirmação de Nicolas integrada pelo PR #12.
- Integracao do relato de Nicolas e dos resumos documentais pelo PR #9.
- CI da main apos o PR #9: testes automatizados #225 e Testcontainers #63 aprovados.
- Registro do aceite individual de Arthur e de sua responsabilidade
  pelo acompanhamento dos riscos, conforme confirmacao de 08/11/2026.

Pendente:
- Completar a identificacao do recurso vinculado ao responsavel
  e esclarecer os horarios e o ambiente descritos no relato.
- Confirmar a versao e os cenarios individuais de Robert.
- Conferir o atendimento dos requisitos obrigatorios da especificacao.
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

Candidata publicada de referência: v1.0.0-rc4.
A consolidação documental seguinte prepara a rc5, conforme o estado no início.
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

Na data deste aceite de Arthur, as confirmações dos demais integrantes
estavam pendentes. Os complementos de 10/11/2026 abaixo atualizam
esse estado com as confirmações de Nicolas e Robert.

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
A confirmação de Robert está registrada no complemento de 10/11/2026 abaixo.

O commit informado no relato permanece f3f2061.
Os detalhes exatos do recurso vinculado, dos horarios corrigidos
e dos arquivos examinados nao foram transcritos neste complemento.
Esses detalhes documentais nao sao preenchidos por suposicao.

Este complemento e posterior a rc3 e nao modifica sua tag.
O envio ao professor continua sujeito ao comprovante do formulario.

## Confirmação de Robert informada por Arthur — 10/11/2026

Arthur Mendes Ramos da Silva informou que Robert Oliveira confirmou
sua concordância com a entrega acadêmica da candidata v1.0.0-rc3,
com as ressalvas documentadas nesta decisão de qualidade.

A colaboração de Robert nos diagramas e na revisão do projeto e do código
está registrada nas seções 7 e 8. Esta confirmação atualiza as indicações
anteriores de decisão individual e confirmação coletiva pendentes.

Com o aceite de Arthur e as confirmações de Nicolas e Robert, fica registrada
a concordância dos três integrantes com a entrega acadêmica com ressalvas.
Os limites técnicos e o escopo dos testes permanecem os documentados.
Este complemento não modifica a tag rc3 nem comprova o envio ao professor.
