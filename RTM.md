# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 29/10/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Esta matriz relaciona requisitos, riscos, testes e evidências.

As tabelas descrevem a situação atual. Os registros históricos preservam os resultados das etapas anteriores.

## 1. Legenda

- **Implementado e verificado:** disponível e verificado no escopo indicado.
- **Parcial:** parte da implementação ou da verificação permanece pendente.
- **Pendente:** implementação ou verificação ainda não realizada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes e cobertura não representam percentual de conclusão.
- Aprovação dos testes não comprova ausência de defeitos.
- Testes com o cliente Flask não equivalem à automação de navegador ou a testes externos por HTTP.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e evidências | Situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Testes de consulta, cancelamento, aprovação, auditoria, manutenção, edição, notificações, relatórios, materiais e não comparecimento | Implementado e verificado nas operações atuais; revisão geral de segurança pendente |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | test_consulta.py e cadastro manual | Implementado e verificado; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e consulta manual | Implementado e verificado; navegador automatizado pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | Testes de reservas, listagem, cancelamento e edição | Implementado e verificado no escopo atual |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos | Testes de criação, aprovação, disponibilidade e edição | Parcial: ampliar cenários explícitos por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas | Teste de duas solicitações simultâneas em test_reservas.py | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Testes de aprovação, vínculo e nova aprovação após edição | Implementado e verificado; interface para vincular responsáveis pendente |
| RF08 | Bloquear recursos em manutenção | Reserva impossível de atender | Testes de manutenção, disponibilidade e edição; consulta manual | Implementado e verificado; concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py, test_materiais_http.py e fluxo manual da reserva nº 11 | Implementado e verificado no serviço, nas rotas e manualmente; navegador automatizado pendente |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, edição, materiais e não comparecimento; rollback e conferência manual | Implementado nas operações atuais; testes específicos de limite e ordenação da consulta pendentes |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py e fluxo manual de leitura | Implementado como avisos internos para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | test_relatorios.py, test_relatorios_http.py e consultas manuais | Parcial: contagens e horas previstas implementadas; conflitos evitados e tempo real de utilização indisponíveis |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP e verificações manuais | Parcial: avaliação em diferentes telas e automação de navegador pendentes |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README inicial e esta matriz | Parcial: ampliar instalação, fluxos e interfaces |

## 3. Regras críticas

| ID | Regra | Risco | Verificação | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Validação no serviço e banco; testes explícitos de edição e disponibilidade | Verificado nesses fluxos; ampliar testes explícitos de criação |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Criação, aprovação, edição, disponibilidade e horários consecutivos | Parcial: ampliar cenários por tipo |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | Teste de concorrência no serviço | Verificado no serviço; concorrência por HTTP pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Testes de manutenção, edição e disponibilidade; consulta manual | Implementado e verificado; concorrência específica pendente |
| RC05 | SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Aprovação e materiais nos serviços e rotas; fluxo manual da reserva nº 11 | Implementado e verificado para materiais |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Aprovação, cancelamento e testes de não comparecimento; reserva nº 12 | Verificado no escopo atual; não comparecimento implementado somente para materiais |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Testes de perfil, vínculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Sem exclusão física disponível; edição e cancelamento após início bloqueados | Verificado nas operações existentes |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Criação, alteração, cancelamento, aprovação, rejeição, retirada, devolução e não comparecimento | Verificado nas transições atuais; novas transições exigirão novos testes |

## 4. Testes automatizados

### Resultado local mais recente

- Data: 29/10/2026.
- Suíte completa: **257 testes aprovados**.
- Resultado: **OK**.
- Duração: **84,677 segundos**.
- Execução com unittest, sem uma nova medição local de cobertura nessa execução.
- Evidência: imagem do terminal apresentada pelo executor.
- Commit funcional associado: **f1d0af2**.
- Esse resultado precede o ajuste posterior do rótulo em auditoria.html.

### Evolução recente

| Etapa | Resultado |
| --- | --- |
| Relatórios administrativos | 213 testes em 58,742 segundos, com cobertura |
| Testes HTTP de materiais | 231 testes em 70,820 segundos |
| Serviço de não comparecimento | 14 testes específicos em 3,476 segundos |
| Não comparecimento antes dos testes HTTP específicos | 245 testes em 69,067 segundos |
| Testes HTTP de não comparecimento | 12 testes específicos aprovados, conforme confirmação do executor |
| Suíte completa após os novos testes | 257 testes em 84,677 segundos |

Alguns métodos utilizam `subTest` para verificar vários cenários.

