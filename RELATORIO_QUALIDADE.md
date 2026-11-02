# Relatório de qualidade — Organização de Recursos

**Data:** 02/11/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.  
**Versão de referência:** e97a0a1, branch funcionalidade/login.  
**Pull Request:** nº 1.

## 1. Objetivo

Consolidar as evidências de qualidade da versão avaliada, incluindo testes, cobertura, análise estática, segurança, desempenho, defeitos e limitações.

Este relatório distingue resultados observados de verificações ainda pendentes. Não representa aprovação formal do grupo nem comprova atendimento integral do enunciado.

## 2. Sistema avaliado

Aplicação web em Python e Flask para organizar reservas de salas, professores e materiais.

A implementação inclui autenticação, perfis, cadastro e consulta de recursos, disponibilidade, reservas, aprovação, manutenção, movimentação de materiais, auditoria, notificações internas e relatórios.

A persistência utiliza SQLAlchemy Core e SQLite.

A arquitetura está documentada em ARQUITETURA.md. Requisitos e regras críticas estão relacionados aos testes em RTM.md.

## 3. Evidências da versão de referência

| Evidência | Identificação | Resultado |
| --- | --- | --- |
| Integração contínua de push | GitHub Actions #134, commit e97a0a1 | Success |
| Testes Python e cobertura | Job da execução #134 | Aprovado |
| Navegador Chromium | Job da execução #134 | Aprovado |
| Relatórios de cobertura | Execução #134 | Um artefato exibido |
| Análise Sonar do PR | Check associado ao commit e97a0a1 | Quality Gate passed |

A execução #134 é de push. A evidência do Sonar foi conferida separadamente nos checks do Pull Request.

O tempo total exibido da execução #134 foi de 1 minuto e 6 segundos. Esse valor inclui etapas de preparação e não equivale à duração isolada da suíte.

## 4. Estratégia de testes

Foram utilizadas verificações de:

- Regras de negócio.
- Integração com SQLite temporário.
- Rotas com o cliente Flask.
- Perfis, propriedade e vínculo com recursos.
- Valores-limite de períodos.
- Transições de estado.
- Concorrência no serviço.
- Rollback após falhas simuladas.
- Fluxo de navegador.
- Segurança em cenários específicos.
- Desempenho exploratório.

Muitos testes de serviço utilizam persistência real temporária. Por isso, a suíte não deve ser apresentada integralmente como testes unitários isolados.

A estratégia e os critérios estão em PLANO_TESTES.md.

## 5. Resultados funcionais e de regressão

### Execuções locais registradas

| Execução | Resultado |
| --- | --- |
| test_consulta.py | 24 testes aprovados em 16,051 segundos |
| test_edicao_http.py | 12 testes aprovados em 3,490 segundos |
| Suíte após os testes adicionais de login | 286 testes aprovados em 121,250 segundos |
| Teste de escape de HTML acrescentado posteriormente | Um teste aprovado em 0,382 segundo, com dois cenários |
| Teste de navegador em 02/11/2026 | Um teste aprovado em 20,869 segundos |

A execução completa local de 286 testes precede a inclusão do teste de escape de HTML.

A CI da versão e97a0a1 apresentou aprovação dos testes Python. A tela de resumo conferida não exibe a quantidade de métodos executados; este relatório não atribui uma nova contagem a essa execução.

### Cenários abrangidos

- Login válido, inválido e usuário inativo.
- Restrições por perfil, propriedade e vínculo.
- Validação de cadastro e filtros.
- Criação, edição e cancelamento.
- Bloqueio por sobreposição.
- Horários consecutivos.
- Disputa simultânea no serviço.
- Aprovação e rejeição.
- Bloqueio por manutenção.
- Movimentações de materiais.
- Não comparecimento de materiais.
- Auditoria e notificações.
- Relatórios e conflitos evitados.
- Migração específica da auditoria.

A cobertura dos cenários não implica verificação de todas as combinações possíveis.

## 6. Cobertura

### Execução #134 — commit e97a0a1

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

Os resultados pertencem à execução identificada.

Medições anteriores apresentaram outros valores, como 95,39% de ramificações. Esses resultados permanecem históricos e não substituem o valor de 95,74% observado na execução #134.

A cobertura Python não mede HTML, CSS ou JavaScript. Também não demonstra cobertura integral dos demais scripts administrativos.

Cobertura elevada não comprova ausência de defeitos.

## 7. Análise estática

### Sonar — commit e97a0a1

| Indicador | Resultado exibido |
| --- | ---: |
| Quality Gate | Passed |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Security Hotspots | 0 |
| Cobertura no código novo | 83,8% |
| Duplicação no código novo | 0,0% |

A cobertura do Sonar utiliza um escopo diferente da cobertura total apresentada pelo coverage.py. Os percentuais não devem ser tratados como medições equivalentes.

Zero novos problemas e zero hotspots não comprovam ausência de vulnerabilidades.

O resultado pertence ao Pull Request e à versão indicada. Não representa uma análise já executada na main após merge.

## 8. Teste de navegador

Ferramenta: Playwright com Chromium.

Arquivo: e2e/test_fluxo_reserva.py.

Fluxo verificado:

1. Login com senha incorreta.
2. Login válido.
3. Criação de reserva.
4. Consulta da reserva.
5. Tentativa de reserva conflitante.
6. Cancelamento com confirmação.
7. Consulta de Ativas e Histórico.
8. Conferência de registros associados no banco de teste.

O cenário inicia servidor HTTP local e SQLite temporário.

Resultados:

- Execução local de 02/11/2026: um teste aprovado em 20,869 segundos.
- Job de Chromium da execução #134: aprovado.

Limitações:

- Um fluxo principal automatizado.
- Somente Chromium na evidência.
- Aprovação, edição e movimentação de materiais ainda sem demonstração E2E equivalente.
- Ambiente de produção não avaliado.

## 9. Segurança

### Controles e testes

- Hash de senhas.
- Autenticação e autorização.
- Verificação de usuário ativo.
- Isolamento por proprietário e responsável vinculado.
- Proteção CSRF.
- Recusa de token pertencente a outra sessão.
- Renovação de token após login.
- Recusa do token anterior no logout.
- Tentativas de injeção SQL no login.
- Escape de HTML no nome do recurso em duas páginas.

### Dependências

O relatório auditoria_dependencias.json fornecido apresentou:

- Dez dependências analisadas.
- Nenhuma vulnerabilidade conhecida reportada.
- Nenhuma correção indicada.

A auditoria refere-se a requirements.lock e à base consultada no momento da execução.

Não está demonstrada nesse JSON a auditoria do requirements-e2e.lock.

### Limitações

- Revisão completa de segurança pendente.
- Configuração de HTTPS e cookies para implantação pendente.
- Limitação de tentativas de login pendente de avaliação.
- Ampliar campos e páginas verificados.
- Não foi realizado um teste de invasão completo.

Detalhes em SEGURANCA.md.

## 10. Desempenho

Os ensaios utilizaram JMeter 5.6.3 e GET /login, com cliente e servidor na mesma máquina.

Configuração comum:

- Dez usuários.
- Ramp-up de cinco segundos.
- Duração configurada de 60 segundos.
- Verificação de HTTP 200 e texto Acesso ao sistema.

### Comparação das execuções

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
- Taxa aproximada no resumo CLI: 9,5 requisições por segundo.

No cenário sem pausa, as falhas apresentaram java.net.BindException e a mensagem Address already in use: connect.

A causa permanece não confirmada.

A pausa reduziu a carga oferecida. O resultado posterior não comprova correção da causa anterior.

Os ensaios foram exploratórios, sem critério de aceitação definido previamente. Não permitem concluir capacidade de produção ou desempenho de autenticação e reservas.

Detalhes e arquivos em performance/README.md.

## 11. Defeitos e retestes

| Registro | Problema | Situação |
| --- | --- | --- |
| DEF01 | Material em uso desaparecia de Ativas após o prazo | Corrigido no escopo verificado |
| DEF02 | Nome do template compartilhado diferente do include | Corrigido no escopo verificado |
| DEF03 | Conexões abertas impediam limpeza dos testes no Windows | Corrigido no escopo verificado |
| DEF04 | Sintaxe YAML impedia execução da CI | Corrigido no escopo verificado |
| DEF05 | Caracteres e formatação corrompidos na documentação | Corrigido nos trechos conferidos |
| INV01 | Falhas de conexão no ensaio sem pausa | Investigação pendente |

O detalhamento de reprodução, correção e evidências está em DEFEITOS.md.

Também foi identificada uma alteração local acidental em templates/novo_recurso.html, contendo texto de um comando. O diff foi conferido e o arquivo restaurado à versão do Git antes desta consolidação.

O registro não representa uma contagem completa de todos os defeitos possíveis.

## 12. Documentação consolidada

| Documento | Finalidade |
| --- | --- |
| README.md | Instalação, execução e fluxos |
| RTM.md | Requisitos, regras e evidências |
| RTM_historico.md | Evidências históricas |
| ARQUITETURA.md | C4, sequências, decisões e riscos |
| PLANO_TESTES.md | Estratégia e critérios |
| DEFEITOS.md | Problemas, correções e investigações |
| SEGURANCA.md | Escopo e resultados de segurança |
| performance/README.md | Ensaios de desempenho |
| auditoria_dependencias.json | Resultado da auditoria de dependências |

A existência desses documentos não substitui a revisão de sua correspondência com o enunciado e com a versão entregue.

## 13. Pendências e riscos residuais

- Revisão por outro integrante ainda sem registro.
- Revisão final da rastreabilidade de todas as regras críticas.
- Banco em container ou alternativa aceita ainda não demonstrado.
- Concorrência por HTTP e entre manutenção e reserva.
- Ampliação dos testes unitários totalmente isolados.
- Ampliação de fluxos, navegadores e tamanhos de tela.
- Testes dos demais scripts administrativos e migrações.
- Restauração de backup.
- Critérios prévios e novos cenários de desempenho.
- Investigação das falhas de conexão sem pausa.
- Revisão adicional de segurança e dependências de E2E.
- Gestão completa de usuários e recursos pela interface.
- Conferência de proteção da main e verificações obrigatórias.
- Aceitação das substituições de ferramentas conforme a disciplina.

Essas pendências impedem afirmar atendimento integral de todos os critérios do trabalho.

## 14. Parecer técnico

As evidências disponíveis sustentam a demonstração acadêmica dos fluxos implementados e verificados.

A versão e97a0a1 apresentou testes Python e Chromium aprovados na execução #134, metas de cobertura atendidas e Quality Gate do Sonar aprovado.

A recomendação é prosseguir com a revisão por pares e a avaliação dos critérios de entrega, mantendo as limitações explícitas.

Este parecer não declara atendimento integral do enunciado, aprovação formal do grupo ou prontidão para produção.

A decisão de entrega deve considerar as pendências registradas e os critérios do professor.

## 15. Referências

- [Repositório](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request nº 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [Execução #134](https://github.com/Arthurmrsilva/organizacao-recursos/actions/runs/41486562302)
- [Sonar do PR nº 1](https://sonarcloud.io/summary/overall?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)
- [Plano de testes](PLANO_TESTES.md)
- [Rastreabilidade](RTM.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Segurança](SEGURANCA.md)
- [Desempenho](performance/README.md)