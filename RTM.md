# Matriz de Rastreabilidade — RTM

**Projeto:** Organização de Recursos

**Última atualização:** 02/11/2026

**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

**Versão dos testes conferidos:** 67b3d00.

**Último Sonar conferido:** 02737a6.

Esta matriz relaciona requisitos, riscos, testes, resultados e limitações.

As evidências históricas EV01 a EV94 permanecem em [RTM_historico.md](RTM_historico.md). Cada resultado pertence à versão em que foi observado.

## 1. Legenda

- **Implementado e verificado:** disponível e verificado no escopo indicado.
- **Parcial:** implementação ou verificação ainda incompleta.
- **Pendente:** sem conclusão demonstrada.
- Testes planejados não representam resultados aprovados.
- Quantidade de testes e cobertura não representam percentual de conclusão.
- Aprovação dos testes não comprova ausência de defeitos.
- Cliente Flask, HTTP real, navegador e carga possuem escopos diferentes.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e evidências | Situação |
| --- | --- | --- | --- | --- |
| RF01 | Autenticação e autorização por perfil | Acesso indevido | test_consulta.py, testes HTTP de permissões, test_seguranca_login.py e login no Chromium | Implementado e verificado nos cenários atuais; revisão completa de segurança pendente |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inválidos | test_consulta.py e cadastro manual | Implementado e verificado; revisão por outro integrante pendente |
| RF03 | Pesquisa por tipo, capacidade, localização, competência e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e consultas manuais | Implementado e verificado; ampliar filtros por navegador |
| RF04 | Criar, alterar e cancelar reservas | Alteração indevida ou reserva incorreta | Testes de reservas, cancelamento, edição e E2E | Implementado e verificado no escopo atual; edição por navegador pendente |
| RF05 | Detectar sobreposição, inclusive na agenda do professor | Dois usos simultâneos | Criação, aprovação, disponibilidade, edição, conflito no E2E e concorrência HTTP | Parcial: ampliar cenários explícitos de sobreposição de reservas por tipo |
| RF06 | Impedir dupla reserva simultânea | Duas solicitações aceitas | test_reservas.py e teste_concorrencia_http.py | Verificado no serviço e no cenário HTTP concorrente; não representa teste amplo de carga |
| RF07 | Exigir aprovação para recursos restritos | Uso sem autorização | Aprovação, vínculo e nova aprovação após edição | Implementado; vínculo no cadastro; alteração de vínculo de recurso existente pela interface pendente |
| RF08 | Bloquear recursos em manutenção | Reserva impossível de atender | Manutenção, disponibilidade, edição e test_concorrencia_manutencao.py | Verificado, incluindo disputa no serviço para SALA, PROFESSOR e MATERIAL |
| RF09 | Registrar retirada e devolução de materiais | Perda de controle | test_materiais.py, test_materiais_http.py e reserva manual nº 11 | Implementado e verificado; E2E desse fluxo pendente |
| RF10 | Manter histórico auditável | Mudanças sem rastreio | Auditoria, edição, materiais, não comparecimento, rollback, E2E e concorrência HTTP | Implementado nas operações atuais; testes específicos do limite e ordenação da consulta pendentes |
| RF11 | Notificação simulada ou integração externa | Usuário não informado | test_notificacoes.py, leitura manual, E2E e concorrência HTTP | Avisos internos implementados para criação, edição, cancelamento, aprovação e rejeição |
| RF12 | Relatórios de utilização, horas e conflitos evitados | Indicadores incorretos | test_relatorios.py, test_relatorios_http.py e consultas manuais | Contagens, horas previstas e conflitos evitados implementados; tempo real não medido |
| RF13 | Interface responsiva e erros compreensíveis | Dificuldade de uso | Testes HTTP, verificações manuais e fluxo Chromium | Parcial: ampliar telas, navegadores e fluxos |
| RF14 | Documentação da API ou dos fluxos públicos | Dificuldade de instalar e utilizar | README, RTM, arquitetura, plano, segurança e relatório de qualidade | Documentada; conferência final da instalação e correspondência com os fluxos pendente |

