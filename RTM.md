# Matriz de Rastreabilidade — RTM

Projeto: Organização de Recursos.

Atualização: 02/11/2026.

Integrantes: Arthur Mendes, Nicolas Ferreira e Robert Oliveira.

Referência detalhada dos 292 testes e cobertura: da93d49.
Referência de checks e Sonar conferidos: 3a76227.

Estado: preparação da entrega, sem aprovação formal do grupo ou tag publicada.

## 1. Legenda

- Verificado: evidência disponível nos cenários indicados.
- Parcial: implementação ou verificação incompleta.
- Pendente: conclusão não demonstrada.
- Testes planejados não representam resultados aprovados.
- Contagem de testes e cobertura não medem percentual de conclusão.
- Cliente Flask, HTTP real, navegador e carga possuem escopos diferentes.
- Resultados históricos pertencem às respectivas versões.

EV01 a EV94 permanecem em [RTM_historico.md](RTM_historico.md).
Detalhes anteriores desta matriz permanecem no histórico Git.

## 2. Requisitos funcionais

Os arquivos test_*.py citados nas tabelas pertencem a tests/,
exceto quando outro caminho estiver indicado.

| ID | Requisito | Risco | Evidências | Situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | test_consulta.py, testes HTTP de permissões, test_seguranca_login.py e Chromium | Verificado nos cenários atuais; revisão completa de segurança pendente |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | test_consulta.py e cadastro manual | Verificado; revisão por pares pendente |
| RF03 | Pesquisa por características e disponibilidade | Resultado incorreto | test_consulta.py e test_disponibilidade.py | Verificado; ampliar filtros no navegador |
| RF04 | Criar, alterar e cancelar reservas | Alteração indevida | test_reservas.py, test_edicao_reservas.py, test_edicao_http.py, test_cancelamento_http.py e E2E | Verificado no escopo atual; edição no navegador pendente |
| RF05 | Detectar sobreposição, inclusive agenda do professor | Dois usos simultâneos | Reservas, aprovação, edição, disponibilidade, E2E e HTTP concorrente | Parcial: ampliar casos explícitos entre reservas por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas aceitações | test_reservas.py e teste_concorrencia_http.py na raiz | Verificado no serviço e no cenário HTTP executado |
| RF07 | Aprovação de recursos restritos | Uso sem autorização | test_aprovacoes.py, test_aprovacoes_http.py e edição | Verificado; alteração de vínculo existente pela interface pendente |
| RF08 | Bloquear recursos em manutenção | Reserva impossível de atender | Manutenção, disponibilidade, edição e test_concorrencia_manutencao.py | Verificado, incluindo disputa no serviço nos três tipos |
| RF09 | Retirada e devolução de materiais | Perda de controle | test_materiais.py, test_materiais_http.py e reserva manual nº 11 | Verificado; E2E pendente |
| RF10 | Histórico auditável | Mudanças sem rastreio | Auditoria, edição, materiais, não comparecimento, rollback, E2E e HTTP | Verificado nas operações atuais; testes do limite e ordenação da auditoria pendentes |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py, E2E e HTTP | Avisos internos para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos | Indicadores incorretos | test_relatorios.py e test_relatorios_http.py | Contagens, horas previstas e conflitos implementados; tempo real não medido |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | HTTP, verificações manuais e Chromium | Parcial: ampliar telas, navegadores e fluxos |
| RF14 | Documentação da API ou fluxos públicos | Reprodução difícil | README, arquitetura, plano, segurança, relatório e instalação limpa | Documentado; clone final da candidata e revisão dos fluxos pendentes |

A aplicação usa HTML e formulários com sessão por cookie.
A documentação não declara uma API REST JSON completa.

## 3. Regras críticas

