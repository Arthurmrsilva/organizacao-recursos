# Plano de testes — Organização de Recursos

**Atualização:** 02/11/2026

**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

## 1. Objetivo

Verificar as regras de reserva, o controle de acesso, a integridade dos registros e os principais fluxos do sistema.

Este plano consolida a estratégia utilizada e as verificações ainda necessárias. Foi documentado após parte das execuções; não representa planejamento prévio de todos os testes realizados.

Os resultados observados estão em RTM.md e RELATORIO_QUALIDADE.md.

## 2. Escopo

- Autenticação, sessão e autorização.
- Cadastro e consulta de recursos.
- Pesquisa por disponibilidade.
- Criação, edição e cancelamento.
- Aprovação e rejeição.
- Manutenção.
- Retirada, devolução e não comparecimento de materiais.
- Auditoria e notificações.
- Relatórios e conflitos evitados.
- Migração específica da auditoria.
- Concorrência de reservas no serviço e por HTTP.
- Concorrência entre manutenção e reserva no serviço.
- Fluxo principal no Chromium.
- Execução da suíte em Docker.
- Segurança e desempenho nos cenários documentados.

Não estão demonstrados testes completos de produção, recuperação de desastre ou todas as combinações de dispositivos e navegadores.

## 3. Priorização por risco

| Prioridade | Risco | Verificação principal |
| --- | --- | --- |
| Alta | Duas reservas aceitas no mesmo período | Sobreposição e concorrência |
| Alta | Manutenção e reserva aceitas para o mesmo recurso e período | Disputa concorrente entre as operações |
| Alta | Usuário altera dados alheios | Propriedade, perfil e vínculo |
| Alta | Operação sem autenticação ou CSRF válido | Testes negativos das rotas |
| Alta | Alteração sem auditoria correspondente | Transação e rollback |
| Alta | Transição de estado inválida | Estados permitidos e recusas |
| Média | Recurso indisponível aparece na pesquisa | Filtros e manutenção |
| Média | Indicador incorreto | Contagens, datas e arredondamento |
| Média | Fluxo falha no navegador | Teste ponta a ponta |
| Média | Degradação sob carga | Ensaios controlados |

A prioridade foi consolidada neste documento e precisa de revisão pelo grupo.

## 4. Níveis e ferramentas

| Tipo | Abordagem | Limite |
| --- | --- | --- |
| Regras e integração | unittest e SQLite temporário | Muitos testes utilizam persistência real |
| Rotas | Cliente Flask | Não executa JavaScript |
| HTTP real | Servidor local e dois clientes autenticados | Um cenário concorrente de criação |
| Navegador | Playwright com Chromium | Um fluxo principal |
| Concorrência no serviço | Threads com início coordenado | SQLite e cenários definidos |
| Container | Docker e suíte com SQLite temporário | Não equivale à implementação de Testcontainers |
| Cobertura | coverage.py | Seis módulos Python definidos |
| Análise estática | SonarQube Cloud | Resultado associado à versão analisada |
| Segurança | Testes específicos e pip-audit | Cobertura parcial de ameaças |
| Desempenho | JMeter | GET /login em ambiente local |
| Verificação manual | Interface e registros | Depende da identificação da evidência |

Não existe integração externa implementada. As notificações são avisos internos persistidos.

## 5. Técnicas utilizadas

- Particionamento de entradas válidas e inválidas.
- Valores-limite de datas e horários.
- Combinações de perfil, vínculo e propriedade.
- Transições de estado permitidas e proibidas.
- Cenários negativos de autenticação e CSRF.
- Persistência e ausência de alterações nas recusas.
- Falhas simuladas para verificar rollback.
- Concorrência no serviço e por HTTP.
- Regressão após correções e refatorações.
- subTest para agrupar variações.

Cobertura de código complementa essas técnicas; não substitui a avaliação das regras.

Testes com banco temporário real também verificam integração. Não são integralmente testes unitários isolados.

