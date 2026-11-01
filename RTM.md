# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 31/10/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Esta matriz relaciona requisitos, riscos, testes, evidências e pendências.

## 1. Legenda

- **Implementado e verificado:** disponível e verificado no escopo indicado.
- **Parcial:** parte da implementação ou da verificação permanece pendente.
- **Pendente:** implementação ou verificação ainda não realizada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes e cobertura não representam percentual de conclusão.
- Aprovação dos testes não comprova ausência de defeitos.
- O cliente Flask não substitui testes externos por HTTP ou automação de navegador.
- Resultados históricos pertencem às versões em que foram medidos.
- Resultados de cobertura somente são comparáveis considerando ferramenta, versão e escopo.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e evidências | Situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Testes de consulta, cancelamento, aprovação, auditoria, manutenção, edição, notificações, relatórios, materiais e não comparecimento | Implementado e verificado nas operações atuais; revisão geral de segurança pendente |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | test_consulta.py, cadastro manual e vínculo de responsável no cadastro | Implementado e verificado; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e consulta manual | Implementado e verificado; navegador automatizado pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | Testes de reservas, listagem, cancelamento e edição; reteste após refatoração do serviço | Implementado e verificado no escopo atual |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos | Testes de criação, aprovação, disponibilidade e edição | Implementado no mecanismo compartilhado; ampliar cenários explícitos por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas | Duas solicitações simultâneas em test_reservas.py, com uma reserva aceita e um conflito registrado | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Testes de aprovação, vínculo, cadastro com responsável e nova aprovação após edição | Implementado e verificado; alteração do vínculo de recursos existentes pela interface pendente |
| RF08 | Bloquear recursos em manutenção | Reserva impossível de atender | Testes de manutenção, disponibilidade e edição; consulta manual | Implementado e verificado; concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py, test_materiais_http.py e fluxo manual da reserva nº 11 | Implementado e verificado no serviço, nas rotas e manualmente; navegador automatizado pendente |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, edição, materiais, não comparecimento e migração da auditoria | Implementado nas operações atuais; testes específicos de limite e ordenação da consulta pendentes |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py e fluxo manual de leitura | Implementado como avisos internos para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | 21 testes do serviço de relatórios, 16 da rota e conferência manual do contador | Contagens, horas previstas e conflitos evitados implementados e verificados |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP, verificações manuais e reteste dos templates refatorados | Parcial: avaliação em diferentes telas e automação de navegador pendentes |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README inicial e esta matriz | Parcial: ampliar instalação, fluxos e interfaces |

O indicador de horas de RF12 representa carga horária prevista ou alocada nas reservas. Não mede o tempo real de utilização do recurso.

A gestão administrativa completa de usuários e recursos deve ser conferida com o enunciado antes da entrega.

## 3. Regras críticas

| ID | Regra | Risco | Verificação | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Serviço, restrição no banco e testes de edição e disponibilidade | Verificado nesses fluxos; ampliar casos explícitos de criação |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Criação, aprovação, edição, disponibilidade e horários consecutivos | Verificado no mecanismo atual; ampliar cenários por tipo |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | Teste de concorrência com usuários distintos; uma reserva e um conflito persistidos | Verificado no serviço; concorrência por HTTP pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Testes de manutenção, edição e disponibilidade; consulta manual | Implementado e verificado; concorrência específica pendente |
| RC05 | SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Aprovação e materiais nos serviços e rotas; fluxo manual da reserva nº 11 | Implementado e verificado para materiais |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Aprovação, cancelamento e não comparecimento; reserva nº 12 | Verificado no escopo atual; não comparecimento somente para materiais |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Perfil, vínculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Sem exclusão física disponível; edição e cancelamento após início bloqueados | Verificado nas operações existentes |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Criação, alteração, cancelamento, aprovação, rejeição, retirada, devolução e não comparecimento | Verificado nas transições atuais |

Tentativas bloqueadas por conflito não alteram o estado da reserva. Elas são registradas separadamente em `conflitos_reservas`.

## 4. Testes automatizados

### Execução local histórica com duração registrada

- Data: 31/10/2026.
- Suíte completa: **283 testes aprovados**.
- Resultado: **OK**.
- Duração: **90,405 segundos**.
- Execução com unittest e coverage.py.
- Evidência: imagem do terminal.
- Incluiu os oito testes de `test_atualizar_auditoria.py`.
- O commit `4c94cf27` corresponde à atualização posteriormente analisada pelo Sonar.

### Retestes e CI posteriores

- A suíte foi informada como aprovada após a refatoração de `servico_reservas.py`.
- A extração dos dados compartilhados dos templates inicialmente provocou erros HTTP 500.
- Foi identificada diferença entre o nome do arquivo criado e o nome usado no `include`.
- O arquivo foi renomeado para `templates/_dados_reserva.html`.
- Após a correção, os testes foram informados como aprovados.
- As execuções de CI #106 e #107 aparecem aprovadas na evidência do GitHub Actions.
- O pacote `relatorios-cobertura.zip` foi baixado e conferido.
- A duração local histórica de 90,405 segundos não deve ser atribuída às execuções posteriores.
- O JSON de cobertura não informa a quantidade de testes nem a duração da suíte; esses dados devem ser consultados no log de testes.

