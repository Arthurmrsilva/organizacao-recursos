# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 29/10/2026  
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
- Os resultados históricos pertencem às versões em que foram medidos.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e evidências | Situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | Testes de consulta, cancelamento, aprovação, auditoria, manutenção, edição, notificações, relatórios, materiais e não comparecimento | Implementado e verificado nas operações atuais; revisão geral de segurança pendente |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | test_consulta.py e cadastro manual | Implementado e verificado; revisão por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e consulta manual | Implementado e verificado; navegador automatizado pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | Testes de reservas, listagem, cancelamento e edição | Implementado e verificado no escopo atual |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos | Testes de criação, aprovação, disponibilidade e edição | Implementado no mecanismo compartilhado; ampliar cenários explícitos por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas | Duas solicitações simultâneas em test_reservas.py, com uma reserva aceita e um conflito registrado | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Testes de aprovação, vínculo e nova aprovação após edição | Implementado e verificado; interface para vincular responsáveis pendente |
| RF08 | Bloquear recursos em manutenção | Reserva impossível de atender | Testes de manutenção, disponibilidade e edição; consulta manual | Implementado e verificado; concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py, test_materiais_http.py e fluxo manual da reserva nº 11 | Implementado e verificado no serviço, nas rotas e manualmente; navegador automatizado pendente |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, edição, materiais e não comparecimento; rollback e conferência manual | Implementado nas operações atuais; testes específicos de limite e ordenação da consulta pendentes |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py e fluxo manual de leitura | Implementado como avisos internos para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | 21 testes do serviço de relatórios, 16 da rota e conferência manual do contador | Contagens, horas previstas e conflitos evitados implementados e verificados; horas representam tempo reservado, não utilização real |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP e verificações manuais | Parcial: avaliação em diferentes telas e automação de navegador pendentes |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README inicial e esta matriz | Parcial: ampliar instalação, fluxos e interfaces |

A interpretação final de RF12 deve ser conferida com o enunciado: o sistema calcula horas previstas de reserva e não mede o tempo real de utilização.

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

Tentativas bloqueadas por conflito não alteram o estado da reserva. Elas são registradas separadamente em conflitos_reservas.

## 4. Testes automatizados

### Resultado local mais recente

- Data: 29/10/2026.
- Suíte completa: **269 testes aprovados**.
- Resultado: **OK**.
- Duração: **91,264 segundos**.
- Execução com unittest.
- Evidência: imagem do terminal.
- Commit associado: **d917f69**.
- Essa execução não realizou uma nova medição de cobertura.

### Arquivos e escopos

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, autorização, cadastro, persistência e filtros |
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

### Arquivos atualizados na etapa de conflitos

| Arquivo | Métodos de teste |
| --- | ---: |
| test_reservas.py | 13 |
| test_edicao_reservas.py | 24 |
| test_aprovacoes.py | 12 |
| test_relatorios.py | 21 |
| test_relatorios_http.py | 16 |

Os métodos podem conter vários cenários com subTest.

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
- Migrações sem testes automatizados.
- Cobertura Python não abrange HTML, CSS e JavaScript.

## 5. Evidências recentes e histórico de versões

As evidências históricas abaixo resumem as etapas anteriores. Os commits e o histórico Git preservam a evolução do código.

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
| Migração da auditoria | Ação NAO_COMPARECEU acrescentada, backup e 11 registros preservados |
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
| Suíte atual | 269 testes aprovados em 91,264 segundos |
| Implementação dos conflitos | Commit d917f69, nove arquivos, commit e push confirmados |
| CI de d917f69 | Confirmação do resultado ainda pendente nesta atualização |

