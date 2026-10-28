# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 28/10/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Esta matriz relaciona os requisitos aos riscos, testes e evidências do projeto.

As tabelas apresentam a situação atual. Os registros históricos preservam os resultados das etapas anteriores.

## 1. Legenda

- **Implementado e verificado:** disponível e verificado no escopo indicado.
- **Parcial:** parte do requisito ou da verificação permanece pendente.
- **Pendente:** implementação ou verificação ainda não realizada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes e cobertura não representam percentual de conclusão do projeto.
- Aprovação dos testes não comprova ausência de defeitos.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e verificações | Situação atual |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Testes de consulta, cancelamento, aprovação, auditoria, manutenção, edição, notificações e relatórios; permissões no serviço de materiais | Parcial: testes HTTP específicos de materiais pendentes |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | Cadastro, validação, autorização e consulta em test_consulta.py | Implementado e verificado; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e verificações manuais | Implementado e verificado com cliente Flask e manualmente; navegador automatizado pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | Testes de reservas, listagem, cancelamento e edição nos serviços e rotas | Implementado e verificado no escopo atual |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos do mesmo recurso | Testes de criação, aprovação, disponibilidade e edição | Parcial: ampliar cenários explícitos de criação e edição por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas para o mesmo período | test_duas_solicitacoes_simultaneas em test_reservas.py | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Testes de aprovação e nova aprovação após edição | Implementado e verificado; interface para vincular responsáveis pendente |
| RF08 | Bloquear recursos em manutenção | Reserva de recurso indisponível | Testes de manutenção, disponibilidade, edição e verificações manuais | Implementado e verificado; concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py e fluxo manual da reserva nº 11 | Implementado e verificado no serviço e manualmente; testes HTTP específicos e navegador pendentes |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, materiais, edição e rollback; conferência manual | Parcial: operações atuais auditadas; ampliar para futuras transições |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py e verificação manual de geração e leitura | Implementado como avisos internos para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | test_relatorios.py, test_relatorios_http.py e verificações manuais | Parcial: contagens e horas previstas implementadas; indicador de conflitos evitados e tempo real de utilização não implementados |
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
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Autor, horário, situações e rollback conjunto testados | Parcial: ampliar para futuras transições |

## 4. Testes automatizados

### Resultado local mais recente

- Data: 28/10/2026.
- Suíte completa: **213 testes aprovados**.
- Resultado: **OK**.
- Duração: **58,742 segundos**, na execução com cobertura.
- Evidência: imagem do terminal apresentada pelo executor.
- Testes específicos do serviço de relatórios: 16 métodos.
- Testes HTTP de relatórios: 12 métodos.
- Os 12 testes HTTP passaram isoladamente em 2,484 segundos.
- Medição atual de cobertura detalhada na seção 12.

Alguns métodos utilizam `subTest` para verificar vários cenários. A contagem de métodos não corresponde necessariamente à quantidade de cenários.

Os testes de serviço com persistência real verificam integração com SQLite. Não devem ser classificados integralmente como testes unitários isolados.

### Arquivos de teste

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização, cadastro, validação, persistência e filtros |
| tests/test_reservas.py | Criação, conflitos, horários consecutivos, concorrência e cancelamento |
| tests/test_minhas_reservas.py | Login, isolamento, lista vazia, distribuição dos filtros, prazo, aviso de atraso e ordenação |
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
| tests/test_notificacoes.py | Geração, destinatário, leitura, isolamento, CSRF, ordenação, escape de HTML e rollback |
| tests/test_relatorios.py | Permissões, datas, contagens por situação, agrupamento, horas previstas, recorte de períodos, arredondamento e indicador indisponível |
| tests/test_relatorios_http.py | Login, perfis, usuário inativo, filtros, erros, preservação dos campos, resultados vazios e consulta sem alteração dos dados |

### Como executar

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Limitações

