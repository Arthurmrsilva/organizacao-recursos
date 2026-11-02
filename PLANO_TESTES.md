# Plano de testes — Organização de Recursos

**Data:** 02/11/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

## 1. Objetivo

Verificar as regras de reserva, o controle de acesso, a integridade dos registros e os principais fluxos do sistema.

Este plano consolida a estratégia utilizada e as verificações ainda necessárias. Foi documentado após parte das execuções; não representa planejamento prévio de todos os testes realizados.

Os resultados observados estão em RTM.md e nos relatórios associados.

## 2. Escopo

- Autenticação, sessão e autorização.
- Cadastro e consulta de recursos.
- Pesquisa por disponibilidade.
- Criação, edição e cancelamento de reservas.
- Aprovação e rejeição.
- Manutenção.
- Retirada, devolução e não comparecimento de materiais.
- Auditoria e notificações.
- Relatórios e conflitos evitados.
- Migração da auditoria com testes específicos.
- Fluxo principal no navegador.
- Segurança e desempenho nos cenários documentados.

Não estão demonstrados testes completos de implantação de produção, recuperação de desastre ou todas as combinações de dispositivos e navegadores.

## 3. Priorização por risco

| Prioridade | Risco | Verificação principal |
| --- | --- | --- |
| Alta | Duas reservas aceitas para o mesmo recurso e período | Sobreposição e concorrência |
| Alta | Usuário altera dados alheios | Autorização por propriedade e vínculo |
| Alta | Operação sem autenticação ou CSRF válido | Testes negativos das rotas |
| Alta | Reserva alterada sem auditoria correspondente | Transação e rollback |
| Alta | Transição de estado inválida | Estados permitidos e recusas |
| Média | Recurso indisponível aparece na pesquisa | Filtros e manutenção |
| Média | Indicador incorreto | Contagens, limites de datas e arredondamento |
| Média | Fluxo falha no navegador | Teste ponta a ponta |
| Média | Degradação sob carga | Ensaios controlados de desempenho |

A prioridade foi consolidada neste documento e precisa de revisão pelo grupo.

## 4. Níveis e ferramentas

| Tipo | Abordagem | Limite |
| --- | --- | --- |
| Regras e integração | unittest e SQLite temporário | Muitos testes utilizam persistência real |
| Rotas HTTP | Cliente de testes Flask | Não executa JavaScript |
| Navegador | Playwright com Chromium e servidor local | Um fluxo principal automatizado |
| Concorrência | Solicitações simultâneas no serviço | Não demonstra concorrência por HTTP |
| Cobertura | coverage.py com linhas e ramificações | Escopo Python definido |
| Análise estática | SonarQube Cloud | Depende da versão analisada |
| Segurança | Testes específicos e pip-audit | Cobertura parcial de ameaças |
| Desempenho | JMeter | GET /login em ambiente local |
| Verificação manual | Interface e registros persistidos | Evidências devem identificar cenário e versão |

## 5. Técnicas utilizadas

- Particionamento de entradas válidas e inválidas.
- Valores-limite de datas, horários e períodos.
- Combinações de perfil, vínculo e propriedade.
- Transições de estado permitidas e proibidas.
- Cenários negativos de autenticação e CSRF.
- Verificação de persistência e ausência de alterações nas recusas.
- Falhas simuladas para verificar rollback.
- Concorrência no serviço.
- Regressão após correções e refatorações.
- subTest para agrupar variações de um cenário.

A cobertura de código complementa essas técnicas; não substitui a avaliação das regras de negócio.

Testes que utilizam banco real temporário também verificam integração. Não devem ser classificados integralmente como testes unitários isolados.

## 6. Cenários críticos

