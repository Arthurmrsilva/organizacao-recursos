# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 26/10/2026

Esta matriz relaciona os requisitos do projeto aos riscos, testes e evidências.

As tabelas principais apresentam a situação atual. Os registros históricos preservam os resultados das etapas anteriores.

## 1. Legenda

- **Implementado e verificado:** funcionalidade disponível e verificada no escopo descrito.
- **Parcial:** parte do requisito ainda precisa ser implementada ou verificada.
- **Pendente:** implementação ou verificação ainda não realizada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes aprovados não representa percentual de cobertura.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e verificações | Situação atual |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Testes de consulta, cancelamento, aprovação, auditoria, manutenção e permissões no serviço de materiais | Parcial: permissões atuais verificadas; testes HTTP específicos de materiais pendentes |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | Cadastro, validação, autorização e consulta em test_consulta.py | Implementado e verificado nesta etapa; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | Filtros e entradas inválidas em test_consulta.py | Parcial: pesquisa por disponibilidade pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | test_reservas.py, test_minhas_reservas.py e test_cancelamento_http.py | Parcial: criação, consulta e cancelamento disponíveis; alteração pendente |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos do mesmo recurso no mesmo horário | Testes de sobreposição, horários consecutivos e conflito na aprovação | Parcial: ampliar cenários explícitos para todos os tipos |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas para o mesmo período | test_duas_solicitacoes_simultaneas em test_reservas.py | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | test_aprovacoes.py e test_aprovacoes_http.py | Implementado e verificado; interface para vincular responsáveis pendente |
| RF08 | Bloquear recursos em manutenção | Reserva de recurso indisponível | test_manutencoes.py, test_manutencoes_http.py e verificações manuais | Implementado e verificado; teste específico de concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py e fluxo manual da reserva nº 11 | Implementado e verificado no serviço e manualmente; testes HTTP específicos e automação no navegador pendentes |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, materiais e conferência manual | Parcial: operações atuais auditadas; ampliar para futuras operações |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | Testes a definir durante a implementação | Pendente |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | Planejado: comparar resultados com dados conhecidos | Pendente |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP existentes e verificações manuais | Parcial: avaliação em diferentes telas e testes automatizados de navegador pendentes |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README inicial e esta matriz | Parcial: ampliar instalação, fluxos e interfaces |

## 3. Regras críticas

| ID | Regra | Risco | Verificação | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Validação no serviço e restrição no banco | Parcial: ampliar testes explícitos de término igual ou anterior |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Testes de sobreposição, horários consecutivos e aprovação | Parcial: ampliar cenários por tipo de recurso |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | test_duas_solicitacoes_simultaneas | Verificado no serviço; concorrência por HTTP pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Testes de manutenção e verificação manual | Implementado e verificado; concorrência específica pendente |
| RC05 | Fluxo SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Testes de aprovação e materiais; fluxo manual da reserva nº 11 | Implementado para materiais e verificado no serviço e manualmente |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Rejeição e cancelamento testados | Parcial: não comparecimento pendente |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Testes de perfil, vínculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Sem exclusão física disponível; cancelamento após início bloqueado | Parcial: revisar nas futuras funcionalidades administrativas |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Auditoria das operações atuais, identificação do autor e rollback | Parcial: transições atuais auditadas; ampliar para novas transições |

## 4. Testes automatizados existentes

### Resultado local mais recente

- **Data:** 26/10/2026.
- **Resultado:** 103 testes aprovados.
- **Tempo:** 28,560 segundos.
- **Resultado apresentado no terminal:** OK.

Alguns métodos utilizam `subTest` para verificar vários cenários.

O total de métodos não corresponde ao total de cenários nem ao percentual de cobertura.