## 3. Regras críticas

| ID | Regra | Risco | Verificação | Situação |
| --- | --- | --- | --- | --- |
| RC01 | Término posterior ao início | Período inválido | Validação no serviço e banco; edição e disponibilidade | Verificado nesses fluxos; ampliar casos explícitos de criação |
| RC02 | Mesmo recurso sem sobreposição | Conflito de utilização | Criação, aprovação, edição, disponibilidade, horários consecutivos e E2E | Parcial: ampliar cenários de reservas por tipo |
| RC03 | Solicitações simultâneas com uma única aceita | Dupla reserva | Concorrência no serviço e teste_concorrencia_http.py | Verificado nos cenários executados |
| RC04 | Recurso em manutenção indisponível | Reserva impossível de atender | Manutenção, edição, disponibilidade e disputa entre manutenção e reserva nos três tipos | Verificado no serviço; disputa manutenção/reserva por HTTP não demonstrada |
| RC05 | SOLICITADA → APROVADA → EM_USO → CONCLUIDA | Estado inconsistente | Aprovação e materiais nos serviços e rotas; reserva nº 11 | Verificado para materiais |
| RC06 | REJEITADA, CANCELADA e NAO_COMPARECEU | Histórico incorreto | Aprovação, cancelamento e não comparecimento | Verificado no escopo atual; não comparecimento somente para materiais |
| RC07 | Somente responsável vinculado aprova recurso restrito | Aprovação indevida | Perfil, vínculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas não podem ser apagadas | Perda de histórico | Ausência de exclusão física pela interface; edição e cancelamento após início bloqueados | Verificado nas operações existentes |
| RC09 | Toda mudança de estado gera auditoria | Falta de rastreabilidade | Criação, alteração, cancelamento, aprovação, rejeição, retirada, devolução e não comparecimento | Verificado nas transições atuais |

As nove regras possuem verificações associadas. Isso não equivale à revisão final de todas as combinações exigidas pelo enunciado.

## 4. Resultados automatizados

### Resultado de referência

**GitHub Actions #146 — commit 67b3d00 — evento push.**

| Verificação | Resultado |
| --- | --- |
| Suíte principal com cobertura | 288 testes aprovados em 15,349 segundos |
| Concorrência por HTTP | Aprovada, executada separadamente |
| Fluxo Chromium | Aprovado em job separado |
| Workflow completo | Success em 59 segundos |
| Artefatos | Um artefato exibido no resumo |

Os 288 métodos da suíte principal não incluem o método HTTP separado nem o método de navegador.

Alguns métodos utilizam subTest e verificam várias situações.

### Execuções locais preservadas

| Execução | Resultado |
| --- | --- |
| test_consulta.py | 24 testes em 16,051 segundos |
| test_edicao_http.py | 12 testes em 3,490 segundos |
| Suíte antes do teste adicional de XSS | 286 testes em 121,250 segundos |
| Escape de HTML | Um teste em 0,382 segundo, com dois cenários |
| Fluxo Chromium | Um teste em 20,869 segundos |
| Concorrência HTTP | Um teste em 3,731 segundos |
| Suíte inicial em Docker | 287 testes em 186,330 segundos |
| Docker após ajuste de segurança | 287 testes em 180,651 segundos |
| Concorrência manutenção/reserva | Um teste em 1,762 segundo, com três cenários |

A execução Docker de 287 testes precede a inclusão do novo teste de manutenção/reserva.

## 5. Arquivos de teste