### Links principais

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Relatórios iniciais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/2ae1f0c)
- [Metas na CI](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4062de2)
- [Não comparecimento](https://github.com/Arthurmrsilva/organizacao-recursos/commit/f1d0af2)
- [Cobertura com 257 testes](https://github.com/Arthurmrsilva/organizacao-recursos/commit/47add5d)
- [Contador de conflitos](https://github.com/Arthurmrsilva/organizacao-recursos/commit/d917f69)

Os prints da entrega devem identificar cenário, data, resultado esperado, resultado observado, requisito e commit, quando aplicável.

A aprovação do workflow não substitui revisão por outro integrante.

## 6. Metas e verificações de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | Última medição anterior aos conflitos: aproximadamente 98%, com 257 testes |
| Cobertura de ramificações | Pelo menos 70% | Última medição anterior aos conflitos: aproximadamente 96%, com 257 testes |
| Cobertura atual | Representar a versão de 269 testes | Nova medição local pendente |
| Rastreabilidade crítica | 100% das regras críticas ligadas a testes e evidências | Consolidar revisão dos cenários críticos |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente na entrega | Verificação completa pendente |
| Testes unitários isolados | Regras sem dependências reais | Ampliação pendente |
| Integração | Persistência e integração das camadas | Verificada no escopo testado |
| Testes em container | Banco com Testcontainers | Pendente |
| Integração externa | WireMock quando aplicável | Sem integração externa; avisos internos adotados para RF11 |
| HTTP em caixa-preta | Acesso externo por HTTP | Pendente |
| Ponta a ponta | Automação no navegador | Pendente |
| Concorrência | Ausência de dupla reserva | Verificada no serviço; ampliar HTTP e manutenção |
| Desempenho | Plano e resultados de carga | Pendente |
| Análise estática | Ferramenta e resultados registrados | Pendente |
| Segurança | Revisão e evidências | Parcial; autenticação, perfis, hash e CSRF implementados |
| Revisão por pares | Revisão de outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gestão de defeitos | Registro, prioridade, correção e reteste | Parcial; consolidar documento |
| Relatório final | Evidências, métricas e decisão de qualidade | Pendente |
| Apresentação | Demonstração e domínio pelo grupo | Pendente |

A confirmação de aceitação de Python e das ferramentas equivalentes às citadas no enunciado permanece pendente de registro.

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

## 8. Aprovação

- Responsável ativo e vinculado ao recurso.
- Aprovação ou rejeição somente de SOLICITADA antes do início.
- Aprovação verifica recurso ativo, manutenção e conflitos.
- Rejeição libera o horário.
- Auditoria e aviso ao solicitante na mesma transação.
- Aprovação bloqueada por outra reserva registra uma tentativa de conflito.
- A tentativa bloqueada mantém os estados e não gera aviso de sucesso.

O vínculo é configurado por script local. Interface administrativa para vincular responsáveis permanece pendente.

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

Pendências: navegador automatizado e revisão por colega.

## 12. Cobertura

### Última medição conferida

- Data: 29/10/2026.
- Ferramenta: coverage.py 7.17.0.
- Execução: 257 testes em 69,538 segundos.
- Linhas: 667 executadas de 684, aproximadamente 98%.
- Ramificações: aproximadamente 96%, conforme HTML.
- Cobertura combinada: 97%.
- JSON atualizado no commit 47add5d.
- HTML gerado e aberto.

Esses valores precedem a implementação do contador de conflitos. Não representam uma nova medição da suíte de 269 testes.

### Histórico

| Versão | Linhas | Ramificações | Combinada |
| --- | --- | --- | --- |
| 103 testes | 89,87% | 85,16% | Medição histórica |
| 213 testes | 93,31% | 90,23% | 92% |
| 257 testes | Aproximadamente 98% | Aproximadamente 96% | 97% |
| 269 testes | Nova medição pendente | Nova medição pendente | Nova medição pendente |

### Escopo

- app.py.
- banco.py.
- servico_reservas.py.
- servico_materiais.py.
- servico_relatorios.py.

Não inclui templates, CSS, JavaScript nem scripts administrativos e de migração.

Cobertura combinada considera linhas e ramificações. Cobertura alta não comprova ausência de defeitos.

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
.\.venv\Scripts\python.exe -m coverage html
```

Regenerar os relatórios após a execução para que representem a versão medida.

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

A migração de detalhes preservou 9 registros com backup. Testes automatizados da migração permanecem pendentes.

## 15. Correção de materiais atrasados

Problema corrigido: EM_USO saía das Ativas após o término, mesmo sem devolução.

- EM_USO permanece em Ativas.
- SOLICITADA e APROVADA dependem de término futuro.
- Histórico usa a condição complementar.
- Aviso de atraso na interface.
- Nenhuma devolução automática.

Evidência: commit 9e94725 e testes de estado, prazo, limite exato e ordenação.

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

Por isso, um período pode apresentar conflitos evitados mesmo sem reservas programadas para aquelas datas.

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

**Workflow:** .github/workflows/testes.yml

- Executa em push e Pull Requests.
- Ubuntu e Python 3.14.
- Instala requirements.txt e coverage.py 7.17.0.
- Executa unittest com cobertura de linhas e ramificações.
- Mede os cinco módulos da seção 12.
- Mostra relatório no log.
- Gera coverage.json.
- Escreve percentuais separados no resumo.
- Falha se algum teste falhar.
- Falha com linhas abaixo de 80% ou ramificações abaixo de 70%.
- Falha se não houver linhas ou ramificações medidas.

O JSON ainda não é publicado como artefato para download.

CI do commit 47add5d informada como aprovada. Resultado da CI de d917f69 ainda pendente de confirmação nesta matriz.

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
- 11 registros preservados.
- Cópia conferida.
- Índices e gatilhos recriados.
- Vínculos da auditoria conferidos.
- Testes automatizados da migração pendentes.

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

- Confirmar a CI do commit d917f69.
- Medir cobertura da versão com 269 testes.
- Revisar o atendimento de cada requisito com o enunciado original.
- Revisar o escopo de não comparecimento para outros tipos.
- Testar migrações.
- Ampliar conflitos por tipo.
- Testar concorrência entre manutenção e reserva.
- Acrescentar HTTP externo e automação de navegador.
- Elaborar plano e execução de carga.
- Completar README de instalação e fluxos.
- Consolidar evidências TDD ou BDD.
- Documentar arquitetura, riscos e decisões.
- Executar análise estática e revisão de segurança.
- Consolidar registro de defeitos e retestes.
- Obter revisão por outro integrante.
- Preparar relatório final e apresentação.

## Histórico detalhado das evidências

A versão anterior, com as evidências EV01 a EV94, está preservada em
[RTM_historico.md](RTM_historico.md).

Esse arquivo é um registro histórico. Para a situação atual do projeto,
consulte esta matriz.

## Atualização de cobertura — 29/10/2026

Esta medição substitui as indicações de cobertura pendente da versão
com 269 testes nas seções anteriores.

- Base funcional: commit d917f69.
- Suíte: 269 testes aprovados em 90,688 segundos.
- Linhas: 680 de 696 — 97,70%.
- Ramificações: 258 de 268 — 96,27%.
- Cobertura combinada exibida: 97%.
- coverage.json e relatório HTML regenerados.
- Escopo: os cinco módulos Python definidos na seção 12.
- Metas de 80% de linhas e 70% de ramificações atendidas localmente.