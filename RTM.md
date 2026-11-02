# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos  
**Última atualização:** 02/11/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Esta matriz relaciona requisitos, riscos, testes, resultados e limitações conhecidas.

As evidências históricas EV01 a EV94 permanecem em [RTM_historico.md](RTM_historico.md). Os resultados pertencem às versões em que foram medidos.

## 1. Legenda

- **Implementado e verificado:** disponível e verificado no escopo indicado.
- **Parcial:** parte da implementação ou da verificação permanece pendente.
- **Pendente:** implementação ou verificação ainda não realizada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes e cobertura não representam percentual de conclusão.
- Aprovação dos testes não comprova ausência de defeitos.
- Testes com o cliente Flask, testes de navegador e testes de carga possuem escopos diferentes.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e evidências | Situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | test_consulta.py, testes HTTP de permissões, test_seguranca_login.py e login no E2E | Implementado e verificado nos cenários atuais; revisão de segurança permanece parcial |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | test_consulta.py e cadastro manual | Implementado e verificado; revisão por outro integrante pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e consultas manuais | Implementado e verificado; cobertura dos filtros por navegador pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou alteração indevida | Testes de reservas, cancelamento, edição e E2E de criação e cancelamento | Implementado e verificado no escopo atual; edição por navegador pendente |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos | Testes de criação, aprovação, disponibilidade e edição; conflito no E2E | Parcial: ampliar cenários explícitos por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas | Teste de solicitações simultâneas em test_reservas.py | Verificado no serviço com SQLite; concorrência por HTTP pendente |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Testes de aprovação, vínculo e nova aprovação após edição | Implementado; vínculo disponível no cadastro; alteração do vínculo de recursos existentes pela interface pendente |
| RF08 | Bloquear recursos em manutenção | Reserva impossível de atender | Testes de manutenção, disponibilidade e edição; consulta manual | Implementado e verificado; concorrência entre manutenção e reserva pendente |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle dos equipamentos | test_materiais.py, test_materiais_http.py e fluxo manual da reserva nº 11 | Implementado e verificado; navegador automatizado desse fluxo pendente |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Testes de auditoria, edição, materiais, não comparecimento e rollback; conferência no E2E | Implementado nas operações atuais; testes específicos do limite e da ordenação da consulta pendentes |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py, leitura manual e persistência conferida no E2E | Implementado como avisos internos para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | test_relatorios.py, test_relatorios_http.py e consultas manuais | Contagens, horas previstas e conflitos evitados implementados; tempo real de utilização não medido |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP, verificações manuais e um fluxo automatizado no Chromium | Parcial: ampliar avaliação em diferentes telas, navegadores e fluxos |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README, RTM, SEGURANCA.md e performance/README.md | Parcial: revisar instalação e documentar todos os fluxos públicos |

## 3. Regras críticas

| ID | Regra | Risco | Verificação | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Validações no serviço e banco; testes de edição e disponibilidade | Verificado nesses fluxos; ampliar casos explícitos de criação |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Criação, aprovação, edição, disponibilidade, horários consecutivos e E2E | Parcial: ampliar cenários por tipo |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | Concorrência no serviço | Verificado no serviço; concorrência por HTTP pendente |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Manutenção, edição, disponibilidade e consulta manual | Implementado e verificado; concorrência específica pendente |
| RC05 | SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Aprovação e materiais nos serviços e rotas; reserva nº 11 | Verificado para materiais |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Aprovação, cancelamento e não comparecimento; evidências manuais | Verificado no escopo atual; não comparecimento somente para materiais |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Perfil, vínculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Sem exclusão física pela interface; edição e cancelamento após início bloqueados | Verificado nas operações existentes |
| RC09 | Toda mudança de estado gera auditoria | Ausência de rastreabilidade | Criação, alteração, cancelamento, aprovação, rejeição, retirada, devolução e não comparecimento | Verificado nas transições atuais; novas transições exigirão novos testes |

A existência de um teste associado não significa que todas as combinações possíveis da regra foram verificadas.

## 4. Testes automatizados e resultados