| Arquivo | Escopo |
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
| tests/test_concorrencia_manutencao.py | Disputa entre manutenção e reserva para os três tipos |
| tests/test_materiais.py | Retirada, devolução, estados, permissões e auditoria |
| tests/test_materiais_http.py | Listagem, isolamento, movimentações e recusas |
| tests/test_disponibilidade.py | Sobreposição, manutenção, limites e filtros combinados |
| tests/test_edicao_reservas.py | Edição, conflitos, aprovação, auditoria, notificações e rollback |
| tests/test_edicao_http.py | Formulário, persistência, auditoria, CSRF e recusas |
| tests/test_notificacoes.py | Geração, destinatário, leitura, isolamento, escape e rollback |
| tests/test_relatorios.py | Contagens, horas previstas, períodos e conflitos evitados |
| tests/test_relatorios_http.py | Acesso, filtros, erros e consulta sem alteração |
| tests/test_nao_comparecimento.py | Permissões, prazo, estados, repetição e rollback |
| tests/test_nao_comparecimento_http.py | Rota, botão, CSRF, mensagem e persistência |
| tests/test_atualizar_auditoria.py | Migração, backup, preservação, índices, gatilhos e rollback |
| tests/test_seguranca_login.py | CSRF, renovação do token e tentativas de injeção SQL |
| tests/test_seguranca_xss.py | Escape de HTML em duas páginas |
| teste_concorrencia_http.py | Duas sessões concorrentes por HTTP e registros persistidos |
| e2e/test_fluxo_reserva.py | Login, criação, consulta, conflito, cancelamento e histórico |

Testes com persistência temporária verificam integração com SQLite. Não são integralmente testes unitários isolados.

## 6. Evidências e versões

EV01 a EV94 permanecem em RTM_historico.md.

| Etapa | Identificação |
| --- | --- |
| Registro de conflitos bloqueados | d917f69 |
| Vínculo de responsável no cadastro | 7298034 |
| Dependências com hashes | d6de95ea |
| Integração inicial do Sonar | f2e3c18 |
| Refatoração do serviço | 00f01ac3 |
| Publicação de relatórios | 23078f86; Actions #106 e #107 |
| Teste inicial de navegador | 8544630 |
| Navegador na CI | 8f4e8b9; Actions #112 e #113 |
| Desempenho de GET /login | bf6822a |
| Segurança do login | 003cc82 |
| Escape de HTML | 75c7622 |
| Correção de acentos do histórico | b8b1de9 |
| Arquitetura | c13ef46 |
| Atualização do README | 4ccb05e |
| Registro de defeitos | cab70cc |
| Plano de testes | e97a0a1 |
| Relatório inicial | f0b57ca |
| Concorrência HTTP | 7cb6a29 |
| Workflow HTTP e arquivos Docker | 73a556e |
| Segurança do Docker e classificação do teste no Sonar | 02737a6 |
| Auditoria das dependências de E2E | 98d26d5 |
| Concorrência entre manutenção e reserva | 67b3d00 |
| Relatório atualizado com os resultados | 4da131b |

Não atribuir hashes ou números de execução sem evidência.

## 7. Metas de qualidade

| Item | Meta ou exigência | Situação |
| --- | --- | --- |
| Linhas | Pelo menos 80% | 97,69% na execução #146 |
| Ramificações | Pelo menos 70% | 95,74% na execução #146 |
| Código novo no Sonar | Pelo menos 80% | 83,8% no commit 02737a6 |
| Duplicação no código novo | No máximo 3% | 0,0% no commit 02737a6 |
| Quality Gate | Aprovação na versão analisada | Aprovado em 02737a6; conferir versão final |
| Artefatos | Relatórios acessíveis | JSON, XML e HTML publicados |
| Rastreabilidade crítica | Regras associadas a verificações | Associações registradas; revisão final pendente |
| Defeitos e vulnerabilidades críticas | Nenhum conhecido pendente | Revisão final pendente; auditorias Python sem achados conhecidos |
| Testes isolados | Regras sem dependências reais | Ampliação pendente |
| Integração | Persistência e camadas | Verificada no escopo executado |
| Container | Ambiente de execução isolado | Suíte com SQLite executada em Docker |
| Testcontainers | Ferramenta ou alternativa aceita | Ainda não demonstrado especificamente |
| Integração externa | Simulação quando aplicável | Sem integração externa; avisos internos adotados |
| Navegador | Fluxo ponta a ponta | Fluxo principal aprovado no Chromium |
| Concorrência de reservas | Uma única solicitação aceita | Verificada no serviço e por HTTP |
| Concorrência manutenção/reserva | Não aceitar ambas no mesmo período | Verificada no serviço para os três tipos |
| Desempenho | Plano, critérios e resultados | Ensaios exploratórios; critérios prévios pendentes |
| Segurança | Revisão e evidências | Parcial |
| Arquitetura | C4, sequências, utility tree, riscos e ADRs | Documento consolidado; revisão pendente |
| Defeitos | Registro e retestes | Documento consolidado; revisão pendente |
| Relatório final | Síntese das evidências | Documento atualizado; conferência final pendente |
| Revisão por pares | Revisão real de outro integrante | Reservada para etapa posterior |
| Apresentação | Demonstração e domínio pelo grupo | Preparação pendente |