| ID | Regra | Verificação | Situação |
| --- | --- | --- | --- |
| RC01 | Término posterior ao início | Serviço, banco, edição e disponibilidade | Verificado nesses fluxos; ampliar casos explícitos de criação |
| RC02 | Mesmo recurso sem sobreposição | Criação, aprovação, edição, disponibilidade e horários consecutivos | Parcial: ampliar reservas por tipo |
| RC03 | Solicitações simultâneas com uma única aceita | Serviço e teste_concorrencia_http.py | Verificado nos cenários executados |
| RC04 | Recurso em manutenção indisponível | Manutenção, edição, disponibilidade e disputa nos três tipos | Verificado no serviço; disputa manutenção/reserva por HTTP não demonstrada |
| RC05 | SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Aprovação e materiais, serviços e rotas | Verificado para materiais |
| RC06 | REJEITADA, CANCELADA e NAO_COMPARECEU | Aprovação, cancelamento e não comparecimento | Verificado no escopo atual; não comparecimento somente para materiais |
| RC07 | Somente responsável vinculado aprova recurso restrito | Perfil, vínculo, prazo e estado | Verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Sem exclusão física pela interface; edição/cancelamento bloqueados após início | Verificado nas operações existentes |
| RC09 | Toda mudança de estado gera auditoria | Criação, alteração, cancelamento, aprovação, rejeição e movimentações | Verificado nas transições atuais |

As associações não substituem revisão final das combinações do enunciado.

## 4. Resultados automatizados

| Referência | Resultado |
| --- | --- |
| da93d49, local | 292 testes aprovados em 116,207 segundos |
| da93d49, Actions #160, push | Workflow aprovado em 53 segundos |
| da93d49, CI | HTTP e Chromium aprovados |
| da93d49, cobertura | 97,46% linhas e 94,83% ramificações |
| b1b308a, Testcontainers push #1 | Aprovado em 49 segundos totais; um artefato |
| 1e42442 | Execução Testcontainers verde informada após correção YAML |
| 3a76227 | Sete checks verdes no pull request |

HTTP, navegador e controle externo do container são separados dos
292 métodos da suíte. Métodos com subTest podem conter várias variações.

Resultados anteriores de 286, 287 e 288 testes permanecem históricos.
Duração de workflow não equivale à duração isolada dos testes.

## 5. Arquivos de teste

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, inatividade, CSRF, cadastro, vínculo e filtros |
| tests/test_reservas.py | Criação, sobreposição, horários consecutivos, concorrência e cancelamento |
| tests/test_minhas_reservas.py | Isolamento, filtros, prazo, atraso e ordenação |
| tests/test_cancelamento_http.py | Autenticação, autorização e CSRF |
| tests/test_aprovacoes.py | Aprovação, rejeição, vínculo, prazo, estado e conflitos |
| tests/test_aprovacoes_http.py | Rotas, perfis, CSRF e isolamento |
| tests/test_auditoria.py | Eventos, autor e rollback |
| tests/test_auditoria_http.py | Login, permissões e visibilidade |
| tests/test_manutencoes.py | Períodos, conflitos e bloqueios |
| tests/test_manutencoes_http.py | Permissões, CSRF, cadastro e consulta |
| tests/test_concorrencia_manutencao.py | Disputa manutenção/reserva nos três tipos |
| tests/test_materiais.py | Retirada, devolução, estados, permissões e auditoria |
| tests/test_materiais_http.py | Listagem, isolamento, movimentações e recusas |
| tests/test_disponibilidade.py | Sobreposição, manutenção, limites e filtros |
| tests/test_edicao_reservas.py | Edição, conflitos, aprovação, auditoria, avisos e rollback |
| tests/test_edicao_http.py | Formulário, persistência, auditoria, CSRF e recusas |
| tests/test_notificacoes.py | Geração, destinatário, leitura, isolamento, escape e rollback |
| tests/test_relatorios.py | Contagens, horas, períodos e conflitos evitados |
| tests/test_relatorios_http.py | Acesso, filtros, erros e consulta sem alteração |
| tests/test_nao_comparecimento.py | Permissões, prazo, estados, repetição e rollback |
| tests/test_nao_comparecimento_http.py | Rota, botão, CSRF, mensagem e persistência |
| tests/test_atualizar_auditoria.py | Migração, backup, preservação, índices, gatilhos e rollback |
| tests/test_seguranca_login.py | CSRF, renovação do token e SQL |
| tests/test_seguranca_xss.py | Escape de HTML em duas páginas |
| tests/test_validar_backup.py | Preservação e recusa de entradas inválidas |
| teste_concorrencia_http.py | Duas sessões por HTTP e registros associados |
| teste_testcontainers.py | Ciclo do container, código de saída e quantidade esperada |
| e2e/test_fluxo_reserva.py | Login, criação, consulta, conflito, cancelamento e histórico |