### Execuções locais conferidas

| Execução | Resultado |
| --- | --- |
| test_consulta.py | 24 testes aprovados em 16,051 segundos |
| test_edicao_http.py | 12 testes aprovados em 3,490 segundos |
| Suíte completa após os testes adicionais de login | 286 testes aprovados em 121,250 segundos |
| test_seguranca_xss.py, acrescentado posteriormente | Um teste aprovado em 0,382 segundo, com dois cenários |

A execução local completa de 286 testes ocorreu antes da inclusão do teste de XSS.

Após essa inclusão, a quantidade esperada na descoberta de tests é de 287 métodos, desde que nenhum outro teste seja acrescentado ou removido. Esse número não é apresentado como uma nova execução completa local já conferida.

O teste E2E está em e2e e é executado separadamente.

### Arquivos e escopos

| Arquivo | Escopo principal |
| --- | --- |
| tests/test_consulta.py | Login, logout, usuário inativo, CSRF, cadastro, vínculo e filtros |
| tests/test_reservas.py | Criação, sobreposição, horários consecutivos, concorrência e cancelamento |
| tests/test_minhas_reservas.py | Isolamento, filtros, prazo, atraso e ordenação |
| tests/test_cancelamento_http.py | Autenticação, autorização e CSRF |
| tests/test_aprovacoes.py | Aprovação, rejeição, vínculo, prazo, estado e conflitos |
| tests/test_aprovacoes_http.py | Rotas, perfis, CSRF e isolamento |
| tests/test_auditoria.py | Eventos, autor e rollback |
| tests/test_auditoria_http.py | Login, permissões e visibilidade |
| tests/test_manutencoes.py | Períodos, conflitos e bloqueios |
| tests/test_manutencoes_http.py | Permissões, CSRF, cadastro e consulta |
| tests/test_materiais.py | Retirada, devolução, estados, permissões e auditoria |
| tests/test_materiais_http.py | Listagem, isolamento, movimentações e recusas |
| tests/test_disponibilidade.py | Sobreposição, manutenção, limites e filtros combinados |
| tests/test_edicao_reservas.py | Edição, conflitos, aprovação, auditoria, notificações e rollback |
| tests/test_edicao_http.py | Formulário, persistência, auditoria, CSRF e recusas |
| tests/test_notificacoes.py | Geração, destinatário, leitura, isolamento, escape e rollback |
| tests/test_relatorios.py | Contagens, horas previstas, períodos e conflitos evitados |
| tests/test_relatorios_http.py | Acesso, filtros, erros e consulta sem alteração dos registros |
| tests/test_nao_comparecimento.py | Permissões, prazo, estados, repetição e rollback |
| tests/test_nao_comparecimento_http.py | Rota, botão, CSRF, mensagem e persistência |
| tests/test_atualizar_auditoria.py | Migração, backup, preservação, índices, gatilhos e rollback |
| tests/test_seguranca_login.py | Isolamento de CSRF, renovação do token e tentativas de injeção SQL |
| tests/test_seguranca_xss.py | Escape de HTML no nome do recurso em duas páginas |
| e2e/test_fluxo_reserva.py | Login, criação, conflito e cancelamento no Chromium |

Alguns métodos utilizam subTest para verificar mais de um cenário.

Testes de serviço com persistência real também verificam integração com SQLite. Não são integralmente testes unitários isolados.

## 5. Evidências e versões

O histórico EV01 a EV94 permanece em RTM_historico.md.