## 6. Cenários críticos

| ID | Cenário | Resultado esperado | Rastreabilidade |
| --- | --- | --- | --- |
| CT01 | Login válido, inválido e usuário inativo | Somente usuário ativo com credenciais válidas autentica | RF01 |
| CT02 | POST sem token ou com token inválido | Recusa sem operação indevida | RF01 |
| CT03 | Token de outra sessão | Operação recusada | RF01 |
| CT04 | Cadastro por não administrador | Acesso recusado e nenhum recurso criado | RF02 |
| CT05 | Término não posterior ao início | Operação recusada | RC01 |
| CT06 | Reserva sobreposta | Operação recusada | RF05, RC02 |
| CT07 | Horários consecutivos | Ausência de conflito por contato no limite | RC02 |
| CT08 | Duas reservas simultâneas no serviço | Uma aceita e outra bloqueada | RF06, RC03 |
| CT09 | Reserva durante manutenção | Operação recusada | RF08, RC04 |
| CT10 | Aprovação sem vínculo | Operação recusada | RF07, RC07 |
| CT11 | Edição ou cancelamento por usuário alheio | Recusa e dados preservados | RF04 |
| CT12 | Edição ou cancelamento após início | Operação recusada | RC08 |
| CT13 | Retirada e devolução | Transições válidas e auditoria | RF09, RC05, RC09 |
| CT14 | Não comparecimento antes e no limite do término | Recusa antes; aceitação no limite para reserva elegível e usuário autorizado | RC06 |
| CT15 | Falha na auditoria ou notificação | Rollback da operação correspondente | RF10, RF11 |
| CT16 | Consulta ou leitura de aviso alheio | Aviso não exposto e operação recusada | RF11 |
| CT17 | Datas inválidas e limites no relatório | Validação e contagens corretas | RF12 |
| CT18 | Bloqueio por sobreposição | Conflito registrado sem alterar a reserva | RF05, RF12 |
| CT19 | Nome de recurso contendo HTML | Saída escapada nos pontos verificados | RF13 |
| CT20 | Fluxo principal no Chromium | Login, criação, conflito, cancelamento e histórico coerentes | RF01, RF04, RF05 |
| CT21 | Duas sessões criam reserva concorrente por HTTP | Uma aceitação, uma recusa e registros consistentes | RF06, RC03, RC09 |
| CT22 | Manutenção e reserva concorrentes nos três tipos | Exatamente uma operação aceita por disputa | RF08, RC04 |

A tabela define expectativas. As evidências e limitações devem ser consultadas na RTM; não declara aprovação automática de todas as variações possíveis.

## 7. Ambiente e dados

### Ambiente local

- Windows.
- Python 3.14.6 no ambiente virtual.
- Flask e SQLAlchemy Core.
- SQLite.
- Chromium instalado pelo Playwright.
- JMeter 5.6.3.
- Docker Desktop com containers Linux.

### Integração contínua

- GitHub Actions em Ubuntu.
- Python 3.14.
- Locks com hashes.
- Chromium executado com tela virtual.
- Teste HTTP em processo separado da suíte principal.

### Container de testes

- Python 3.14 slim.
- Dependências de requirements.lock com hashes.
- Execução como usuário sem privilégios de root.
- Bancos de teste temporários.
- Banco local e arquivos de ambiente excluídos conforme .dockerignore.

A imagem-base utiliza tag, sem fixação por digest.

### Dados

- Usuários ativos e inativos.
- ADMIN, RESPONSAVEL e SOLICITANTE.
- Recursos comuns, restritos, ativos e inativos.
- Responsável vinculado e não vinculado.
- Períodos futuros, limites exatos e reservas iniciadas.
- Estados relevantes das reservas.
- Bancos temporários isolados.

A aplicação cria estrutura durante a importação. Os testes que substituem a conexão precisam preparar esse isolamento antes de importar app.

Não executar escrita ou carga sobre dados importantes sem isolamento.