### Arquivos e escopos

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização, cadastro, persistência, filtros e vínculo de responsável |
| tests/test_reservas.py | Criação, conflitos persistidos, horários consecutivos, concorrência, tentativas repetidas e cancelamento |
| tests/test_minhas_reservas.py | Login, isolamento, filtros, prazo, atraso e ordenação |
| tests/test_cancelamento_http.py | Autenticação, autorização e CSRF no cancelamento |
| tests/test_aprovacoes.py | Aprovação, rejeição, vínculo, prazo, estado e persistência do conflito bloqueado |
| tests/test_aprovacoes_http.py | Rotas, perfis, CSRF e isolamento por responsável |
| tests/test_auditoria.py | Registro das operações, autor e rollback |
| tests/test_auditoria_http.py | Login, permissões e visibilidade do botão |
| tests/test_manutencoes.py | Períodos, conflitos e bloqueio de reservas |
| tests/test_manutencoes_http.py | Permissões, CSRF, cadastro e consulta |
| tests/test_materiais.py | Retirada, devolução, permissões, horários, estados, manutenção e auditoria |
| tests/test_materiais_http.py | Listagem, isolamento, retirada, devolução, permissões, CSRF e recusas |
| tests/test_disponibilidade.py | Períodos, sobreposição, estados, manutenção, limites e filtros combinados |
| tests/test_edicao_reservas.py | Edição, validações, conflitos persistidos, manutenção, aprovação, auditoria, notificações e rollback |
| tests/test_edicao_http.py | Formulário, persistência, auditoria, CSRF e recusas |
| tests/test_notificacoes.py | Geração, destinatário, leitura, isolamento, CSRF, ordenação, escape e rollback |
| tests/test_relatorios.py | Permissões, datas, contagens, horas, agrupamento, limites, arredondamento e conflitos evitados |
| tests/test_relatorios_http.py | Login, perfis, filtros, erros, campos, contador e consulta sem alteração dos registros |
| tests/test_nao_comparecimento.py | Permissões, prazo, estados, recurso inativo, repetição, auditoria e rollback |
| tests/test_nao_comparecimento_http.py | Rota, botão, perfis, CSRF, prazo, repetição, mensagem e persistência |
| tests/test_atualizar_auditoria.py | Migração em banco temporário, backup, preservação dos registros, índices, gatilhos, rollback e repetição |

### Quantidades de arquivos selecionados

| Arquivo | Métodos de teste |
| --- | ---: |
| test_consulta.py | 24 |
| test_reservas.py | 13 |
| test_edicao_reservas.py | 24 |
| test_aprovacoes.py | 12 |
| test_relatorios.py | 21 |
| test_relatorios_http.py | 16 |
| test_atualizar_auditoria.py | 8 |

Os métodos podem conter vários cenários com `subTest`.

Testes de serviço com persistência real também verificam integração com SQLite. Não são integralmente testes unitários isolados.

### Executar a suíte

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Limitações

- Persistência testada com bancos SQLite temporários.
- Rotas testadas com o cliente Flask.
- Sessão simulada em vários testes; login e senha possuem testes próprios.
- O cliente Flask não executa JavaScript nem confirmações dos botões.
- HTTP externo, navegador automatizado e carga pendentes.
- Verificação com banco em container pendente.
- A migração `atualizar_auditoria.py` possui testes; os demais scripts ainda precisam de verificação específica.
- Cobertura Python não abrange HTML, CSS e JavaScript.

## 5. Evidências recentes e histórico de versões

Os resultados históricos pertencem às versões em que foram medidos.

| Etapa | Evidência |
| --- | --- |
| Cadastro e TDD inicial | Commits 1ed928d, 49b42fe e 250f9b2; 16 testes em 6,098 segundos |
| Reservas e concorrência inicial | Commit 940a392; 22 testes em 7,883 segundos |
| Cancelamento | Commits ecb0eb7 e 7ae60b7; etapa de 31 testes |
| Aprovação e perfis | Commits cca4432 e 9946585; etapa de 56 testes |
| Auditoria | Commits 1515dcd, 0fc4cf5, 6ac9d65 e db1e5e8; evolução até 65 testes |
| Manutenção | 86 testes em 21,313 segundos; bloqueio manual da Sala 101 e reserva consecutiva nº 9 |
| Materiais | Commit 22014eb; 103 testes em 28,560 segundos; retirada e devolução da reserva nº 11 |
| Cobertura inicial | Commit 400b119; 89,87% de linhas e 85,16% de ramificações |
| Disponibilidade | Commit 6b8d472; 118 testes em 48,257 segundos |
| Edição e detalhes | Commits 35b5fe5 e b9d752d; etapas de 142 e 154 testes |
| Correção de materiais atrasados | Commit 9e94725; 161 testes em 54,707 segundos |
| Notificações | Commit 5a18890; suíte de 185 testes informada como aprovada |
| Relatórios | Commit 2ae1f0c; 213 testes com cobertura em 58,742 segundos |
| RTM e cobertura | Commit d776bd7; relatório JSON e HTML da etapa de 213 testes |
| Metas de cobertura na CI | Commit 4062de2; aprovação informada pelo executor |
| Testes HTTP de materiais | Commit 4ca4689; 231 testes em 70,820 segundos |
| Migração da auditoria para não comparecimento | Ação NAO_COMPARECEU acrescentada, backup e 11 registros preservados |
| Serviço de não comparecimento | 14 testes específicos em 3,476 segundos |
| Suíte intermediária | 245 testes em 69,067 segundos |
| Não comparecimento completo | Commit f1d0af2; 257 testes em 84,677 segundos; CI informada como aprovada |
| Verificação manual | Reserva nº 12, criação, aprovação e não comparecimento conferidos na auditoria |
| Atualização anterior do RTM | Commit 3536954, com push confirmado |
| Nova medição de cobertura | 257 testes em 69,538 segundos; cobertura combinada de 97% |
| JSON de cobertura atualizado | Commit 47add5d, com push confirmado; CI informada como aprovada |
| Contador inicialmente vazio | Relatório apresentou 0 conflitos após reiniciar o Flask |
| Bloqueio manual | Sala 101, tentativa para 10/11/2026, das 14h30 às 15h30, recusada por sobreposição |
| Contador após bloqueio | Relatório sem datas apresentou 13 reservas, 5,33 horas previstas e 1 conflito evitado |
| Implementação dos conflitos | Commit d917f69; nove arquivos; commit e push confirmados |
| Suíte da etapa de conflitos | 269 testes aprovados em 91,264 segundos |
| Cobertura da etapa de conflitos | 269 testes em 90,688 segundos; 97,70% de linhas, 96,27% de ramificações e 97% combinada |
| Histórico preservado | Commit a755c10; atualização do RTM e preservação de RTM_historico.md |
| Cobertura com 269 testes | Commit ec99faa; atualização do JSON e documentação |
| Vínculo no cadastro | Commit 7298034; cadastro com responsável e seis testes adicionais |
| Suíte após vínculo | 275 testes aprovados em 102,288 segundos |
| CI do vínculo | Execuções #85 e #86 aprovadas, conferidas em 31/10/2026 |
| Dependências fixadas | requirements.txt passou a registrar versões exatas |
| Falha de sintaxe YAML | Execução #87 recusada antes de iniciar os testes; corrigida posteriormente |
| Correção do YAML | Commit c81e8ae; execuções #88 e #89 aprovadas |
| Hashes das dependências | Commit d6de95ea; requirements.lock e instalação com --require-hashes |
| Integração Sonar | Commit f2e3c18; execuções #92 e #93 aprovadas |
| Primeira cobertura importada | Sonar apresentou 77,8% e duplicação de 3,9%; Quality Gate reprovado |
| Testes da migração | Oito testes aprovados em banco temporário após correção do fechamento das conexões |
| Medição local com 283 testes | 283 testes aprovados em 90,405 segundos; cobertura combinada local de 96% no escopo medido |
| Aprovação Sonar anterior | Commit 4c94cf27; Quality Gate Passed; cobertura exibida de 82,4% e duplicação de 3,9% |
| Refatoração do serviço | Validações e consultas repetidas extraídas em funções auxiliares; testes informados como aprovados |
| Medição intermediária de duplicação | Sonar mostrou 1,68% no código novo, limite de 3% e Quality Gate Passed |
| Refatoração dos templates | Dados comuns extraídos para templates/_dados_reserva.html e reutilizados em aprovacoes.html e materiais.html |
| Defeito de nome do template | Execução mostrou 19 falhas com respostas HTTP 500; nome corrigido e reteste informado como aprovado |
| Análise intermediária do Sonar | Commit exibido 00f01ac3; cobertura no código novo de 83,74%, duplicação de 0,34% e Quality Gate Passed |
| Espera pelo Quality Gate | Workflow alterado para aguardar até 300 segundos e falhar em caso de reprovação |
| CI da espera pelo Quality Gate | Execuções #104 e #105 aparecem aprovadas na evidência do GitHub Actions |
| Publicação dos relatórios | Commit 23078f86; geração de HTML e publicação do pacote relatorios-cobertura |
| CI com artefatos | Execuções #106 e #107 aparecem aprovadas |
| Sonar mais recente | Commit 23078f86; Quality Gate Passed; cobertura no código novo de 83,74%; duplicação no código novo e estimada após o merge de 0,0% |
| Conferência do artefato | ZIP baixado com JSON, XML e HTML; 97,69% de linhas, 95,39% de ramificações e 97,08% de cobertura combinada nos seis módulos medidos |