Testes de serviço com persistência real também verificam integração com SQLite. Não devem ser classificados integralmente como testes unitários isolados.

### Arquivos de teste

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização, cadastro, persistência e filtros |
| tests/test_reservas.py | Criação, conflitos, horários consecutivos, concorrência e cancelamento |
| tests/test_minhas_reservas.py | Login, isolamento, filtros, prazo, atraso e ordenação |
| tests/test_cancelamento_http.py | Autenticação, autorização e CSRF no cancelamento |
| tests/test_aprovacoes.py | Aprovação, rejeição, vínculo, prazo, estado e conflito |
| tests/test_aprovacoes_http.py | Rotas, perfis, CSRF e isolamento por responsável |
| tests/test_auditoria.py | Registro das operações, autor e rollback |
| tests/test_auditoria_http.py | Login, permissões e visibilidade do botão |
| tests/test_manutencoes.py | Períodos, conflitos e bloqueio de reservas |
| tests/test_manutencoes_http.py | Permissões, CSRF, cadastro e consulta |
| tests/test_materiais.py | Retirada, devolução, permissões, horários, estados, manutenção e auditoria |
| tests/test_materiais_http.py | Listagem, isolamento, retirada, devolução, permissões, CSRF e recusas |
| tests/test_disponibilidade.py | Períodos, sobreposição, estados, manutenção, limites e filtros combinados |
| tests/test_edicao_reservas.py | Edição, permissões, validações, conflitos, manutenção, aprovação, auditoria e rollback |
| tests/test_edicao_http.py | Formulário, persistência, auditoria, CSRF e recusas |
| tests/test_notificacoes.py | Geração, destinatário, leitura, isolamento, CSRF, ordenação, escape e rollback |
| tests/test_relatorios.py | Permissões, datas, contagens, agrupamento, horas, limites e arredondamento |
| tests/test_relatorios_http.py | Login, perfis, filtros, erros, campos, resultados vazios e consulta sem alteração |
| tests/test_nao_comparecimento.py | Permissões, prazo, estados, recurso inativo, repetição, auditoria e rollback |
| tests/test_nao_comparecimento_http.py | Rota, botão, perfis, CSRF, prazo, repetição, mensagem e persistência |

### Execução

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Limitações

- Persistência testada com bancos SQLite temporários.
- Rotas testadas com o cliente Flask.
- Sessão simulada em vários testes; login e senha possuem testes próprios.
- O cliente Flask não executa JavaScript nem a confirmação dos botões.
- HTTP externo, navegador automatizado e carga permanecem pendentes.
- Verificação com banco em container permanece pendente.
- Scripts de migração ainda não possuem testes automatizados.
- A cobertura medida nos módulos Python não abrange HTML, CSS e JavaScript.

## 5. Evidências

### Histórico preservado