A permissão informada para utilizar Python não comprova aceitação automática de todas as substituições de ferramentas.

## 8. Reservas e cancelamento

- Usuário e recurso ativos.
- Finalidade e período válidos.
- Início no futuro.
- Sobreposição bloqueada em SOLICITADA, APROVADA e EM_USO.
- Horários consecutivos permitidos.
- Escritas serializadas com BEGIN IMMEDIATE no SQLite.
- Cancelamento pelo proprietário antes do início.
- Somente SOLICITADA e APROVADA podem ser canceladas.
- Registro cancelado preservado e horário liberado.
- Sem exclusão física pela interface.
- Operações bem-sucedidas geram auditoria e aviso na mesma transação.

Evidências: testes de reservas, cancelamento HTTP, listagem, E2E e concorrência HTTP.

## 9. Aprovação e responsáveis

- Responsável ativo e vinculado.
- Reserva SOLICITADA e ainda não iniciada.
- Aprovação verifica recurso ativo, manutenção e sobreposição.
- Rejeição libera o horário.
- Auditoria e aviso participam da transação.
- Conflito com outra reserva registra tentativa bloqueada.

O cadastro permite selecionar responsável ativo com perfil RESPONSAVEL. O servidor valida o vínculo.

O vínculo é opcional. Recursos que exigem aprovação podem aguardar enquanto não houver responsável configurado.

Alterar o vínculo de recurso existente pela interface permanece pendente.

## 10. Auditoria e filtros

Operações auditadas:

- Criação e alteração.
- Cancelamento.
- Aprovação e rejeição.
- Retirada e devolução.
- Não comparecimento de materiais.

Cada evento registra reserva, autor, ação, horário e situações anterior e nova. Alterações preservam detalhes anteriores e novos.

Falhas provocam rollback da operação correspondente.

A consulta é exclusiva do administrador e apresenta os 100 eventos mais recentes.

### Próprias reservas

- Ativas: EM_USO e SOLICITADA ou APROVADA com término futuro.
- Histórico: complemento da condição de Ativas.
- Todas: registros do usuário conectado.
- Ativas: início e ID crescentes.
- Histórico e Todas: início e ID decrescentes.
- EM_USO permanece em Ativas até a devolução.

Limitações: sem paginação, sem reconstrução de eventos anteriores e testes específicos do limite e ordenação da auditoria pendentes.

## 11. Manutenção

- Cadastro e consulta pelo administrador.
- Período futuro e término posterior ao início.
- Motivo obrigatório de até 200 caracteres.
- Sobreposição com manutenção ou reserva ativa bloqueada.
- Criação, edição e aprovação de reserva verificam manutenção.
- Horários consecutivos permitidos.
- Proteção CSRF.
- Autor e data na tabela de manutenção.

O cadastro não gera evento na auditoria de reservas.

A disputa entre manutenção e reserva foi testada no serviço para SALA, PROFESSOR e MATERIAL. O teste exige exatamente uma operação aceita e uma recusada.

