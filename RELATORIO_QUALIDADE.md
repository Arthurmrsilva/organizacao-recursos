# Relatório de qualidade — Organização de Recursos

**Data:** 02/11/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.  
**Versão de referência dos testes:** 67b3d00, branch funcionalidade/login.  
**Última análise Sonar conferida:** 02737a6.  
**Pull Request:** nº 1.

## 1. Objetivo

Consolidar as evidências de testes, cobertura, análise estática, segurança, desempenho e correções.

Os resultados estão associados às versões efetivamente verificadas. Este relatório não representa aprovação formal do grupo nem atendimento integral do enunciado.

## 2. Sistema avaliado

Aplicação web em Python e Flask para organizar reservas de salas, professores e materiais.

Inclui autenticação, perfis, cadastro e consulta de recursos, disponibilidade, reservas, aprovação, manutenção, movimentação de materiais, auditoria, notificações internas e relatórios.

A persistência utiliza SQLAlchemy Core e SQLite.

A arquitetura está em ARQUITETURA.md. Os requisitos e as regras críticas estão em RTM.md.

## 3. Evidências mais recentes

| Evidência | Identificação | Resultado |
| --- | --- | --- |
| Suíte com cobertura na CI | Actions #146, commit 67b3d00 | 288 testes aprovados em 15,349 segundos |
| Concorrência por HTTP | Actions #146 | Aprovada |
| Navegador Chromium | Actions #146 | Aprovado |
| Execução completa do workflow | Actions #146, evento push | Success, duração total de 59 segundos |
| Relatórios de cobertura | Actions #146 | Um artefato exibido |
| Análise Sonar do PR | Commit 02737a6 | Quality Gate passed |
| Suíte em Docker após ajuste de segurança | Execução local apresentada | 287 testes aprovados em 180,651 segundos |
| Concorrência entre manutenção e reserva | Teste local incluído em 67b3d00 | Um método aprovado em 1,762 segundo, com três cenários |
| Auditoria das dependências de E2E | JSON registrado em 98d26d5 | Nenhuma vulnerabilidade conhecida reportada |

A duração total do workflow inclui preparação e demais etapas. Não equivale à duração isolada da suíte.

O Sonar foi conferido no commit 02737a6. Seu resultado não é atribuído automaticamente ao commit posterior 67b3d00.

## 4. Estratégia de testes

Foram utilizadas verificações de:

- Regras de negócio e integração com SQLite temporário.
- Rotas com o cliente Flask.
- Perfis, propriedade e vínculo.
- Valores-limite de datas e horários.
- Transições de estado.
- Concorrência no serviço e por HTTP.
- Concorrência entre manutenção e reserva.
- Rollback após falhas simuladas.
- Fluxo no navegador.
- Segurança em cenários específicos.
- Dependências Python.
- Execução da suíte em container.
- Desempenho exploratório.

Muitos testes utilizam persistência real temporária. A suíte não deve ser apresentada integralmente como testes unitários isolados.

A estratégia e os critérios estão em PLANO_TESTES.md.

## 5. Resultados funcionais e de regressão

### Resultado da CI

Na execução #146, commit 67b3d00:

- 288 testes aprovados.
- Duração da suíte: 15,349 segundos.
- Resultado: OK.
- Teste de concorrência HTTP aprovado em processo separado.
- Fluxo de navegador aprovado em job separado.

Os 288 testes não incluem o método HTTP executado separadamente nem o método de navegador.

Alguns métodos utilizam subTest. A contagem de métodos não equivale à quantidade total de variações verificadas.

### Execuções locais anteriores

| Execução | Resultado |
| --- | --- |
| test_consulta.py | 24 testes em 16,051 segundos |
| test_edicao_http.py | 12 testes em 3,490 segundos |
| Suíte antes do teste adicional de escape de HTML | 286 testes em 121,250 segundos |
| Escape de HTML | Um teste em 0,382 segundo, com dois cenários |
| Fluxo no navegador | Um teste em 20,869 segundos |
| Concorrência por HTTP | Um teste em 3,731 segundos |
| Suíte inicial em Docker | 287 testes em 186,330 segundos |
| Suíte em Docker após ajuste de segurança | 287 testes em 180,651 segundos |
| Concorrência entre manutenção e reserva | Um teste em 1,762 segundo, com três cenários |