- Os testes de persistência utilizam bancos SQLite temporários.
- Os testes HTTP atuais utilizam o cliente de testes do Flask.
- A autenticação é simulada em vários testes de rotas; login e senha possuem testes próprios.
- O cliente Flask não executa o JavaScript dos templates.
- Os detalhes de auditoria foram conferidos manualmente na interface.
- Testes externos por HTTP, navegador e carga permanecem pendentes.
- Verificação com banco em container permanece pendente.
- A cobertura atual não inclui templates, CSS, JavaScript nem scripts administrativos e de migração.
- A migração da auditoria foi executada manualmente; seus testes automatizados permanecem pendentes.

## 5. Evidências

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
| EV32 | Medição histórica: 89,87% de linhas e 85,16% de ramificações nos quatro arquivos principais |
| EV33 | Commit 400b119: registro da medição de cobertura |
| EV34 | Commit 6b8d472: pesquisa por disponibilidade com 15 testes; push confirmado |
| EV35 | Suíte de 118 testes aprovada em 48,257 segundos após disponibilidade |
| EV36 | Busca manual excluiu Sala 101 durante manutenção e permitiu período consecutivo |
| EV37 | Busca com término anterior ao início apresentou erro |
| EV38 | Migração da auditoria para detalhes de alteração executada com backup e preservação de 9 registros |
| EV39 | Reserva nº 9: finalidade alterada, mantendo período de 01/11/2026, das 16h às 17h |
| EV40 | Edição da reserva nº 9 para 14:30–15:30 recusada por manutenção; horário original preservado |
| EV41 | Evento nº 10 apresentou autor, horário e finalidade antes e depois da alteração |
| EV42 | Suíte anterior de 118 testes aprovada em 32,354 segundos após mudanças de edição |
| EV43 | 24 testes de edição aprovados; suíte completa de 142 testes informada como aprovada |
| EV44 | Commit 35b5fe5: edição com auditoria e 24 testes; push confirmado |
| EV45 | Actions #53 do commit 35b5fe5 aprovado em 24 segundos |
| EV46 | Actions #54 do Pull Request aprovado em 23 segundos |
| EV47 | 12 testes HTTP de edição aprovados isoladamente |
| EV48 | Commit b9d752d: testes HTTP de edição e RTM; push confirmado |
| EV49 | Actions #55 aprovado em 23 segundos e #56 aprovado em 25 segundos |
| EV50 | Filtros: 10 testes aprovados, incluindo 7 métodos novos |
| EV51 | Suíte completa de 161 testes aprovada em 54,707 segundos |
| EV52 | Commit 9e94725: correção de EM_USO nas Ativas e 7 testes; push confirmado |
| EV53 | Actions #57 e #58 aprovados, conforme imagem apresentada |
| EV54 | Tabela notificacoes criada com sucesso no banco local |
| EV55 | Tela de notificações sem avisos apresentada corretamente |
| EV56 | Edição da reserva nº 9 gerou aviso não lido em 28/10/2026, às 19:10:08 |
| EV57 | Marcação de leitura apresentou situação Lida, preservou o aviso e removeu o botão |
| EV58 | Botão Notificações acrescentado ao menu inicial; funcionamento confirmado pelo executor |
| EV59 | 24 testes de notificações aprovados isoladamente |
| EV60 | Suíte completa de 185 testes informada como aprovada em 28/10/2026 |
| EV61 | Commit 5a18890: notificações internas com leitura e 24 testes; push confirmado e árvore limpa |
| EV62 | GitHub Actions do commit 5a18890 informado como aprovado; número e duração não registrados |
| EV63 | 16 testes do serviço de relatórios aprovados; suíte de 201 testes informada como aprovada |
| EV64 | Consulta manual sem datas apresentou 11 reservas e 4,33 horas previstas |
| EV65 | Filtro de 01/11/2026 a 01/11/2026 apresentou uma reserva da Sala 101 e 1,00 hora prevista |
| EV66 | Período de 02/11/2026 a 01/11/2026 recusado com mensagem; campos preservados e indicadores não apresentados |
| EV67 | 12 testes HTTP de relatórios aprovados em 2,484 segundos |
| EV68 | Commit 2ae1f0c: relatórios administrativos com filtros e testes; push confirmado e árvore limpa |
| EV69 | GitHub Actions do commit 2ae1f0c informado como aprovado; número e duração não registrados |
| EV70 | Execução com cobertura em 28/10/2026: 213 testes aprovados em 58,742 segundos |
| EV71 | Cobertura atual: 93,31% de linhas e 90,23% de ramificações nos cinco módulos medidos |
| EV72 | servico_relatorios.py apresentou 100% de cobertura combinada de linhas e ramificações |
| EV73 | coverage.json atualizado localmente e percentuais separados conferidos no terminal |

