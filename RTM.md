# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 27/10/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Esta matriz relaciona os requisitos aos riscos, testes e evidências do projeto.

As tabelas apresentam a situação atual. Os registros históricos preservam os resultados das etapas anteriores.

## 1. Legenda

- **Implementado e verificado:** disponível e verificado no escopo indicado.
- **Parcial:** parte do requisito ou da verificação permanece pendente.
- **Pendente:** implementação ou verificação ainda não realizada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes não representa cobertura nem percentual de conclusão.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e verificações | Situação atual |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Testes de consulta, cancelamento, aprovação, auditoria, manutenção, edição HTTP e permissões no serviço de materiais | Parcial: testes HTTP específicos de materiais pendentes |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | Cadastro, validação, autorização e consulta em test_consulta.py | Implementado e verificado; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e verificações manuais | Implementado e verificado no serviço HTTP interno e manualmente; automação de navegador pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | test_reservas.py, test_minhas_reservas.py, test_cancelamento_http.py, test_edicao_reservas.py e test_edicao_http.py | Implementado e verificado nos serviços, cliente Flask e verificações manuais |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos do mesmo recurso | Testes de criação, aprovação, disponibilidade e edição | Parcial: ampliar cenários explícitos de criação e edição por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas para o mesmo período | test_duas_solicitacoes_simultaneas em test_reservas.py | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | test_aprovacoes.py, test_aprovacoes_http.py e testes de nova aprovação após edição | Implementado e verificado; interface para vincular responsáveis pendente |
| RF08 | Bloquear recursos em manutenção | Reserva de recurso indisponível | Testes de manutenção, disponibilidade, edição e verificações manuais | Implementado e verificado; concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py e fluxo manual da reserva nº 11 | Implementado e verificado no serviço e manualmente; testes HTTP específicos e navegador pendentes |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, materiais e edição; conferência manual dos detalhes | Parcial: operações atuais auditadas; ampliar para futuras transições |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | Testes a definir durante a implementação | Pendente |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | Planejado: comparar resultados com dados conhecidos | Pendente |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP existentes e verificações manuais | Parcial: avaliação em diferentes telas e testes de navegador pendentes |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README inicial e esta matriz | Parcial: ampliar instalação, fluxos e interfaces |

## 3. Regras críticas

| ID | Regra | Risco | Verificação | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Validação no serviço e banco; testes explícitos de edição e disponibilidade | Verificado nesses fluxos; ampliar testes explícitos de criação |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Testes de criação, aprovação, edição, disponibilidade e horários consecutivos | Parcial: ampliar cenários por tipo |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | test_duas_solicitacoes_simultaneas | Verificado no serviço; concorrência por HTTP pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Testes de manutenção, edição e disponibilidade; verificação manual | Implementado e verificado; concorrência específica pendente |
| RC05 | Fluxo SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Testes de aprovação e materiais; fluxo manual da reserva nº 11 | Implementado para materiais e verificado no serviço e manualmente |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Rejeição e cancelamento testados | Parcial: registro de não comparecimento pendente |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Testes de perfil, vínculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Sem exclusão física disponível; cancelamento e edição após início bloqueados | Verificado nas operações existentes; revisar futuras funções administrativas |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Operações atuais registram autor, horário e situações; rollback conjunto testado | Parcial: ampliar para futuras transições |

## 4. Testes automatizados

### Resultados da etapa atual

- Data: 27/10/2026.
- Suíte completa com edição no serviço: 142 testes aprovados, conforme execução local informada.
- Testes HTTP de edição: 12 testes aprovados em execução isolada.
- Total esperado após incluir os testes HTTP: 154 métodos.
- A confirmação explícita do resultado final da suíte de 154 testes deve ser registrada antes de considerá-la evidência consolidada.
- O tempo da execução completa de 154 testes ainda não foi registrado nesta matriz.

Alguns métodos utilizam `subTest` para verificar vários cenários.