| Etapa posterior | Evidência registrada |
| --- | --- |
| Registro de conflitos bloqueados | Commit d917f69 |
| Vínculo de responsável no cadastro | Commit 7298034; suíte de 275 testes aprovada |
| Dependências com hashes | Commit d6de95ea |
| Integração inicial do Sonar | Commit f2e3c18 |
| Refatoração do serviço | Commit exibido 00f01ac3 |
| Publicação de relatórios | Commit 23078f86; Actions #106 e #107 aprovados |
| Artefato de cobertura | ZIP conferido com JSON, XML e HTML |
| Teste de navegador | Commit 8544630; execução local aprovada |
| Navegador na CI | Commit 8f4e8b9; Actions #112 e #113 aprovados |
| Desempenho da página de login | Commit bf6822a; Actions #114 e #115 aprovados |
| Segurança do login | Commit 003cc82; push confirmado |
| Escape de HTML | Commit 75c7622; teste local e push confirmados |
| Auditoria de dependências | JSON fornecido com dez dependências e nenhuma vulnerabilidade conhecida reportada |
| Documentação de segurança | SEGURANCA.md e auditoria_dependencias.json; envio informado como concluído |
| Exclusões do ambiente de auditoria | Atualização de .gitignore e sonar-project.properties informada como concluída |

Quando não houver hash, número de execução ou relatório conferido, a evidência não deve receber uma identificação inventada.