### Links principais

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Sonar — Pull Request nº 1](https://sonarcloud.io/summary/overall?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)
- [Relatórios iniciais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/2ae1f0c)
- [Metas na CI](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4062de2)
- [Não comparecimento](https://github.com/Arthurmrsilva/organizacao-recursos/commit/f1d0af2)
- [Cobertura com 257 testes](https://github.com/Arthurmrsilva/organizacao-recursos/commit/47add5d)
- [Contador de conflitos](https://github.com/Arthurmrsilva/organizacao-recursos/commit/d917f69)
- [Vínculo no cadastro](https://github.com/Arthurmrsilva/organizacao-recursos/commit/7298034)
- [Aprovação Sonar anterior](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4c94cf27)
- [Refatoração do serviço](https://github.com/Arthurmrsilva/organizacao-recursos/commit/00f01ac3)
- [Publicação dos relatórios](https://github.com/Arthurmrsilva/organizacao-recursos/commit/23078f86)

Os prints da entrega devem identificar cenário, data, resultado esperado, resultado observado, requisito e commit, quando aplicável.

Antes da entrega, comparar o hash analisado pelo Sonar com a versão que será apresentada.

A aprovação do workflow ou do Sonar não substitui revisão por outro integrante.

## 6. Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | 97,69% — 761 de 779 linhas, no JSON do artefato conferido |
| Cobertura de ramificações | Pelo menos 70% | 95,39% — 269 de 282 ramificações, no JSON do artefato conferido |
| Cobertura no Sonar | Pelo menos 80% no código novo | 83,74% no commit 23078f86; condição atendida |
| Duplicação no Sonar | No máximo 3% no código novo | 0,0% no commit 23078f86; condição atendida |
| Quality Gate na CI | Aguardar resultado e falhar em caso de reprovação | Implementado; execução de PR #107 aprovada no cenário positivo |
| Relatórios de cobertura | Disponíveis para download | JSON, XML e HTML publicados e ZIP conferido |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Consolidar revisão dos cenários críticos |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Sonar mostra zero novos problemas; revisão completa pendente |
| Testes unitários isolados | Regras sem dependências reais | Ampliação pendente |
| Integração | Persistência e integração das camadas | Verificada no escopo testado |
| Testes em container | Banco com Testcontainers ou equivalente aceito | Pendente de adequação e execução |
| Integração externa | WireMock quando aplicável | Sem integração externa; avisos internos adotados para RF11 |
| HTTP em caixa-preta | Acesso externo por HTTP | Pendente |
| Ponta a ponta | Automação no navegador | Pendente |
| Concorrência | Ausência de dupla reserva | Verificada no serviço; ampliar HTTP e manutenção |
| Desempenho | Plano e resultados de carga | Pendente |
| Análise estática | Ferramenta e resultados registrados | SonarQube Cloud integrado e Quality Gate aprovado |
| Segurança | Revisão e evidências | Parcial; autenticação, perfis, hash, CSRF e verificação de hashes das dependências implementados |
| Revisão por pares | Revisão de outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Parcial; consolidar documento |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio pelo grupo | Pendente |

O responsável pelo desenvolvimento informou que o professor permite a implementação em Python. Essa confirmação não implica aceitação automática de todas as substituições de ferramentas ou entregáveis do enunciado.

## 7. Reservas e cancelamento

- Criação com recurso ativo, finalidade e período válido.
- Início no futuro.
- Usuário ativo verificado no serviço de criação.
- Sobreposição bloqueada nos estados SOLICITADA, APROVADA e EM_USO.
- Horários consecutivos permitidos.
- Gravações serializadas com BEGIN IMMEDIATE no SQLite.
- Cancelamento pelo proprietário antes do início.
- Cancelamento permitido somente em SOLICITADA e APROVADA.
- Registro cancelado preservado e horário liberado.
- Sem exclusão física de reservas pela interface.

Criação e cancelamento bem-sucedidos geram auditoria e notificação na mesma transação.

Validações e consultas compartilhadas foram extraídas para funções auxiliares em `servico_reservas.py`. Os testes foram informados como aprovados após a refatoração, com execuções posteriores da CI também aprovadas.

## 8. Aprovação e vínculo de responsáveis

- Responsável ativo e vinculado ao recurso.
- Aprovação ou rejeição somente de SOLICITADA antes do início.
- Aprovação verifica recurso ativo, manutenção e conflitos.
- Rejeição libera o horário.
- Auditoria e aviso ao solicitante na mesma transação.
- Aprovação bloqueada por outra reserva registra uma tentativa de conflito.
- A tentativa bloqueada mantém os estados e não gera aviso de sucesso.

### Vínculo no cadastro

Implementado no commit `7298034`.

- Administrador pode selecionar um responsável no cadastro do recurso.
- A lista apresenta somente usuários ativos com perfil RESPONSAVEL.
- O servidor valida novamente o responsável no envio do formulário.
- Perfil incorreto, usuário inexistente e responsável inativo são recusados.
- Erros de validação preservam a seleção válida.
- O vínculo é opcional.
- Recurso restrito ou professor sem responsável pode permanecer aguardando aprovação até que o vínculo seja configurado.
- Alteração do vínculo de recursos existentes pela interface permanece pendente.

O fluxo manual de cadastro com responsável, reserva e aprovação pelo usuário vinculado foi informado como bem-sucedido.

## 9. Auditoria e filtros das próprias reservas

### Auditoria

Operações auditadas:

- Criação.
- Alteração.
- Cancelamento.
- Aprovação.
- Rejeição.
- Retirada.
- Devolução.
- Não comparecimento de materiais.

Cada evento registra reserva, autor, ação, horário e situações anterior e nova.

A auditoria usa a transação da operação. Falhas provocam rollback conjunto.

A consulta é exclusiva do administrador e apresenta os 100 eventos mais recentes.

### Filtros

- **Ativas:** todas em EM_USO; SOLICITADA e APROVADA com término futuro.
- **Histórico:** complemento da condição de Ativas.
- **Todas:** todos os registros do usuário conectado.
- Ativas ordenadas por início e ID crescentes.
- Histórico e Todas por início e ID decrescentes.
- EM_USO continua em Ativas até a devolução, com aviso após o prazo.

O encerramento do período não altera automaticamente a situação.

### Limitações

- Eventos anteriores à implantação não são reconstruídos.
- Horários seguem o relógio local do servidor.
- Consulta sem paginação.
- Nome exibido corresponde ao recurso atual da reserva.
- Alterações preservam dados anteriores e novos em detalhes.
- Limite e ordenação da auditoria precisam de testes específicos.

## 10. Manutenção

- Cadastro e consulta pelo administrador.
- Período futuro e término posterior ao início.
- Motivo obrigatório de até 200 caracteres.
- Bloqueio de sobreposição com manutenção ou reserva ativa.
- Criação, edição e aprovação de reserva verificam manutenção.
- Horários consecutivos permitidos.
- Proteção CSRF.
- Autor e data registrados na tabela de manutenção.

O cadastro não gera evento na auditoria de reservas.

Pendências: edição e desativação pela interface, manutenção imediata e concorrência específica.

## 11. Materiais

- Administrador gerencia movimentações.
- Responsável gerencia materiais vinculados.
- Retirada de reserva APROVADA durante o período permitido.
- Bloqueio de recurso inativo, em manutenção ou já em uso.
- Retirada: APROVADA → EM_USO.
- Devolução: EM_USO → CONCLUIDA.
- Devolução permitida após o prazo e com recurso inativo.
- Auditoria das movimentações.
- Materiais atrasados em uso continuam visíveis.
- GET não realiza movimentação.
- Permissões, vínculo, estados e CSRF verificados.

### Evidência manual histórica

Reserva nº 11 do Projetor 01 em 26/10/2026:

- Período reservado: 20h15 às 21h15.
- Retirada: 20h17min10s.
- Devolução: 20h18min04s.
- Autor: Administrador do projeto.
- Eventos nº 8 e nº 9 conferidos na auditoria.

### Reutilização do template

Os dados comuns da reserva foram extraídos para `templates/_dados_reserva.html`.

Esse arquivo é incluído pelas páginas de aprovação e de gestão de materiais. Os formulários e as condições específicas permanecem nas respectivas páginas.

## 12. Cobertura de testes

### Resultado mais recente conferido no artefato da CI

**Evidência:** relatorios-cobertura.zip, baixado do GitHub Actions e conferido em 31/10/2026.  
**Ferramenta:** coverage.py 7.17.0.

| Métrica | Quantidade coberta | Quantidade total | Resultado |
| --- | ---: | ---: | ---: |
| Linhas | 761 | 779 | 97,69% |
| Ramificações | 269 | 282 | 95,39% |
| Combinada | 1.030 | 1.061 | 97,08% |

- Linhas não cobertas: 18.
- Ramificações não cobertas: 13.
- Linhas excluídas informadas no total: 0.
- Cobertura combinada arredondada pelo relatório: 97%.
- Meta de linhas de 80%: atendida.
- Meta de ramificações de 70%: atendida.

A cobertura combinada considera linhas e ramificações. Ela não substitui os percentuais separados exigidos pela CI.

### Resultado por módulo

| Arquivo | Linhas cobertas / total | Ramificações cobertas / total | Cobertura combinada |
| --- | ---: | ---: | ---: |
| app.py | 365 / 373 | 146 / 150 | 97,71% |
| atualizar_auditoria.py | 59 / 65 | 16 / 22 | 86,21% |
| banco.py | 16 / 18 | 1 / 2 | 85,00% |
| servico_materiais.py | 56 / 57 | 29 / 30 | 97,70% |
| servico_relatorios.py | 67 / 67 | 24 / 24 | 100,00% |
| servico_reservas.py | 198 / 199 | 53 / 54 | 99,21% |
| TOTAL | 761 / 779 | 269 / 282 | 97,08% |

### Escopo

A medição inclui:

- app.py.
- banco.py.
- servico_reservas.py.
- servico_materiais.py.
- servico_relatorios.py.
- atualizar_auditoria.py.

Não inclui cobertura de templates, CSS, JavaScript nem dos demais scripts administrativos e de migração.

O ZIP de cobertura não contém, por si só, identificação suficiente para comprovar o hash e o número da execução. Preservar também a página da execução da qual ele foi baixado.

### Medição mais recente no Sonar

**Commit:** 23078f86.  
**Pull Request:** nº 1.

| Indicador | Resultado |
| --- | --- |
| Quality Gate | Passed |
| Cobertura no código novo | 83,74% |
| Condição de cobertura | Pelo menos 80% |
| Linhas novas a cobrir | 923 |
| Cobertura estimada após o merge | 82,9% |
| Duplicação no código novo | 0,0% |
| Condição de duplicação | No máximo 3% |
| Duplicação estimada após o merge | 0,0% |

O Sonar considera um escopo e métricas que não coincidem integralmente com a medição dos seis módulos pelo coverage.py.

Os 97,69% de linhas do artefato e os 83,74% de cobertura no código novo do Sonar representam medições diferentes.

### Histórico

| Etapa | Linhas | Ramificações | Combinada |
| --- | --- | --- | --- |
| 103 testes | 89,87% | 85,16% | Medição histórica |
| 213 testes | 93,31% | 90,23% | 92% |
| 257 testes | Aproximadamente 98% | Aproximadamente 96% | 97% |
| 269 testes | 97,70% — 680 de 696 | 96,27% — 258 de 268 | 97% |
| 283 testes, antes das refatorações | 96,81% — 759 de 784 | Percentual exato não transcrito | 96% |
| Artefato após as refatorações | 97,69% — 761 de 779 | 95,39% — 269 de 282 | 97,08% |

A execução com 269 testes durou 90,688 segundos e teve como base funcional o commit `d917f69`. O JSON foi atualizado no commit `ec99faa`.

A execução local anterior às refatorações, com 283 testes, durou 90,405 segundos.

Mudanças no código podem alterar a quantidade de linhas e ramificações medidas.

### Como medir localmente

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios,atualizar_auditoria -m unittest discover -s tests -v
```

```powershell
.\.venv\Scripts\python.exe -m coverage report -m
```

```powershell
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
```

```powershell
.\.venv\Scripts\python.exe -m coverage xml -o coverage.xml
```

```powershell
.\.venv\Scripts\python.exe -m coverage html -d htmlcov
```

Regenerar os relatórios após a execução para que representem a versão medida.

Cobertura alta não comprova ausência de defeitos.

## 13. Pesquisa por disponibilidade

- Início e término opcionais, preenchidos em conjunto.
- Validação de datas e ordem.
- Exclusão de recursos com reservas sobrepostas em SOLICITADA, APROVADA ou EM_USO.
- Exclusão de manutenção ativa sobreposta.
- Horários consecutivos permitidos.
- Combinação com os demais filtros.
- Consulta de períodos passados permitida.
- Atualização da lista sem subir a página.
- Limpeza também remove o período.

A pesquisa não registra tentativa de conflito: ela apenas consulta disponibilidade.

## 14. Edição

- Proprietário ativo e autenticado.
- Permitida em SOLICITADA ou APROVADA antes do início.
- Alteração de recurso, período e finalidade.
- Verificação de manutenção e conflitos, excluindo a própria reserva.
- Recursos restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicitação sem mudança recusada.
- Auditoria ALTERACAO com dados anteriores e novos.
- Edição, auditoria e notificação na mesma transação.
- Conflito bloqueado preserva reserva, auditoria e notificações.
- Tentativa bloqueada registrada separadamente.

A migração histórica de detalhes preservou nove registros com backup.

O script `atualizar_auditoria.py` possui oito testes automatizados em bancos temporários. Esses testes não equivalem à execução de uma nova migração no banco real.

## 15. Correção de materiais atrasados

Problema corrigido: EM_USO saía das Ativas após o término, mesmo sem devolução.

- EM_USO permanece em Ativas.
- SOLICITADA e APROVADA dependem de término futuro.
- Histórico usa a condição complementar.
- Aviso de atraso na interface.
- Nenhuma devolução automática.

Evidência: commit `9e94725` e testes de estado, prazo, limite exato e ordenação.

## 16. Notificações internas

Avisos persistidos simulam notificações ao proprietário da reserva.

| Operação | Aviso |
| --- | --- |
| Criação comum | Criada e aprovada automaticamente |
| Criação restrita ou professor | Aguardando aprovação |
| Edição comum | Alterada e aprovada |
| Edição restrita ou professor | Aguardando nova aprovação |
| Cancelamento | Reserva cancelada |
| Aprovação | Aprovada pelo responsável |
| Rejeição | Rejeitada pelo responsável |

- Destinatário, reserva, mensagem, data e leitura persistidos.
- Avisos novos não lidos.
- Falha no aviso desfaz a operação.
- Recusas não geram avisos de sucesso.
- GET /notificacoes lista somente os próprios avisos.
- POST /notificacoes/<id>/ler exige login e CSRF.
- Aviso alheio ou inexistente retorna 404.
- GET não marca leitura.
- Repetição não duplica registros.
- Avisos lidos permanecem disponíveis.

Limitações: sem e-mail, SMS, paginação ou atualização em tempo real. Retirada, devolução e não comparecimento não geram avisos.

## 17. Relatórios administrativos

### Acesso

- GET /relatorios.
- Somente administrador ativo.
- Serviço também verifica permissão.
- Outros perfis recebem 403.
- Usuário inativo perde a sessão.
- Consulta não altera reservas nem conflitos.

### Período

- Duas datas opcionais, preenchidas em conjunto.
- Datas iguais permitidas.
- Data final incluída por inteiro.
- Limite final exclusivo no início do dia seguinte.
- Erros retornam 400 e preservam os campos.

### Indicadores

- Total de reservas.
- Contagem das sete situações.
- Agrupamento por recurso.
- Quantidade de reservas por recurso.
- Quantidade considerada no cálculo de horas.
- Horas previstas por recurso e no total.
- Conflitos evitados.

Recursos inativos aparecem quando possuem reservas. Recursos sem reservas no período não aparecem no agrupamento.

Horas previstas consideram APROVADA, EM_USO e CONCLUIDA. Somente a parte sobreposta ao filtro é somada. O arredondamento acontece após a soma.

O indicador de horas representa tempo reservado, não tempo real de utilização.

### Conflitos evitados

- Implementados no commit d917f69.
- Contam tentativas bloqueadas por outra reserva.
- Operações: CRIACAO, ALTERACAO e APROVACAO.
- Cada tentativa bloqueada gera um registro.
- Repetir a tentativa pode aumentar o contador.
- Várias reservas sobrepostas na mesma tentativa geram somente um registro.
- O filtro considera criado_em, a data do bloqueio.
- Sem datas, conta todo o histórico registrado.
- Zero significa ausência de tentativas registradas no recorte.
- Tentativas anteriores à implantação não são reconstruídas.
- Manutenção, erros de preenchimento e acessos sem permissão não entram na contagem.
- Cancelar a reserva conflitante ou inativar o recurso não apaga o histórico registrado.

Um período pode apresentar conflitos evitados mesmo sem reservas programadas para aquelas datas.

### Verificação

- 21 testes de relatório.
- 16 testes da rota.
- Contagem sem registros e com as três operações.
- Filtro pela data do registro.
- Limites de início e fim do dia.
- Tentativas repetidas.
- Preservação após cancelamento e inativação.
- Consulta repetida sem modificar dados.
- Conferência manual: contador passou de 0 para 1.

Limitações: tempo real de utilização, exportação, paginação e navegador automatizado.

## 18. Integração contínua

**Workflow:** `.github/workflows/testes.yml`

### Execução

- Executa em push e Pull Requests.
- Ubuntu e Python 3.14.
- Permissão declarada: contents: read.
- Limite total do job: 15 minutos.
- Instala dependências de requirements.lock.
- Exige pacotes binários com --only-binary=:all:.
- Verifica hashes com --require-hashes.
- Executa unittest com cobertura de linhas e ramificações.
- Mede os seis módulos da seção 12.
- Mostra relatório no log.
- Gera coverage.json, coverage.xml e htmlcov.
- Publica os relatórios antes da verificação das metas e do Sonar.
- Escreve percentuais separados de linhas e ramificações no resumo.
- Falha se algum teste falhar.
- Falha com linhas abaixo de 80% ou ramificações abaixo de 70%.
- Falha se não houver linhas ou ramificações medidas.
- Obtém histórico completo do Git com fetch-depth: 0.

### Quality Gate

- O scanner executa nos Pull Requests e nos pushes da main.
- Utiliza SONAR_TOKEN armazenado como segredo no GitHub.
- sonar.qualitygate.wait=true faz o scanner aguardar o resultado.
- sonar.qualitygate.timeout=300 limita a espera a cinco minutos.
- Reprovação do Quality Gate ou expiração da espera provoca falha da etapa.
- Push em funcionalidade/login executa os testes, mas pula o scanner; a execução associada ao PR realiza a análise.
- A análise automática do Sonar foi desativada para utilizar a análise pela CI.

A aprovação da execução #107 verifica o cenário positivo da integração. Ainda não foi registrada uma execução deliberadamente reprovada pelo Quality Gate para demonstrar o cenário negativo.

Falha do workflow e bloqueio de merge são controles diferentes. A proteção da main com verificações obrigatórias ainda deve ser conferida.

### Publicação dos relatórios

- Action: actions/upload-artifact@v7.
- Nome do artefato: relatorios-cobertura.
- Retenção configurada: 30 dias.
- Conteúdo: coverage.json, coverage.xml e diretório htmlcov.
- if-no-files-found: error.
- ZIP baixado e conteúdo conferido.
- Relatório HTML acessível por htmlcov/index.html após extração.

Como a publicação ocorre antes das metas e do Sonar, uma reprovação posterior dessas etapas não apaga o artefato já publicado.

A configuração atual não garante relatórios quando os testes falham, pois as etapas seguintes dependem do sucesso das anteriores.

O artefato contém relatórios de cobertura. Não inclui um relatório estruturado da suíte em JUnit XML ou equivalente.

### Dependências

- requirements.txt registra versões exatas.
- requirements.lock foi gerado com pip-tools e contém hashes.
- Alterações de dependências exigem regenerar e revisar o lock.
- O lock é versionado no repositório.
- Tokens não devem ser inseridos em código, documentação ou prints.

A verificação de hashes confirma os arquivos esperados pelo lock. Não substitui a análise de vulnerabilidades das dependências.

### Resultados registrados

| Execuções | Resultado registrado |
| --- | --- |
| #85 e #86 | Aprovadas após vínculo de responsável |
| #87 | Falha por sintaxe YAML |
| #88 e #89 | Aprovadas após correção |
| #92 e #93 | Aprovadas na integração inicial do Sonar |
| #104 e #105 | Aprovadas após configuração de espera pelo Quality Gate |
| #106 | Push do commit de publicação dos relatórios aprovado |
| #107 | Execução do Pull Request aprovada |

A duração total exibida da execução #107 foi de aproximadamente 2 minutos e 2 segundos. Esse tempo inclui outras etapas do job e não equivale à duração isolada dos testes.

## 19. Não comparecimento de materiais

- Exclusivo para MATERIAL.
- Reserva deve estar APROVADA.
- Horário atual igual ou posterior ao término.
- Administrador ativo pode registrar.
- Responsável ativo somente em recurso vinculado.
- Recurso inativo não impede o registro histórico.
- EM_USO exige devolução e não permite não comparecimento.
- Operação manual.
- APROVADA → NAO_COMPARECEU.
- Repetição recusada sem duplicar auditoria.
- Atualização e auditoria na mesma transação.
- Login, perfil, vínculo e CSRF verificados.
- Sucesso remove o cartão da gestão, preservando o histórico.
- Sem notificação dessa operação.

### Banco e migração

- Ação NAO_COMPARECEU acrescentada à auditoria.
- Script atualizar_auditoria_nao_comparecimento.py.
- Backup antes da troca.
- 11 registros preservados na execução histórica.
- Cópia conferida.
- Índices e gatilhos recriados.
- Vínculos da auditoria conferidos.
- Testes específicos desse script ainda pendentes.
- Os testes de atualizar_auditoria.py não comprovam automaticamente o funcionamento deste outro script.

### Evidência manual

Reserva nº 12 do Projetor 01, em 29/10/2026:

- Criação: evento nº 12 às 17h44min15s.
- Aprovação pelo responsável: evento nº 13 às 17h45min05s.
- Não comparecimento pelo administrador: evento nº 14 às 17h54min06s.
- Situação anterior: Aprovada.
- Nova situação: Não compareceu.
- Mensagem de sucesso e remoção do cartão conferidas.
- Rótulo da auditoria conferido manualmente.

### Testes

- 14 métodos no serviço.
- 12 métodos nas rotas.
- Perfis, vínculo, estados, prazo e limite exato.
- Recurso inativo.
- Recusa de sala e professor.
- Repetição.
- Auditoria e rollback.
- CSRF, botão e mensagem.

## 20. Registro de conflitos bloqueados

**Tabela:** conflitos_reservas  
**Commit:** d917f69.

### Dados registrados

- Usuário que realizou a tentativa.
- Recurso solicitado.
- Reserva que causou o bloqueio.
- Operação.
- Início e término solicitados.
- Data e horário do bloqueio.

A finalidade não é armazenada nessa tabela.

### Transação

A sobreposição é consultada dentro de BEGIN IMMEDIATE.

Quando existe conflito:

1. Nenhuma criação, alteração ou aprovação da reserva é gravada.
2. O registro da tentativa bloqueada é inserido.
3. Esse registro é confirmado.
4. O serviço apresenta ValueError com a mensagem de conflito.

O registro é confirmado antes do erro para não ser perdido pelo rollback do tratamento da recusa.

A função de bloqueio é chamada antes de qualquer gravação da operação na reserva.

A refatoração manteve esse tratamento separado da confirmação das operações bem-sucedidas.

### Testes verificados

- Criação bloqueada registra autor, recurso, período, operação e reserva conflitante.
- Reserva, auditoria e notificações preservadas.
- Duas solicitações simultâneas geram uma aceita e uma bloqueada.
- Tentativas repetidas geram registros separados.
- Horários consecutivos não geram conflito.
- Usuário inválido ou inativo não gera registro.
- Erro de finalidade não gera registro.
- Edição bloqueada mantém ambas as reservas.
- Aprovação bloqueada registra o responsável que tentou aprovar.
- Contador e filtro por criado_em verificados no relatório e na rota.

### Verificações adicionais pendentes

- Falha simulada na inserção do registro de conflito.
- Cenários explícitos para todos os tipos de recurso.
- Concorrência por HTTP externo.
- Revisão da transação por outro integrante.

## 21. Próximas verificações

- Revisar o atendimento de cada requisito com o enunciado original.
- Conferir a gestão administrativa de usuários e recursos.
- Revisar o escopo de não comparecimento para outros tipos.
- Testar os demais scripts administrativos e de migração.
- Ampliar conflitos por tipo.
- Testar concorrência entre manutenção e reserva.
- Acrescentar HTTP externo e automação de navegador.
- Elaborar plano e execução de carga.
- Completar README de instalação e fluxos.
- Consolidar evidências TDD ou BDD.
- Documentar arquitetura, riscos e decisões.
- Preservar a identificação da execução de origem de cada artefato.
- Conferir se a análise Sonar corresponde à versão da entrega.
- Conferir proteção da main e verificações obrigatórias.
- Registrar, se realizado, teste controlado de reprovação do Quality Gate.
- Avaliar publicação de relatório estruturado dos testes.
- Concluir revisão de segurança.
- Consolidar registro de defeitos e retestes.
- Obter revisão por outro integrante.
- Preparar relatório final e apresentação.

Concluído nesta etapa:

- Medição de cobertura após as refatorações conferida no artefato.
- Metas de linhas e ramificações atendidas no escopo medido.
- Quality Gate aprovado.
- Cobertura e duplicação do código novo dentro das condições exibidas.
- Espera pelo Quality Gate configurada.
- Relatórios JSON, XML e HTML publicados e baixados.

## 22. Migração da auditoria: testes específicos

**Arquivo:** tests/test_atualizar_auditoria.py  
**Quantidade:** oito métodos de teste.  
**Resultado:** aprovados localmente e incluídos na suíte de 283 testes.

### Cenários verificados

1. Banco inexistente gera erro e não cria arquivo.
2. Ausência da tabela de auditoria gera erro e não cria backup.
3. Estrutura atualizada dispensa migração e backup.
4. Migração preserva registros, cria backup e acrescenta detalhes.
5. Índice e gatilho continuam disponíveis após a migração.
6. Coluna desconhecida impede a migração.
7. Falha por ação inválida reverte a transação e preserva a tabela original.
8. Segunda execução não duplica registros nem backups.

### Isolamento

- Cada teste utiliza pasta e banco temporários.
- Os caminhos do módulo são substituídos durante os testes.
- A conexão SQLite é fechada explicitamente.
- O engine de teste é descartado antes da remoção da pasta.
- As operações verificadas não usam o banco real do projeto.

### Defeito encontrado e reteste

A primeira versão dos testes deixou conexões SQLite abertas.

No Windows, isso provocou PermissionError ao remover os bancos temporários.

A correção acrescentou fechamento explícito das conexões em finally, preservando commit ou rollback da transação.

Após a correção:

- Os oito testes específicos passaram.
- A suíte completa passou com 283 testes.
- A medição mais recente do artefato mostra cobertura combinada de 86,21% para o script.

Esse resultado ainda não cobre todas as falhas possíveis, como interrupção do processo durante a operação ou falta de espaço em disco.

## 23. Análise estática com SonarQube Cloud

### Configuração

- Organização: arthurmrsilva.
- Projeto: Arthurmrsilva_organizacao-recursos.
- Pull Request analisado: nº 1.
- Origem: funcionalidade/login.
- Destino: main.
- Configuração versionada em sonar-project.properties.
- Análise executada pelo GitHub Actions.
- Cobertura Python importada de coverage.xml.
- Diretório tests identificado separadamente como código de teste.
- Scanner configurado para aguardar o Quality Gate.

### Correções no workflow

Na configuração inicial, o Sonar apresentou três apontamentos:

- Duas instalações sem exigência de pacotes binários.
- Uma instalação sem verificação por hashes.

Correções realizadas:

- Fixação das versões das dependências.
- Geração de requirements.lock com hashes.
- Instalação com --only-binary=:all:.
- Instalação com --require-hashes.
- Correção da sintaxe YAML do comando de instalação.

Os três apontamentos deixaram de aparecer na análise posterior.

### Histórico

| Evidência | Resultado |
| --- | --- |
| Primeira cobertura importada | 77,8%; Quality Gate reprovado |
| Commit 4c94cf27 | Quality Gate Passed; cobertura exibida de 82,4%; duplicação exibida de 3,9% |
| Medição intermediária | Duplicação no código novo de 1,68%; Quality Gate Passed |
| Commit exibido 00f01ac3 | Cobertura no código novo de 83,74%; duplicação no código novo de 0,34%; Quality Gate Passed |
| Commit 23078f86 | Cobertura no código novo de 83,74%; duplicação no código novo de 0,0%; Quality Gate Passed |

Os valores históricos foram transcritos das respectivas telas. Não devem ser tratados como medições do mesmo escopo sem conferir a visualização utilizada.

### Resultado mais recente

**Commit exibido:** 23078f86  
**Data da evidência:** 31/10/2026  
**Quality Gate:** Passed

| Indicador | Resultado exibido | Condição exibida |
| --- | --- | --- |
| Novos problemas | 0 | Sem condição indicada no cartão |
| Problemas aceitos | 0 | Sem condição indicada no cartão |
| Cobertura no código novo | 83,74% | Pelo menos 80% |
| Duplicação no código novo | 0,0% | No máximo 3% |
| Security hotspots exibidos | 0 | Sem condição indicada no cartão |
| Riscos de dependências exibidos | 0 | Sem condição indicada no cartão |
| Cobertura estimada após o merge | 82,9% | Indicador distinto do código novo |
| Duplicação estimada após o merge | 0,0% | Indicador distinto do código novo |

A tela informa 923 linhas novas a cobrir para cobertura e aproximadamente 14 mil linhas novas no cartão de duplicação. Esses indicadores utilizam bases diferentes.

### Interpretação e limites

- A evidência atende às condições exibidas de cobertura e duplicação no código novo.
- O resultado pertence ao commit e ao Pull Request indicados.
- Antes da entrega, conferir o hash da versão analisada.
- Não representa uma análise atualizada da main antes do merge.
- Estimativas após o merge não equivalem a uma análise já executada na main.
- Zero novos problemas não comprova ausência de vulnerabilidades.
- Duplicação exibida como 0,0% representa o resultado da ferramenta, de acordo com seus critérios e arredondamento.
- A análise estática não substitui testes de segurança, carga ou navegador.
- Scripts sem cobertura importada continuam exigindo testes específicos.

## 24. Refatorações para redução de duplicação

### Serviço de reservas

**Arquivo:** servico_reservas.py.

Foram extraídos auxiliares para:

- Validar recurso, período e texto do agendamento.
- Consultar usuário ativo.
- Exigir usuário ativo nos fluxos correspondentes.
- Consultar recurso disponível.
- Consultar reserva do próprio usuário.
- Validar alteração ou cancelamento antes do início.
- Localizar reservas sobrepostas.
- Verificar manutenção e registrar bloqueio por conflito.
- Determinar o estado inicial conforme necessidade de aprovação.
- Organizar os dados anteriores e novos da auditoria.

As funções públicas de criação, alteração, cancelamento, avaliação, manutenção, auditoria e notificação foram mantidas.

O reteste local foi informado como aprovado e as execuções posteriores da CI aparecem aprovadas.

No artefato conferido, o serviço apresenta cobertura combinada de 99,21%.

### Templates

Arquivos envolvidos:

- templates/_dados_reserva.html.
- templates/aprovacoes.html.
- templates/materiais.html.

O trecho compartilhado apresenta:

- Nome do recurso.
- Número da reserva.
- Tipo, quando solicitado pela página de aprovação.
- Solicitante.
- Início e término.
- Finalidade.
- Situação.

Cada página mantém seus formulários e suas condições específicas:

- Aprovar ou rejeitar na página de aprovação.
- Retirar, devolver ou registrar não comparecimento na gestão de materiais.
- Campos CSRF.
- Confirmações JavaScript.
- Alertas de atraso e mensagens de indisponibilidade.

### Defeito encontrado na aplicação dos templates

| Campo | Registro |
| --- | --- |
| Problema | Arquivo compartilhado criado com nome diferente do usado no include |
| Efeito observado | Respostas HTTP 500 e 19 falhas na suíte |
| Correção | Nome ajustado para templates/_dados_reserva.html |
| Reteste | Execução local informada como bem-sucedida |
| Verificação posterior | Execuções de CI posteriores aprovadas |
| Situação | Corrigido no escopo verificado |

### Evolução registrada no Sonar

| Etapa | Duplicação no código novo |
| --- | ---: |
| Medição intermediária anterior | 1,68% |
| Evidência seguinte | 0,34% |
| Commit 23078f86 | 0,0% |

Na evidência mais recente, a duplicação estimada após o merge também aparece como 0,0%.

Não foram acrescentadas exclusões de duplicação para os arquivos refatorados nesta etapa.

A comparação deve considerar o commit e o escopo de cada análise.

## Histórico detalhado das evidências

A versão anterior, com as evidências EV01 a EV94, está preservada em [RTM_historico.md](RTM_historico.md).

Esse arquivo é um registro histórico. Para a situação atual do projeto, consulte esta matriz.