### Arquivos de teste

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização, cadastro, validação, persistência e filtros |
| tests/test_reservas.py | Criação, conflitos, horários consecutivos, concorrência e regras de cancelamento |
| tests/test_minhas_reservas.py | Login obrigatório, isolamento entre usuários e mensagens de lista vazia |
| tests/test_cancelamento_http.py | Autenticação, autorização e CSRF no cancelamento |
| tests/test_aprovacoes.py | Aprovação, rejeição, vínculo do responsável, prazo, estado e conflito |
| tests/test_aprovacoes_http.py | Acesso às rotas, perfis, CSRF e isolamento por responsável |
| tests/test_auditoria.py | Registro das operações, identificação do autor e rollback |
| tests/test_auditoria_http.py | Login obrigatório, permissões e visibilidade do botão |
| tests/test_manutencoes.py | Períodos de manutenção, conflitos e bloqueio de reservas |
| tests/test_manutencoes_http.py | Permissões, CSRF, cadastro e consulta de manutenção |
| tests/test_materiais.py | Retirada, devolução, permissões, horários, estados, manutenção e auditoria |

### Como executar

Na raiz do projeto, pelo terminal do VS Code:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Limitações dos testes atuais

- Os testes utilizam bancos SQLite temporários.
- Os testes HTTP existentes usam o cliente de testes do Flask.
- Ainda faltam testes externos por HTTP, automação no navegador e carga.
- Ainda falta a verificação com banco em container prevista no enunciado.
- Os filtros Ativas, Histórico e Todas foram conferidos manualmente, mas precisam de testes específicos de distribuição e ordenação.
- A cobertura de linhas e branches ainda não foi medida.

## 5. Evidências registradas

| ID | Evidência |
| --- | --- |
| EV01 | Commit 1ed928d: etapa RED dos testes de acesso ao cadastro |
| EV02 | Commit 49b42fe: etapa GREEN com implementação do cadastro |
| EV03 | Commit 250f9b2: ampliação para 16 testes e configuração do GitHub Actions |
| EV04 | Execução local histórica: 16 testes aprovados em 6,098 segundos |
| EV05 | GitHub Actions do commit 250f9b2 aprovado em 21 segundos |
| EV06 | Cadastro manual da Sala 202 confirmado na interface |
| EV07 | Pull Request nº 1 aberto; revisão por outro integrante pendente |
| EV08 | Commit 940a392: reservas, conflitos, horários consecutivos e concorrência |
| EV09 | Execução local do commit 940a392: 22 testes aprovados em 7,883 segundos |
| EV10 | GitHub Actions: execuções #13 de push e #14 de Pull Request aprovadas |
| EV11 | Commit ecb0eb7: cancelamento; 31 testes aprovados em 9,850 segundos |
| EV12 | Reserva nº 3 cancelada e reserva nº 4 aprovada para o mesmo recurso e período em 30/10/2026, das 15:30 às 16:30 |
| EV13 | Commit 7ae60b7: testes HTTP de cancelamento |
| EV14 | Commit cca4432: aprovação por responsável, vínculo e temas por perfil |
| EV15 | Commit 9946585: testes HTTP de aprovação; 56 testes aprovados |
| EV16 | GitHub Actions #27 aprovado em 21 segundos e #28 aprovado em 22 segundos |
| EV17 | Reserva nº 6 aprovada e depois cancelada pelo solicitante; reserva nº 7 rejeitada |
| EV18 | Commit 1515dcd: tabela de auditoria, registro no serviço e testes |
| EV19 | Commit 0fc4cf5: consulta de auditoria e filtros; 62 testes aprovados em 15,956 segundos; GitHub Actions #33 aprovado em 26 segundos |
| EV20 | Commit 6ac9d65: botão de auditoria no menu do administrador |
| EV21 | Administrador consultou criação e cancelamento com autor, horário e situações |
| EV22 | Acesso direto de responsável a /auditoria bloqueado |
| EV23 | Commit db1e5e8: testes HTTP de auditoria; 65 testes aprovados em 15,054 segundos; GitHub Actions #37 aprovado em 22 segundos |
| EV24 | Etapa de manutenção: 86 testes aprovados em 21,313 segundos |
| EV25 | Manutenção nº 1 da Sala 101 em 01/11/2026, das 14:00 às 16:00; conflitos bloqueados e reserva nº 9 aceita a partir das 16:00 |
| EV26 | Reserva nº 11 do Projetor 01: aprovação, retirada e devolução conferidas em 26/10/2026 |
| EV27 | Auditoria da reserva nº 11: retirada às 20:17:10 e devolução às 20:18:04 pelo Administrador do projeto |
| EV28 | Execução local em 26/10/2026: 103 testes aprovados em 28,560 segundos |
| EV29 | Commit 22014eb: gestão de materiais com auditoria e testes; push confirmado para funcionalidade/login |
| EV30 | GitHub Actions #45: push do commit 22014eb aprovado em 17 segundos |
| EV31 | GitHub Actions #46: atualização do Pull Request nº 1 aprovada em 23 segundos |