### Links

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Sonar do PR nº 1](https://sonarcloud.io/summary/overall?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)

## 6. Metas de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | 97,69% no artefato detalhado conferido |
| Cobertura de ramificações | Pelo menos 70% | 95,39% no mesmo artefato |
| Cobertura no código novo do Sonar | Pelo menos 80% | 83,74% na evidência do commit 23078f86 |
| Duplicação no código novo | No máximo 3% | 0,0% na mesma evidência |
| Quality Gate na CI | Aguardar resultado e falhar em reprovação | Configurado; cenário positivo verificado |
| Relatórios para download | Evidências acessíveis | JSON, XML e HTML publicados |
| Rastreabilidade crítica | Todas as regras críticas com testes e evidências | Revisão final pendente |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente | Revisão final pendente; auditoria de dependências sem achados conhecidos |
| Testes unitários isolados | Regras sem dependências reais | Ampliação pendente |
| Integração | Persistência e camadas | Verificada no escopo testado |
| Banco em container | Testcontainers ou equivalente aceito | Pendente de adequação e execução |
| Integração externa | Simulação quando aplicável | Sem integração externa; avisos internos implementados |
| Navegador | Fluxo ponta a ponta | Um fluxo aprovado localmente e integrado à CI |
| Concorrência | Impedir dupla reserva | Verificada no serviço; HTTP concorrente pendente |
| Desempenho | Plano e resultados | Ensaio exploratório GET /login realizado |
| Análise estática | Ferramenta e resultados | Sonar integrado |
| Segurança | Revisão e evidências | Parcial; testes específicos e auditoria registrados |
| Revisão por pares | Revisão por outro integrante | Pendente |
| Arquitetura | C4, sequências, utility tree, riscos e ADRs | Pendente de consolidação |
| Gestão de defeitos | Registro e retestes | Parcial |
| Relatório final e apresentação | Síntese e demonstração | Pendentes |

A permissão para implementar em Python foi informada pelo responsável pelo desenvolvimento. Isso não comprova aceitação automática de todas as substituições de ferramentas e entregáveis.

## 7. Reservas e cancelamento

- Criação exige usuário e recurso ativos, finalidade e período válidos.
- Início deve estar no futuro.
- Sobreposição é bloqueada em SOLICITADA, APROVADA e EM_USO.
- Horários consecutivos são permitidos.
- Gravações são serializadas com BEGIN IMMEDIATE no SQLite.
- Cancelamento exige proprietário e ocorre antes do início.
- Somente SOLICITADA e APROVADA podem ser canceladas.
- O registro cancelado permanece no banco e libera o horário.
- Não existe exclusão física de reservas pela interface.
- Operações bem-sucedidas geram auditoria e notificação na mesma transação.

Evidências: testes de reservas, cancelamento HTTP, listagem e fluxo E2E.

## 8. Aprovação e vínculo de responsáveis

- Aprovação e rejeição exigem responsável ativo vinculado.
- Reserva deve estar SOLICITADA e ainda não iniciada.
- Aprovação verifica recurso ativo, manutenção e sobreposição.
- Rejeição libera o horário.
- Auditoria e aviso ao solicitante participam da transação.
- Aprovação bloqueada por outra reserva registra conflito evitado.

O cadastro de recurso permite selecionar responsável ativo com perfil RESPONSAVEL. O servidor valida novamente o vínculo no envio.

O vínculo é opcional. Recursos que exigem aprovação podem permanecer aguardando enquanto não houver responsável configurado.

A alteração do vínculo de recursos existentes pela interface permanece pendente.

## 9. Auditoria e filtros

Operações auditadas: criação, alteração, cancelamento, aprovação, rejeição, retirada, devolução e não comparecimento de materiais.

Cada evento registra reserva, autor, ação, horário e situações anterior e nova. Alterações também preservam detalhes anteriores e novos.

Falhas na auditoria provocam rollback da operação correspondente.

A consulta é exclusiva do administrador e apresenta os 100 eventos mais recentes.

### Próprias reservas

- Ativas: EM_USO e reservas SOLICITADA ou APROVADA com término futuro.
- Histórico: complemento da condição de Ativas.
- Todas: todos os registros do usuário conectado.
- Ativas são ordenadas por início e ID crescentes.
- Histórico e Todas utilizam início e ID decrescentes.
- EM_USO permanece em Ativas até a devolução.

Limitações: sem paginação, eventos anteriores não reconstruídos e testes específicos do limite e ordenação da auditoria pendentes.

## 10. Manutenção

- Cadastro e consulta exclusivos do administrador.
- Período futuro e término posterior ao início.
- Motivo obrigatório de até 200 caracteres.
- Sobreposição com manutenção ou reserva ativa bloqueada.
- Criação, edição e aprovação verificam manutenção.
- Horários consecutivos permitidos.
- Proteção CSRF.
- Autor e data registrados na tabela de manutenção.

O cadastro de manutenção não gera evento na auditoria de reservas.

Evidência manual histórica: manutenção da Sala 101 e reserva consecutiva nº 9.

Pendências: edição e desativação pela interface, manutenção imediata e concorrência específica.

## 11. Retirada e devolução de materiais

- Administrador gerencia movimentações.
- Responsável gerencia materiais vinculados.
- Retirada exige reserva APROVADA e período permitido.
- Recurso inativo, em manutenção ou já em uso bloqueia retirada.
- Retirada: APROVADA → EM_USO.
- Devolução: EM_USO → CONCLUIDA.
- Devolução é permitida após o prazo e com recurso inativo.
- Movimentações geram auditoria.
- GET não realiza movimentação.
- Permissões, vínculo, estados e CSRF são verificados.

Evidência manual da reserva nº 11, em 26/10/2026:

- Retirada às 20h17min10s.
- Devolução às 20h18min04s.
- Eventos nº 8 e nº 9 conferidos na auditoria.

Testes em test_materiais.py e test_materiais_http.py. Fluxo de materiais por navegador ainda pendente.

## 12. Cobertura

### Artefato detalhado conferido

| Indicador | Resultado |
| --- | ---: |
| Linhas | 761 de 779 — 97,69% |
| Ramificações | 269 de 282 — 95,39% |
| Cobertura combinada | 97,08% |

Escopo medido:

- app.py
- banco.py
- servico_reservas.py
- servico_materiais.py
- servico_relatorios.py
- atualizar_auditoria.py

Os valores detalhados pertencem ao artefato conferido, não a uma nova medição automática da versão atual.

### Execução local de 286 testes

O terminal apresentou cobertura combinada total arredondada de 97%.

| Módulo | Cobertura combinada exibida |
| --- | ---: |
| app.py | 98% |
| atualizar_auditoria.py | 86% |
| banco.py | 85% |
| servico_materiais.py | 98% |
| servico_relatorios.py | 100% |
| servico_reservas.py | 99% |

A medição Python não abrange HTML, CSS e JavaScript. Os demais scripts administrativos não estão automaticamente cobertos por esse escopo.

### Comandos

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
.\.venv\Scripts\python.exe -m coverage xml
```

```powershell
.\.venv\Scripts\python.exe -m coverage html
```

Cobertura elevada não comprova ausência de defeitos nem verificação de todas as entradas possíveis.

## 13. Pesquisa por disponibilidade

- Início e término opcionais, preenchidos em conjunto.
- Validação de datas e ordem do período.
- Exclusão de recursos com reservas sobrepostas em estados ativos.
- Exclusão de manutenção ativa sobreposta.
- Horários consecutivos permitidos.
- Combinação com tipo, capacidade, localização e competência.
- Consulta de períodos passados permitida.
- Limpeza dos filtros remove o período.

Evidências: test_disponibilidade.py, test_consulta.py e consultas manuais da Sala 101.

## 14. Edição e detalhes de auditoria

- Proprietário ativo e autenticado.
- SOLICITADA ou APROVADA antes do início.
- Alteração de recurso, período e finalidade.
- Recurso ativo, datas e finalidade validados.
- Manutenção e conflitos verificados, excluindo a própria reserva.
- Recursos restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicitação sem mudança é recusada.
- Auditoria ALTERACAO com dados anteriores e novos.
- Reserva, auditoria e notificação na mesma transação.

Evidências: 24 testes de serviço e 12 testes HTTP; alteração manual da reserva nº 9 e evento nº 10.

A migração de detalhes possui testes específicos em test_atualizar_auditoria.py. Esses testes não comprovam automaticamente outros scripts de migração.

## 15. Defeitos e retestes registrados

| Problema | Correção | Evidência de reteste |
| --- | --- | --- |
| Material EM_USO desaparecia de Ativas após o prazo | Filtro passou a manter EM_USO até devolução | Testes de prazo, estados, filtros e ordenação; commit 9e94725 |
| Nome do template compartilhado diferente do include | Nome corrigido para _dados_reserva.html | Reteste local informado como aprovado e CI posterior aprovada |
| Conexões SQLite abertas nos testes de migração impediam limpeza no Windows | Fechamento explícito e descarte dos recursos | Oito testes específicos aprovados |
| Sintaxe YAML impedia início da CI | Comando de instalação corrigido | Actions #88 e #89 aprovados |
| Documento RTM com caracteres e marcação corrompidos | Texto reconstruído em Markdown com acentos corretos | Conferência visual após salvar permanece necessária |

O ensaio de carga sem pausa apresentou falhas de conexão cuja causa permanece não confirmada. Ele não é registrado como defeito corrigido da aplicação.

O registro final de defeitos ainda deve consolidar prioridade, responsável, versão e evidência de encerramento.

## 16. Notificações internas

Avisos persistidos simulam notificações ao dono da reserva.

| Operação | Aviso |
| --- | --- |
| Criação comum | Criada e aprovada automaticamente |
| Criação restrita ou professor | Aguardando aprovação |
| Edição comum | Alterada e aprovada |
| Edição restrita ou professor | Aguardando nova aprovação |
| Cancelamento | Reserva cancelada |
| Aprovação | Aprovada pelo responsável |
| Rejeição | Rejeitada pelo responsável |

- Avisos novos são não lidos.
- Reserva, auditoria e aviso compartilham a transação.
- Falha no aviso desfaz a operação.
- Consulta lista somente os próprios avisos.
- Marcação de leitura exige login e CSRF.
- Aviso inexistente ou alheio retorna 404.
- GET não marca leitura.
- Avisos lidos permanecem na lista.

Limitações: sem e-mail, SMS, paginação, atualização em tempo real ou aviso ao responsável. Retirada, devolução e não comparecimento não geram aviso interno.

## 17. Relatórios e conflitos evitados

Acesso exclusivo do administrador ativo.

### Indicadores

- Total de reservas.
- Contagem das sete situações.
- Agrupamento por recurso.
- Horas previstas por recurso e no total.
- Conflitos evitados registrados.

Horas previstas consideram APROVADA, EM_USO e CONCLUIDA. Somente a parcela sobreposta ao período consultado é somada.

O indicador representa tempo reservado, não tempo real de utilização.

### Conflitos evitados

A tabela conflitos_reservas registra tentativas bloqueadas por sobreposição na criação, edição e aprovação.

Registra usuário, recurso, reserva conflitante, operação, período solicitado e data do bloqueio.

- Filtro considera criado_em, a data da tentativa bloqueada.
- Sem datas, consulta todo o histórico registrado.
- Tentativas repetidas geram registros separados.
- Cancelamento ou inativação posterior não apaga o histórico.
- Manutenção, erros de preenchimento e acessos sem permissão não entram nessa contagem.
- Tentativas anteriores à implementação não são reconstruídas.

A tentativa é confirmada antes da apresentação do erro de conflito. A reserva permanece inalterada.

Evidências: 21 testes de relatório, 16 testes HTTP e conferência manual do contador de zero para um.

Limitações: tempo real de utilização, exportação, paginação e automação de navegador desse relatório.

## 18. Integração contínua e Sonar

**Workflow:** .github/workflows/testes.yml

### Testes e cobertura

- Executa em push e Pull Requests.
- Ubuntu e Python 3.14.
- Instala requirements.lock com hashes e pacotes binários.
- Executa unittest com cobertura de linhas e ramificações.
- Mede os seis módulos da seção 12.
- Falha em erro de teste.
- Exige pelo menos 80% de linhas e 70% de ramificações.
- Falha se não houver linhas ou ramificações medidas.
- Publica coverage.json, coverage.xml e htmlcov.
- Artefato: relatorios-cobertura, retenção de 30 dias.
- Publicação ocorre antes da verificação das metas e do Sonar.

A configuração não garante relatórios após falha dos testes quando as etapas seguintes dependem do sucesso das anteriores.

### Navegador

- Job separado para Chromium.
- Dependências em requirements-e2e.lock com hashes.
- Instalação do Chromium e dependências do sistema.
- Execução com xvfb-run.
- Descoberta de testes no diretório e2e.

### Quality Gate

- Scanner executado em PRs e pushes da main.
- SONAR_TOKEN armazenado como segredo.
- Espera pelo resultado habilitada.
- Limite de espera de 300 segundos.
- Reprovação ou expiração provoca falha da etapa.
- Push da branch funcional executa os testes; análise do PR ocorre na execução associada ao PR.

O cenário positivo foi verificado. Teste controlado do cenário negativo e proteção da main ainda precisam de conferência.

### Evidência detalhada do Sonar

**Commit exibido:** 23078f86  
**Data da evidência:** 31/10/2026  
**Quality Gate:** Passed

| Indicador | Resultado |
| --- | ---: |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Cobertura no código novo | 83,74% |
| Duplicação no código novo | 0,0% |
| Security hotspots exibidos | 0 |
| Riscos de dependências exibidos | 0 |
| Cobertura estimada após merge | 82,9% |
| Duplicação estimada após merge | 0,0% |

Os resultados pertencem ao commit indicado. Conferir a análise da versão final antes da entrega.

Zero problemas na ferramenta não comprova ausência de vulnerabilidades. Estimativas após merge não equivalem a uma análise já executada na main.

## 19. Não comparecimento de materiais

- Exclusivo para MATERIAL.
- Reserva APROVADA.
- Horário atual igual ou posterior ao término.
- Administrador ativo ou responsável ativo vinculado.
- Recurso inativo não impede registro histórico.
- EM_USO exige devolução.
- Operação manual: APROVADA → NAO_COMPARECEU.
- Repetição recusada sem duplicar auditoria.
- Atualização e auditoria na mesma transação.
- Login, perfil, vínculo e CSRF verificados.
- Sucesso remove o cartão da gestão e preserva o histórico.
- Sem notificação interna dessa operação.

### Evidências

- 14 testes de serviço.
- 12 testes HTTP.
- Commit funcional f1d0af2.
- Reserva nº 12 do Projetor 01, em 29/10/2026.
- Criação: evento nº 12, às 17h44min15s.
- Aprovação: evento nº 13, às 17h45min05s.
- Não comparecimento: evento nº 14, às 17h54min06s.

O script atualizar_auditoria_nao_comparecimento.py foi executado com backup e preservação de 11 registros. Seus testes específicos permanecem pendentes.

## 20. Migração e refatorações

### Migração da auditoria

Arquivo de teste: tests/test_atualizar_auditoria.py.

Oito métodos verificam:

1. Banco inexistente sem criação indevida.
2. Ausência da tabela de auditoria.
3. Estrutura atualizada sem migração desnecessária.
4. Preservação dos registros, backup e coluna detalhes.
5. Preservação de índice e gatilho.
6. Recusa de coluna desconhecida.
7. Rollback após ação inválida.
8. Repetição sem duplicar registros ou backups.

Os testes utilizam caminhos e bancos temporários. Conexões são fechadas antes da limpeza.

Não cobrem automaticamente interrupção do processo, falta de espaço ou outros scripts.

### Refatoração do serviço

Auxiliares extraídos para validação de usuário, recurso, período, propriedade, sobreposição, manutenção, estado inicial e detalhes de auditoria.

### Refatoração dos templates

Dados comuns extraídos para templates/_dados_reserva.html e reutilizados em aprovacoes.html e materiais.html.

Formulários, CSRF, ações e condições específicas permanecem em cada página.

As execuções posteriores de CI foram aprovadas. A evidência do Sonar no commit 23078f86 apresentou duplicação no código novo de 0,0%.

## 21. Teste ponta a ponta no navegador

**Arquivo:** e2e/test_fluxo_reserva.py  
**Ferramenta:** Playwright com Chromium.

### Cenário

1. Login com senha incorreta e mensagem de erro.
2. Login válido.
3. Criação de reserva.
4. Conferência da reserva aprovada.
5. Tentativa de reserva sobreposta e mensagem de conflito.
6. Cancelamento com confirmação do navegador.
7. Conferência das listas de Ativas e Histórico.
8. Consulta ao banco de teste para conferir reserva, auditoria, notificações e conflito.

### Ambiente e resultado

- SQLite temporário.
- Servidor HTTP local de teste em porta dinâmica.
- Um método de teste.
- Execução local aprovada em 58,588 segundos.
- Commit do teste: 8544630.
- Integração na CI: 8f4e8b9.
- Actions #112 e #113 aprovados.

O cenário verifica HTTP real e interação com navegador no ambiente local de teste. Não comprova comportamento em infraestrutura externa de produção.

Pendências: ampliar para aprovação, materiais, edição e outros navegadores; registrar capturas ou traces como artefatos.

## 22. Desempenho com JMeter

**Documentação:** performance/README.md  
**Plano:** performance/consulta_login_10usuarios_60s.jmx  
**Commit:** bf6822a.

### Ambiente

- Windows.
- JMeter 5.6.3.
- Java Zulu 25.0.3.
- Flask local na porta 5003, com debug desativado.
- Cliente de carga e servidor na mesma máquina.
- GET /login.
- Execução sem interface gráfica.
- Validações de HTTP 200 e texto Acesso ao sistema.

O cenário consulta a página de login. Não executa autenticação, carregamento de todos os arquivos estáticos ou operações de reserva.

### Execução sem pausa

**Evidência:** performance/carga_login_10usuarios_60s_01.jtl

- Dez usuários configurados.
- Ramp-up de cinco segundos.
- Duração configurada de 60 segundos.
- 17.633 amostras.
- 16.344 respostas HTTP 200.
- 1.289 falhas de conexão, equivalentes a 7,31%.
- Erro: java.net.BindException.
- Mensagem: Address already in use: connect.

A causa não foi confirmada. Não atribuir automaticamente essas falhas à aplicação.

### Execução com pausa

**Evidência:** performance/carga_login_10usuarios_60s_pausa_01.jtl

- Dez usuários configurados.
- Ramp-up de cinco segundos.
- Duração configurada de 60 segundos.
- Constant Timer de 1.000 ms antes de cada requisição.

| Indicador | Resultado |
| --- | ---: |
| Amostras | 570 |
| Respostas HTTP 200 | 570 |
| Falhas | 0 |
| Média | 5,49 ms |
| Mediana | 5 ms |
| Percentil 95 | 8 ms |
| Mínimo | 2 ms |
| Máximo | 38 ms |
| Taxa aproximada no resumo CLI | 9,5 requisições/s |
| Pico de usuários ativos | 10 |

Usuários ativos incluem usuários aguardando o timer e não significam dez requisições simultâneas.

A pausa altera a carga oferecida. O resultado sem erros nesse cenário não comprova correção da causa da execução anterior.

O ensaio foi exploratório, sem critério de aceitação de tempo de resposta definido previamente.

Pendências: critérios de aceitação, repetições controladas e cenários autenticados em ambiente de teste.

## 23. Segurança

**Documento:** SEGURANCA.md  
**Auditoria:** auditoria_dependencias.json.

### Testes de login

Arquivo: tests/test_seguranca_login.py.

- Token CSRF de outra sessão recusado.
- Token renovado após autenticação.
- Token anterior recusado no logout.
- Token atual permite logout.
- Três entradas de tentativa de injeção SQL não autenticam.
- Registros de usuários preservados nos cenários testados.

Commit 003cc82; testes locais aprovados e push confirmado.

### Escape de HTML

Arquivo: tests/test_seguranca_xss.py.

- Nome de recurso contendo uma tag script.
- Verificação da página inicial e do formulário de nova reserva.
- Respostas HTTP 200.
- Conteúdo apresentado com caracteres escapados.
- Ausência da tag original sem escape nesses pontos.

Um teste com dois cenários, aprovado em 0,382 segundo. Commit 75c7622.

O teste verifica escape no HTML retornado. Não executa um conjunto completo de ataques no navegador nem cobre todos os campos.

### Dependências

Auditoria executada com pip-audit sobre requirements.lock, com --require-hashes e --strict.

O JSON fornecido apresenta:

- Dez dependências analisadas.
- Nenhuma vulnerabilidade conhecida reportada.
- Lista de correções vazia.

O resultado depende da base consultada no momento da execução. Não comprova ausência de vulnerabilidades na aplicação.

O ambiente .venv-auditoria foi separado do ambiente principal. Sua exclusão do Git e do Sonar foi configurada.

A auditoria do requirements-e2e.lock não está demonstrada por esse JSON.

### Limitações

- Revisão completa de segurança pendente.
- Configuração de cookies e HTTPS em implantação pendente.
- Limitação de tentativas de login pendente de avaliação.
- Ampliar verificação de XSS para outros campos e páginas.
- Ausência de achados não equivale a um teste de invasão completo.

## 24. Próximas verificações e entrega

- Revisar requisitos e regras críticas com o enunciado.
- Conferir gestão administrativa de usuários e recursos.
- Revisar escopo de não comparecimento para outros tipos.
- Ampliar cenários explícitos de conflito por tipo.
- Testar concorrência por HTTP e entre manutenção e reserva.
- Verificar banco em container ou alternativa aceita.
- Testar os demais scripts administrativos e de migração.
- Ampliar fluxos E2E e evidências de navegador.
- Definir critérios e ampliar os ensaios de desempenho.
- Completar revisão de segurança e dependências de E2E.
- Revisar README de instalação e fluxos.
- Consolidar evidências TDD ou BDD.
- Documentar C4, sequências, utility tree, riscos, trade-offs e ADRs.
- Consolidar registro de defeitos e retestes.
- Obter revisão por outro integrante.
- Conferir proteção da main e verificações obrigatórias.
- Conferir commit e resultado da análise Sonar da versão final.
- Identificar a origem dos artefatos usados na entrega.
- Preparar relatório final e apresentação.

### Cuidados com as evidências

- Identificar cenário, versão, resultado esperado e observado.
- Preservar resultados negativos e suas limitações.
- Não transformar quantidade esperada de testes em execução comprovada.
- Não apresentar métricas históricas como medições da versão atual.
- Não registrar merge, revisão por pares ou aprovação final sem evidência.
- Preservar RTM_historico.md como registro das etapas anteriores.