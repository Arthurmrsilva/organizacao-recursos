# Matriz de Rastreabilidade — RTM

Projeto: Organização de Recursos  
Última atualização: 25/10/2026

Esta matriz relaciona requisitos, riscos, testes e evidências.
As tabelas principais representam a situação atual.
As evidências históricas preservam os resultados de cada etapa.

## Legenda

- Parcial: somente parte do requisito foi implementada ou verificada.
- Pendente: implementação ou verificação ainda não realizada.
- Implementado nesta etapa: comportamento disponível e verificado no escopo descrito.
- Testes planejados não representam evidência de aprovação.
- Quantidade de testes aprovados não representa percentual de cobertura.

## Requisitos funcionais

| ID | Requisito | Risco | Testes e verificações | Situação atual |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | test_consulta.py, test_cancelamento_http.py, test_aprovacoes_http.py e test_auditoria_http.py | Parcial: login e permissões das funcionalidades atuais verificados; ampliar conforme novas rotas forem criadas |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos ou perda de informação | Cadastro dos três tipos, validação dos campos, autorização e consulta de ativos em test_consulta.py | Implementado e testado nesta etapa; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto ou recurso indisponível listado | Filtros de pesquisa e entradas inválidas em test_consulta.py | Parcial: tipo, capacidade, localização e competência disponíveis; pesquisa por disponibilidade pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | test_reservas.py, test_minhas_reservas.py e test_cancelamento_http.py | Parcial: criação, consulta das próprias reservas e cancelamento disponíveis; alteração pendente |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos do mesmo recurso no mesmo horário | Testes de sobreposição e horários consecutivos em test_reservas.py; verificação de conflito na aprovação em test_aprovacoes.py | Parcial: conflito por recurso implementado; ampliar cenários explícitos para todos os tipos e agenda do professor |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas para o mesmo recurso e período | test_duas_solicitacoes_simultaneas em test_reservas.py | Verificado no serviço com SQLite: uma solicitação aceita, outra recusada e apenas uma reserva gravada; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | test_aprovacoes.py e test_aprovacoes_http.py | Implementado nesta etapa: recursos restritos e professores aguardam aprovação do responsável vinculado; interface de vinculação pendente |
| RF08 | Bloquear recursos em manutenção | Reserva de recurso indisponível | Planejado: testar reservas durante e fora do bloqueio | Pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | Planejado: retirada, devolução e operações inválidas | Pendente |
| RF10 | Manter histórico auditável | Mudanças sem identificação ou rastreio | test_auditoria.py, test_auditoria_http.py e conferência manual da tela | Parcial: criação, cancelamento, aprovação e rejeição auditados; consulta dos 100 eventos mais recentes exclusiva do administrador; ampliar para futuras operações |
| RF11 | Notificação simulada ou integração externa | Usuário não informado sobre a reserva | Planejado: conferir notificações dos eventos da reserva | Pendente |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | Planejado: comparar resultados com dados conhecidos | Pendente |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso e erros sem orientação | Mensagens verificadas pelos testes HTTP e verificações manuais da interface | Parcial: temas por perfil, botões e filtros disponíveis; testes de navegador e avaliação em diferentes telas pendentes |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar, usar e manter | README inicial e esta matriz | Parcial: ampliar documentação de instalação, fluxos e interfaces |

## Regras críticas

| ID | Regra | Risco | Verificação atual ou planejada | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Validação no serviço e restrição no banco; ampliar testes explícitos de término igual ou anterior | Parcial |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Testes de sobreposição e horários consecutivos; conflito na aprovação | Parcial: ampliar cenários por tipo de recurso |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | test_duas_solicitacoes_simultaneas | Verificado no serviço; teste concorrente por HTTP pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Planejado: testar interseção com bloqueio | Pendente |
| RC05 | Fluxo SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Aprovação implementada e testada; retirada e devolução pendentes | Parcial |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Rejeição e cancelamento testados; registro de não comparecimento pendente | Parcial |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Testes de perfil, vínculo com o recurso, prazo e estado da reserva | Implementado e testado nesta etapa |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Sem exclusão física disponível; cancelamento após início bloqueado e testado | Parcial: revisar também nas futuras funcionalidades administrativas |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Auditoria das operações atuais, identificação do autor e testes de rollback | Parcial: cobrir novas transições quando implementadas |

## Testes existentes

A execução local mais recente apresentou **65 métodos de teste aprovados**.

