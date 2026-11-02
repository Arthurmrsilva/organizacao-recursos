# Relatório de qualidade — Organização de Recursos

Data: 02/11/2026.

Integrantes: Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Branch: funcionalidade/login. Pull request: nº 1.

Estado: consolidação para revisão do grupo; release candidata ainda não publicada.

## 1. Objetivo e escopo

Consolidar evidências funcionais, cobertura, análise estática, segurança,
concorrência, navegador, containers, recuperação de dados e desempenho.

O sistema utiliza Python, Flask, SQLAlchemy Core e SQLite para reservas
de salas, professores e materiais.

Os resultados pertencem às versões identificadas. Este relatório não
representa aprovação formal do grupo nem prontidão para produção.

## 2. Evidências e versões

| Evidência | Referência | Resultado |
| --- | --- | --- |
| Suíte local | da93d49 | 292 testes aprovados em 116,207 segundos |
| Pipeline principal | Actions #160, da93d49, push | Success; duração total de 53 segundos |
| Cobertura na CI | da93d49 | 97,46% de linhas; 94,83% de ramificações |
| Concorrência HTTP | Actions #160 | Aprovada |
| Chromium | Actions #160 | Aprovado |
| Testcontainers na CI | b1b308a, execução push #1 | Success; 49 segundos totais; um artefato |
| Quality Gate | 047995b | Passed; 84,1% de cobertura no código novo |
| Correção YAML do Testcontainers | 1e42442 | Execução verde informada pelo executor |
| Instalação limpa | c84dac2 | Login e criação/consulta de reserva confirmados |
| Backup e restauração | Script incluído em 8820445 | Integridade, estrutura e dados conferidos |
| Testes do verificador de backup | da93d49 | Quatro testes incorporados à suíte |
| Carga planejada | Resultados registrados em 49f9268 | Duas execuções atenderam aos critérios definidos |

Duração total do workflow não equivale à duração isolada da suíte.

As evidências acima são anteriores à release candidata.
A validação final deverá identificar o commit avaliado e seus links de CI.

## 3. Estratégia de testes

Foram utilizadas verificações de:

- Regras de negócio e integração com SQLite temporário.
- Rotas com cliente Flask.
- Perfis, propriedade da reserva e vínculo com o recurso.
- Valores-limite de datas e horários.
- Transições de estado.
- Concorrência no serviço e por HTTP.
- Rollback após falhas simuladas.
- Fluxo no navegador Chromium.
- Cenários específicos de segurança.
- Dependências Python.
- Execução em container controlado pelo Testcontainers.
- Backup e restauração SQLite.
- Desempenho local.

Muitos testes utilizam persistência real temporária.
A suíte não deve ser apresentada integralmente como testes unitários isolados.

Métodos com subTest podem verificar várias variações.
A contagem de métodos não equivale à contagem de todas as combinações.

## 4. Resultados funcionais

A suíte registrada de 292 testes abrange cenários de:

- Login válido, inválido e usuário inativo.
- Restrições por perfil, propriedade e vínculo.
- Cadastro, filtros e disponibilidade.
- Criação, edição e cancelamento.
- Sobreposição e horários consecutivos.
- Solicitações concorrentes.
- Aprovação e rejeição.
- Bloqueio por manutenção.
- Disputa entre manutenção e reserva.
- Movimentação e não comparecimento de materiais.
- Auditoria, notificações e rollback.
- Relatórios e conflitos evitados.
- Migração específica da auditoria.
- Validação do verificador de backup.

Os testes separados de HTTP, navegador e controle do container
não são somados à contagem de 292 testes.

Os resultados não demonstram todas as combinações possíveis.

## 5. Cobertura

Referência: CI do commit da93d49.

| Métrica | Resultado | Meta da CI | Avaliação |
| --- | ---: | ---: | --- |
| Linhas | 97,46% | 80% | Atendida |
| Ramificações | 94,83% | 70% | Atendida |

Escopo medido:

- app.py
- banco.py
- servico_reservas.py
- servico_materiais.py
- servico_relatorios.py
- atualizar_auditoria.py
- validar_backup.py

A medição é produzida pela suíte principal.
HTTP, navegador e Testcontainers são executados separadamente.

A cobertura não inclui HTML, CSS, JavaScript nem todos os scripts
administrativos. Cobertura elevada não comprova ausência de defeitos.

O workflow publica JSON, XML e HTML no artefato relatorios-cobertura.

## 6. Análise estática e correções

Análise Sonar conferida no commit 047995b:

| Indicador | Resultado |
| --- | ---: |
| Quality Gate | Passed |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Security Hotspots | 0 |
| Cobertura no código novo | 84,1% |
| Duplicação no código novo | 0,0% |

A cobertura do código novo no Sonar possui escopo diferente
da cobertura de linhas e ramificações medida pelo Coverage.py.

Correções registradas durante o desenvolvimento:

- Cópias explícitas no Dockerfile, substituindo a cópia recursiva ampla.
- Execução dos testes no container com usuário sem privilégios de root.
- Classificação dos testes separados na configuração do Sonar.
- Instalação de Testcontainers com exigência de pacotes binários.
- Correção YAML usando bloco run para o comando de instalação.

O commit b1b308a teve Testcontainers aprovado, mas Quality Gate reprovado
pela instalação sem exigir pacotes binários.

O commit 047995b corrigiu o apontamento de segurança, porém exigiu
correção posterior da sintaxe YAML no commit 1e42442.

Zero problemas e hotspots não comprovam ausência de vulnerabilidades.
A análise final da main após integração permanece pendente.

## 7. Navegador e concorrência

### Chromium

Arquivo: e2e/test_fluxo_reserva.py. Ferramenta: Playwright.

Fluxo verificado:

1. Login inválido e válido.
2. Criação e consulta da reserva.
3. Tentativa de reserva conflitante.
4. Cancelamento com confirmação.
5. Consulta de Ativas e Histórico.
6. Conferência dos registros associados no banco temporário.

Aprovação, edição e movimentação de materiais ainda não possuem
cobertura E2E equivalente.

### Concorrência por HTTP

Arquivo: teste_concorrencia_http.py.

Utiliza servidor local em threads, duas sessões autenticadas
e SQLite temporário. Duas solicitações disputam o mesmo recurso e período.

Verifica uma solicitação aceita e outra recusada, uma reserva persistida,
auditoria, notificação e registro da tentativa bloqueada.

A coordenação dos clientes não garante uma ordem interna específica.
Uma execução aprovada não elimina todas as condições de corrida possíveis.

### Manutenção e reserva

Arquivo: tests/test_concorrencia_manutencao.py.

Disputa concorrente no serviço entre manutenção e reserva,
com cenários SALA, PROFESSOR e MATERIAL.

Verifica exatamente uma operação aceita, outra recusada e ausência
de reserva e manutenção aceitas simultaneamente no mesmo período.

Também verifica datas, estado inicial da reserva, auditoria e notificação
quando a reserva vence.

Esse cenário não utiliza HTTP e não força ambas as ordens de execução
em cada tipo de recurso.

## 8. Docker e Testcontainers

Arquivos: Dockerfile.testes, .dockerignore e teste_testcontainers.py.

A imagem utiliza Python 3.14 slim, requirements.lock com hashes
e usuário sem privilégios de root.

O contexto exclui banco local, ambientes virtuais, backups e arquivos
de ambiente conforme .dockerignore.

O Testcontainers inicia a imagem, aguarda o término, coleta o log
e verifica código de saída zero e a presença dos 292 testes esperados.

A execução local foi informada como aprovada.
A execução push #1 do commit b1b308a também passou na CI.

Após as correções de instalação e YAML, foi informada execução verde
no commit 1e42442.

SQLite é utilizado dentro do container. Não há servidor PostgreSQL
ou MySQL separado, nem montagem do banco local do computador.

Limitações:

- Imagem-base não fixada por digest no Dockerfile.
- Dependências externas do Testcontainers sem lock completo com hashes.
- Quantidade esperada precisa acompanhar alterações da suíte.
- Aceitação dessa abordagem frente ao requisito acadêmico deve ser confirmada.

## 9. Segurança

Controles e cenários verificados:

- Hash de senhas.
- Autenticação, autorização e usuário ativo.
- Isolamento por proprietário e responsável vinculado.
- Proteção CSRF e renovação do token após login.
- Recusa de token anterior e de outra sessão nos cenários testados.
- Tentativas de injeção SQL no login.
- Escape de HTML no nome do recurso em duas páginas.

| Dependências auditadas | Evidência | Resultado registrado |
| --- | --- | --- |
| requirements.lock | auditoria_dependencias.json | Nenhuma vulnerabilidade conhecida reportada |
| requirements-e2e.lock | auditoria_dependencias_e2e.json | Nenhuma vulnerabilidade conhecida reportada |

Os resultados dependem das versões e da base consultada na execução.
Não abrangem automaticamente o binário Chromium, o sistema operacional
da imagem Docker ou o ambiente externo Testcontainers.

Permanecem pendentes revisão completa de segurança, configuração
de implantação, avaliação de limitação de tentativas de login
e ampliação dos campos e páginas verificados.

Não foi realizado teste de invasão completo.

## 10. Instalação limpa e recuperação de dados

### Instalação

No commit c84dac2, foi utilizado clone separado em diretório temporário,
com ambiente virtual e banco novos, no mesmo computador Windows.

Foram confirmados:

- Instalação das dependências.
- Criação das tabelas e exemplos.
- Criação de administrador e login.
- Criação da reserva nº 1 da Sala 101.
- Consulta da reserva aprovada.

Período da reserva: 03/11/2026, das 14h às 15h.

Essa evidência não representa instalação em outra máquina
nem validação da futura release.

### Backup e restauração

O script validar_backup.py foi executado sobre o banco do clone separado.