### Arquivos de teste

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização, cadastro, validação, persistência e filtros |
| tests/test_reservas.py | Criação, conflitos, horários consecutivos, concorrência e cancelamento |
| tests/test_minhas_reservas.py | Login obrigatório, isolamento entre usuários e lista vazia |
| tests/test_cancelamento_http.py | Autenticação, autorização e CSRF no cancelamento |
| tests/test_aprovacoes.py | Aprovação, rejeição, vínculo, prazo, estado e conflito |
| tests/test_aprovacoes_http.py | Rotas, perfis, CSRF e isolamento por responsável |
| tests/test_auditoria.py | Registro das operações, identificação do autor e rollback |
| tests/test_auditoria_http.py | Login obrigatório, permissões e visibilidade do botão |
| tests/test_manutencoes.py | Períodos, conflitos e bloqueio de reservas |
| tests/test_manutencoes_http.py | Permissões, CSRF, cadastro e consulta |
| tests/test_materiais.py | Retirada, devolução, permissões, horários, estados, manutenção e auditoria |
| tests/test_disponibilidade.py | Períodos, sobreposição, estados, manutenção, limites consecutivos e filtros combinados |
| tests/test_edicao_reservas.py | Edição, permissões, validações, conflitos, manutenção, nova aprovação, auditoria e rollback |
| tests/test_edicao_http.py | Acesso à edição, formulário preenchido, persistência, auditoria, CSRF e recusas |

### Como executar

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Limitações

- Os testes de persistência utilizam bancos SQLite temporários.
- Os testes HTTP atuais utilizam o cliente de testes do Flask.
- A autenticação é simulada nos testes HTTP de edição; login e senha possuem testes próprios.
- O cliente Flask não executa o JavaScript dos templates.
- A apresentação dos detalhes de auditoria foi conferida manualmente.
- Testes externos por HTTP, navegador e carga permanecem pendentes.
- Verificação com banco em container permanece pendente.
- Filtros Ativas, Histórico e Todas precisam de testes específicos de distribuição e ordenação.
- A cobertura precisa ser medida novamente após disponibilidade e edição.
- A migração da auditoria foi executada manualmente; testes automatizados da migração permanecem pendentes.

## 5. Evidências históricas

| ID | Evidência |
| --- | --- |
| EV01 | Commit 1ed928d: etapa RED dos testes de acesso ao cadastro |
| EV02 | Commit 49b42fe: etapa GREEN com implementação do cadastro |
| EV03 | Commit 250f9b2: ampliação para 16 testes e GitHub Actions |
| EV04 | Execução local histórica: 16 testes aprovados em 6,098 segundos |
| EV05 | GitHub Actions do commit 250f9b2 aprovado em 21 segundos |
| EV06 | Cadastro manual da Sala 202 confirmado |
| EV07 | Pull Request nº 1 aberto; revisão por outro integrante pendente |
| EV08 | Commit 940a392: reservas, conflitos, horários consecutivos e concorrência |
| EV09 | Execução local: 22 testes aprovados em 7,883 segundos |
| EV10 | GitHub Actions #13 e #14 aprovados |
| EV11 | Commit ecb0eb7: cancelamento; 31 testes aprovados em 9,850 segundos |
| EV12 | Reserva nº 3 cancelada e reserva nº 4 aprovada para o mesmo recurso e período |
| EV13 | Commit 7ae60b7: testes HTTP de cancelamento |
| EV14 | Commit cca4432: aprovação por responsável, vínculo e temas por perfil |
| EV15 | Commit 9946585: testes HTTP de aprovação; 56 testes aprovados |
| EV16 | GitHub Actions #27 e #28 aprovados |
| EV17 | Reserva nº 6 aprovada e depois cancelada; reserva nº 7 rejeitada |
| EV18 | Commit 1515dcd: tabela de auditoria, registro no serviço e testes |
| EV19 | Commit 0fc4cf5: consulta de auditoria e filtros; 62 testes aprovados |
| EV20 | Commit 6ac9d65: botão de auditoria no menu do administrador |
| EV21 | Consulta manual de criação e cancelamento com autor, horário e situações |
| EV22 | Acesso direto de responsável a /auditoria bloqueado |
| EV23 | Commit db1e5e8: testes HTTP de auditoria; 65 testes aprovados; Actions #37 aprovado |
| EV24 | Etapa de manutenção: 86 testes aprovados em 21,313 segundos |
| EV25 | Manutenção nº 1 da Sala 101 em 01/11/2026, das 14h às 16h; conflitos bloqueados e reserva nº 9 aceita a partir das 16h |
| EV26 | Reserva nº 11 do Projetor 01: aprovação, retirada e devolução conferidas em 26/10/2026 |
| EV27 | Auditoria da reserva nº 11: retirada às 20:17:10 e devolução às 20:18:04 |
| EV28 | Execução local em 26/10/2026: 103 testes aprovados em 28,560 segundos |
| EV29 | Commit 22014eb: gestão de materiais com auditoria e testes; push confirmado |
| EV30 | GitHub Actions #45 aprovado em 17 segundos |
| EV31 | GitHub Actions #46 aprovado em 23 segundos |
| EV32 | Medição histórica: 89,87% de linhas e 85,16% de branches nos quatro arquivos principais |
| EV33 | Commit 400b119: registro da medição de cobertura |
| EV34 | Commit 6b8d472: pesquisa por disponibilidade com 15 testes; push confirmado |
| EV35 | Suíte de 118 testes aprovada em 48,257 segundos após disponibilidade |
| EV36 | Busca manual excluiu Sala 101 durante manutenção e permitiu período consecutivo |
| EV37 | Busca com término anterior ao início apresentou erro |
| EV38 | Migração da auditoria para detalhes de alteração executada com backup e preservação de 9 registros |
| EV39 | Reserva nº 9: finalidade alterada com sucesso, mantendo período de 01/11/2026, das 16h às 17h |
| EV40 | Tentativa de editar reserva nº 9 para 14:30–15:30 recusada por manutenção; horário original preservado |
| EV41 | Evento nº 10 da auditoria apresentou autor, horário e finalidade antes e depois da alteração |
| EV42 | Suíte anterior de 118 testes aprovada em 32,354 segundos após mudanças de edição |
| EV43 | 24 testes de edição no serviço aprovados; suíte completa de 142 testes informada como aprovada |
| EV44 | Commit 35b5fe5: edição de reservas com auditoria e 24 testes; push confirmado |
| EV45 | GitHub Actions #53 do commit 35b5fe5 aprovado em 24 segundos |
| EV46 | GitHub Actions #54 do Pull Request aprovado em 23 segundos |
| EV47 | 12 testes HTTP de edição informados como aprovados em execução isolada; commit próprio ainda pendente |