Persistência temporária real também caracteriza integração.
A suíte não é integralmente composta por testes unitários isolados.

## 6. Evidências e versões principais

| Etapa | Commit |
| --- | --- |
| TDD: RED do controle de acesso | 1ed928d |
| TDD: GREEN | 49b42fe |
| Ampliação e CI do TDD | 250f9b2 |
| Segurança do login | 003cc82 |
| Escape de HTML | 75c7622 |
| Concorrência HTTP | 7cb6a29 |
| Segurança Docker e classificação HTTP no Sonar | 02737a6 |
| Auditoria E2E | 98d26d5 |
| Concorrência manutenção/reserva | 67b3d00 |
| Plano e versão da instalação limpa | c84dac2 |
| Registro da instalação limpa | 2d31e4f |
| Verificador de backup | 8820445 |
| Testes do backup e cobertura de sete módulos | da93d49 |
| Integração Testcontainers | b1b308a |
| Exigência de pacotes binários | 047995b |
| Correção YAML | 1e42442 |
| Duas medições planejadas de carga | 49f9268 |
| Checklist | f533ef8 |
| Índice de evidências | b990407 |
| README atualizado | b94a8ea |
| Changelog | 04f2d2c |
| Relatório consolidado | 3a76227 |
| Segurança consolidada | c11c3ba |
| Plano consolidado | 5ffea52 |

Não atribuir resultados de uma versão automaticamente a outra.

## 7. Metas e critérios

| Item | Critério | Evidência ou estado |
| --- | --- | --- |
| Linhas | Pelo menos 80% | 97,46% em da93d49 |
| Ramificações | Pelo menos 70% | 94,83% em da93d49 |
| Código novo no Sonar | Pelo menos 80% | 84,1% em 3a76227 |
| Duplicação no código novo | No máximo 3% | 0,0% em 3a76227 |
| Quality Gate | Aprovação | Aprovado em 3a76227; conferir candidata final |
| Artefatos | Relatórios acessíveis | Cobertura JSON/XML/HTML e log Testcontainers |
| Regras críticas | Verificações associadas | Revisão final pendente |
| Container | Execução controlada | Testcontainers com SQLite aprovado |
| Banco em container | Correspondência com exigência acadêmica | Confirmar aceitação; sem servidor de banco separado |
| Navegador | Fluxo principal | Chromium aprovado |
| Desempenho | Metas prévias no cenário definido | Duas repetições de GET /login aprovadas |
| Instalação | Ambiente novo | Clone separado c84dac2; repetir na candidata |
| Recuperação | Integridade e dados | Backup/restauração SQLite verificados |
| Segurança | Controles e revisão | Parcial; não há certificação |
| Revisão por pares | Outro integrante | Pendente |
| Release | Main avaliada e tag | Pendente |
| Decisão do grupo | Contribuições e riscos confirmados | Pendente |

Python foi informado como permitido. Isso não comprova aceitação
automática de todas as equivalências de ferramentas.

## 8. Reservas e cancelamento

Usuário/recurso ativos, finalidade válida e início futuro.
Sobreposição bloqueada nos estados SOLICITADA, APROVADA e EM_USO.
Horários consecutivos são permitidos.

As escritas utilizam BEGIN IMMEDIATE no SQLite.

Cancelamento pelo proprietário antes do início, somente em SOLICITADA
ou APROVADA. O registro é preservado e o horário liberado.
Não há exclusão física pela interface.

Reserva, auditoria e aviso das operações correspondentes compartilham
transação.

## 9. Aprovação e responsáveis