### Links do projeto

- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Commit da gestão de materiais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/22014eb)

### Organização das evidências

Os prints precisam ser organizados no pacote de entrega com:

- Identificação do cenário.
- Data da execução.
- Resultado esperado.
- Resultado observado.
- Requisito ou regra relacionado.

As evidências históricas mantêm suas contagens originais.

As execuções #45 e #46 foram confirmadas como aprovadas nas telas do GitHub Actions.

A aprovação automática do workflow não substitui a revisão por outro integrante.

## 6. Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | Ainda não medida |
| Cobertura de branches | Pelo menos 70% | Ainda não medida |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Parcial |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa pendente |
| Testes unitários isolados | Verificar regras sem dependências reais | Pendente: testes de serviço atuais utilizam persistência real |
| Testes de integração | Verificar persistência e integração das camadas | Parcial: SQLite temporário e cliente Flask |
| Testes em container | Banco com Testcontainers | Pendente |
| Integrações externas | WireMock quando aplicável | Pendente de definição |
| API em caixa-preta | Acesso externo por HTTP | Pendente |
| Testes ponta a ponta | Automação dos fluxos no navegador | Pendente |
| Concorrência | Uma única reserva aceita para o mesmo período | Verificado no serviço; HTTP e carga pendentes |
| TDD ou BDD | Pelo menos uma funcionalidade com evidências | RED e GREEN registrados; consolidar documentação |
| CI | Execução em push e Pull Requests | Confirmado: execuções #45 e #46 aprovadas na etapa de materiais |
| Análise estática | Integração ao SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revisão por pares | Revisão de outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Pendente de consolidação |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio pelo grupo | Pendente |

A aceitação de Python e das ferramentas equivalentes às citadas no enunciado ainda precisa ser confirmada com o professor.

## 7. Histórico — Cancelamento de reservas

**Data da etapa:** 25/10/2026.

### Funcionalidades

- Consulta das próprias reservas.
- Cancelamento pelo proprietário.
- Cancelamento em SOLICITADA e APROVADA antes do início.
- Preservação da reserva cancelada.
- Liberação do período após cancelamento.

### Evidências

- 31 testes aprovados em 9,850 segundos.
- Commit ecb0eb7.
- Reserva nº 3 cancelada.
- Reserva nº 4 aprovada para o mesmo recurso e período: 30/10/2026, das 15:30 às 16:30.

Os testes HTTP e a auditoria foram acrescentados posteriormente.

A alteração de reservas continua pendente.

## 8. Histórico — Aprovação de reservas

**Data da etapa:** 25/10/2026.

### Funcionalidades

- Vinculação de responsável ao recurso por script local.
- Consulta das solicitações dos recursos vinculados.
- Aprovação e rejeição de reservas em SOLICITADA.
- Bloqueio de outros perfis e responsáveis sem vínculo.
- Bloqueio de avaliação após o início.
- Verificação de recurso ativo e conflitos.
- Liberação do período após rejeição.
- Temas por perfil: administrador azul, responsável roxo e solicitante verde.