### Links

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Commit de materiais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/22014eb)
- [Commit de disponibilidade](https://github.com/Arthurmrsilva/organizacao-recursos/commit/6b8d472)
- [Commit de edição](https://github.com/Arthurmrsilva/organizacao-recursos/commit/35b5fe5)

### Organização das evidências

Os prints do pacote de entrega devem informar:

- Cenário e data.
- Resultado esperado.
- Resultado observado.
- Requisito ou regra relacionado.
- Commit associado, quando aplicável.

As evidências históricas mantêm suas contagens originais.

A aprovação do workflow não substitui revisão por outro integrante.

## 6. Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | Medição histórica de 89,87%; medir novamente a versão atual |
| Cobertura de branches | Pelo menos 70% | Medição histórica de 85,16%; medir novamente a versão atual |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Parcial |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa pendente |
| Testes unitários isolados | Regras sem dependências reais | Pendente de ampliação; testes de serviço utilizam persistência real |
| Testes de integração | Persistência e integração das camadas | Parcial: SQLite temporário e cliente Flask |
| Testes em container | Banco com Testcontainers | Pendente |
| Integrações externas | WireMock quando aplicável | Pendente de definição |
| HTTP em caixa-preta | Acesso externo por HTTP | Pendente |
| Testes ponta a ponta | Automação no navegador | Pendente |
| Concorrência | Uma única reserva aceita para o mesmo período | Verificado no serviço; HTTP e carga pendentes |
| TDD ou BDD | Funcionalidade com evidências | RED e GREEN registrados; consolidar documentação |
| CI | Execução em push e Pull Requests | Confirmado até o commit 35b5fe5; execuções #53 e #54 aprovadas |
| Análise estática | Integração ao SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revisão por pares | Revisão de outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Pendente de consolidação |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio pelo grupo | Pendente |

A confirmação de aceitação de Python e das ferramentas equivalentes às citadas no enunciado permanece pendente de registro.

## 7. Histórico — Cancelamento

**Data:** 25/10/2026.

- Consulta das próprias reservas.
- Cancelamento pelo proprietário antes do início.
- Situações permitidas: SOLICITADA e APROVADA.
- Preservação do registro cancelado.
- Liberação do período após cancelamento.
- 31 testes aprovados em 9,850 segundos.
- Commit ecb0eb7.

Naquela etapa, edição e auditoria ainda não estavam implementadas. Ambas foram acrescentadas posteriormente.

## 8. Histórico — Aprovação

**Data:** 25/10/2026.

- Responsável vinculado ao recurso por script local.
- Aprovação e rejeição de solicitações dos recursos vinculados.
- Verificações de perfil, vínculo, prazo, recurso ativo e conflito.
- Temas por perfil: administrador azul, responsável roxo e solicitante verde.
- 56 testes aprovados.
- Commits cca4432 e 9946585.
- Actions #27 e #28 aprovados.

Pendências: interface para vincular responsáveis e notificações.

## 9. Histórico — Auditoria e filtros de reservas

**Data inicial:** 25/10/2026.

- Auditoria de criação, cancelamento, aprovação e rejeição.
- Autor, reserva, ação, horário e situações.
- Gravação na mesma transação da operação.
- Rollback conjunto em caso de falha.
- Consulta dos 100 eventos mais recentes pelo administrador.
- Acesso dos demais perfis bloqueado.
- Filtros Ativas, Histórico e Todas.
- Resultado histórico: 65 testes aprovados.
- Commit db1e5e8; Actions #37 aprovado.

### Critério atual dos filtros

- **Ativas:** SOLICITADA, APROVADA ou EM_USO com término posterior à consulta.
- **Histórico:** reservas que não atendem ao critério de Ativas.
- **Todas:** todas as reservas do usuário conectado.

O encerramento do período não altera automaticamente a situação.

**Pendência conhecida:** manter EM_USO em Ativas mesmo após o término previsto, enquanto a devolução não ocorrer.

### Limitações da auditoria

- Eventos anteriores à implantação não são reconstruídos.
- Horários seguem o relógio local do servidor.
- Consulta limitada a 100 eventos, sem paginação.
- O nome do recurso exibido corresponde ao recurso atual da reserva.
- Em alterações, os códigos anterior e novo do recurso ficam nos detalhes.
- Testes HTTP atuais não comprovam sozinhos limite e ordenação.
- Novas operações precisam registrar seus eventos.

## 10. Histórico — Manutenção

**Data:** 25/10/2026.

- Cadastro e consulta pelo administrador.
- Período futuro e término posterior ao início.
- Motivo obrigatório de até 200 caracteres.
- Bloqueio de sobreposição com manutenção ou reserva ativa.
- Bloqueio de criação e aprovação durante manutenção.
- Horários consecutivos permitidos.
- Proteção CSRF.
- 12 testes de serviço e 9 testes HTTP.
- Suíte histórica: 86 testes aprovados em 21,313 segundos.

Autor e data de criação são registrados na tabela de manutenção. O cadastro não gera evento na auditoria de reservas.

Pendências: edição e desativação pela interface, manutenção imediata e concorrência específica.

## 11. Histórico — Materiais

**Data:** 26/10/2026.

- Administrador gerencia movimentações de materiais.
- Responsável gerencia materiais vinculados.
- Retirada de reserva APROVADA durante o período permitido.
- Bloqueio de recurso inativo, em manutenção ou já em uso.
- Retirada: APROVADA → EM_USO.
- Devolução: EM_USO → CONCLUIDA.
- Devolução permitida após o prazo e com recurso inativo.
- Auditoria de retirada e devolução.
- 17 testes específicos.
- Suíte histórica: 103 testes aprovados em 28,560 segundos.
- Commit 22014eb.
- Actions #45 e #46 aprovados.

### Fluxo manual

Reserva nº 11 do Projetor 01, em 26/10/2026, das 20:15 às 21:15:

1. Solicitação aprovada.
2. Reserva apresentada na gestão de materiais.
3. Interface aguardou o início do período.
4. Retirada às 20:17:10 pelo Administrador do projeto.
5. Situação alterada para EM_USO.
6. Devolução às 20:18:04 pelo mesmo administrador.
7. Situação alterada para CONCLUIDA.
8. Cartão removido das movimentações em andamento.
9. Eventos nº 8 e nº 9 conferidos na auditoria.

Os rótulos amigáveis Retirada e Devolução foram acrescentados posteriormente e conferidos na interface.

Pendências: testes HTTP específicos, navegador, não comparecimento e revisão por colega.

## 12. Medição histórica de cobertura

**Data:** 26/10/2026.

- Ferramenta: coverage.py 7.17.0.
- Execução: 103 testes aprovados em 26,625 segundos.
- Escopo: app.py, banco.py, servico_reservas.py e servico_materiais.py.
- Linhas executadas: 417 de 464 — 89,87%.
- Branches executados: 155 de 182 — 85,16%.
- Metas atingidas no escopo e na versão medidos.
- Relatórios: coverage.json e htmlcov/index.html.
- Registro versionado no commit 400b119.

Esta medição não inclui templates, CSS, JavaScript nem scripts administrativos e de migração.

Os resultados não representam conclusão do projeto nem comprovam ausência de defeitos.

A versão atual possui alterações posteriores à medição. É necessário gerar novos relatórios para avaliar sua cobertura.

### Como medir novamente

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais -m unittest discover -s tests -v
```

```powershell
.\.venv\Scripts\python.exe -m coverage report -m
```

```powershell
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
```

```powershell
.\.venv\Scripts\python.exe -m coverage html
```

## 13. Atualização — Pesquisa por disponibilidade

**Data:** 27/10/2026.

- Filtros opcionais de início e término.
- Preenchimento dos dois campos quando houver pesquisa por período.
- Validação das datas e da ordem do período.
- Exclusão de recursos com reservas sobrepostas em SOLICITADA, APROVADA ou EM_USO.
- Exclusão de recursos com manutenção ativa sobreposta.
- Horários consecutivos permitidos.
- Combinação com os demais filtros.
- Consulta por períodos passados permitida.
- Atualização da lista sem subir a página.
- Limpeza dos filtros também remove o período.

### Evidências

- 15 testes em test_disponibilidade.py.
- Suíte de 118 testes aprovada em 48,257 segundos.
- Commit 6b8d472.
- Sala 101 excluída durante a manutenção.
- Período consecutivo à manutenção permitido.
- Período com término anterior ao início recusado.

## 14. Atualização — Edição e detalhes de auditoria

**Data:** 27/10/2026.

### Funcionalidades

- Edição pelo proprietário autenticado.
- Permitida em SOLICITADA ou APROVADA antes do início.
- Alteração de recurso, início, término e finalidade.
- Validação de usuário ativo, recurso ativo, datas e finalidade.
- Verificação de conflitos e manutenção.
- A própria reserva não é tratada como conflito.
- Recursos restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicitação sem mudança é recusada.
- Edição e auditoria ocorrem na mesma transação.
- Falha na auditoria desfaz a edição.
- Evento ALTERACAO registra dados anteriores e novos.
- Interface de auditoria apresenta antes e depois.

### Banco e migração

- Coluna detalhes adicionada à auditoria.
- Ação ALTERACAO incluída na restrição de ações válidas.
- Backup criado antes da migração.
- Migração executada com 9 registros preservados.
- Registros antigos permanecem sem detalhes de alteração.
- Testes automatizados da migração ainda pendentes.

### Testes de serviço

Arquivo: tests/test_edicao_reservas.py.

24 métodos aprovados, incluindo:

- Edição válida e detalhes de auditoria.
- Mudança de período e recurso.
- Liberação do recurso anterior.
- Nova aprovação de recurso restrito ou professor.
- Bloqueio de outro usuário e usuário inativo.
- Reserva inexistente.
- Estados não editáveis e reserva iniciada.
- Finalidade, recurso e datas inválidos.
- Conflitos e horários consecutivos.
- Manutenção ativa e inativa.
- Ausência de alterações.
- Rollback quando a auditoria falha.

### Testes HTTP

Arquivo: tests/test_edicao_http.py.

12 métodos aprovados em execução isolada, incluindo:

- Login obrigatório em GET e POST.
- Formulário preenchido para o proprietário.
- Edição válida, redirecionamento e auditoria.
- Bloqueio de outro usuário.
- Reserva inexistente.
- CSRF ausente e incorreto.
- Dados inválidos preservados no formulário.
- Bloqueio de reserva cancelada ou iniciada.
- Perda de acesso de usuário inativo.

### Verificação manual

- Reserva nº 9 aberta com os dados preenchidos.
- Finalidade alterada para “Teste de edição da reserva.”
- Mensagem de sucesso apresentada.
- Tentativa para 01/11/2026, das 14:30 às 15:30, recusada por manutenção.
- Período original das 16h às 17h preservado.
- Evento nº 10 apresentou finalidade anterior e nova, autor e horário.

### Versionamento e CI

- Commit 35b5fe5: edição com auditoria e 24 testes de serviço.
- Push confirmado na branch funcionalidade/login.
- Actions #53 e #54 aprovados.
- Os 12 testes HTTP foram acrescentados depois desse commit.
- Commit e CI dos testes HTTP ainda precisam ser registrados.

## 15. Próximas verificações

- Consolidar resultado da suíte completa de 154 testes.
- Versionar testes HTTP e esta atualização.
- Confirmar CI do próximo commit.
- Medir novamente cobertura.
- Revisar filtro de materiais EM_USO com prazo encerrado.
- Acrescentar testes HTTP de materiais.
- Implementar notificações e relatórios.
- Implementar registro de não comparecimento.
- Ampliar documentação de instalação e fluxos.
- Completar verificações de arquitetura, segurança, carga e navegador.
- Obter revisão por outro integrante.