Foram conferidos integridade da origem, backup temporário,
restauração reaberta, estrutura e dados, com sete tabelas da aplicação.
A origem foi aberta somente para leitura.

Quatro testes verificam preservação da estrutura e dados,
arquivo inexistente, diretório e arquivo inválido.

Não equivale a política de backup persistente nem a recuperação
completa da aplicação após desastre.

## 11. Desempenho

### Execuções planejadas

Referência: docs/performance/resultado-01.md, registrado em 49f9268.

Ambiente: Windows, JMeter 5.6.3 e Flask com debug desligado.
Aplicação e gerador de carga no mesmo computador.

Cenário:

- GET /login.
- Dez usuários virtuais.
- Subida gradual de cinco segundos.
- Duração configurada de 60 segundos.
- Pausa de um segundo entre consultas.
- Verificação de HTTP 200 e texto Acesso ao sistema.

Critérios definidos antes das duas execuções:

- Zero erros.
- p95 até 500 ms.
- Pelo menos 500 amostras por execução.

| Execução | Amostras | Erros | Média (ms) | p95 (ms) | Máximo (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 | 85 |
| 2 | 565 | 0 | 8,11 | 19 | 69 |

As duas execuções atenderam aos critérios desse cenário.

Não medem autenticação por POST, navegação autenticada, operações
de reserva, acesso pela internet ou capacidade máxima de produção.

### Ensaios exploratórios anteriores

O cenário anterior sem pausa registrou 17.633 amostras,
com 1.289 falhas de conexão e taxa de falhas de 7,31%.

As mensagens incluíam java.net.BindException e
Address already in use: connect. A causa permanece não confirmada.

O ensaio anterior com pausa registrou 570 amostras sem falhas,
média de 5,49 ms e p95 de 8 ms.

A pausa reduziu a carga oferecida. Resultados posteriores não demonstram
correção da causa das falhas do ensaio sem pausa.

Esses ensaios permanecem históricos e separados das medições planejadas.

## 12. Defeitos e limitações

Registros detalhados em DEFEITOS.md:

| Registro | Problema | Situação registrada |
| --- | --- | --- |
| DEF01 | Material em uso desaparecia de Ativas após o prazo | Corrigido no escopo verificado |
| DEF02 | Nome do template diferente do include | Corrigido no escopo verificado |
| DEF03 | Conexões impediam limpeza no Windows | Corrigido no escopo verificado |
| DEF04 | Sintaxe YAML impedia a CI | Corrigido no escopo verificado |
| DEF05 | Caracteres e formatação corrompidos | Corrigido nos trechos conferidos |
| INV01 | Falhas no ensaio sem pausa | Investigação pendente |

Limitações funcionais e técnicas:

- Gestão completa de usuários e edição/desativação de recursos pela interface.
- Fluxos adicionais de navegador e tamanhos de tela.
- Carga dos fluxos autenticados e de reserva.
- Cobertura incompleta de scripts administrativos e migrações.
- Revisão adicional de segurança e implantação.
- Conferência da proteção da main e dos checks obrigatórios.

## 13. Fechamento acadêmico pendente

- Consolidar RTM, plano de testes e documentação de segurança.
- Conferir a documentação das rotas.
- Confirmar as equivalências das ferramentas da disciplina.
- Registrar revisão real por outro integrante.
- Confirmar nomes completos e contribuições individuais.
- Conferir o conteúdo antes da publicação do repositório.
- Integrar o pull request revisado e obter CI verde na main.
- Validar a candidata em clone limpo.
- Registrar decisão de qualidade e riscos com responsáveis.
- Criar tag anotada e vincular as evidências ao commit avaliado.
- Realizar o envio pelo integrante escolhido pelo grupo.

A autorização informada para Python não comprova aceitação automática
de todas as substituições específicas de ferramentas.

## 14. Parecer técnico

As evidências sustentam a demonstração acadêmica dos fluxos verificados,
com 292 testes registrados, metas de cobertura atendidas, concorrência
HTTP, Chromium, Testcontainers e Quality Gate aprovados nas versões
identificadas.

Também existem evidências de instalação limpa, recuperação SQLite
e duas medições planejadas da página de login.

O pacote permanece em preparação para revisão e decisão do grupo.
Não se declara atendimento integral do enunciado, aprovação formal
ou prontidão para produção.

## 15. Referências

- [Índice de evidências](docs/evidencias/README.md)
- [Checklist de entrega](docs/entrega/checklist.md)
- [README](README.md)
- [Changelog](CHANGELOG.md)
- [Plano de testes](PLANO_TESTES.md)
- [Rastreabilidade](RTM.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Segurança](SEGURANCA.md)
- [Instalação limpa](VALIDACAO_INSTALACAO.md)
- [Carga planejada](docs/performance/resultado-01.md)
- [Desempenho histórico](performance/README.md)
- [Pull request](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Sonar do PR](https://sonarcloud.io/dashboard?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)