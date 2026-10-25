# Matriz de Rastreabilidade — RTM

Projeto: Organização de Recursos.

Esta matriz acompanha requisitos, riscos, testes e evidências.
É atualizada conforme a implementação avança.

## Legenda

- Parcial: somente parte do requisito foi implementada e verificada.
- Pendente: implementação ou verificação ainda não realizada.
- Testes planejados não representam evidência de aprovação.

## Requisitos funcionais

| ID | Requisito | Risco | Teste existente ou planejado | Evidência e situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Login correto/incorreto, usuário inativo, acesso e envio do cadastro por perfil | Parcial: testes em tests/test_consulta.py; demais permissões pendentes |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos ou perda de informação | Cadastro dos três tipos, campos inválidos e consulta de ativos | Implementado e testado nesta etapa; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto ou recurso indisponível listado | test_filtrar_por_tipo, test_tipo_invalido_mostra_todos_os_ativos, test_filtros_de_pesquisa e test_filtros_invalidos | Parcial: filtros de tipo, capacidade, localização e competência implementados e testados; disponibilidade pendente. Evidência: commit c82a46e e execução #7 do GitHub Actions aprovada |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | test_criar_reserva_valida; alteração, cancelamento e permissões ainda precisam de testes | Parcial: criação implementada e testada no serviço; alteração e cancelamento pendentes. Evidências EV08 a EV10 |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos do mesmo recurso no mesmo horário | test_bloquear_horarios_sobrepostos e test_permitir_horarios_consecutivos | Parcial: conflito por recurso testado com sala; ampliar os cenários para professor e demais tipos. Evidências EV08 a EV10 |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas para o mesmo recurso e período | test_duas_solicitacoes_simultaneas | Implementado e verificado no serviço com SQLite: uma solicitação aceita, outra recusada e apenas uma reserva gravada; teste concorrente pela rota HTTP pendente. Evidências EV08 a EV10 |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Aprovação por responsável e bloqueio dos outros perfis | Pendente: somente o campo restrito existe |
| RF08 | Bloquear recursos em manutenção | Reserva de recurso indisponível | Reserva durante e fora do bloqueio de manutenção | Pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | Retirada, devolução e operações inválidas | Pendente |
| RF10 | Manter histórico auditável | Mudanças sem identificação ou rastreio | Conferência da auditoria após cada mudança | Pendente |
| RF11 | Notificação simulada ou integração externa | Usuário não informado sobre a reserva | Conferência de notificação após eventos da reserva | Pendente |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | Comparação com dados conhecidos no banco | Pendente |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso e erros sem orientação | Testes de mensagens existentes; testes de navegador e telas planejados | Parcial |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar, usar e manter | Conferência das instruções e dos fluxos documentados | Parcial: README inicial criado |

## Regras críticas

| ID | Regra | Risco | Verificação planejada | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Rejeitar término anterior ou igual ao início | Pendente |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Testar sala, material e professor | Pendente |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | Teste automatizado de concorrência | Pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Testar interseção com bloqueio | Pendente |
| RC05 | Fluxo SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Testar transições permitidas e proibidas | Pendente |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Testar condições de cada transição | Pendente |
| RC07 | Somente responsável aprova recurso restrito | Aprovação indevida | Testar todos os perfis | Pendente |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Tentar apagar reserva iniciada | Pendente |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Conferir autor, ação, reserva e momento | Pendente |

## Testes existentes

Arquivo: tests/test_consulta.py
Classe: TestSistema

| Área | Métodos |
| --- | --- |
| Autenticação | test_inicio_exige_login; test_login_correto; test_senha_incorreta; test_usuario_inativo_nao_entra; test_sair_encerra_acesso |
| Proteção dos formulários | test_login_sem_token_e_bloqueado; test_cadastro_sem_token_nao_grava |
| Consulta | test_listar_recursos_ativos; test_filtrar_por_tipo; test_tipo_invalido_mostra_todos_os_ativos |
| Autorização do cadastro | test_cadastro_exige_login; test_admin_pode_abrir_cadastro; test_outros_perfis_nao_podem_abrir_cadastro; test_outros_perfis_nao_podem_gravar_recurso |
| Persistência e validação | test_admin_cadastra_os_tres_tipos; test_cadastro_invalido_nao_grava |

