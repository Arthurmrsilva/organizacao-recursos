# Plano de testes — Organização de Recursos

Atualização: 02/11/2026.

Integrantes: Arthur Mendes, Robert Oliveira, Nicolas Ferreira.

## 1. Objetivo

Verificar regras de reserva, controle de acesso, integridade dos registros
e principais fluxos do sistema.

Este documento consolida a estratégia utilizada e verificações pendentes.
Foi elaborado após parte das execuções; não representa planejamento
prévio de todos os testes.

Os critérios das duas medições planejadas de carga foram definidos
antes dessas execuções específicas.

Resultados e versões estão em RELATORIO_QUALIDADE.md e no índice
docs/evidencias/README.md.

## 2. Escopo

- Autenticação, sessão, autorização e CSRF.
- Cadastro, consulta, filtros e disponibilidade.
- Criação, edição e cancelamento de reservas.
- Aprovação e rejeição.
- Manutenção e movimentação de materiais.
- Não comparecimento.
- Auditoria, notificações e relatórios.
- Migração específica da auditoria.
- Concorrência no serviço e por HTTP.
- Fluxo principal no Chromium.
- Suíte em Docker controlada pelo Testcontainers.
- Verificador de backup e restauração SQLite.
- Instalação em clone separado.
- Segurança e desempenho nos cenários documentados.

Não demonstra produção, recuperação completa de desastre
ou todas as combinações de dispositivos e navegadores.

## 3. Priorização por risco

| Prioridade | Risco | Verificação principal |
| --- | --- | --- |
| Alta | Duas reservas aceitas no mesmo período | Sobreposição e concorrência |
| Alta | Manutenção e reserva incompatíveis aceitas | Disputa entre operações |
| Alta | Usuário altera dados alheios | Propriedade, perfil e vínculo |
| Alta | Operação sem autenticação ou CSRF | Testes negativos |
| Alta | Alteração sem auditoria | Transação e rollback |
| Alta | Transição inválida | Estados permitidos e recusas |
| Alta | Restauração perde ou altera dados | Comparação e integridade SQLite |
| Média | Pesquisa retorna recurso indisponível | Filtros e manutenção |
| Média | Indicador incorreto | Contagens, datas e arredondamento |
| Média | Fluxo falha no navegador | Teste E2E |
| Média | Degradação sob carga | Medições controladas |

A priorização precisa de revisão pelo grupo.

## 4. Níveis e ferramentas

| Tipo | Abordagem | Limite |
| --- | --- | --- |
| Regras e integração | unittest e SQLite temporário | Muitos testes usam persistência real |
| Rotas | Cliente Flask | Não executa JavaScript |
| HTTP real | Servidor e clientes autenticados | Um cenário concorrente de criação |
| Navegador | Playwright com Chromium | Um fluxo principal |
| Concorrência no serviço | Threads coordenadas | Não força todas as ordens internas |
| Container | Docker e Testcontainers | SQLite no container; sem servidor de banco separado |
| Cobertura | Coverage.py | Sete módulos Python |
| Análise estática | SonarQube Cloud | Associada ao commit analisado |
| Segurança | Cenários específicos e pip-audit | Cobertura parcial de ameaças |
| Desempenho | JMeter | GET /login local |
| Recuperação | sqlite3 e comparação de estrutura/dados | Sem recuperação completa da aplicação |
| Instalação | Clone e ambiente separados | Mesmo computador Windows |

As notificações são internas. Não há integração externa implementada.

## 5. Técnicas

- Particionamento de entradas válidas e inválidas.
- Valores-limite de datas e horários.
- Combinações de perfil, vínculo e propriedade.
- Transições de estado.
- Cenários negativos de autenticação e CSRF.
- Verificação dos efeitos persistidos e das recusas.
- Falhas simuladas e rollback.
- Concorrência no serviço e por HTTP.
- Regressão após correções.
- subTest para variações.
- Comparação de estrutura e dados na restauração.

Cobertura de código complementa a avaliação das regras.
Testes com banco real temporário também são testes de integração.

## 6. Cenários críticos