## 8. Critérios de entrada

Antes de executar:

- Identificar versão e branch.
- Instalar as dependências previstas.
- Preparar ambiente e dados.
- Confirmar isolamento.
- Definir resultado esperado.
- Verificar as ferramentas necessárias.

Para novos ensaios de desempenho, definir previamente carga, duração, pausas, métricas e critérios de aceitação.

## 9. Critérios de saída

| Critério | Evidência |
| --- | --- |
| Testes da versão de entrega aprovados | Logs identificados |
| Pelo menos 80% de linhas | Relatório no escopo definido |
| Pelo menos 70% de ramificações | Relatório no escopo definido |
| Quality Gate aprovado | Análise da versão de entrega |
| Regras críticas rastreadas | Revisão de RC01 a RC09 |
| Defeitos críticos conhecidos tratados | Registro e decisão documentada |
| Limitações identificadas | RTM, DEFEITOS e relatório |
| Revisão por outro integrante | Registro real de revisão |

Esses critérios devem ser conferidos antes da entrega. Nem todos estão demonstrados como atendidos.

## 10. Execução e regressão

Os comandos são referências para reprodução. Atualizar documentação não exige automaticamente repetir a suíte local.

### Suíte principal

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Concorrência HTTP

Executar separadamente:

```powershell
.\.venv\Scripts\python.exe .\teste_concorrencia_http.py
```

O teste prepara servidor e banco temporários próprios.

### Concorrência entre manutenção e reserva

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_concorrencia_manutencao.py -v
```

Esse arquivo também entra automaticamente na descoberta da suíte principal.

### Navegador

Após instalar as dependências e o Chromium conforme README.md:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s e2e -v
```

### Docker

Com Docker em funcionamento:

```powershell
docker build -f Dockerfile.testes -t organizacao-recursos-testes .
docker run --rm organizacao-recursos-testes
```

O comando padrão da imagem executa a suíte de tests. Não executa automaticamente o Chromium nem o teste HTTP separado.