Responsável ativo, vinculado, reserva SOLICITADA e ainda não iniciada.
Aprovação verifica recurso ativo, manutenção e sobreposição.
Rejeição libera o horário. Auditoria e aviso participam da transação.

O cadastro permite responsável ativo com perfil RESPONSAVEL.
Vínculo é opcional; recursos que exigem aprovação podem aguardar
enquanto não houver responsável configurado.

Alteração de vínculo existente pela interface permanece pendente.

## 10. Auditoria e próprias reservas

Auditadas: criação, alteração, cancelamento, aprovação, rejeição,
retirada, devolução e não comparecimento de materiais.

Eventos registram reserva, autor, ação, horário e situações.
Alterações preservam detalhes anteriores e novos.
Falhas simuladas verificam rollback.

A auditoria é exclusiva do administrador e apresenta até 100 eventos.
Testes específicos desse limite e ordenação permanecem pendentes.

Próprias reservas:

- Ativas: EM_USO ou SOLICITADA/APROVADA com término futuro.
- Histórico: complemento de Ativas.
- Todas: registros do usuário conectado.
- Ativas ordenadas por início/ID crescentes.
- Histórico/Todas por início/ID decrescentes.
- EM_USO permanece ativa até devolução.

Sem paginação ou reconstrução dos eventos anteriores.

## 11. Manutenção

Administrador cadastra período futuro, motivo obrigatório até 200 caracteres
e término posterior ao início.

Sobreposição com manutenção ou reserva ativa é bloqueada.
Criação, edição e aprovação de reserva conferem manutenção.
Horários consecutivos são permitidos.

O cadastro de manutenção não gera evento na auditoria de reservas.

A disputa manutenção/reserva verifica uma aceitação e uma recusa
para SALA, PROFESSOR e MATERIAL, datas e estado inicial;
quando a reserva vence, também auditoria e aviso.

Não força todas as ordens internas nem utiliza HTTP.
Edição/desativação pela interface e manutenção imediata permanecem pendentes.

## 12. Materiais e não comparecimento

Retirada: administrador ou responsável vinculado, APROVADA,
período permitido, recurso ativo e sem bloqueios de manutenção/uso.

Transições: APROVADA → EM_USO → CONCLUIDA.
Devolução permitida após prazo e com recurso inativo.
Movimentações exigem POST, permissões e CSRF e geram auditoria.

Não comparecimento:

- Somente MATERIAL, reserva APROVADA.
- Horário igual ou posterior ao término.
- Administrador ativo ou responsável ativo vinculado.
- Recurso inativo não impede registro histórico.
- EM_USO exige devolução.
- Operação manual, sem mudança automática pelo prazo.
- Repetição recusada sem duplicar auditoria.
- Atualização/auditoria na mesma transação.
- Sem aviso interno dessa movimentação.

Evidências manuais históricas: reservas nº 11 e nº 12.
O script atualizar_auditoria_nao_comparecimento.py teve preservação
e backup observados; testes específicos permanecem pendentes.

## 13. Cobertura

Referência da93d49: 97,46% de linhas e 94,83% de ramificações.

Escopo: app, banco, servico_reservas, servico_materiais,
servico_relatorios, atualizar_auditoria e validar_backup.

HTTP separado, Chromium e controle externo Testcontainers não são
somados à medição da suíte principal.

Não abrange HTML, CSS, JavaScript ou todos os scripts administrativos.
Comandos atualizados no README e PLANO_TESTES.

Cobertura elevada não comprova ausência de defeitos.

## 14. Disponibilidade e edição

Disponibilidade exige início/término juntos quando informados,
valida datas e exclui reservas ativas e manutenção sobrepostas.

Permite consulta de períodos passados e horários consecutivos,
combinando tipo, capacidade, localização e competência.

Edição exige proprietário ativo, SOLICITADA/APROVADA e início futuro.
Valida recurso, período e finalidade; exclui a própria reserva do conflito.
Restritos/professores voltam a SOLICITADA; comuns ficam APROVADA.

Pedido sem mudança é recusado.
Auditoria ALTERACAO registra antes/depois; reserva e aviso são transacionais.