Alguns métodos utilizam `subTest` para verificar vários cenários.
O total de métodos não corresponde ao total de cenários nem à cobertura.

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização do cadastro, validação, persistência e filtros de recursos |
| tests/test_reservas.py | Criação, conflitos, horários consecutivos, concorrência e regras de cancelamento |
| tests/test_minhas_reservas.py | Login obrigatório, isolamento entre usuários e mensagens de lista vazia nos filtros Ativas, Histórico e Todas |
| tests/test_cancelamento_http.py | Autenticação, autorização e proteção CSRF na rota de cancelamento |
| tests/test_aprovacoes.py | Regras de aprovação, rejeição, vínculo do responsável, prazo, estado e conflito |
| tests/test_aprovacoes_http.py | Acesso às rotas, perfis, proteção CSRF e isolamento por responsável |
| tests/test_auditoria.py | Registro das operações atuais, identificação do autor e rollback da operação e da auditoria |
| tests/test_auditoria_http.py | Login obrigatório, bloqueio de responsável e solicitante, acesso do administrador e visibilidade do botão |

Os testes utilizam bancos SQLite temporários.
Os testes HTTP atuais usam o cliente de testes do Flask.

Esses testes não substituem os testes de navegador, API em
caixa-preta por HTTP externo, carga ou banco em container previstos
para a entrega final.

Os filtros Ativas, Histórico e Todas também foram conferidos
manualmente. Ainda faltam testes automatizados específicos para
a distribuição dos registros entre esses filtros e sua ordenação.

## Evidências registradas

| ID | Evidência |
| --- | --- |
| EV01 | Commit 1ed928d: etapa RED dos testes de acesso ao cadastro |
| EV02 | Commit 49b42fe: etapa GREEN com implementação do cadastro e testes de acesso aprovados |
| EV03 | Commit 250f9b2: ampliação para 16 testes e configuração do GitHub Actions |
| EV04 | Execução local histórica: 16 testes aprovados em 6,098 segundos |
| EV05 | GitHub Actions do commit 250f9b2 aprovado em 21 segundos |
| EV06 | Cadastro manual da Sala 202 confirmado na interface |
| EV07 | Pull Request nº 1 aberto; revisão por outro integrante pendente |
| EV08 | Commit 940a392: criação de reservas e testes de conflito, horários consecutivos e concorrência |
| EV09 | Execução local do commit 940a392: 22 testes aprovados em 7,883 segundos |
| EV10 | GitHub Actions: execuções #13 de push e #14 de Pull Request aprovadas |
| EV11 | Commit ecb0eb7: cancelamento de reservas; execução local de 31 testes aprovada em 9,850 segundos |
| EV12 | Teste manual: reserva nº 3 cancelada e reserva nº 4 aprovada para o mesmo recurso e período em 30/10/2026, das 15:30 às 16:30 |
| EV13 | Commit 7ae60b7: testes HTTP de cancelamento |
| EV14 | Commit cca4432: aprovação por responsável, vínculo com recurso e identificação visual dos perfis |
| EV15 | Commit 9946585: testes HTTP de aprovação; execução local de 56 testes aprovada |
| EV16 | GitHub Actions: execução #27 aprovada em 21 segundos e execução #28 do Pull Request aprovada em 22 segundos |
| EV17 | Testes manuais: reserva nº 6 aprovada pelo responsável e depois cancelada pelo próprio solicitante; reserva nº 7 rejeitada |
| EV18 | Commit 1515dcd: tabela de auditoria, registro no serviço e testes automatizados |
| EV19 | Commit 0fc4cf5: consulta de auditoria e filtros da listagem de reservas; execução local de 62 testes aprovada em 15,956 segundos; CI confirmado pelo integrante |
| EV20 | Commit 6ac9d65: botão de auditoria no menu do administrador |
| EV21 | Teste manual: administrador consultou os eventos de criação e cancelamento, com autor, data, horário e situações anterior e nova |
| EV22 | Teste manual: acesso direto de responsável a /auditoria bloqueado com a mensagem “Acesso negado. Área exclusiva do administrador.” |
| EV23 | Commit db1e5e8: testes HTTP de acesso à auditoria; execução local de 65 testes aprovada em 15,054 segundos; confirmação do CI desse commit pendente |

### Links

- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [Execuções do GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)

Os prints ainda precisam ser organizados no pacote de entrega,
com identificação do cenário, data e resultado.
As evidências históricas mantêm suas contagens originais.

## Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | Ainda não medida |
| Cobertura de branches | Pelo menos 70% | Ainda não medida |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Parcial: regras mapeadas; implementação e verificações restantes pendentes |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa ainda não realizada |
| Testes unitários isolados | Regras de negócio verificadas isoladamente | Pendente: testes de serviço atuais utilizam persistência real |
| Testes de integração | Persistência real e integração das camadas | Parcial: SQLite temporário e cliente de testes do Flask |
| Testes em container | Banco com Testcontainers | Pendente |
| Integrações externas | WireMock quando aplicável | Pendente de definição e implementação |
| API em caixa-preta | Aplicação acessada externamente por HTTP | Pendente |
| Testes ponta a ponta | Fluxos no navegador | Pendente: verificações manuais não substituem automação |
| Concorrência | Uma única reserva aceita para o mesmo período | Verificado no serviço; concorrência por HTTP e carga pendentes |
| TDD ou BDD | Pelo menos uma funcionalidade com evidências | RED e GREEN registrados para acesso ao cadastro; consolidar documentação do ciclo |
| CI | Execução em push e Pull Requests | Workflow ativo com execuções aprovadas; conferir execução do commit db1e5e8 |
| Análise estática | Projeto integrado ao SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revisão por pares | Revisão real de outro integrante | Pendente |
| Arquitetura | C4, sequências críticas, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Pendente de consolidação |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio do projeto pelo grupo | Pendente |

## Histórico — Cancelamento de reservas — 25/10/2026

### Funcionalidades implementadas

- Consulta das próprias reservas.
- Cancelamento pelo proprietário da reserva.
- Cancelamento permitido em SOLICITADA e APROVADA antes do início.
- Preservação da reserva cancelada no histórico.
- Liberação do período após cancelamento.

### Evidências da etapa

- Execução local de 31 testes aprovada em 9,850 segundos.
- Commit ecb0eb7.
- Reserva nº 3 cancelada e reserva nº 4 aprovada para o mesmo
  recurso e período em 30/10/2026, das 15:30 às 16:30.

### Evolução posterior

Os testes HTTP de cancelamento e a auditoria foram acrescentados
em etapas posteriores. A alteração de reservas continua pendente.

## Histórico — Aprovação de reservas — 25/10/2026

### Funcionalidades implementadas

- Vinculação de responsável ao recurso por script local.
- Consulta das solicitações dos recursos do responsável conectado.
- Aprovação e rejeição de reservas em SOLICITADA.
- Bloqueio de outros perfis e de responsáveis sem vínculo.
- Bloqueio da avaliação após o início.
- Verificação de recurso ativo e conflitos na aprovação.
- Liberação do período após rejeição.
- Temas por perfil: administrador azul, responsável roxo
  e solicitante verde.

### Evidências da etapa

- Reserva nº 6 aprovada e posteriormente cancelada pelo solicitante.
- Reserva nº 7 rejeitada pelo responsável.
- Execução local de 56 testes aprovada.
- Commits cca4432 e 9946585.
- GitHub Actions #27 e #28 aprovados.

### Pendências atuais relacionadas

- Interface administrativa para vincular responsáveis.
- Notificações de aprovação e rejeição.
- Medição da cobertura das regras críticas.

A auditoria das operações atuais foi implementada posteriormente.

## Atualização — Auditoria e organização das reservas — 25/10/2026

### Funcionalidades implementadas

- Registro de criação, cancelamento, aprovação e rejeição.
- Identificação da reserva, autor, ação, data e horário.
- Registro das situações anterior e nova.
- Gravação da auditoria na mesma transação da operação.
- Rollback conjunto se a gravação falhar.
- Consulta dos 100 eventos mais recentes pelo administrador.
- Botão de auditoria visível apenas ao administrador.
- Bloqueio de acesso direto para os outros perfis.
- Filtros Ativas, Histórico e Todas em Minhas reservas.

### Critério dos filtros

- Ativas: reservas em SOLICITADA, APROVADA ou EM_USO,
  com término posterior ao momento da consulta.
- Histórico: reservas que não atendem ao critério de Ativas.
- Todas: todas as reservas do usuário conectado.

O fim do período não altera automaticamente a situação da reserva.
Uma reserva aprovada com período encerrado aparece no Histórico,
mantendo a situação APROVADA até existir uma operação que a altere.

### Limitações atuais

- Eventos anteriores à implantação da auditoria não são reconstruídos.
- Os horários seguem o relógio local do servidor.
- A consulta apresenta os 100 eventos mais recentes, sem paginação.
- Operações futuras deverão acrescentar seus próprios eventos.
- Testes de acesso HTTP não comprovam, por si só, o limite e a
  ordenação dos eventos.
- Cobertura de linhas e branches ainda não foi medida.

### Resultado mais recente

Execução local: 65 testes aprovados em 15,054 segundos.

Commit dos testes de acesso à auditoria: db1e5e8.
Confirmação da execução do CI desse commit ainda pendente.