### Evidências

- Reserva nº 6 aprovada e posteriormente cancelada pelo solicitante.
- Reserva nº 7 rejeitada.
- 56 testes aprovados.
- Commits cca4432 e 9946585.
- GitHub Actions #27 e #28 aprovados.

### Pendências relacionadas

- Interface para vincular responsáveis.
- Notificações de aprovação e rejeição.
- Medição da cobertura das regras críticas.

A auditoria dessas operações foi implementada posteriormente.

## 9. Histórico — Auditoria e organização das reservas

**Data da etapa:** 25/10/2026.

### Funcionalidades

- Registro de criação, cancelamento, aprovação e rejeição.
- Identificação da reserva, autor, ação, data e horário.
- Situações anterior e nova.
- Auditoria na mesma transação da operação.
- Rollback conjunto em caso de falha.
- Consulta dos 100 eventos mais recentes pelo administrador.
- Botão exclusivo do administrador.
- Bloqueio de acesso direto dos outros perfis.
- Filtros Ativas, Histórico e Todas em Minhas reservas.

### Critério atual dos filtros

- **Ativas:** SOLICITADA, APROVADA ou EM_USO com término posterior ao momento da consulta.
- **Histórico:** reservas que não atendem ao critério de Ativas.
- **Todas:** todas as reservas do usuário conectado.

O encerramento do período não altera automaticamente a situação.

Uma reserva APROVADA com período encerrado aparece no Histórico, mantendo sua situação até uma operação alterá-la.

É necessário revisar o filtro para manter reservas EM_USO como ativas mesmo após o prazo previsto.

### Limitações

- Eventos anteriores à implantação não são reconstruídos.
- Horários seguem o relógio local do servidor.
- Consulta limitada aos 100 eventos mais recentes, sem paginação.
- Novas operações precisam acrescentar seus eventos.
- Testes de acesso HTTP não comprovam sozinhos o limite e a ordenação.
- Cobertura ainda não medida.

### Resultado histórico

- 65 testes aprovados em 15,054 segundos.
- Commit db1e5e8.
- GitHub Actions #37 aprovado em 22 segundos.

## 10. Histórico — Manutenção de recursos

**Data da etapa:** 25/10/2026.

### Funcionalidades

- Cadastro e consulta exclusivos do administrador.
- Período futuro com término posterior ao início.
- Motivo obrigatório com até 200 caracteres.
- Bloqueio de manutenções sobrepostas.
- Bloqueio de manutenção coincidente com reserva em SOLICITADA, APROVADA ou EM_USO.
- Bloqueio de criação e aprovação de reservas durante manutenção.
- Permissão de horários consecutivos.
- Proteção CSRF no cadastro.

### Testes

- test_manutencoes.py: 12 métodos.
- test_manutencoes_http.py: 9 métodos.
- Suíte completa na etapa: 86 testes aprovados em 21,313 segundos.

### Verificações manuais

- Manutenção nº 1 da Sala 101 em 01/11/2026, das 14:00 às 16:00.
- Segunda manutenção das 14:30 às 15:30 bloqueada.
- Reserva das 14:30 às 15:30 bloqueada.
- Reserva nº 9 registrada com início às 16:00.

### Pendências

- Edição e desativação de manutenção pela interface.
- Manutenção emergencial com início imediato.
- Teste específico de concorrência entre manutenção e reserva.
- Revisão por colega.
- Medição da cobertura.

Autor e data de criação são registrados na tabela manutencoes.

O cadastro de manutenção não gera evento na auditoria de reservas.

## 11. Atualização — Gestão de materiais

**Data da etapa:** 26/10/2026.

### Funcionalidades