## 15. Defeitos e retestes

| Registro | Problema | Estado |
| --- | --- | --- |
| DEF01 | EM_USO desaparecia de Ativas após prazo | Corrigido no escopo verificado |
| DEF02 | Template diferente do include | Corrigido e retestado |
| DEF03 | Conexões impediam limpeza no Windows | Fechamento explícito e testes |
| DEF04 | YAML impedia CI | Corrigido nas execuções registradas |
| DEF05 | Caracteres corrompidos | Corrigidos nos trechos conferidos |
| INV01 | Falhas de conexão na carga sem pausa | Causa não confirmada |

Também foram corrigidos apontamentos Docker/Sonar e instalação/YAML
do Testcontainers. Detalhes no relatório de qualidade e histórico Git.

## 16. Notificações

Avisos internos ao proprietário para criação, edição, cancelamento,
aprovação e rejeição, com mensagem conforme o estado.

Novos avisos são não lidos. Consulta/leitura somente pelo destinatário.
Marcação exige login e CSRF; aviso alheio/inexistente retorna 404.
GET não marca leitura; avisos lidos permanecem.

Operação, auditoria e aviso compartilham transação nos fluxos abrangidos.

Sem e-mail, SMS, tempo real, paginação ou aviso ao responsável.
Movimentações e não comparecimento não geram aviso.

## 17. Relatórios e conflitos evitados

Administrador ativo consulta contagens das sete situações,
agrupamento por recurso, horas previstas e conflitos registrados.

Horas consideram APROVADA, EM_USO e CONCLUIDA,
somente o trecho sobreposto ao período consultado.
Representam tempo reservado, não utilização real.

conflitos_reservas registra sobreposição na criação, edição e aprovação,
com usuário, recurso, reserva conflitante, período, operação e data.

Filtro por criado_em; sem datas, todo histórico.
Repetições geram registros separados.
Cancelamento/inativação posterior não apaga tentativas.
Manutenção, preenchimento e falta de permissão não entram no indicador.
Tentativas anteriores não são reconstruídas.

Sem tempo real, exportação, paginação ou E2E equivalente do relatório.

## 18. CI e Sonar

Workflows testes.yml e testcontainers.yml em .github/workflows.

Pipeline principal: HTTP separado, suíte, cobertura, artefatos e Chromium.
Metas: 80% linhas e 70% ramificações; medições vazias são recusadas.
Cobertura publicada como relatorios-cobertura por 30 dias.

Sonar em PRs e pushes da main; segredo SONAR_TOKEN;
espera pelo Quality Gate com limite de 300 segundos.
Arquivos HTTP e Testcontainers classificados como testes.

Testcontainers: constrói imagem e publica resultado-testcontainers.

Referência 3a76227: sete checks verdes, Gate aprovado,
84,1% código novo, 0,0% duplicação, zero novos problemas e hotspots.

Proteção da main e CI após merge ainda precisam de conferência.

## 19. Migração, backup e refatorações

test_atualizar_auditoria.py verifica ausência de banco/tabela,
estrutura atualizada, preservação/backup, coluna detalhes,
índice/gatilho, coluna desconhecida, rollback e repetição.

Não cobre automaticamente falta de espaço, interrupção ou demais scripts.

validar_backup.py abre origem somente para leitura, verifica integridade,
cria backup/restauração temporários e compara estrutura e dados.
Execução registrada: sete tabelas do banco do clone separado.

Quatro testes verificam preservação, arquivo inexistente, diretório
e arquivo inválido.

Não constitui backup persistente nem recuperação completa de desastre.

Refatorações extraíram validações comuns no serviço
e dados de reserva em templates/_dados_reserva.html.
Formulários, CSRF e ações específicas permanecem nas páginas.

## 20. Navegador e HTTP

Chromium: login inválido/válido, criação, consulta, conflito,
cancelamento, Ativas/Histórico e registros associados.
Servidor em porta dinâmica e SQLite temporário.