Essas execuções pertencem às etapas indicadas. A execução Docker de 287 testes precede a inclusão do teste de concorrência entre manutenção e reserva.

### Cenários abrangidos

- Login válido, inválido e usuário inativo.
- Restrições por perfil, propriedade e vínculo.
- Cadastro, filtros e disponibilidade.
- Criação, edição e cancelamento.
- Sobreposição e horários consecutivos.
- Solicitações concorrentes de reserva.
- Aprovação e rejeição.
- Bloqueio por manutenção.
- Disputa entre manutenção e reserva.
- Movimentações e não comparecimento de materiais.
- Auditoria, notificações e rollback.
- Relatórios e conflitos evitados.
- Migração específica da auditoria.

Essas evidências não demonstram todas as combinações possíveis.

## 6. Cobertura

### Actions #146 — commit 67b3d00

| Métrica | Resultado | Meta | Avaliação |
| --- | ---: | ---: | --- |
| Linhas | 97,69% | 80% | Atendida |
| Ramificações | 95,74% | 70% | Atendida |

Escopo medido:

- app.py
- banco.py
- servico_reservas.py
- servico_materiais.py
- servico_relatorios.py
- atualizar_auditoria.py

A medição é produzida pela suíte principal. O teste HTTP e o teste de navegador são executados separadamente e não são somados a essa medição.

Os mesmos percentuais foram observados anteriormente na execução #134. Medições históricas com outros valores permanecem associadas às respectivas versões.

A cobertura Python não mede HTML, CSS ou JavaScript nem todos os scripts administrativos.

Cobertura elevada não comprova ausência de defeitos.

## 7. Análise estática

### Sonar — commit 02737a6

| Indicador | Resultado exibido |
| --- | ---: |
| Quality Gate | Passed |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Security Hotspots | 0 |
| Cobertura no código novo | 83,8% |
| Duplicação no código novo | 0,0% |

O commit anterior 73a556e apresentou Quality Gate reprovado, com cobertura de código novo abaixo da meta e apontamentos no Dockerfile.

O ajuste posterior:

- Substituiu a cópia de todo o diretório por cópias dos arquivos e diretórios necessários.
- Definiu usuário sem privilégios de root para executar os testes no container.
- Classificou teste_concorrencia_http.py como arquivo de teste no Sonar.

A análise conferida após o ajuste apresentou aprovação.

A cobertura de código novo do Sonar e a cobertura dos módulos medida pelo coverage.py possuem escopos diferentes.

Zero novos problemas e zero hotspots não comprovam ausência de vulnerabilidades.

Não está registrada aqui uma análise da main após merge.

## 8. Navegador e HTTP

### Fluxo no Chromium

Ferramenta: Playwright.

Arquivo: e2e/test_fluxo_reserva.py.

Fluxo verificado:

1. Login com senha incorreta.
2. Login válido.
3. Criação de reserva.
4. Consulta da reserva.
5. Tentativa de reserva conflitante.
6. Cancelamento com confirmação.
7. Consulta de Ativas e Histórico.
8. Conferência dos registros associados no banco temporário.

O job de Chromium da execução #146 foi aprovado.

A evidência cobre um fluxo principal em um navegador. Aprovação, edição e movimentação de materiais ainda não possuem demonstração E2E equivalente.

### Concorrência por HTTP

Arquivo: teste_concorrencia_http.py.

O teste utiliza servidor HTTP local com atendimento em threads, duas sessões autenticadas e SQLite temporário.

Os clientes coordenam o envio de duas solicitações para o mesmo recurso e período.

Resultado esperado e observado:

- Uma solicitação aceita.
- Outra recusada por conflito.
- Uma reserva persistida.
- Auditoria e notificação da reserva aceita.
- Registro da tentativa bloqueada.