| ID | Evidência |
| --- | --- |
| EV01 | Commit 1ed928d: etapa RED do acesso ao cadastro |
| EV02 | Commit 49b42fe: etapa GREEN do cadastro |
| EV03 | Commit 250f9b2: 16 testes e GitHub Actions |
| EV04 | 16 testes aprovados em 6,098 segundos |
| EV05 | Actions do commit 250f9b2 aprovado em 21 segundos |
| EV06 | Cadastro manual da Sala 202 |
| EV07 | PR nº 1 aberto; revisão por outro integrante pendente |
| EV08 | Commit 940a392: reservas, conflitos, horários consecutivos e concorrência |
| EV09 | 22 testes em 7,883 segundos |
| EV10 | Actions #13 e #14 aprovados |
| EV11 | Commit ecb0eb7: cancelamento; 31 testes em 9,850 segundos |
| EV12 | Reserva nº 3 cancelada e nº 4 aprovada no mesmo período |
| EV13 | Commit 7ae60b7: testes HTTP de cancelamento |
| EV14 | Commit cca4432: aprovação, vínculo e temas por perfil |
| EV15 | Commit 9946585: testes HTTP de aprovação; 56 testes |
| EV16 | Actions #27 e #28 aprovados |
| EV17 | Reserva nº 6 aprovada e cancelada; nº 7 rejeitada |
| EV18 | Commit 1515dcd: auditoria no serviço e testes |
| EV19 | Commit 0fc4cf5: consulta de auditoria e filtros; 62 testes |
| EV20 | Commit 6ac9d65: botão de auditoria |
| EV21 | Conferência manual de autor, horário e situações |
| EV22 | Responsável bloqueado em /auditoria |
| EV23 | Commit db1e5e8: 65 testes; Actions #37 aprovado |
| EV24 | Manutenção: 86 testes em 21,313 segundos |
| EV25 | Manutenção nº 1 da Sala 101 em 01/11/2026, das 14h às 16h; reserva nº 9 aceita a partir das 16h |
| EV26 | Fluxo de materiais da reserva nº 11 em 26/10/2026 |
| EV27 | Retirada às 20:17:10 e devolução às 20:18:04 na auditoria |
| EV28 | 103 testes em 28,560 segundos |
| EV29 | Commit 22014eb: materiais, auditoria e testes; push confirmado |
| EV30 | Actions #45 aprovado em 17 segundos |
| EV31 | Actions #46 aprovado em 23 segundos |
| EV32 | Cobertura histórica: 89,87% de linhas e 85,16% de ramificações |
| EV33 | Commit 400b119: registro da cobertura |
| EV34 | Commit 6b8d472: disponibilidade com 15 testes |
| EV35 | 118 testes em 48,257 segundos |
| EV36 | Consulta excluiu Sala 101 durante manutenção e permitiu período consecutivo |
| EV37 | Período invertido recusado na busca |
| EV38 | Migração para detalhes de alteração com backup e 9 registros preservados |
| EV39 | Finalidade da reserva nº 9 alterada, mantendo 01/11/2026, das 16h às 17h |
| EV40 | Edição para 14:30–15:30 recusada por manutenção; período preservado |
| EV41 | Evento nº 10 com finalidade anterior e nova |
| EV42 | 118 testes em 32,354 segundos após mudanças de edição |
| EV43 | 24 testes de edição; suíte de 142 informada como aprovada |
| EV44 | Commit 35b5fe5: edição, auditoria e testes |
| EV45 | Actions #53 aprovado em 24 segundos |
| EV46 | Actions #54 aprovado em 23 segundos |
| EV47 | 12 testes HTTP de edição aprovados |
| EV48 | Commit b9d752d: testes HTTP e RTM |
| EV49 | Actions #55 em 23 segundos e #56 em 25 segundos |
| EV50 | 10 testes de filtros, incluindo 7 novos |
| EV51 | 161 testes em 54,707 segundos |
| EV52 | Commit 9e94725: EM_USO nas Ativas e testes |
| EV53 | Actions #57 e #58 aprovados |
| EV54 | Tabela notificacoes criada |
| EV55 | Tela sem notificações apresentada corretamente |
| EV56 | Edição da reserva nº 9 gerou aviso em 28/10/2026 às 19:10:08 |
| EV57 | Aviso marcado como Lida e preservado |
| EV58 | Botão Notificações confirmado no menu |
| EV59 | 24 testes de notificações aprovados |
| EV60 | Suíte de 185 testes informada como aprovada |
| EV61 | Commit 5a18890: notificações, leitura e testes |
| EV62 | Actions de 5a18890 informado como aprovado |
| EV63 | 16 testes de relatórios; suíte de 201 informada como aprovada |
| EV64 | Relatório sem datas: 11 reservas e 4,33 horas previstas |
| EV65 | Relatório de 01/11/2026: uma reserva da Sala 101 e 1,00 hora prevista |
| EV66 | Datas invertidas recusadas, com campos preservados |
| EV67 | 12 testes HTTP de relatórios em 2,484 segundos |
| EV68 | Commit 2ae1f0c: relatórios, filtros e testes |
| EV69 | Actions de relatórios informado como aprovado; posteriormente conferidos #63 e #64 verdes |
| EV70 | 213 testes com cobertura em 58,742 segundos |
| EV71 | Medição de 28/10/2026: 93,31% de linhas e 90,23% de ramificações |
| EV72 | servico_relatorios.py com 100% de cobertura combinada nessa medição |
| EV73 | coverage.json gerado e percentuais separados conferidos |

### Evidências acrescentadas nesta atualização