### Cobertura

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios,atualizar_auditoria -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m coverage report -m
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
.\.venv\Scripts\python.exe -m coverage xml
.\.venv\Scripts\python.exe -m coverage html
```

O teste HTTP separado e o navegador não são somados a essa medição.

### Reteste

1. Identificar ou reproduzir a falha.
2. Registrar esperado e observado.
3. Aplicar a correção.
4. Executar os testes relacionados.
5. Executar regressão adequada ao impacto.
6. Registrar versão e resultado.

Para documentação, conferir conteúdo, links, comandos e renderização.

## 11. Resultados registrados

### CI de referência

**Actions #146 — commit 67b3d00 — evento push.**

| Verificação | Resultado |
| --- | --- |
| Suíte principal | 288 testes em 15,349 segundos, OK |
| Concorrência HTTP | Aprovada |
| Chromium | Aprovado |
| Linhas | 97,69% |
| Ramificações | 95,74% |
| Workflow completo | Success em 59 segundos |

O método HTTP e o método de navegador são separados dos 288 testes.

### Execuções locais

| Execução | Resultado |
| --- | --- |
| Suíte antes do teste adicional de XSS | 286 testes em 121,250 segundos |
| Escape de HTML | Um teste em 0,382 segundo, com dois cenários |
| Chromium | Um teste em 20,869 segundos |
| Concorrência HTTP | Um teste em 3,731 segundos |
| Docker após ajuste de segurança | 287 testes em 180,651 segundos |
| Manutenção/reserva | Um teste em 1,762 segundo, com três cenários |

A execução Docker registrada precede o teste adicional de manutenção/reserva.

Respostas de erro previstas, como senha incorreta ou reserva conflitante, não representam falha quando correspondem à expectativa do teste.

### Concorrência

O cenário HTTP verifica duas sessões autenticadas, uma reserva aceita, outra tentativa recusada e os registros associados.

O cenário manutenção/reserva verifica SALA, PROFESSOR e MATERIAL no serviço.

A coordenação dos clientes ou threads não garante uma ordem interna específica. Os testes não comprovam ausência de todas as condições de corrida.

### Sonar

Última análise conferida: 02737a6.

- Quality Gate aprovado.
- Zero novos problemas.
- Zero Security Hotspots.
- 83,8% de cobertura no código novo.
- 0,0% de duplicação no código novo.

Conferir a análise da versão final antes da entrega.

## 12. Segurança

Cenários:

- Autenticação e autorização.
- CSRF ausente, inválido ou de outra sessão.
- Renovação de token após login.
- Tentativas de injeção SQL no login.
- Escape de HTML em duas páginas.
- Auditoria de requirements.lock.
- Auditoria de requirements-e2e.lock.
- Ajuste do container para execução sem root.

As duas auditorias Python não reportaram vulnerabilidades conhecidas nas versões consultadas.

A auditoria Python não equivale à análise do binário Chromium ou da imagem Docker.

Pendências:

- Ampliar campos e páginas.
- Avaliar limitação de tentativas de login.
- Revisar HTTPS e cookies para implantação.
- Completar revisão de código e configuração.

Detalhes em SEGURANCA.md. Não representa teste de invasão completo.

## 13. Desempenho

Evidências em performance/README.md e nos arquivos JTL.

GET /login com dez usuários, ramp-up de cinco segundos e duração configurada de 60 segundos.

| Indicador | Sem pausa | Pausa de um segundo |
| --- | ---: | ---: |
| Amostras | 17.633 | 570 |
| HTTP 200 | 16.344 | 570 |
| Falhas | 1.289 | 0 |
| Taxa de falhas | 7,31% | 0% |

Com pausa: média 5,49 ms, p95 de 8 ms e máximo de 38 ms.

Sem pausa: java.net.BindException; causa não confirmada.

A pausa altera a carga oferecida e não comprova correção da causa anterior.

Os ensaios foram exploratórios, sem critérios prévios.

Novos ensaios devem:

- Definir metas antes da execução.
- Registrar ambiente e versão.
- Repetir em condições controladas.
- Avaliar fluxos autenticados com dados isolados.
- Observar recursos e conexões de cliente e servidor.
- Preservar resultados negativos.

## 14. Evidências e responsabilidades

Cada evidência deve identificar:

- Cenário e requisito.
- Versão.
- Ambiente.
- Resultado esperado e observado.
- Data e origem.

Defeitos e investigações estão em DEFEITOS.md.

| Atividade | Responsabilidade |
| --- | --- |
| Preparar e executar | Integrante executor |
| Registrar evidências | Integrante executor |
| Corrigir | Integrante responsável pela alteração |
| Revisar código, testes e documentos | Outro integrante |
| Decidir sobre entrega | Grupo |

A distribuição nominal deve ser confirmada pelo grupo.

A revisão por pares está reservada para etapa posterior e precisa ser realizada de fato. A CI não substitui essa revisão.

## 15. Lacunas conhecidas

- Testcontainers ou alternativa aceita pelo professor.
- Ampliação dos testes unitários totalmente isolados.
- Cenários explícitos adicionais de sobreposição entre reservas por tipo.
- Disputa manutenção/reserva por HTTP.
- Outros fluxos E2E, navegadores e tamanhos de tela.
- Demais scripts administrativos e migrações.
- Restauração de backup.
- Critérios e cenários adicionais de desempenho.
- Revisão final de segurança.
- Instalação limpa e conferência dos comandos.
- Proteção da main e checks obrigatórios.
- Revisão por pares e decisão de entrega.

Executar SQLite e a suíte em Docker não comprova, por si só, atendimento específico de Testcontainers.

## 16. Referências

- [README](README.md)
- [Rastreabilidade](RTM.md)
- [Relatório de qualidade](RELATORIO_QUALIDADE.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Segurança](SEGURANCA.md)
- [Desempenho](performance/README.md)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)