O teste passou localmente e na CI.

A coordenação dos clientes não garante uma ordem específica de execução interna. Uma execução aprovada não comprova ausência de todas as condições de corrida.

## 9. Concorrência entre manutenção e reserva

Arquivo: tests/test_concorrencia_manutencao.py.

O teste executa duas operações concorrentes no serviço:

- Cadastro de manutenção pelo administrador.
- Criação de reserva pelo solicitante.

Os cenários utilizam SALA, PROFESSOR e MATERIAL, com o mesmo período em cada disputa.

A verificação exige:

- Exatamente uma operação aceita.
- Exatamente uma operação recusada.
- Ausência de reserva e manutenção aceitas simultaneamente para o período.
- Preservação das datas.
- Estado inicial correto quando a reserva vence.
- Auditoria e notificação quando a reserva é aceita.

O método passou localmente e foi incluído na suíte aprovada da execução #146.

Essa evidência verifica concorrência no serviço com SQLite. Não representa um teste HTTP de disputa entre manutenção e reserva.

## 10. Execução em container

Arquivos:

- Dockerfile.testes
- .dockerignore

A imagem utiliza Python 3.14 slim e instala requirements.lock com verificação de hashes.

O container executa a suíte como usuário sem privilégios de root.

O banco local, ambientes virtuais, backups e arquivos de ambiente são excluídos do contexto conforme .dockerignore.

### Comandos

```powershell
docker build -f Dockerfile.testes -t organizacao-recursos-testes .
docker run --rm organizacao-recursos-testes
```

A execução local após o ajuste apresentou 287 testes aprovados em 180,651 segundos.

Essa execução utilizou SQLite dentro do ambiente de testes em container. Não deve ser apresentada como implementação de Testcontainers ou integração com um servidor de banco externo.

A tag da imagem-base não está fixada por digest neste Dockerfile.

## 11. Segurança

### Controles e testes

- Hash de senhas.
- Autenticação e autorização.
- Verificação de usuário ativo.
- Isolamento por proprietário e responsável vinculado.
- Proteção CSRF.
- Recusa de token de outra sessão.
- Renovação do token após login.
- Recusa do token anterior no logout.
- Tentativas de injeção SQL no login.
- Escape de HTML no nome do recurso em duas páginas.

### Dependências

| Arquivo auditado | Evidência | Resultado |
| --- | --- | --- |
| requirements.lock | auditoria_dependencias.json | Nenhuma vulnerabilidade conhecida reportada |
| requirements-e2e.lock | auditoria_dependencias_e2e.json, commit 98d26d5 | Nenhuma vulnerabilidade conhecida reportada |

A auditoria de E2E também incluiu Playwright 1.64.1 e suas dependências Python listadas no relatório.

Os resultados dependem das versões e da base consultada no momento da execução. A auditoria do lock Python não equivale à auditoria do navegador Chromium nem da imagem Docker.

### Limitações

- Revisão completa de segurança pendente.
- Configuração de HTTPS e cookies para implantação pendente.
- Limitação de tentativas de login pendente de avaliação.
- Ampliação dos campos e páginas verificados.
- Ausência de teste de invasão completo.

Detalhes em SEGURANCA.md.

## 12. Desempenho

Os ensaios utilizaram JMeter 5.6.3 e GET /login, com cliente e servidor na mesma máquina.

Configuração comum:

- Dez usuários.
- Ramp-up de cinco segundos.
- Duração configurada de 60 segundos.
- Verificação de HTTP 200 e texto Acesso ao sistema.

| Indicador | Sem pausa | Pausa de um segundo |
| --- | ---: | ---: |
| Amostras | 17.633 | 570 |
| HTTP 200 | 16.344 | 570 |
| Falhas | 1.289 | 0 |
| Taxa de falhas | 7,31% | 0% |

No cenário com pausa:

- Média: 5,49 ms.
- Mediana: 5 ms.
- Percentil 95: 8 ms.
- Mínimo: 2 ms.
- Máximo: 38 ms.
- Taxa aproximada: 9,5 requisições por segundo.

No cenário sem pausa, as falhas apresentaram java.net.BindException e Address already in use: connect. A causa permanece não confirmada.

A pausa reduziu a carga oferecida. O resultado posterior não comprova correção da causa anterior.

Os ensaios foram exploratórios, sem critérios de aceitação definidos previamente. Não permitem concluir capacidade de produção nem desempenho dos fluxos autenticados e de reserva.

Detalhes em performance/README.md.

## 13. Defeitos, documentação e pendências

### Problemas registrados

| Registro | Problema | Situação |
| --- | --- | --- |
| DEF01 | Material em uso desaparecia de Ativas após o prazo | Corrigido no escopo verificado |
| DEF02 | Nome do template diferente do include | Corrigido no escopo verificado |
| DEF03 | Conexões impediam limpeza no Windows | Corrigido no escopo verificado |
| DEF04 | Sintaxe YAML impedia a CI | Corrigido no escopo verificado |
| DEF05 | Caracteres e formatação corrompidos | Corrigido nos trechos conferidos |
| INV01 | Falhas no ensaio sem pausa | Investigação pendente |

O detalhamento está em DEFEITOS.md.

Também foi restaurada uma alteração local acidental em templates/novo_recurso.html que continha texto de um comando.

### Documentação

- README.md: instalação, execução e fluxos.
- RTM.md: requisitos, regras e evidências.
- RTM_historico.md: resultados históricos.
- ARQUITETURA.md: arquitetura, decisões e riscos.
- PLANO_TESTES.md: estratégia e critérios.
- DEFEITOS.md: problemas e retestes.
- SEGURANCA.md: verificações de segurança.
- performance/README.md: ensaios de desempenho.
- Arquivos JSON: auditorias das dependências.

A correspondência entre os documentos e a versão de entrega ainda precisa de conferência final.

### Pendências

- Revisão por outro integrante, reservada para etapa posterior.
- Revisão final da rastreabilidade das regras críticas.
- Atendimento específico de Testcontainers ou alternativa aceita pelo professor.
- Ampliação dos testes unitários totalmente isolados.
- Ampliação de fluxos de navegador e tamanhos de tela.
- Testes dos demais scripts administrativos e migrações.
- Restauração de backup.
- Critérios prévios e novos cenários de desempenho.
- Investigação das falhas de conexão sem pausa.
- Revisão adicional de segurança.
- Gestão completa de usuários e recursos pela interface.
- Conferência da proteção da main e dos checks obrigatórios.
- Aceitação das substituições de ferramentas conforme a disciplina.
- Preparação da apresentação e revisão do material de entrega.

## 14. Parecer técnico

A versão 67b3d00 apresentou 288 testes aprovados na execução #146, metas de cobertura atendidas, concorrência HTTP aprovada e fluxo Chromium aprovado.

A análise Sonar conferida no commit 02737a6 apresentou Quality Gate aprovado.

Também existem evidências de execução da suíte em Docker, concorrência entre manutenção e reserva e auditoria das dependências de aplicação e E2E.

Esses resultados sustentam a demonstração acadêmica dos fluxos verificados.

As pendências permanecem explícitas. Este parecer não declara atendimento integral do enunciado, aprovação formal do grupo ou prontidão para produção.

## 15. Referências

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Versão dos testes](https://github.com/Arthurmrsilva/organizacao-recursos/commit/67b3d00)
- [Ajuste do Docker e Sonar](https://github.com/Arthurmrsilva/organizacao-recursos/commit/02737a6)
- [Auditoria de E2E](https://github.com/Arthurmrsilva/organizacao-recursos/commit/98d26d5)
- [Sonar do PR](https://sonarcloud.io/summary/overall?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)
- [Plano de testes](PLANO_TESTES.md)
- [Rastreabilidade](RTM.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Segurança](SEGURANCA.md)
- [Desempenho](performance/README.md)