| ID | Evidência |
| --- | --- |
| EV74 | HTML da cobertura gerado e aberto; cinco módulos e total combinado de 92% |
| EV75 | Commit d776bd7: RTM e cobertura com 213 testes; push confirmado |
| EV76 | Actions #65 e #66 aprovados, conforme imagem |
| EV77 | Commit 4062de2: workflow com medição e metas separadas de cobertura |
| EV78 | Execuções do workflow com metas informadas como verdes pelo executor |
| EV79 | 18 testes HTTP de materiais informados como aprovados |
| EV80 | 231 testes aprovados em 70,820 segundos |
| EV81 | Commit 4ca4689: testes HTTP de materiais; push confirmado |
| EV82 | Actions da etapa de materiais informado como aprovado |
| EV83 | Migração para ação NAO_COMPARECEU concluída em 28/10/2026, com backup e 11 registros preservados |
| EV84 | 14 testes do serviço de não comparecimento aprovados em 3,476 segundos |
| EV85 | 245 testes aprovados em 69,067 segundos |
| EV86 | 12 testes HTTP de não comparecimento informados como aprovados |
| EV87 | 257 testes aprovados em 84,677 segundos, em 29/10/2026 |
| EV88 | Commit f1d0af2: não comparecimento com auditoria, migração e testes; push confirmado |
| EV89 | GitHub Actions de f1d0af2 informado como aprovado; número e duração não registrados |
| EV90 | Reserva nº 12 do Projetor 01 criada; evento nº 12 em 29/10/2026 às 17:44:15 |
| EV91 | Reserva nº 12 aprovada pelo Responsável de Recursos; evento nº 13 às 17:45:05 |
| EV92 | Interface confirmou não comparecimento da reserva nº 12 e removeu o cartão da gestão |
| EV93 | Evento nº 14: Administrador do projeto registrou Aprovada → Não compareceu em 29/10/2026 às 17:54:06 |
| EV94 | Rótulo “Não compareceu” apresentado corretamente no título da auditoria após ajuste do template |