### Links

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Materiais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/22014eb)
- [Disponibilidade](https://github.com/Arthurmrsilva/organizacao-recursos/commit/6b8d472)
- [Edição](https://github.com/Arthurmrsilva/organizacao-recursos/commit/35b5fe5)
- [Testes HTTP de edição](https://github.com/Arthurmrsilva/organizacao-recursos/commit/b9d752d)
- [Correção dos filtros](https://github.com/Arthurmrsilva/organizacao-recursos/commit/9e94725)
- [Notificações](https://github.com/Arthurmrsilva/organizacao-recursos/commit/5a18890)
- [Relatórios](https://github.com/Arthurmrsilva/organizacao-recursos/commit/2ae1f0c)

### Organização das evidências

Os prints do pacote de entrega devem informar:

- Cenário e data.
- Resultado esperado e observado.
- Requisito ou regra relacionado.
- Commit associado, quando aplicável.

As evidências históricas mantêm suas contagens originais.

A aprovação do workflow não substitui revisão por outro integrante.

## 6. Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | Atingida no escopo atual medido: 93,31% |
| Cobertura de ramificações | Pelo menos 70% | Atingida no escopo atual medido: 90,23% |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Parcial |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa pendente |
| Testes unitários isolados | Regras sem dependências reais | Pendente de ampliação; testes de serviço utilizam persistência real |
| Testes de integração | Persistência e integração das camadas | Parcial: SQLite temporário e cliente Flask |
| Testes em container | Banco com Testcontainers | Pendente |
| Integrações externas | WireMock quando aplicável | Sem integração externa implementada; avisos internos adotados para RF11 |
| HTTP em caixa-preta | Acesso externo por HTTP | Pendente |
| Testes ponta a ponta | Automação no navegador | Pendente |
| Concorrência | Uma única reserva aceita para o mesmo período | Verificado no serviço; HTTP e carga pendentes |
| TDD ou BDD | Funcionalidade com evidências | RED e GREEN registrados; consolidar documentação |
| CI | Execução em push e Pull Requests | Verificada em etapas anteriores; execução do commit de relatórios informada como aprovada |
| Análise estática | Integração ao SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revisão por pares | Revisão de outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Parcial: correção do filtro documentada; consolidar registro de defeitos |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio pelo grupo | Pendente |

A confirmação de aceitação de Python e das ferramentas equivalentes às citadas no enunciado permanece pendente de registro.

As metas de cobertura foram atingidas nos módulos medidos. Isso não significa que todas as exigências de qualidade ou regras críticas estejam concluídas.

## 7. Histórico — Cancelamento

**Data:** 25/10/2026.

- Consulta das próprias reservas.
- Cancelamento pelo proprietário antes do início.
- Situações permitidas: SOLICITADA e APROVADA.
- Preservação do registro e liberação do período.
- 31 testes aprovados em 9,850 segundos.
- Commit ecb0eb7.

Edição, auditoria e notificações foram acrescentadas posteriormente.

## 8. Histórico — Aprovação

**Data:** 25/10/2026.

- Responsável vinculado ao recurso por script local.
- Aprovação e rejeição das solicitações vinculadas.
- Verificações de perfil, vínculo, prazo, recurso ativo e conflito.
- Temas: administrador azul, responsável roxo e solicitante verde.
- 56 testes aprovados.
- Commits cca4432 e 9946585.
- Actions #27 e #28 aprovados.

A interface para vincular responsáveis continua pendente.

Avisos ao solicitante sobre aprovação e rejeição foram acrescentados em 28/10/2026.

## 9. Auditoria e filtros de reservas

**Implantação inicial:** 25/10/2026.

- Auditoria de criação, cancelamento, aprovação e rejeição.
- Posteriormente ampliada para retirada, devolução e alteração.
- Autor, reserva, ação, horário e situações.
- Gravação na mesma transação da operação.
- Rollback conjunto em caso de falha.
- Consulta dos 100 eventos mais recentes pelo administrador.
- Acesso dos demais perfis bloqueado.
- Resultado histórico inicial: 65 testes aprovados.
- Commit db1e5e8; Actions #37 aprovado.

### Critério atual dos filtros

Atualizado em 28/10/2026:

- **Ativas:** todas as reservas EM_USO, mesmo após o prazo; SOLICITADA e APROVADA somente com término posterior à consulta.
- **Histórico:** reservas que não atendem ao critério de Ativas.
- **Todas:** todas as reservas do usuário conectado.

O encerramento do período não altera automaticamente a situação.

Uma reserva EM_USO permanece ativa até a devolução. Quando o prazo termina, a tela apresenta um aviso de devolução pendente.

### Ordenação

- Ativas: início crescente e ID crescente.
- Histórico e Todas: início decrescente e ID decrescente.

### Limitações da auditoria

- Eventos anteriores à implantação não são reconstruídos.
- Horários seguem o relógio local do servidor.
- Consulta limitada a 100 eventos, sem paginação.
- O nome exibido corresponde ao recurso atual da reserva.
- Em alterações, os códigos anterior e novo ficam nos detalhes.
- Limite e ordenação da auditoria precisam de testes específicos.
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

Autor e data ficam na tabela de manutenção. O cadastro não gera evento na auditoria de reservas.

Pendências: edição e desativação pela interface, manutenção imediata e concorrência específica.

## 11. Histórico — Materiais

**Data:** 26/10/2026.

- Administrador gerencia movimentações.
- Responsável gerencia materiais vinculados.
- Retirada de reserva APROVADA durante o período permitido.
- Bloqueio de recurso inativo, em manutenção ou já em uso.
- Retirada: APROVADA → EM_USO.
- Devolução: EM_USO → CONCLUIDA.
- Devolução permitida após o prazo e com recurso inativo.
- Auditoria das movimentações.
- 17 testes específicos.
- Suíte histórica: 103 testes aprovados em 28,560 segundos.
- Commit 22014eb; Actions #45 e #46 aprovados.

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

Os rótulos Retirada e Devolução foram acrescentados posteriormente.

Pendências: testes HTTP específicos, navegador, não comparecimento e revisão por colega.

## 12. Cobertura de testes

### Medição atual

**Data:** 28/10/2026.  
**Base funcional:** commit 2ae1f0c, antes desta atualização documental.

- Ferramenta: coverage.py, com medição de ramificações habilitada.
- Execução: 213 testes aprovados em 58,742 segundos.
- Escopo: app.py, banco.py, servico_reservas.py, servico_materiais.py e servico_relatorios.py.
- Linhas executadas: **628 de 673 — 93,31%**.
- Ramificações executadas: **231 de 256 — 90,23%**.
- Cobertura combinada exibida no terminal: **92%**, arredondada pela ferramenta.
- Relatório JSON atualizado localmente: coverage.json.
- As metas de 80% de linhas e 70% de ramificações foram atingidas nesse escopo.

| Módulo | Cobertura combinada exibida |
| --- | --- |
| app.py | 89% |
| banco.py | 84% |
| servico_materiais.py | 97% |
| servico_relatorios.py | 100% |
| servico_reservas.py | 95% |
| Total | 92% |

A coluna de cobertura combinada considera linhas e ramificações. Ela não deve ser confundida com o percentual separado de linhas.

A medição não inclui templates, CSS, JavaScript nem scripts administrativos e de migração.

O resultado de 100% em servico_relatorios.py indica que as linhas e ramificações medidas foram executadas. Não comprova ausência de defeitos nem cobertura de todos os valores de entrada possíveis.

O relatório HTML precisa ser regenerado para representar esta execução. Um HTML de execução anterior não comprova os resultados atuais.

### Medição histórica

**Data:** 26/10/2026.

- Ferramenta: coverage.py 7.17.0.
- Execução: 103 testes aprovados em 26,625 segundos.
- Escopo: app.py, banco.py, servico_reservas.py e servico_materiais.py.
- Linhas executadas: 417 de 464 — 89,87%.
- Ramificações executadas: 155 de 182 — 85,16%.
- Relatórios registrados naquela etapa: coverage.json e htmlcov/index.html.
- Commit 400b119.

A medição histórica utilizou uma versão e um escopo diferentes. Seus valores são preservados apenas como histórico.

### Como medir novamente

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios -m unittest discover -s tests -v
```

```powershell
.\.venv\Scripts\python.exe -m coverage report -m
```

```powershell
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
```

Para exibir os percentuais separados:

```powershell
.\.venv\Scripts\python.exe -c "import json; t=json.load(open('coverage.json'))['totals']; print('Linhas: {:.2f}%'.format(100*t['covered_lines']/t['num_statements'])); print('Ramificacoes: {:.2f}%'.format(100*t['covered_branches']/t['num_branches']))"
```

Para gerar o relatório HTML da execução atual:

```powershell
.\.venv\Scripts\python.exe -m coverage html
```

## 13. Pesquisa por disponibilidade

**Data:** 27/10/2026.

- Filtros opcionais de início e término, preenchidos em conjunto.
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
- Sala 101 excluída durante manutenção.
- Período consecutivo permitido.
- Término anterior ao início recusado.

## 14. Edição e detalhes de auditoria

**Data:** 27/10/2026.

### Funcionalidades

- Edição pelo proprietário autenticado.
- Permitida em SOLICITADA ou APROVADA antes do início.
- Alteração de recurso, período e finalidade.
- Validação de usuário ativo, recurso ativo, datas e finalidade.
- Verificação de conflitos e manutenção.
- A própria reserva não é tratada como conflito.
- Recursos restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicitação sem mudança é recusada.
- Edição e auditoria na mesma transação.
- Falha na auditoria desfaz a edição.
- Evento ALTERACAO com dados anteriores e novos.
- Interface apresenta antes e depois.

### Banco e migração

- Coluna detalhes e ação ALTERACAO adicionadas à auditoria.
- Backup criado antes da migração.
- Migração executada com 9 registros preservados.
- Registros antigos permanecem sem detalhes.
- Testes automatizados da migração pendentes.

### Testes

- tests/test_edicao_reservas.py: 24 métodos.
- tests/test_edicao_http.py: 12 métodos.
- Validações, permissões, conflitos, manutenção, nova aprovação, auditoria e rollback.
- Rotas com login obrigatório, isolamento, CSRF e recusas.

### Verificação manual

- Reserva nº 9 aberta com dados preenchidos.
- Finalidade alterada para “Teste de edição da reserva.”
- Tentativa para 01/11/2026, das 14:30 às 15:30, recusada por manutenção.
- Período original das 16h às 17h preservado.
- Evento nº 10 apresentou finalidade anterior e nova, autor e horário.

### Versionamento

- Commit 35b5fe5: edição com auditoria e testes de serviço.
- Actions #53 e #54 aprovados.
- Commit b9d752d: testes HTTP e atualização do RTM.
- Actions #55 e #56 aprovados.

## 15. Correção — Reservas em uso após o prazo

**Data:** 28/10/2026.

### Problema

O filtro Ativas exigia término futuro também para EM_USO. Assim, um material ainda não devolvido aparecia no Histórico após o prazo.

### Correção

- EM_USO permanece em Ativas independentemente do prazo.
- SOLICITADA e APROVADA dependem de término futuro.
- Histórico utiliza o complemento da condição de Ativas.
- A interface apresenta aviso quando EM_USO atinge o término previsto.
- A consulta não altera o estado nem registra uma devolução automática.

### Verificação

- 7 métodos acrescentados a test_minhas_reservas.py.
- Arquivo passou de 3 para 10 métodos.
- Testes de distribuição por estado e prazo.
- Teste do instante exato do término com relógio fixo.
- Testes de aviso, filtro inválido e ordenação.
- Suíte de 161 testes aprovada em 54,707 segundos.
- Commit 9e94725.
- Actions #57 e #58 aprovados.

## 16. Notificações internas

**Data:** 28/10/2026.

### Escopo

Avisos internos persistidos no banco simulam notificações ao dono da reserva.

Não há envio de e-mail, SMS, mensagem externa ou atualização automática em tempo real.

### Eventos implementados

| Operação | Aviso ao dono da reserva |
| --- | --- |
| Criação comum | Reserva criada e aprovada automaticamente |
| Criação restrita ou professor | Solicitação aguardando aprovação |
| Edição comum | Reserva alterada e aprovada |
| Edição restrita ou professor | Solicitação aguardando nova aprovação |
| Cancelamento | Reserva cancelada |
| Aprovação | Reserva aprovada pelo responsável |
| Rejeição | Reserva rejeitada pelo responsável |

Retirada e devolução continuam registradas na auditoria, mas ainda não geram notificações internas.

### Persistência e transação

- Tabela notificacoes.
- Destinatário, reserva, mensagem, data e leitura.
- Avisos novos começam como não lidos.
- Reserva, auditoria e aviso usam a mesma transação.
- Falha na notificação desfaz a operação e a auditoria.
- Operações recusadas não geram avisos de sucesso.
- Avisos anteriores à implantação não são reconstruídos.

### Consulta e leitura

- GET /notificacoes exige autenticação.
- Lista somente os avisos do usuário conectado.
- Ordenação por data decrescente e ID decrescente.
- POST /notificacoes/<id>/ler exige autenticação e CSRF.
- O vínculo com o destinatário faz parte do UPDATE.
- Outros usuários, responsáveis e administradores não marcam avisos alheios.
- Aviso inexistente ou de outra pessoa retorna 404.
- GET não marca leitura.
- Repetir a marcação mantém o mesmo registro.
- Avisos lidos permanecem na lista.
- Botão Notificações disponível para todos os perfis autenticados.

### Testes e evidências

- tests/test_notificacoes.py: 24 métodos.
- Geração dos avisos e destinatário correto.
- Aprovação e rejeição notificam o solicitante.
- Conflito não cria aviso extra.
- Rollback de criação, edição, cancelamento, aprovação e rejeição quando o aviso falha.
- Login, isolamento, CSRF e leitura persistida.
- Repetição da leitura sem duplicação.
- Ordenação e escape de HTML.
- Botão na página inicial para os três perfis.
- Verificação manual de aviso da edição da reserva nº 9.
- Verificação manual de mudança para Lida e remoção do botão.
- Suíte histórica de 185 testes informada como aprovada.
- Commit 5a18890 enviado.
- GitHub Actions informado como aprovado.

### Limitações atuais

- Sem paginação ou filtro de leitura.
- Sem contador de não lidas no menu.
- Sem aviso ao responsável sobre nova solicitação.
- Sem avisos de retirada, devolução ou lembrete de prazo.
- Consulta da página não marca avisos automaticamente.
- Testes de usuário inativo específicos dessas rotas podem ser ampliados.

## 17. Relatórios administrativos

**Data:** 28/10/2026.  
**Commit:** 2ae1f0c.

### Acesso e interface

- Consulta em GET /relatorios.
- Login obrigatório.
- Somente administrador ativo pode consultar.
- Solicitantes e responsáveis recebem HTTP 403.
- Usuário inativo perde a sessão e é redirecionado ao login.
- Serviço também verifica o perfil e a situação do usuário.
- Botão Relatórios acrescentado ao bloco administrativo do menu.
- Filtros de data inicial e final.
- Campos vazios consultam todo o histórico.
- Erros de filtro retornam HTTP 400 e preservam os valores informados.
- Consulta não altera reservas.

### Critério do período

- As duas datas devem ser preenchidas em conjunto.
- Data final não pode ser anterior à inicial.
- O mesmo dia pode ser usado como início e fim.
- O dia final é incluído por inteiro.
- Internamente, o limite final corresponde ao início do dia seguinte.
- Reservas que atravessam o período são consideradas.
- Reservas que apenas encostam nos limites, sem sobreposição, ficam fora.
- Para as horas, somente a parte sobreposta ao período entra no cálculo.

### Indicadores implementados

- Quantidade total de reservas encontradas.
- Quantidade por cada uma das sete situações.
- Agrupamento por recurso.
- Quantidade de reservas por recurso.
- Quantidade de reservas consideradas no cálculo de horas.
- Horas previstas por recurso e no total.
- Recursos inativos também aparecem quando possuem reservas no período.
- Recursos sem reservas no período não aparecem no agrupamento.

### Interpretação das horas

As horas previstas utilizam os períodos das reservas em:

- APROVADA.
- EM_USO.
- CONCLUIDA.

SOLICITADA, REJEITADA, CANCELADA e NAO_COMPARECEU entram nas contagens, mas não acrescentam horas previstas.

As horas são somadas antes do arredondamento para duas casas decimais.

O indicador representa tempo reservado, não tempo real entre retirada e devolução. A situação CONCLUIDA também utiliza o período previsto da reserva.

### Conflitos evitados

O indicador permanece indisponível porque as tentativas recusadas por conflito ainda não são persistidas para essa finalidade.

- O serviço retorna ausência de valor para o indicador.
- A tela apresenta “Indicador ainda indisponível.”
- Ausência de dados não é apresentada como zero.
- Tentativas anteriores não podem ser reconstruídas com precisão a partir das reservas aceitas.
- Registro, definição do período de contagem e testes desse indicador permanecem pendentes.

### Testes

- tests/test_relatorios.py: 16 métodos.
- tests/test_relatorios_http.py: 12 métodos.
- Permissões no serviço e na rota.
- Datas vazias, incompletas, inválidas e invertidas.
- Limite máximo de data.
- Contagem das sete situações.
- Agrupamento de recursos.
- Inclusão de recurso inativo com reservas.
- Recorte de horas nos limites do período.
- Exclusão de períodos sem sobreposição.
- Arredondamento após a soma.
- Resultado vazio.
- Preservação dos campos com erro.
- Consulta sem alteração dos registros.
- Indicador de conflitos indisponível.

### Verificação manual

- Sem datas: 11 reservas e 4,33 horas previstas.
- De 01/11/2026 a 01/11/2026: uma reserva da Sala 101 e 1,00 hora prevista.
- De 02/11/2026 a 01/11/2026: erro compreensível, campos preservados e indicadores não apresentados.
- Tela de relatórios aberta corretamente pelo administrador.

### Versionamento e execução

- Commit 2ae1f0c enviado ao GitHub.
- Árvore de trabalho limpa após o push.
- GitHub Actions informado como aprovado pelo executor.
- Número e duração do workflow não registrados.
- Suíte completa com cobertura: 213 testes aprovados em 58,742 segundos.

### Limitações

- Sem indicador implementado de conflitos evitados.
- Sem medição de tempo real de utilização.
- Sem exportação dos resultados.
- Sem paginação do agrupamento.
- Horários seguem a convenção local utilizada pelo sistema.
- Sem automação de navegador para a tela.
- O requisito RF12 permanece parcial.

## 18. Próximas verificações

- Definir e implementar o registro de conflitos recusados para produzir indicadores verificáveis.
- Implementar registro de não comparecimento.
- Acrescentar testes HTTP de materiais.
- Testar a migração da auditoria.
- Regenerar o relatório HTML de cobertura e organizar as evidências atuais.
- Conferir o escopo e as metas de cobertura no workflow.
- Medir novamente a cobertura após futuras alterações.
- Ampliar instalação e fluxos no README.
- Consolidar evidências TDD ou BDD.
- Completar arquitetura, análise estática, segurança, carga e navegador.
- Consolidar registro de defeitos e retestes.
- Obter revisão por outro integrante.
- Preparar relatório final e apresentação.