- Consulta de materiais com reservas APROVADA ou EM_USO.
- Administrador pode gerenciar a movimentação dos materiais.
- Responsável pode gerenciar os materiais vinculados a ele.
- Retirada somente durante o período da reserva aprovada.
- Bloqueio de retirada de recurso inativo ou em manutenção.
- Bloqueio de retirada quando o material já está em uso.
- Retirada altera APROVADA para EM_USO.
- Devolução altera EM_USO para CONCLUIDA.
- Devolução permitida após o término previsto.
- Devolução permitida mesmo com recurso inativo.
- Retirada e devolução registradas na auditoria.
- Botão Gestão de materiais para administrador e responsável.
- Reserva concluída preservada no histórico.

### Testes automatizados

- Arquivo: tests/test_materiais.py.
- 17 métodos específicos de materiais.
- Suíte completa local: 103 testes aprovados em 28,560 segundos.
- Execução local em 26/10/2026.
- GitHub Actions #45 aprovado em 17 segundos.
- GitHub Actions #46 aprovado em 23 segundos.
- Cobertura ainda não medida.

Os tempos do GitHub Actions correspondem às execuções completas dos workflows, não ao tempo isolado dos testes.

### Fluxo manual verificado

**Recurso:** Projetor 01.  
**Reserva:** nº 11.  
**Período:** 26/10/2026, das 20:15 às 21:15.

1. Solicitação exibida na tela de aprovação do responsável.
2. Reserva aprovada.
3. Reserva apresentada na gestão de materiais.
4. Antes do início, interface informou que aguardava o período de retirada.
5. Retirada registrada às 20:17:10 pelo Administrador do projeto.
6. Situação alterada de Aprovada para Em uso.
7. Devolução registrada às 20:18:04 pelo Administrador do projeto.
8. Situação alterada de Em uso para Concluída.
9. Cartão removido da lista de movimentações em andamento.
10. Eventos de retirada e devolução conferidos na auditoria.

### Registros de auditoria conferidos

| Evento | Ação | Situação anterior | Nova situação | Autor |
| --- | --- | --- | --- | --- |
| 8 | RETIRADA | APROVADA | EM_USO | Administrador do projeto |
| 9 | DEVOLUCAO | EM_USO | CONCLUIDA | Administrador do projeto |

Os eventos apresentaram reserva, recurso, autor, data, horário e situações anterior e nova.

Os horários informados correspondem aos registros apresentados na auditoria.

### Versionamento

- **Commit:** 22014eb.
- **Mensagem:** Implementa retirada e devolucao de materiais com auditoria e testes.
- **Branch:** funcionalidade/login.
- **Push:** confirmado.
- **GitHub Actions do push:** execução #45 aprovada em 17 segundos.
- **GitHub Actions do Pull Request nº 1:** execução #46 aprovada em 23 segundos.
- **Revisão por outro integrante:** pendente.

### Pendências relacionadas

- Testes HTTP específicos das rotas de materiais.
- Fluxo automatizado no navegador.
- Medição de cobertura.
- Revisão por outro integrante.
- Organização dos prints de evidência.
- Rótulos amigáveis para RETIRADA e DEVOLUCAO na auditoria.
- Revisão do filtro Ativas para reservas EM_USO com prazo encerrado.
- Registro de não comparecimento.

## 12. Medição de cobertura — 26/10/2026

- Ferramenta: coverage.py 7.17.0.
- Execução: 103 testes aprovados em 26,625 segundos.
- Escopo: app.py, banco.py, servico_reservas.py e servico_materiais.py.
- Linhas executadas: 417 de 464 — 89,87%.
- Branches executados: 155 de 182 — 85,16%.
- Metas de 80% de linhas e 70% de branches atingidas no escopo medido.
- Relatórios gerados: coverage.json e htmlcov/index.html.

Esta medição não inclui templates, CSS, JavaScript nem scripts
administrativos e de migração. Não representa percentual de
conclusão do projeto nem comprova ausência de defeitos.

As referências anteriores a “cobertura ainda não medida”
descrevem as etapas históricas anteriores a esta medição.