| ID | Cenário | Resultado esperado | Rastreabilidade |
| --- | --- | --- | --- |
| CT01 | Login válido, inválido e usuário inativo | Somente credenciais válidas de usuário ativo autenticam | RF01 |
| CT02 | POST sem token ou com token inválido | Recusa sem operação indevida | RF01 |
| CT03 | Token pertencente a outra sessão | Autenticação recusada | RF01 |
| CT04 | Cadastro por perfil não administrador | Acesso recusado e nenhum recurso criado | RF02 |
| CT05 | Período com término não posterior ao início | Operação recusada | RC01 |
| CT06 | Reserva sobreposta no mesmo recurso | Operação recusada | RF05, RC02 |
| CT07 | Horários consecutivos | Ausência de conflito por simples contato no limite | RC02 |
| CT08 | Duas solicitações simultâneas | Uma aceita e outra bloqueada | RF06, RC03 |
| CT09 | Reserva durante manutenção | Operação recusada | RF08, RC04 |
| CT10 | Aprovação por responsável sem vínculo | Operação recusada | RF07, RC07 |
| CT11 | Edição ou cancelamento por outro usuário | Acesso recusado e dados preservados | RF04 |
| CT12 | Edição ou cancelamento após início | Operação recusada | RC08 |
| CT13 | Retirada e devolução de material | Transições válidas e auditoria | RF09, RC05, RC09 |
| CT14 | Não comparecimento antes e no limite do término | Recusa antes; aceitação no limite para perfil autorizado e reserva elegível | RC06 |
| CT15 | Falha na auditoria ou notificação | Rollback da operação correspondente | RF10, RF11 |
| CT16 | Consulta ou leitura de aviso alheio | Aviso não exposto e operação recusada | RF11 |
| CT17 | Relatório com datas inválidas e limites de período | Validação e contagens corretas | RF12 |
| CT18 | Tentativa bloqueada por sobreposição | Registro do conflito sem alterar a reserva | RF05, RF12 |
| CT19 | Nome de recurso contendo HTML | Saída escapada nas páginas verificadas | RF13 |
| CT20 | Login, criação, conflito e cancelamento no Chromium | Fluxo completo com registros coerentes | RF01, RF04, RF05 |

Esta tabela define cenários e expectativas. O estado da implementação e das evidências deve ser consultado em RTM.md; a tabela não declara aprovação automática de todos os casos.

## 7. Ambiente e dados

### Ambiente local

- Windows.
- Python 3.14.6 no ambiente virtual.
- Flask e SQLAlchemy Core.
- SQLite.
- Chromium instalado pelo Playwright.
- JMeter 5.6.3 para os ensaios registrados.

### Integração contínua

- GitHub Actions em Ubuntu.
- Python 3.14.
- Dependências instaladas por locks com hashes.
- Chromium executado com suporte de tela virtual.

### Preparação dos dados

- Utilizar usuários ativos e inativos.
- Variar ADMIN, RESPONSAVEL e SOLICITANTE.
- Preparar recursos comuns, restritos, ativos e inativos.
- Variar responsável vinculado e não vinculado.
- Preparar períodos futuros, limites exatos e reservas iniciadas.
- Utilizar todos os estados relevantes.
- Isolar os registros de teste em bancos temporários.

A aplicação possui criação de estrutura durante a importação. A preparação do ambiente deve considerar esse efeito colateral e preservar bases importantes.

Não executar cenários de escrita ou carga sobre dados importantes sem isolamento e preparação específicos.

## 8. Critérios de entrada

Antes de uma execução:

- Identificar versão e branch.
- Instalar as dependências previstas.
- Preparar ambiente e dados necessários.
- Confirmar o isolamento do cenário.
- Definir resultado esperado.
- Verificar disponibilidade das ferramentas utilizadas.

Para novos ensaios de desempenho, definir antecipadamente carga, duração, pausas, métricas e critérios de aceitação.

## 9. Critérios de saída

| Critério | Evidência necessária |
| --- | --- |
| Testes da versão de entrega aprovados | Logs da execução identificada |
| Cobertura mínima de 80% de linhas | Relatório no escopo definido |
| Cobertura mínima de 70% de ramificações | Relatório no escopo definido |
| Quality Gate aprovado | Análise associada à versão de entrega |
| Regras críticas rastreadas | Revisão de RC01 a RC09 na RTM |
| Defeitos críticos conhecidos tratados | Registro de defeitos e decisão documentada |
| Limitações e investigações identificadas | RTM, DEFEITOS e relatório final |
| Revisão por outro integrante | Registro real de revisão |

O atendimento de cada critério deve ser conferido antes da entrega. Este plano não declara que todos já foram atendidos.

## 10. Execução e regressão

Os comandos desta seção são instruções para futuras execuções. Sua presença no documento não significa que precisam ser executados a cada atualização.

### Suíte principal

Executar na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Navegador