Também verifica datas, estado inicial e, quando a reserva vence, auditoria e notificação.

Evidências: teste local em 1,762 segundo e suíte aprovada na execução #146.

Pendências: edição e desativação pela interface, manutenção imediata e disputa manutenção/reserva por HTTP.

## 12. Materiais e não comparecimento

### Retirada e devolução

- Administrador ou responsável vinculado.
- Retirada exige APROVADA e período permitido.
- Recurso inativo, em manutenção ou já em uso bloqueia retirada.
- APROVADA → EM_USO.
- EM_USO → CONCLUIDA.
- Devolução permitida após o prazo e com recurso inativo.
- Auditoria das movimentações.
- GET não realiza movimentações.
- Login, perfil, vínculo, estado e CSRF verificados.

Reserva manual nº 11, em 26/10/2026:

- Retirada às 20h17min10s.
- Devolução às 20h18min04s.
- Eventos nº 8 e nº 9 conferidos.

### Não comparecimento

- Exclusivo para MATERIAL.
- Reserva APROVADA.
- Horário igual ou posterior ao término.
- Administrador ativo ou responsável ativo vinculado.
- Recurso inativo não impede registro histórico.
- EM_USO exige devolução.
- APROVADA → NAO_COMPARECEU.
- Operação manual, sem alteração automática pelo prazo.
- Repetição recusada sem duplicar auditoria.
- Atualização e auditoria na mesma transação.
- Sem notificação interna dessa operação.

Evidências: 14 testes de serviço, 12 HTTP e commit f1d0af2.

Reserva nº 12, em 29/10/2026:

- Criação: evento nº 12, às 17h44min15s.
- Aprovação: evento nº 13, às 17h45min05s.
- Não comparecimento: evento nº 14, às 17h54min06s.

O script atualizar_auditoria_nao_comparecimento.py preservou 11 registros com backup. Seus testes específicos permanecem pendentes.

O fluxo de materiais por navegador ainda precisa ser ampliado.

## 13. Cobertura

### Resultado atual conferido

**Actions #146 — commit 67b3d00.**

| Métrica | Resultado |
| --- | ---: |
| Linhas | 97,69% |
| Ramificações | 95,74% |

Módulos medidos:

- app.py
- banco.py
- servico_reservas.py
- servico_materiais.py
- servico_relatorios.py
- atualizar_auditoria.py

A medição utiliza a suíte principal. HTTP separado e Chromium não são somados a esse relatório.

O artefato histórico anteriormente conferido apresentou 761 de 779 linhas, 269 de 282 ramificações e 97,08% de cobertura combinada. Esses totais históricos não são atribuídos à execução #146.

Não abrange HTML, CSS, JavaScript nem todos os scripts administrativos.