| ID | Cenário | Resultado esperado | Rastreabilidade |
| --- | --- | --- | --- |
| CT01 | Login válido, inválido e usuário inativo | Somente credenciais válidas de usuário ativo autenticam | RF01 |
| CT02 | POST sem token ou com token inválido | Recusa sem operação indevida | RF01 |
| CT03 | Token de outra sessão | Recusa | RF01 |
| CT04 | Cadastro por não administrador | Recusa e nenhum recurso criado | RF02 |
| CT05 | Término não posterior ao início | Recusa | RC01 |
| CT06 | Reserva sobreposta | Recusa | RF05, RC02 |
| CT07 | Horários consecutivos | Sem conflito por contato no limite | RC02 |
| CT08 | Reservas simultâneas no serviço | Uma aceita e outra bloqueada | RF06, RC03 |
| CT09 | Reserva durante manutenção | Recusa | RF08, RC04 |
| CT10 | Aprovação sem vínculo | Recusa | RF07, RC07 |
| CT11 | Edição/cancelamento por usuário alheio | Recusa e dados preservados | RF04 |
| CT12 | Edição/cancelamento após início | Recusa | RC08 |
| CT13 | Retirada e devolução | Transições válidas e auditoria | RF09, RC05, RC09 |
| CT14 | Não comparecimento antes e no limite do término | Recusa antes; aceitação no limite para reserva elegível e usuário autorizado | RC06 |
| CT15 | Falha na auditoria ou notificação | Rollback correspondente | RF10, RF11 |
| CT16 | Consulta/leitura de aviso alheio | Sem exposição ou alteração indevida | RF11 |
| CT17 | Datas inválidas e limites no relatório | Validação e contagens corretas | RF12 |
| CT18 | Bloqueio por sobreposição | Conflito registrado e reserva preservada | RF05, RF12 |
| CT19 | Nome de recurso com HTML | Saída escapada nos pontos verificados | RF13 |
| CT20 | Fluxo no Chromium | Login, criação, conflito, cancelamento e histórico coerentes | RF01, RF04, RF05 |
| CT21 | Duas sessões criam reserva por HTTP | Uma aceitação, uma recusa e registros consistentes | RF06, RC03, RC09 |
| CT22 | Manutenção e reserva nos três tipos | Exatamente uma operação aceita por disputa | RF08, RC04 |
| CT23 | Backup/restauração SQLite | Estrutura e dados preservados; origem inalterada | Verificação técnica de recuperação |
| CT24 | Suíte via Testcontainers | Término com código zero e 292 testes esperados | Verificação técnica de execução |
| CT25 | Instalação limpa | Instalar, iniciar, autenticar e criar/consultar reserva | Reprodutibilidade |

A tabela define expectativas, não aprovação automática de todas
as variações. CT23 a CT25 não criam novos requisitos funcionais.

## 7. Ambiente e dados

Ambiente local: Windows, Python 3.14.6, Flask, SQLAlchemy Core,
SQLite, Chromium, JMeter 5.6.3 e Docker Desktop com containers Linux.

CI: Ubuntu, Python 3.14, locks principais e E2E com hashes,
Chromium com tela virtual e HTTP em processo separado.

Imagem: Python 3.14 slim, usuário sem privilégios de root,
bancos temporários e exclusões conforme .dockerignore.
A imagem-base não está fixada por digest.

Dados de teste:

- Usuários ativos/inativos e três perfis.
- Recursos comuns, restritos, ativos/inativos.
- Responsável vinculado/não vinculado.
- Períodos futuros, limites exatos e reservas iniciadas.
- Estados relevantes das reservas.
- Arquivos SQLite válidos, inválidos e inexistentes.

A aplicação cria estrutura durante a importação.
O isolamento deve ser preparado antes de importar app nos testes
que substituem a conexão.

Usar dados temporários nos testes com escrita.

## 8. Critérios de entrada

- Identificar versão e branch.
- Instalar dependências previstas.
- Preparar ambiente e isolamento.
- Definir resultado esperado.
- Confirmar ferramentas necessárias.
- Para carga, definir cenário, duração, pausas e metas antes da execução.

## 9. Critérios de saída da entrega

| Critério | Evidência necessária |
| --- | --- |
| Testes aprovados | Logs do commit avaliado |
| Linhas pelo menos 80% | Relatório dos sete módulos |
| Ramificações pelo menos 70% | Relatório dos sete módulos |
| Quality Gate aprovado | Análise do commit avaliado |
| Regras críticas rastreadas | Conferência de RC01 a RC09 |
| Defeitos tratados ou limitações decididas | Registro e decisão proporcional às evidências |
| Instalação reproduzível | Clone limpo da candidata |
| Revisão por outro integrante | Registro real |
| Release identificada | Tag anotada e SHA |
| Pacote verificável | Índice com links válidos |

Nem todos os critérios finais estão concluídos.
CI verde não substitui revisão do grupo.

## 10. Execução e regressão

Comandos completos de preparação estão no README.

### Suíte

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### HTTP separado

```powershell
.\.venv\Scripts\python.exe teste_concorrencia_http.py
```