Após instalar as dependências e o Chromium conforme README.md:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s e2e -v
```

O teste de navegador inicia servidor e banco temporários próprios.

### Cobertura

Utilizar os comandos de README.md para executar a suíte com coverage.py e gerar JSON, XML e HTML.

### Estratégia de reteste

1. Reproduzir ou identificar a falha.
2. Registrar resultado esperado e observado.
3. Aplicar a correção.
4. Executar os testes diretamente relacionados.
5. Executar regressão adequada ao impacto.
6. Registrar versão e resultado.

Alterações apenas de documentação exigem conferência de conteúdo, links e renderização, sem necessidade automática de repetir toda a suíte local.

### Execuções locais registradas

| Execução | Resultado observado |
| --- | --- |
| Suíte principal após os testes adicionais de login | 286 testes aprovados em 121,250 segundos |
| Teste de escape de HTML acrescentado posteriormente | Um teste aprovado em 0,382 segundo, com dois cenários |
| Teste de navegador em 02/11/2026 | Um teste aprovado em 20,869 segundos |

A execução de 286 testes precede a inclusão do teste de escape de HTML. Não é apresentada como uma execução completa posterior a essa inclusão.

O teste de navegador inclui respostas de erro esperadas para senha incorreta e reserva conflitante. Esses retornos são avaliados pelo cenário e não representam, por si só, falha do teste.

## 11. Segurança

Cenários registrados:

- Autenticação e autorização.
- CSRF ausente, inválido ou de outra sessão.
- Renovação de token após login.
- Tentativas de injeção SQL no login.
- Escape de HTML em duas páginas.
- Auditoria das dependências de requirements.lock.

O JSON fornecido da auditoria apresentou dez dependências sem vulnerabilidades conhecidas reportadas pela ferramenta no momento da consulta.

Pendências:

- Ampliar campos e páginas avaliados.
- Avaliar limitação de tentativas de login.
- Revisar cookies e HTTPS na implantação.
- Auditar também as dependências de E2E.
- Completar revisão de código e configuração.

Consulte SEGURANCA.md. Os cenários não representam teste de invasão completo.

## 12. Desempenho

Os ensaios realizados estão em performance/README.md e nos arquivos JTL.

Foram executados cenários GET /login com dez usuários e duração configurada de 60 segundos, com e sem pausa.

### Sem pausa

- 17.633 amostras.
- 16.344 respostas HTTP 200.
- 1.289 falhas de conexão.
- Taxa de falhas de 7,31%.
- Erro java.net.BindException.
- Causa não confirmada.

### Com pausa de um segundo

- 570 amostras.
- Todas com HTTP 200.
- Nenhuma falha registrada.
- Média de 5,49 ms.
- Percentil 95 de 8 ms.
- Máximo de 38 ms.

A pausa altera a carga oferecida. O resultado posterior não comprova correção da causa das falhas anteriores.

Esses ensaios foram exploratórios. Não havia critério de aceitação definido previamente.

Novos ensaios devem:

- Definir metas antes da execução.
- Preservar os resultados negativos.
- Registrar ambiente e versão.
- Repetir em condições controladas.
- Avaliar fluxos autenticados com dados isolados.
- Observar recursos e conexões do cliente e servidor.

## 13. Evidências e defeitos

Cada evidência deve identificar, quando aplicável:

- Cenário e requisito.
- Versão ou commit.
- Ambiente.
- Resultado esperado.
- Resultado observado.
- Data e origem da execução.

Defeitos e investigações são registrados em DEFEITOS.md.

Resultados históricos não devem ser apresentados como medições da versão atual. Uma mudança de cenário não comprova correção da causa de uma falha anterior.

## 14. Responsabilidades

A distribuição nominal das atividades deve ser confirmada pelo grupo.

| Atividade | Responsabilidade |
| --- | --- |
| Preparar e executar testes | Integrante executor |
| Registrar evidências | Integrante executor |
| Corrigir defeitos | Integrante responsável pela alteração |
| Revisar código, testes e documentação | Outro integrante |
| Decidir sobre pendências e entrega | Grupo |

A revisão por pares deve ser efetivamente realizada e registrada; não pode ser substituída pela aprovação automática da CI.

## 15. Lacunas conhecidas

- Ampliação dos testes unitários totalmente isolados.
- Concorrência por HTTP e entre manutenção e reserva.
- Banco em container ou alternativa aceita.
- Outros fluxos, navegadores e tamanhos de tela.
- Demais scripts administrativos e migrações.
- Restauração de backup.
- Critérios e cenários adicionais de desempenho.
- Revisão final de segurança.
- Revisão por pares e decisão final de qualidade.

## 16. Referências

- [README](README.md)
- [Rastreabilidade](RTM.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos e retestes](DEFEITOS.md)
- [Segurança](SEGURANCA.md)
- [Desempenho](performance/README.md)