HTTP concorrente: duas sessões coordenadas, uma aceitação, uma recusa,
uma reserva, auditoria, notificação e conflito registrado.

A coordenação não garante ordem interna.
Ampliar aprovação, edição, materiais, navegadores e capturas/traces.

## 21. Docker e Testcontainers

Imagem Python 3.14 slim, requirements.lock com hashes,
cópias explícitas e usuário sem privilégios de root.

.dockerignore exclui bancos locais, ambientes virtuais, backups
e arquivos de ambiente. Sem montagem do banco local.

teste_testcontainers.py inicia, aguarda e remove o container,
coleta log e exige código zero e 292 testes esperados.

Reconstruir a imagem após alterações e atualizar a quantidade esperada
quando a suíte mudar.

SQLite está dentro do container; sem servidor externo de banco.
Aceitação acadêmica dessa abordagem deve ser confirmada.
Imagem-base sem digest e ambiente externo sem lock completo com hashes.

## 22. Desempenho

Plano: performance/consulta_login_10usuarios_60s.jmx.

Duas execuções planejadas: Windows, JMeter 5.6.3, Flask local,
debug desligado, cliente e servidor na mesma máquina.

GET /login; dez usuários, subida de cinco segundos, 60 segundos,
pausa de um segundo; verifica HTTP 200 e texto Acesso ao sistema.

Metas prévias: zero erros, p95 até 500 ms e pelo menos 500 amostras.

| Execução | Amostras | Erros | Média (ms) | p95 (ms) | Máximo (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 | 85 |
| 2 | 565 | 0 | 8,11 | 19 | 69 |

Ambas atenderam. Evidências em docs/performance/resultado-01.md,
registradas no commit 49f9268.

Histórico exploratório: sem pausa, 1.289 falhas em 17.633 amostras;
com pausa, 570 sem falha, média 5,49 ms e p95 8 ms.

BindException teve causa não confirmada. Reduzir carga não comprova
correção. Usuários ativos incluem espera pelo timer.

Não mede autenticação por POST, reservas ou capacidade de produção.
Cenários autenticados continuam pendentes.

## 23. Segurança e instalação

test_seguranca_login.py: tokens, renovação e tentativas de SQL.
test_seguranca_xss.py: escape em duas páginas.

Auditorias dos locks principal e E2E sem vulnerabilidades conhecidas
reportadas nas execuções registradas.
Não abrangem automaticamente Chromium, imagem Docker ou Testcontainers.

Limitações: revisão completa, implantação HTTPS/cookies,
limitação de tentativas e ampliação de XSS. Sem teste de invasão completo.

Instalação limpa no commit c84dac2: clone temporário e ambiente novo,
mesmo computador; dependências, banco, exemplos, administrador,
login e criação/consulta da Sala 101 confirmados.

Reserva nº 1: 03/11/2026, 14h–15h, aprovada.
Detalhes em VALIDACAO_INSTALACAO.md.
Repetir a validação na candidata final.

## 24. Entrega e verificações restantes

- Confirmar equivalências de ferramentas com o professor.
- Conferir requisitos e limitações contra o enunciado.
- Revisar gestão administrativa e conflitos por tipo.
- Ampliar cenários conforme riscos e registrar ressalvas reais.
- Conferir documentação das rotas e links.
- Confirmar nomes completos e contribuições.
- Obter revisão real por outro integrante.
- Conferir conteúdo antes de tornar o repositório público.
- Integrar alteração revisada e conferir CI/Sonar na main.
- Validar candidata em clone limpo.
- Registrar decisão de qualidade e riscos com responsáveis.
- Criar tag anotada sem mover tags publicadas.
- Vincular CI e evidências ao commit avaliado.
- Preparar demonstração e realizar envio único pelo grupo.

Referências de fechamento:

- docs/entrega/checklist.md
- docs/evidencias/README.md
- CHANGELOG.md
- RELATORIO_QUALIDADE.md
- PLANO_TESTES.md
- SEGURANCA.md

Não registrar assinatura, revisão, merge ou aprovação sem evidência.
Não apresentar resultados locais como prontidão para produção.