O hash e o push do ajuste posterior de auditoria.html ainda não foram conferidos nesta matriz.

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
- [RTM e cobertura](https://github.com/Arthurmrsilva/organizacao-recursos/commit/d776bd7)
- [Metas na CI](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4062de2)
- [Testes HTTP de materiais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4ca4689)
- [Não comparecimento](https://github.com/Arthurmrsilva/organizacao-recursos/commit/f1d0af2)

### Organização das evidências

Os prints da entrega devem identificar cenário, data, resultado esperado, resultado observado, requisito relacionado e commit, quando aplicável.

As contagens históricas são preservadas.

A aprovação do workflow não substitui revisão por outro integrante.

## 6. Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | 93,31% na medição detalhada de 213 testes; CI atual informada como aprovada |
| Cobertura de ramificações | Pelo menos 70% | 90,23% na medição detalhada de 213 testes; CI atual informada como aprovada |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Parcial; consolidar revisão dos cenários críticos |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa pendente |
| Testes unitários isolados | Regras sem dependências reais | Ampliação pendente; serviços utilizam persistência real nos testes |
| Integração | Persistência e integração das camadas | Verificada no escopo testado com SQLite e cliente Flask |
| Testes em container | Banco com Testcontainers | Pendente |
| Integração externa | WireMock quando aplicável | Sem integração externa; notificações internas adotadas para RF11 |
| HTTP em caixa-preta | Acesso externo por HTTP | Pendente |
| Ponta a ponta | Automação no navegador | Pendente |
| Concorrência | Uma única reserva aceita no mesmo período | Verificada no serviço; HTTP e carga pendentes |
| TDD ou BDD | Funcionalidade com evidências | RED e GREEN registrados; consolidar documentação |
| CI | Testes em push e Pull Requests | Implementada, com medição e metas separadas de cobertura |
| Análise estática | SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revisão por pares | Revisão de outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Parcial: correção do filtro registrada; consolidar documento |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio pelo grupo | Pendente |

A confirmação de aceitação de Python e das ferramentas equivalentes às citadas no enunciado permanece pendente de registro.

## 7. Histórico — Cancelamento

**Data:** 25/10/2026.

- Consulta das próprias reservas.
- Cancelamento pelo proprietário antes do início.
- Situações permitidas: SOLICITADA e APROVADA.
- Registro preservado e período liberado.
- 31 testes em 9,850 segundos.
- Commit ecb0eb7.

Edição, auditoria e notificações foram acrescentadas posteriormente.

## 8. Histórico — Aprovação

**Data:** 25/10/2026.

- Responsável vinculado ao recurso por script local.
- Aprovação e rejeição das solicitações vinculadas.
- Verificação de perfil, vínculo, prazo, recurso ativo e conflito.
- Administrador azul, responsável roxo e solicitante verde.
- 56 testes; commits cca4432 e 9946585.
- Actions #27 e #28 aprovados.

A interface para vincular responsáveis permanece pendente.

Avisos ao solicitante foram acrescentados em 28/10/2026.

## 9. Auditoria e filtros de reservas

**Implantação inicial:** 25/10/2026.

Operações auditadas atualmente:

- Criação.
- Alteração.
- Cancelamento.
- Aprovação.
- Rejeição.
- Retirada.
- Devolução.
- Não comparecimento de materiais.

Cada evento registra reserva, autor, ação, horário e situações anterior e nova.

A auditoria usa a mesma transação da operação. Falhas provocam rollback conjunto.

A consulta é exclusiva do administrador e apresenta os 100 eventos mais recentes.

### Filtros das próprias reservas

- **Ativas:** todas em EM_USO; SOLICITADA e APROVADA somente com término futuro.
- **Histórico:** complemento da condição de Ativas.
- **Todas:** todos os registros do usuário conectado.
- Ativas: início e ID crescentes.
- Histórico e Todas: início e ID decrescentes.

O encerramento do período não altera automaticamente a situação.

EM_USO continua em Ativas até a devolução, com aviso após o prazo.

### Limitações

- Eventos anteriores à implantação não são reconstruídos.
- Horários seguem o relógio local do servidor.
- Consulta sem paginação.
- Nome exibido corresponde ao recurso atual da reserva.
- Alterações preservam dados anteriores e novos na coluna detalhes.
- Limite de 100 eventos e ordenação da auditoria precisam de testes específicos.
- Novas operações exigirão novos eventos e testes.

## 10. Histórico — Manutenção

**Data:** 25/10/2026.

- Cadastro e consulta pelo administrador.
- Período futuro e término posterior ao início.
- Motivo obrigatório de até 200 caracteres.
- Bloqueio de sobreposição com manutenção ou reserva ativa.
- Criação e aprovação de reserva bloqueadas durante manutenção.
- Horários consecutivos permitidos.
- Proteção CSRF.
- 12 testes de serviço e 9 de rotas.
- Suíte histórica: 86 testes em 21,313 segundos.

Autor e data ficam na tabela de manutenção. O cadastro não gera evento na auditoria de reservas.

Pendências: edição e desativação pela interface, manutenção imediata e concorrência específica.

## 11. Materiais — Retirada e devolução

**Implantação inicial:** 26/10/2026.

- Administrador gerencia movimentações.
- Responsável gerencia materiais vinculados.
- Retirada de reserva APROVADA durante o período permitido.
- Bloqueio de recurso inativo, em manutenção ou já em uso.
- Retirada: APROVADA → EM_USO.
- Devolução: EM_USO → CONCLUIDA.
- Devolução permitida após o prazo e com recurso inativo.
- Auditoria das movimentações.

### Testes

- test_materiais.py: 17 métodos.
- test_materiais_http.py: 18 métodos.
- Permissões, isolamento por responsável, CSRF, estados e persistência.
- Materiais atrasados em uso continuam visíveis.
- Operação por GET não realiza movimentação.
- Ações inválidas e reservas inexistentes são recusadas.
- Recusas verificadas sem alteração de estado ou criação de auditoria.

Commit dos testes HTTP: 4ca4689.

### Fluxo manual histórico

Reserva nº 11 do Projetor 01, em 26/10/2026, das 20:15 às 21:15:

1. Solicitação aprovada.
2. Material apresentado na gestão.
3. Retirada às 20:17:10 pelo Administrador do projeto.
4. Situação alterada para EM_USO.
5. Devolução às 20:18:04 pelo mesmo administrador.
6. Situação alterada para CONCLUIDA.
7. Cartão removido das movimentações em andamento.
8. Eventos nº 8 e nº 9 conferidos na auditoria.

Suíte histórica inicial: 103 testes em 28,560 segundos.
Commit 22014eb; Actions #45 e #46 aprovados.

Pendências: automação de navegador e revisão por colega.

## 12. Cobertura de testes

### Última medição com percentuais detalhados conferidos

**Data:** 28/10/2026.  
**Base funcional:** commit 2ae1f0c.

- Ferramenta: coverage.py 7.17.0.
- Execução: 213 testes em 58,742 segundos.
- Linhas executadas: **628 de 673 — 93,31%**.
- Ramificações executadas: **231 de 256 — 90,23%**.
- Cobertura combinada exibida: **92%**.
- coverage.json gerado.
- Relatório HTML posteriormente gerado e aberto.

| Módulo | Cobertura combinada |
| --- | --- |
| app.py | 89% |
| banco.py | 84% |
| servico_materiais.py | 97% |
| servico_relatorios.py | 100% |
| servico_reservas.py | 95% |
| Total | 92% |

Esses valores pertencem à versão de 213 testes. Não são apresentados como os percentuais exatos da versão de 257 testes.

### Situação da versão atual

O workflow passou a medir os mesmos cinco módulos e verificar separadamente:

- Pelo menos 80% de linhas.
- Pelo menos 70% de ramificações.

As execuções após f1d0af2 foram informadas como aprovadas pelo executor.

Os percentuais exatos dessa execução ainda precisam ser transcritos do resumo ou de uma nova medição local.

### Escopo e limites

Módulos medidos:

- app.py.
- banco.py.
- servico_reservas.py.
- servico_materiais.py.
- servico_relatorios.py.

Não inclui templates, CSS, JavaScript nem scripts administrativos e de migração.

Cobertura combinada considera linhas e ramificações.

100% em um módulo não comprova ausência de defeitos ou teste de todas as entradas possíveis.

### Medição histórica anterior

**Data:** 26/10/2026.

- 103 testes em 26,625 segundos.
- Quatro módulos, sem servico_relatorios.py.
- Linhas: 417 de 464 — 89,87%.
- Ramificações: 155 de 182 — 85,16%.
- Commit 400b119.

### Como medir

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios -m unittest discover -s tests -v
```

```powershell
.\.venv\Scripts\python.exe -m coverage report -m
```

```powershell
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
```

```powershell
.\.venv\Scripts\python.exe -c "import json; t=json.load(open('coverage.json'))['totals']; print('Linhas: {:.2f}%'.format(100*t['covered_lines']/t['num_statements'])); print('Ramificacoes: {:.2f}%'.format(100*t['covered_branches']/t['num_branches']))"
```

```powershell
.\.venv\Scripts\python.exe -m coverage html
```

Os relatórios precisam ser regenerados após uma nova execução para representar seus resultados.

## 13. Pesquisa por disponibilidade

**Data:** 27/10/2026.

- Início e término opcionais, preenchidos em conjunto.
- Validação de datas e ordem do período.
- Exclusão de recursos com reservas sobrepostas em SOLICITADA, APROVADA ou EM_USO.
- Exclusão de recursos com manutenção ativa sobreposta.
- Horários consecutivos permitidos.
- Combinação com os demais filtros.
- Consulta de períodos passados permitida.
- Atualização da lista sem subir a página.
- Limpeza também remove o período.

Evidências: 15 testes, suíte histórica de 118 em 48,257 segundos, commit 6b8d472 e verificações manuais da Sala 101.

## 14. Edição e detalhes de auditoria

**Data:** 27/10/2026.

- Edição pelo proprietário ativo e autenticado.
- Permitida em SOLICITADA ou APROVADA antes do início.
- Alteração de recurso, período e finalidade.
- Validação de recurso ativo, datas e finalidade.
- Verificação de manutenção e conflitos, excluindo a própria reserva.
- Recursos restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicitação sem mudança é recusada.
- Auditoria ALTERACAO com dados anteriores e novos.
- Edição e auditoria na mesma transação.
- Interface apresenta antes e depois.

### Migração

- Coluna detalhes e ação ALTERACAO acrescentadas.
- Backup e preservação de 9 registros.
- Eventos antigos permanecem sem detalhes.
- Testes automatizados da migração pendentes.

### Verificação

- 24 testes de serviço e 12 de rotas.
- Reserva nº 9 alterada, mantendo 01/11/2026, das 16h às 17h.
- Tentativa de 14:30–15:30 recusada por manutenção.
- Evento nº 10 conferido manualmente.
- Commits 35b5fe5 e b9d752d.
- Actions #53 a #56 aprovados.

## 15. Correção — Materiais em uso após o prazo

**Data:** 28/10/2026.

Problema: EM_USO saía das Ativas após o término, mesmo sem devolução.

Correção:

- EM_USO permanece em Ativas.
- SOLICITADA e APROVADA dependem de término futuro.
- Histórico utiliza a condição complementar.
- Aviso de prazo encerrado na interface.
- Nenhuma devolução automática.

Verificação:

- 7 métodos novos; arquivo passou de 3 para 10.
- Distribuição por estado e prazo.
- Limite exato com relógio fixo.
- Aviso, filtro inválido e ordenação.
- 161 testes em 54,707 segundos.
- Commit 9e94725; Actions #57 e #58 aprovados.

## 16. Notificações internas

**Data:** 28/10/2026.

Avisos persistidos no banco simulam notificações ao dono da reserva.

| Operação | Aviso |
| --- | --- |
| Criação comum | Criada e aprovada automaticamente |
| Criação restrita ou professor | Aguardando aprovação |
| Edição comum | Alterada e aprovada |
| Edição restrita ou professor | Aguardando nova aprovação |
| Cancelamento | Reserva cancelada |
| Aprovação | Aprovada pelo responsável |
| Rejeição | Rejeitada pelo responsável |

### Persistência

- Destinatário, reserva, mensagem, data e leitura.
- Avisos novos não lidos.
- Reserva, auditoria e aviso na mesma transação.
- Falha no aviso desfaz a operação.
- Recusas não geram avisos de sucesso.
- Eventos anteriores não são reconstruídos.

### Rotas

- GET /notificacoes exige login e lista somente os próprios avisos.
- Ordenação por data e ID decrescentes.
- POST /notificacoes/<id>/ler exige login e CSRF.
- UPDATE vinculado ao destinatário.
- Aviso inexistente ou alheio retorna 404.
- GET não marca leitura.
- Repetição não duplica registros.
- Avisos lidos permanecem na lista.

### Verificação e limitações

- 24 testes de geração, destinatário, leitura, isolamento, CSRF, escape e rollback.
- Fluxo manual da reserva nº 9.
- Commit 5a18890; CI informada como aprovada.
- Sem e-mail, SMS, integração externa ou atualização em tempo real.
- Sem paginação, contador de não lidas ou aviso ao responsável.
- Retirada, devolução e não comparecimento ainda não geram notificações.
- Testes específicos de usuário inativo nessas rotas podem ser ampliados.

## 17. Relatórios administrativos

**Data:** 28/10/2026.  
**Commit:** 2ae1f0c.

### Acesso

- GET /relatorios.
- Somente administrador ativo.
- Serviço também verifica permissão.
- Outros perfis recebem 403.
- Usuário inativo é redirecionado ao login.
- Consulta sem alteração das reservas.

### Período

- Duas datas opcionais, preenchidas em conjunto.
- Datas iguais permitidas.
- Data final incluída por inteiro.
- Limite final interno no início do dia seguinte.
- Reservas sobrepostas ao período são consideradas.
- Contato sem sobreposição nos limites é excluído.
- Erros retornam 400 e preservam os campos.

### Indicadores

- Total de reservas.
- Contagem das sete situações.
- Agrupamento por recurso.
- Quantidade de reservas por recurso.
- Quantidade considerada no cálculo de horas.
- Horas previstas por recurso e no total.
- Recursos inativos incluídos quando possuem reservas.
- Recursos sem reservas no período não aparecem.

Horas previstas consideram APROVADA, EM_USO e CONCLUIDA.

As demais situações entram nas contagens, mas não somam horas.

Somente a parte do período sobreposta ao filtro é somada. O arredondamento ocorre depois da soma.

O indicador representa tempo reservado, não tempo real de utilização.

### Conflitos evitados

- Indicador ainda indisponível.
- Tentativas recusadas não são persistidas para essa finalidade.
- Ausência de dados não é apresentada como zero.
- Tentativas anteriores não podem ser reconstruídas com precisão.
- Implementação, definição do período e testes pendentes.

### Verificação

- 16 testes de serviço e 12 de rotas.
- Permissões, datas, limites, contagens, agrupamento e arredondamento.
- Sem datas: 11 reservas e 4,33 horas previstas na base daquele teste manual.
- Em 01/11/2026: uma reserva e 1,00 hora prevista.
- Datas invertidas recusadas.
- Actions #63 e #64 aprovados, conforme imagem posterior.

Limitações: conflitos evitados, tempo real de utilização, exportação, paginação e navegador automatizado.

RF12 permanece parcial.

## 18. Integração contínua e metas de cobertura

**Workflow:** .github/workflows/testes.yml  
**Commit da alteração:** 4062de2.

- Executa em push e Pull Requests.
- Ubuntu e Python 3.14.
- Instala dependências de requirements.txt.
- Instala coverage.py 7.17.0.
- Executa unittest com medição de linhas e ramificações.
- Mede os cinco módulos definidos na seção 12.
- Mostra relatório no log.
- Gera coverage.json na execução.
- Calcula percentuais separados.
- Escreve a tabela no resumo do GitHub Actions.
- Falha se algum teste falhar.
- Falha com linhas abaixo de 80% ou ramificações abaixo de 70%.
- Falha se a medição não contiver linhas ou ramificações.

O workflow gera o JSON durante a execução, mas ainda não publica os relatórios como artefatos para download.

As execuções foram informadas como verdes após a alteração e após a etapa de não comparecimento.

## 19. Não comparecimento de materiais

**Implementação iniciada:** 28/10/2026.  
**Verificação manual:** 29/10/2026.  
**Commit funcional:** f1d0af2.

### Regra implementada

- Exclusiva para recursos do tipo MATERIAL.
- Reserva deve estar APROVADA.
- Horário atual deve ser igual ou posterior ao término.
- Administrador ativo pode registrar.
- Responsável ativo pode registrar somente em recurso vinculado.
- Solicitante e responsável alheio não podem registrar.
- Recurso inativo não impede o registro histórico.
- Reserva EM_USO exige devolução e não pode receber não comparecimento.
- Ação manual; não existe alteração automática ao vencer o período.
- Mudança: APROVADA → NAO_COMPARECEU.
- Repetição é recusada e não duplica auditoria.

### Banco e migração

- Ação NAO_COMPARECEU adicionada à restrição da auditoria.
- Situação NAO_COMPARECEU já existia nas reservas.
- Script atualizar_auditoria_nao_comparecimento.py.
- Backup completo antes da migração.
- Migração manual concluída com 11 registros preservados.
- Cópia dos registros conferida antes da troca de tabela.
- Índices e gatilhos existentes recriados.
- Vínculos da tabela de auditoria conferidos.
- Testes automatizados da migração pendentes.

### Serviço, rota e interface

- Função registrar_nao_comparecimento em servico_materiais.py.
- Atualização e auditoria na mesma transação.
- Falha na auditoria desfaz a mudança.
- POST /materiais/<id>/movimentar com acao=NAO_COMPARECEU.
- Login, perfil e CSRF exigidos.
- Serviço verifica vínculo, prazo e situação.
- Botão aparece para reserva APROVADA com período encerrado.
- Confirmação antes do envio.
- Sucesso apresenta mensagem e remove o cartão da gestão.
- Registro continua no banco e no histórico.
- Auditoria exibe o rótulo “Não compareceu”.
- Não há notificação interna dessa operação.

### Testes

- test_nao_comparecimento.py: 14 métodos.
- test_nao_comparecimento_http.py: 12 métodos.
- Administrador e responsável vinculado.
- Usuário inativo, inexistente, solicitante e responsável alheio.
- Reserva inexistente.
- Antes do término e instante exato do término.
- Bloqueio dos demais estados.
- Recurso inativo.
- Recusa de sala e professor.
- Repetição sem duplicar auditoria.
- Rollback após falha simulada na auditoria.
- CSRF ausente e incorreto.
- Exibição do botão e mensagem de sucesso.
- Preservação dos dados nas recusas.

### Fluxo manual da reserva nº 12

**Recurso:** Projetor 01.

1. Criação pelo Administrador do projeto.
2. Evento nº 12: 29/10/2026 às 17:44:15, aguardando aprovação.
3. Aprovação pelo Responsável de Recursos.
4. Evento nº 13: 29/10/2026 às 17:45:05.
5. Nenhuma retirada registrada.
6. Após o término, botão de não comparecimento utilizado.
7. Mensagem “Não comparecimento da reserva nº 12 registrado!”.
8. Cartão removido da gestão de materiais.
9. Evento nº 14: 29/10/2026 às 17:54:06.
10. Autor: Administrador do projeto.
11. Situação anterior: Aprovada.
12. Nova situação: Não compareceu.
13. Título do evento apresentado como “Não compareceu”.

### Limites

- Implementado somente para materiais.
- Sem registro automático.
- Sem notificação ao solicitante.
- Sem automação de navegador.
- Migração ainda sem testes automatizados.
- Ajuste posterior do rótulo do template verificado manualmente; hash e push ainda não conferidos nesta atualização.

## 20. Próximas verificações

- Confirmar commit e push do ajuste de auditoria.html.
- Registrar os percentuais exatos da cobertura da versão atual.
- Atualizar os relatórios locais de cobertura quando necessário.
- Implementar registro de conflitos recusados e indicador verificável.
- Revisar o escopo de não comparecimento para outros tipos, conforme enunciado.
- Testar as migrações da auditoria.
- Ampliar cenários explícitos de conflitos por tipo.
- Testar concorrência entre manutenção e reserva.
- Acrescentar HTTP externo, navegador e carga.
- Completar README de instalação e fluxos.
- Consolidar evidências TDD ou BDD.
- Completar arquitetura, análise estática e revisão de segurança.
- Consolidar registro de defeitos e retestes.
- Obter revisão por outro integrante.
- Preparar relatório final e apresentação.