A suíte contém 22 métodos de teste, incluindo casos parametrizados
com subTest. Utiliza o cliente de testes do Flask e bancos SQLite
temporários reais.

Esses testes não substituem os testes de navegador, concorrência,
API em caixa-preta ou banco em container exigidos para a entrega final.

## Evidências registradas

| ID | Evidência |
| --- | --- |
| EV01 | Commit RED 1ed928d: testes de acesso ao cadastro falhando antes da implementação |
| EV02 | Commit GREEN 49b42fe: implementação do cadastro e testes de acesso aprovados |
| EV03 | Commit 250f9b2: ampliação para 16 testes e configuração do GitHub Actions |
| EV04 | Execução local: 16 testes aprovados em 6,098 segundos |
| EV05 | GitHub Actions: execução do commit 250f9b2 aprovada em 21 segundos |
| EV06 | Cadastro manual da Sala 202 confirmado na interface |
| EV07 | Pull Request nº 1 aberto; revisão por outro integrante pendente |
| EV08 | Commit 940a392: criação de reservas e testes de conflito, horários consecutivos e concorrência |
| EV09 | Execução local do commit 940a392: 22 testes aprovados em 7,883 segundos |
| EV10 | GitHub Actions: execuções #13 (push) e #14 (Pull Request) aprovadas |

Pull Request:
https://github.com/Arthurmrsilva/organizacao-recursos/pull/1

Execuções de CI:
https://github.com/Arthurmrsilva/organizacao-recursos/actions

Os prints de evidência ainda precisam ser organizados e adicionados
ao pacote de entrega do repositório.

## Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | Ainda não medida |
| Cobertura de branches | Pelo menos 70% | Ainda não medida |
| Rastreabilidade crítica | 100% dos requisitos críticos ligados a testes e evidências | Regras listadas; testes e evidências pendentes |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa ainda não realizada |
| Testes unitários isolados | Regras de negócio verificadas | Pendente |
| Testes de integração | Persistência real | Parcial: SQLite temporário |
| Testes em container | Banco com Testcontainers | Pendente |
| Integrações externas | WireMock quando aplicável | Pendente de definição e implementação |
| Testes de API em caixa-preta | Aplicação acessada externamente por HTTP | Pendente |
| Testes ponta a ponta | Fluxos no navegador | Pendente |
| Concorrência | Uma única reserva aceita | Pendente |
| TDD ou BDD | Pelo menos uma funcionalidade com evidências | RED e GREEN registrados para acesso ao cadastro; documentação do ciclo em andamento |
| CI | Execução em Pull Requests | Workflow configurado e primeira execução por push aprovada; conferir resultado do PR |
| Análise estática | Projeto integrado ao SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revisão por pares | Revisão real de outro integrante | Pendente |
| Arquitetura | C4, sequências críticas, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Pendente |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio do projeto pelo grupo | Pendente |

## Atualização — Cancelamento de reservas — 25/10/2026

### Funcionalidades implementadas

- Consulta das próprias reservas na tela "Minhas reservas".
- Cancelamento pelo proprietário da reserva.
- Cancelamento permitido nos estados SOLICITADA e APROVADA,
  desde que o horário de início ainda não tenha chegado.
- Preservação da reserva cancelada no histórico.
- Liberação do horário após o cancelamento.

### Evidências de validação

- Execução local: 31 testes aprovados em 9,850 segundos.
- Commit do cancelamento: `ecb0eb7`.
- Teste manual: reserva nº 3 cancelada e reserva nº 4 aprovada
  para o mesmo recurso e período, em 30/10/2026, das 15:30 às 16:30.
- Testes automatizados em `tests/test_reservas.py` verificam:
  cancelamento de reservas aprovadas e solicitadas,
  bloqueio de outro usuário, bloqueio após o início,
  rejeição de estados não permitidos e liberação do horário.

### Situação do requisito RF04

Parcialmente implementado: criação, consulta das próprias reservas
e cancelamento disponíveis. Alteração de reservas ainda pendente.

### Validações pendentes desta etapa

- Testes HTTP específicos da rota de cancelamento:
  autenticação, proteção CSRF e autorização.
- Confirmação da execução da integração contínua no GitHub
  para o commit `ecb0eb7`.
- Registro de auditoria das mudanças de situação.