### Comandos

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios,atualizar_auditoria -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m coverage report -m
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
.\.venv\Scripts\python.exe -m coverage xml
.\.venv\Scripts\python.exe -m coverage html
```

Cobertura elevada não comprova ausência de defeitos.

## 14. Disponibilidade e edição

### Disponibilidade

- Início e término opcionais, preenchidos em conjunto.
- Datas e ordem do período validadas.
- Exclusão de reservas em estados ativos e manutenção sobrepostas.
- Horários consecutivos permitidos.
- Combinação com tipo, capacidade, localização e competência.
- Consulta de períodos passados permitida.
- Limpeza dos filtros remove o período.

Evidências: test_disponibilidade.py, test_consulta.py e consultas manuais da Sala 101.

### Edição

- Proprietário ativo e autenticado.
- SOLICITADA ou APROVADA antes do início.
- Alteração de recurso, período e finalidade.
- Recurso, datas e finalidade validados.
- Própria reserva excluída da busca de conflito.
- Restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicitação sem mudança recusada.
- Auditoria ALTERACAO com antes e depois.
- Reserva, auditoria e aviso na mesma transação.

Evidências: 24 testes de serviço, 12 HTTP e alteração manual da reserva nº 9 com evento nº 10.

## 15. Defeitos e retestes

| Registro | Problema | Evidência |
| --- | --- | --- |
| DEF01 | EM_USO desaparecia de Ativas após o prazo | Filtro corrigido; testes e commit 9e94725 |
| DEF02 | Nome do template diferente do include | Nome _dados_reserva.html corrigido e retestes |
| DEF03 | Conexões SQLite impediam limpeza no Windows | Fechamento explícito; oito testes específicos |
| DEF04 | Sintaxe YAML impedia a CI | Actions #88 e #89 aprovados após correção |
| DEF05 | Caracteres corrompidos na documentação | Reconstrução e conferência visual |
| INV01 | Falhas no ensaio de carga sem pausa | Causa não confirmada; investigação pendente |

O Quality Gate também reprovou no commit 73a556e. Após ajuste do Dockerfile e classificação do teste HTTP, passou em 02737a6.

Detalhes e limitações estão em DEFEITOS.md e RELATORIO_QUALIDADE.md.

Uma alteração acidental com texto de comando em novo_recurso.html foi restaurada.

## 16. Notificações internas

Avisos persistidos ao dono da reserva:

| Operação | Aviso |
| --- | --- |
| Criação comum | Criada e aprovada |
| Criação restrita ou professor | Aguardando aprovação |
| Edição comum | Alterada e aprovada |
| Edição restrita ou professor | Aguardando nova aprovação |
| Cancelamento | Cancelada |
| Aprovação | Aprovada pelo responsável |
| Rejeição | Rejeitada pelo responsável |

- Avisos novos são não lidos.
- Reserva, auditoria e aviso compartilham a transação.
- Falha no aviso desfaz a operação.
- Consulta e leitura somente pelo destinatário.
- Marcação exige login e CSRF.
- Aviso inexistente ou alheio retorna 404.
- GET não marca leitura.
- Avisos lidos permanecem na lista.

Sem e-mail, SMS, paginação, tempo real ou aviso ao responsável. Movimentações e não comparecimento não geram aviso interno.

## 17. Relatórios e conflitos evitados

Acesso pelo administrador ativo.

Indicadores:

- Total de reservas e contagem das sete situações.
- Agrupamento por recurso.
- Horas previstas por recurso e no total.
- Conflitos evitados registrados.

Horas previstas consideram APROVADA, EM_USO e CONCLUIDA. Somente o trecho sobreposto ao período consultado é somado.

O indicador representa tempo reservado, não utilização real.

### Tentativas bloqueadas

conflitos_reservas registra sobreposição na criação, edição e aprovação.

Registra usuário, recurso, reserva conflitante, operação, período e data.

- Filtro pela data da tentativa, criado_em.
- Sem datas, todo o histórico registrado.
- Tentativas repetidas geram registros separados.
- Cancelamento ou inativação posterior não apaga o histórico.
- Manutenção, erros de preenchimento e falta de permissão não entram na contagem.
- Tentativas anteriores não são reconstruídas.
- A tentativa é confirmada antes do erro de conflito; reserva preservada.

Evidências: 21 testes de relatório, 16 HTTP, contador manual de zero para um e persistência no E2E e teste HTTP concorrente.

Limitações: tempo real, exportação, paginação e E2E desse relatório.

## 18. Integração contínua e Sonar

**Workflow:** .github/workflows/testes.yml.

### Suíte e cobertura

- Push e Pull Requests.
- Ubuntu e Python 3.14.
- Dependências com hashes e pacotes binários.
- Teste HTTP em processo separado.
- Suíte principal com linhas e ramificações.
- Metas de 80% de linhas e 70% de ramificações.
- Falha em teste reprovado ou medição sem linhas ou ramificações.
- JSON, XML e HTML publicados como relatorios-cobertura.
- Retenção de 30 dias.
- Publicação antes da verificação das metas e do Sonar.

Etapas posteriores dependentes podem não executar após falha dos testes.

### Chromium

- Job separado.
- requirements-e2e.lock com hashes.
- Instalação do Chromium e dependências.
- Execução com xvfb-run.
- Descoberta em e2e.

### Sonar

- Análise em PRs e pushes da main.
- SONAR_TOKEN como segredo.
- Espera pelo Quality Gate, com limite de 300 segundos.
- Reprovação ou expiração falha a etapa.
- Teste HTTP classificado como teste.

Última evidência conferida: commit 02737a6.

| Indicador | Resultado |
| --- | ---: |
| Quality Gate | Passed |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Security Hotspots | 0 |
| Cobertura no código novo | 83,8% |
| Duplicação no código novo | 0,0% |

Esse resultado não comprova análise posterior ao merge nem substitui a conferência do commit final.

Proteção da main e verificações obrigatórias ainda precisam de conferência.

## 19. Migração e refatorações

### Migração da auditoria

tests/test_atualizar_auditoria.py contém oito métodos:

1. Banco inexistente sem criação indevida.
2. Ausência da tabela de auditoria.
3. Estrutura atualizada sem migração desnecessária.
4. Preservação, backup e coluna detalhes.
5. Índice e gatilho preservados.
6. Recusa de coluna desconhecida.
7. Rollback após ação inválida.
8. Repetição sem duplicar registros ou backups.

Utiliza caminhos e bancos temporários. Não cobre automaticamente interrupção, falta de espaço ou outros scripts.

### Refatorações

Auxiliares extraídos para validar usuário, recurso, período, propriedade, conflitos, manutenção, estado inicial e detalhes de auditoria.

Dados comuns dos templates extraídos para _dados_reserva.html, reutilizado em aprovacoes.html e materiais.html.

Formulários, CSRF e ações específicas permanecem em cada página.

## 20. Navegador e concorrência HTTP

### Chromium

Arquivo: e2e/test_fluxo_reserva.py.

Verifica login inválido e válido, criação, consulta, conflito, cancelamento com confirmação, Ativas, Histórico e registros associados no banco.

Servidor local em porta dinâmica e SQLite temporário.

Resultado na execução #146: aprovado.

A execução local mais recente registrada foi de 20,869 segundos. O resultado inicial de 58,588 segundos permanece histórico.

Pendências: aprovação, materiais, edição, outros navegadores e capturas ou traces como artefatos.

### Concorrência HTTP

Arquivo: teste_concorrencia_http.py.

Duas sessões autenticadas enviam solicitações coordenadas para o mesmo recurso e período.

Verifica uma aceitação, uma recusa, uma reserva, auditoria, notificação e conflito registrado.

Resultado local: um teste em 3,731 segundos. Também aprovado na execução #146.

A barreira coordena os clientes, sem garantir uma ordem interna específica. O cenário não comprova todas as condições de corrida possíveis.

## 21. Docker

Arquivos: Dockerfile.testes e .dockerignore.

- Python 3.14 slim.
- Instalação com hashes de requirements.lock.
- Cópia dos arquivos Python, templates, static e tests.
- Execução como usuário sem privilégios de root.
- Banco local, ambientes virtuais, backups e arquivos de ambiente excluídos conforme .dockerignore.
- Sem montagem do banco local nos comandos utilizados.

```powershell
docker build -f Dockerfile.testes -t organizacao-recursos-testes .
docker run --rm organizacao-recursos-testes
```

Resultado após ajuste: 287 testes em 180,651 segundos, OK.

A imagem dessa execução precede o teste adicional de manutenção/reserva.

Executar SQLite e a suíte em Docker não equivale à implementação de Testcontainers nem à integração com um servidor de banco externo.

A imagem-base não está fixada por digest.

## 22. Desempenho

Documentação: performance/README.md.

Plano: performance/consulta_login_10usuarios_60s.jmx.

Commit: bf6822a.

Ambiente: Windows, JMeter 5.6.3, Java Zulu 25.0.3 e Flask local na porta 5003, sem debug. Cliente e servidor na mesma máquina.

GET /login, dez usuários, ramp-up de cinco segundos e duração configurada de 60 segundos.

Validações de HTTP 200 e texto Acesso ao sistema.

| Indicador | Sem pausa | Pausa de 1.000 ms |
| --- | ---: | ---: |
| Amostras | 17.633 | 570 |
| HTTP 200 | 16.344 | 570 |
| Falhas | 1.289 | 0 |
| Taxa de falhas | 7,31% | 0% |

Com pausa: média 5,49 ms, mediana 5 ms, p95 de 8 ms, mínimo 2 ms e máximo 38 ms. Taxa aproximada de 9,5 requisições/s.

Usuários ativos incluem espera pelo timer; não equivalem a dez requisições simultâneas.

Sem pausa, houve java.net.BindException com Address already in use: connect. Causa não confirmada.

A pausa reduziu a carga e não comprova correção da causa anterior.

Os ensaios foram exploratórios, sem critérios prévios. Não avaliam autenticação, reservas ou capacidade de produção.

Evidências:

- performance/carga_login_10usuarios_60s_01.jtl
- performance/carga_login_10usuarios_60s_pausa_01.jtl

Pendências: critérios definidos antes das execuções, repetições e cenários autenticados isolados.

## 23. Segurança

Documento: SEGURANCA.md.

### Login e saída HTML

test_seguranca_login.py verifica CSRF entre sessões, renovação após login, recusa do token anterior, logout com token atual e três tentativas de injeção SQL sem autenticação.

test_seguranca_xss.py verifica escape no nome do recurso na página inicial e no formulário de nova reserva.

O teste HTML não representa conjunto completo de ataques no navegador.

### Dependências

| Lock | Relatório | Resultado |
| --- | --- | --- |
| requirements.lock | auditoria_dependencias.json | Dez dependências; nenhuma vulnerabilidade conhecida reportada |
| requirements-e2e.lock | auditoria_dependencias_e2e.json | Nenhuma vulnerabilidade conhecida reportada |

Auditorias com pip-audit, --require-hashes e --strict.

O JSON de E2E foi registrado no commit 98d26d5 e inclui Playwright 1.64.1.

O ambiente .venv-auditoria é separado e excluído do Git e do Sonar.

A auditoria dos pacotes Python não equivale à auditoria do binário Chromium nem da imagem Docker.

Resultados dependem da base consultada no momento da execução.

### Limitações

- Revisão completa de segurança.
- HTTPS e cookies para implantação.
- Avaliação de limitação de tentativas de login.
- Ampliação de campos e páginas contra XSS.
- Ausência de teste de invasão completo.

## 24. Próximas verificações e entrega

- Conferir requisitos e regras com o enunciado.
- Revisar gestão administrativa de usuários e recursos.
- Revisar não comparecimento para outros tipos.
- Ampliar cenários explícitos de conflito entre reservas por tipo.
- Atender Testcontainers ou registrar alternativa aceita.
- Testar os demais scripts e migrações.
- Verificar restauração de backup.
- Ampliar E2E e tamanhos de tela.
- Definir critérios e ampliar desempenho.
- Conferir instalação limpa e README.
- Revisar documentação TDD, arquitetura e defeitos.
- Alinhar PLANO_TESTES.md e SEGURANCA.md com as novas evidências.
- Conferir proteção da main e checks obrigatórios.
- Conferir Sonar do commit final.
- Preparar apresentação e roteiro de demonstração.
- Realizar revisão por outro integrante na etapa combinada.

### Evidências

- Identificar cenário, versão e resultados esperado e observado.
- Preservar falhas e limitações.
- Não transformar contagens esperadas em execuções comprovadas.
- Não apresentar métricas históricas como atuais.
- Não registrar revisão, merge ou aprovação sem evidência.
- Preservar RTM_historico.md como histórico.