### Navegador

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s e2e -v
```

### Docker e Testcontainers

Após preparar o ambiente Testcontainers conforme README:

```powershell
docker build -f Dockerfile.testes -t organizacao-recursos-testes .
.\.venv-testcontainers\Scripts\python.exe teste_testcontainers.py
```

Reconstruir a imagem após mudanças nos arquivos utilizados.

O comando padrão da imagem executa tests.
Não executa automaticamente Chromium ou o teste HTTP separado.

### Cobertura

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios,atualizar_auditoria,validar_backup -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m coverage report -m
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
.\.venv\Scripts\python.exe -m coverage xml -o coverage.xml
.\.venv\Scripts\python.exe -m coverage html -d htmlcov
```

HTTP, navegador e controle do container não são somados à medição.

### Reteste

1. Identificar a falha e o resultado esperado.
2. Registrar observado e versão.
3. Corrigir.
4. Executar testes relacionados e regressão adequada ao impacto.
5. Registrar resultado.

Para alterações documentais, conferir conteúdo, links e comandos.
Não é necessário repetir automaticamente toda a suíte local.

## 11. Resultados registrados

| Referência | Resultado |
| --- | --- |
| da93d49, local | 292 testes, 116,207 segundos, OK |
| da93d49, CI #160 | Workflow aprovado em 53 segundos |
| da93d49, cobertura CI | 97,46% linhas; 94,83% ramificações |
| b1b308a, Testcontainers push #1 | Aprovado; 49 segundos totais |
| c84dac2 | Instalação limpa e fluxo manual registrados |
| 3a76227 | Sete checks verdes no pull request |
| 3a76227, Sonar | Quality Gate aprovado; 84,1% no código novo; 0,0% duplicação; zero novos problemas e hotspots |

Resultados históricos adicionais permanecem no relatório e no Git.

O método HTTP, o método de navegador e o controle externo
do Testcontainers são separados dos 292 testes.

Respostas negativas esperadas, como conflito de reserva,
não representam falha do teste quando verificadas corretamente.

## 12. Segurança e recuperação

Verificações de autenticação, autorização, CSRF, SQL e escape de HTML,
além das auditorias dos locks principal e E2E.

As auditorias não reportaram vulnerabilidades conhecidas nas execuções
registradas. Não abrangem automaticamente Chromium, imagem Docker
ou ambiente Testcontainers.

O verificador de backup compara estrutura e dados e abre a origem
somente para leitura. Quatro testes verificam preservação e recusas
de entradas inválidas.

Não representa recuperação completa após desastre.

Detalhes em SEGURANCA.md e VALIDACAO_INSTALACAO.md.

## 13. Desempenho

### Duas medições planejadas

GET /login, dez usuários, subida de cinco segundos, 60 segundos
e pausa de um segundo.

Critérios definidos antes da execução:

- Zero erros.
- p95 até 500 ms.
- Pelo menos 500 amostras em cada repetição.

| Execução | Amostras | Erros | Média (ms) | p95 (ms) | Máximo (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 | 85 |
| 2 | 565 | 0 | 8,11 | 19 | 69 |

Ambas atenderam aos critérios.
Resultados registrados em docs/performance/resultado-01.md.

Não medem autenticação por POST, reservas ou produção.

### Histórico exploratório

O ensaio sem pausa apresentou 1.289 falhas em 17.633 amostras,
com BindException; causa não confirmada.

O ensaio anterior com pausa apresentou 570 amostras sem falha,
média de 5,49 ms e p95 de 8 ms.

Reduzir a carga não comprova correção da causa anterior.
Esses ensaios não tiveram critérios previamente definidos.

### Ampliação

Cenários autenticados devem usar dados isolados e metas próprias.
Novas medições devem registrar versão, ambiente e resultados negativos.

## 14. Evidências e responsabilidades

Cada evidência deve identificar cenário, versão, ambiente,
resultado esperado/observado e origem.

- Executor: prepara dados, executa e registra.
- Responsável pela alteração: corrige e retesta.
- Outro integrante: revisa código, testes e documentos.
- Grupo: confirma contribuições e decide sobre a entrega.

A distribuição nominal precisa ser confirmada.
Não presumir revisão ou assinatura.

## 15. Lacunas

- Cenários explícitos adicionais de conflito entre reservas por tipo.
- Disputa manutenção/reserva por HTTP.
- Outros fluxos E2E, navegadores e tamanhos de tela.
- Scripts administrativos e migrações restantes.
- Desempenho autenticado e investigação do ensaio sem pausa.
- Revisão completa de segurança.
- Aceitação acadêmica das equivalências de ferramentas e do banco em container.
- Proteção da main, revisão por pares e fechamento da candidata.

## 16. Referências

- [README](README.md)
- [Rastreabilidade](RTM.md)
- [Relatório](RELATORIO_QUALIDADE.md)
- [Segurança](SEGURANCA.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Carga planejada](docs/performance/resultado-01.md)
- [Instalação](VALIDACAO_INSTALACAO.md)
- [Índice de evidências](docs/evidencias/README.md)
- [Checklist](docs/entrega/checklist.md)