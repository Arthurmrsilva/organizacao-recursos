# Organização de Recursos

## Estado da entrega — 10/11/2026

Decisão do grupo: **entrega acadêmica com ressalvas**.
Arthur registrou seu aceite; Nicolas e Robert confirmaram a concordância
com a entrega e as ressalvas, conforme comunicação de Arthur em 10/11/2026.

A última candidata publicada é a **v1.0.0-rc4**, commit
`ca08ea6132c462fec7228d22892f50ad8ae82926`.
Sua CI e seus relatórios estão na [release rc4](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc4).

Esta consolidação corrige referências documentais posteriores à rc4 e
prepara a **rc5**. A rc5 somente estará publicada após integração,
CI aprovada, criação da nova tag anotada e publicação da release.
As tags anteriores permanecem fixas.

Para avaliar uma candidata, use o commit e as execuções identificados
nas notas da respectiva release. Resultados anteriores mantêm sua versão
de origem. O envio pelo formulário ainda não tem comprovante neste registro.

Projeto da disciplina de Qualidade de Software — ADS, 4º semestre.

Sistema web para reservar salas, professores e materiais, evitar
sobreposições e controlar aprovação, manutenção e movimentação de materiais.

## Integrantes

- Arthur Mendes Ramos da Silva
- Nicolas Ferreira Souza
- Robert Santos de Oliveira

## Contribuições individuais — atualização de 10/11/2026

- **Nicolas Ferreira Souza:** Colaborou com ideias para a programação e com a definição visual da interface, incluindo as cores do CSS. Executou e documentou 21 cenários de testes funcionais dos perfis ADMIN e RESPONSAVEL, publicou o relatório por commit e pull request e participou da revisão do código.
- **Robert Santos de Oliveira:** Colaborou na elaboração dos diagramas e participou da revisão do projeto e do código.

As contribuições adicionais foram informadas por Arthur Mendes Ramos da Silva.
O relato funcional de Nicolas mantém o escopo de 21 cenários.
As confirmações de Nicolas e Robert sobre a entrega acadêmica com ressalvas,
comunicadas por Arthur em 10/11/2026, estão registradas na decisão de qualidade.
A concordância dos três integrantes está registrada.
Este registro atualiza as indicações anteriores sobre a participação e a
revisão dos integrantes, preservando os limites dos testes documentados.

## Funcionalidades

- Login e logout, senhas armazenadas como hash e proteção CSRF.
- Perfis ADMIN, RESPONSAVEL e SOLICITANTE.
- Cadastro de recursos pelo administrador.
- Pesquisa por tipo, capacidade, localização, competência e disponibilidade.
- Criação, edição e cancelamento das próprias reservas.
- Bloqueio de sobreposição e permissão de horários consecutivos.
- Aprovação e rejeição pelo responsável vinculado.
- Bloqueio de recursos em manutenção.
- Retirada, devolução e não comparecimento de materiais.
- Auditoria das operações de reserva.
- Notificações internas.
- Relatórios de contagens, horas previstas e conflitos evitados.

A gestão completa de usuários, a edição e a desativação de recursos
pela interface permanecem como limitações.

## Tecnologias

| Finalidade | Tecnologia |
| --- | --- |
| Aplicação | Python 3.14 e Flask |
| Persistência | SQLAlchemy Core e SQLite |
| Interface | Jinja, HTML, CSS e JavaScript |
| Testes | unittest e Playwright com Chromium |
| Cobertura | Coverage.py |
| Containers | Docker e Testcontainers Python |
| Integração contínua | GitHub Actions |
| Análise estática | SonarQube Cloud |
| Desempenho | Apache JMeter |
| Auditoria de dependências | pip-audit |

Conforme informado pelo grupo, o professor autorizou o uso de qualquer
linguagem de programação. O projeto utiliza Python.

Neste projeto, unittest executa os testes e Coverage.py mede a cobertura,
publicando relatórios JSON, XML e HTML pela integração contínua.
Essas ferramentas cumprem os papéis de testes e cobertura apresentados
no roteiro com Maven e JaCoCo.

O projeto não executa Maven nem gera relatório JaCoCo.

## Instalação limpa no Windows

Pré-requisitos: Git e Python 3.14. O ambiente de desenvolvimento
utiliza Python 3.14.6.

### 1. Obter o projeto

Para reproduzir a candidata já publicada rc4:

```powershell
git clone --branch v1.0.0-rc4 --single-branch https://github.com/Arthurmrsilva/organizacao-recursos.git
cd organizacao-recursos
git rev-parse HEAD
```

Confira o SHA com o commit da rc4 informado acima. O aviso de detached HEAD
é esperado ao clonar uma tag. Quando a rc5 estiver publicada, use a tag rc5
e o SHA registrado nas notas dessa nova release.

### 2. Preparar o ambiente

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: --require-hashes -r requirements.lock
```

Não é necessário ativar o ambiente: os comandos usam seu executável.

### 3. Criar o banco e os exemplos

```powershell
.\.venv\Scripts\python.exe banco.py
.\.venv\Scripts\python.exe seed.py
```

O banco local é recursos.db. O seed cadastra Sala 101, Professor Carlos
e Projetor 01, verificando se os exemplos já existem.

Os exemplos não configuram automaticamente os responsáveis necessários
à aprovação de recursos restritos e professores.

A criação de tabelas não substitui migrações de bases antigas.
Para atualizar uma instalação existente, preserve backup e revise
os scripts administrativos antes de executá-los.

### 4. Criar administrador

```powershell
.\.venv\Scripts\python.exe criar_admin.py
```

Login: admin. O script solicita senha de pelo menos oito caracteres
e confirmação. A senha não aparece durante a digitação.

Se admin já existir, o script não altera seus dados.

### 5. Iniciar a aplicação

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5003 --no-debugger --no-reload
```

Acesse http://127.0.0.1:5003/login.

Mantenha o terminal aberto. Para encerrar, pressione Ctrl+C.
A execução direta de app.py utiliza a porta padrão 5000.

## Demonstração básica

1. Entrar com o administrador.
2. Consultar os recursos e selecionar uma sala comum.
3. Criar uma reserva para um período futuro válido.
4. Conferir a reserva em Minhas reservas.
5. Tentar outra reserva sobreposta e conferir a recusa.
6. Cancelar a reserva antes do início.
7. Conferir histórico, notificações e auditoria.

Para demonstrar aprovação, prepare um usuário RESPONSAVEL ativo
vinculado ao recurso. criar_admin.py prepara somente o administrador.

| Perfil | Operações principais |
| --- | --- |
| SOLICITANTE | Consultar recursos e gerenciar as próprias reservas |
| RESPONSAVEL | Avaliar solicitações e gerenciar materiais vinculados |
| ADMIN | Cadastrar recursos, registrar manutenção e consultar auditoria e relatórios |

As permissões também dependem do vínculo, da propriedade da reserva,
do prazo e do estado da operação.

## Interface HTTP

A aplicação utiliza páginas HTML e formulários, com sessão por cookie.
Não disponibiliza uma API REST JSON.

Os identificadores nas rotas são números inteiros. A tabela lista
as rotas da aplicação; arquivos estáticos são servidos separadamente
pelo Flask.

| Endereço | Método | Finalidade e acesso |
| --- | --- | --- |
| `/login` | GET e POST | Exibir formulário e autenticar usuário ativo |
| `/sair` | POST | Encerrar sessão |
| `/` | GET | Consultar recursos e aplicar filtros como usuário autenticado |
| `/recursos/novo` | GET e POST | Cadastrar recurso como ADMIN |
| `/reservas/nova` | GET e POST | Criar reserva como usuário autenticado |
| `/reservas` | GET | Consultar as próprias reservas |
| `/reservas/<reserva_id>/editar` | GET e POST | Editar a própria reserva, conforme prazo e situação |
| `/reservas/<reserva_id>/cancelar` | POST | Cancelar a própria reserva, conforme regras da operação |
| `/aprovacoes` | GET | Consultar solicitações como RESPONSAVEL vinculado |
| `/reservas/<reserva_id>/avaliar` | POST | Aprovar ou rejeitar solicitação como RESPONSAVEL vinculado |
| `/manutencoes` | GET e POST | Consultar e cadastrar manutenção como ADMIN |
| `/materiais` | GET | Consultar materiais como ADMIN ou RESPONSAVEL, respeitando o vínculo |
| `/materiais/<reserva_id>/movimentar` | POST | Registrar retirada, devolução ou não comparecimento como ADMIN ou RESPONSAVEL autorizado |
| `/auditoria` | GET | Consultar os 100 eventos mais recentes como ADMIN |
| `/notificacoes` | GET | Consultar os próprios avisos |
| `/notificacoes/<notificacao_id>/ler` | POST | Marcar uma notificação própria como lida |
| `/relatorios` | GET | Consultar indicadores como ADMIN |

### Parâmetros e formulários

- Consulta de recursos: `tipo`, `localizacao`, `competencia`, `capacidade`,
  `inicio` e `fim`.
- Consulta de reservas: `filtro` com valor `ativas`, `historico` ou `todas`.
- Consulta de relatórios: `inicio` e `fim`.
- Login: `login` e `senha`.
- Cadastro de recurso: `nome`, `tipo`, `localizacao`, `capacidade`,
  `competencia`, `restrito` e `responsavel_id`.
- Criação e edição de reserva: `recurso_id`, `inicio`, `fim` e `finalidade`.
- Avaliação de reserva: `decisao` com valor `APROVADA` ou `REJEITADA`.
- Cadastro de manutenção: `recurso_id`, `inicio`, `fim` e `motivo`.
- Movimentação de material: `acao` com valor `RETIRADA`, `DEVOLUCAO`
  ou `NAO_COMPARECEU`.

Todos os formulários POST exigem `csrf_token` válido da sessão.
O campo de recurso restrito utiliza o valor `sim` quando selecionado.

As operações também verificam propriedade, vínculo com o recurso,
período, disponibilidade e situação da reserva, conforme cada fluxo.

### Respostas HTTP

- 200: exibição normal de página.
- 302: redirecionamento, incluindo acesso sem autenticação às páginas
  protegidas e conclusão de operações por formulário.
- 400: token CSRF inválido ou dados inválidos nos fluxos que
  retornam erro diretamente.
- 401: login ou senha inválidos.
- 403: perfil sem permissão.
- 404: reserva ou notificação não encontrada para o usuário,
  nos fluxos que fazem essa verificação diretamente.

Cancelamento, avaliação e movimentação de materiais também podem
redirecionar após uma recusa de negócio. Nesses casos, a página de
destino apresenta a mensagem de erro; o redirecionamento sozinho
não significa que a operação foi aprovada.

## Testes Python

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

A suíte registrada contém 292 testes. Na validação de 03/11/2026,
no commit b55f1ef87ea97bb5fee3bf076a57cf0555656e74,
todos passaram em 86,353 segundos, em clone separado e ambiente
virtual novo no mesmo computador.

Consulte o [registro da validação](docs/entrega/validacao-2026-11-03.md).

Os testes preparados utilizam bancos temporários. Vários testes de rotas
simulam sessão; outros verificam autenticação real.

A aplicação cria a estrutura do banco durante a importação.
Execute testes em ambiente de desenvolvimento e preserve bases importantes.

### Concorrência por HTTP

```powershell
.\.venv\Scripts\python.exe teste_concorrencia_http.py
```

O teste utiliza duas sessões autenticadas, servidor HTTP e SQLite temporário.
Verifica que apenas uma das reservas concorrentes é aceita e confere
os registros de reserva, auditoria, notificação e conflito.

Esse teste é executado separadamente da suíte de 292 testes.

## Cobertura

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios,atualizar_auditoria,validar_backup -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m coverage report -m
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
.\.venv\Scripts\python.exe -m coverage xml -o coverage.xml
.\.venv\Scripts\python.exe -m coverage html -d htmlcov
```

Abra htmlcov/index.html.

Referência registrada da CI no commit da93d49:

- Linhas: 97,46%.
- Ramificações: 94,83%.
- Metas verificadas na CI: 80% de linhas e 70% de ramificações.

O escopo contém sete módulos Python. Não inclui HTML, CSS, JavaScript
nem todos os scripts administrativos.

A cobertura sobre código novo exibida no Sonar é uma métrica distinta.
Resultados devem ser associados ao commit e à execução de origem.

## Teste de navegador

```powershell
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: --require-hashes -r requirements-e2e.lock
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m unittest discover -s e2e -v
```

O teste inicia seu próprio servidor e banco temporário.
Verifica login inválido e válido, criação, consulta, conflito,
cancelamento e histórico, incluindo registros associados.

Não exige o servidor da porta 5003 aberto.

## Docker e Testcontainers

Pré-requisito: Docker com suporte a containers Linux em execução.
No Windows, foi utilizado Docker Desktop.

Construa a imagem na raiz do projeto:

```powershell
docker build -f Dockerfile.testes -t organizacao-recursos-testes .
```

Para executar diretamente:

```powershell
docker run --rm organizacao-recursos-testes
```

Para executar pelo Testcontainers:

```powershell
py -3.14 -m venv .venv-testcontainers
.\.venv-testcontainers\Scripts\python.exe -m pip install --only-binary=:all: testcontainers==4.15.0 docker==7.2.0
.\.venv-testcontainers\Scripts\python.exe teste_testcontainers.py
```

O teste externo inicia o container, aguarda seu término, imprime o log
e verifica código de saída zero e a presença dos 292 testes esperados.

A imagem deve ser reconstruída após mudanças nos arquivos utilizados.
A quantidade esperada no teste externo deve acompanhar alterações da suíte.

SQLite é executado dentro do container, sem montar o banco local.
Não há servidor PostgreSQL ou MySQL separado.

O lock principal verifica hashes das dependências da imagem.
A instalação externa do Testcontainers fixa suas dependências diretas,
mas ainda não possui lock completo com hashes das transitivas.

## Backup e restauração

```powershell
.\.venv\Scripts\python.exe validar_backup.py .\recursos.db
```

O script abre a origem somente para leitura, verifica integridade,
cria backup e restauração em diretório temporário e compara estrutura
e dados. Os arquivos temporários são removidos ao terminar.

Não substitui uma política de backup persistente nem um ensaio completo
de recuperação da aplicação após desastre.

## Integração contínua

Os workflows executam em pushes e pull requests:

- .github/workflows/testes.yml: concorrência HTTP, suíte Python,
  cobertura, artefatos e Chromium.
- .github/workflows/testcontainers.yml: construção da imagem,
  execução via Testcontainers e publicação do log.

A análise Sonar é executada nos pull requests e nos pushes da main,
aguardando o Quality Gate.

Execuções:
https://github.com/Arthurmrsilva/organizacao-recursos/actions

Artefatos:

- relatorios-cobertura: JSON, XML e HTML.
- resultado-testcontainers: log da execução em container.

A aprovação da CI não substitui revisão por outro integrante.
A evidência final da release deve identificar o commit avaliado.

## Segurança e TDD

Os controles incluem hash de senha, CSRF, renovação de token,
perfis, isolamento por usuário e validações de entrada.

Há testes de injeção SQL no login, token de outra sessão e escape
de HTML no nome do recurso.

As auditorias versionadas das dependências principais e de navegador
não reportaram vulnerabilidades conhecidas nas execuções registradas.
Isso não comprova ausência de vulnerabilidades na aplicação.

TDD do controle de acesso ao cadastro:

- RED: 1ed928d.
- GREEN: 49b42fe.
- Ampliação da suíte e CI: 250f9b2.

Consulte SEGURANCA.md e RTM_historico.md para detalhes.

## Desempenho

Duas execuções planejadas de GET /login foram registradas em 02/11/2026:
10 usuários, subida de 5 segundos, duração de 60 segundos e pausa de
1 segundo entre consultas.

| Execução | Amostras | Erros | Média (ms) | p95 (ms) | Máximo (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 | 85 |
| 2 | 565 | 0 | 8,11 | 19 | 69 |

Ambas atenderam aos critérios previamente definidos: zero erros,
p95 até 500 ms e pelo menos 500 amostras.

Aplicação e JMeter foram executados no mesmo computador, com o servidor
de desenvolvimento Flask. O cenário não mede autenticação por POST,
operações de reserva ou capacidade de produção.

Os ensaios exploratórios anteriores permanecem separados.

## Documentação e entrega

| Documento | Conteúdo |
| --- | --- |
| [Checklist](docs/entrega/checklist.md) | Estado da entrega e pendências |
| [Decisão de qualidade](docs/decisao-qualidade.md) | Entrega acadêmica com ressalvas; concordância dos três integrantes registrada |
| [Validação de 03/11](docs/entrega/validacao-2026-11-03.md) | Clone limpo, 292 testes e fluxo manual |
| [Changelog](CHANGELOG.md) | Alterações da versão |
| [Índice de evidências](docs/evidencias/README.md) | Documentos, testes e resultados |
| [RTM](RTM.md) | Requisitos e rastreabilidade |
| [Histórico](RTM_historico.md) | Evidências históricas |
| [Arquitetura](ARQUITETURA.md) | Diagramas, decisões e riscos |
| [Plano de testes](PLANO_TESTES.md) | Estratégia e cenários |
| [Relatório de qualidade](RELATORIO_QUALIDADE.md) | Avaliação e limitações |
| [Defeitos](DEFEITOS.md) | Registro de problemas |
| [Segurança](SEGURANCA.md) | Controles e auditorias |
| [Instalação limpa](VALIDACAO_INSTALACAO.md) | Validação do commit c84dac2 |
| [Resultado de carga](docs/performance/resultado-01.md) | Duas medições e critérios |
| [Ensaios exploratórios](performance/README.md) | Histórico de desempenho |
| [Auditoria principal](auditoria_dependencias.json) | Resultado pip-audit |
| [Auditoria E2E](auditoria_dependencias_e2e.json) | Resultado pip-audit do navegador |

Documentos históricos podem conter resultados de versões anteriores.
O checklist e o índice identificam o estado registrado e as pendências
de fechamento da entrega.

## Limitações e fechamento

- Gestão completa de usuários e edição/desativação de recursos pela interface.
- Ampliação dos fluxos de navegador e dos cenários de carga autenticados.
- Testes adicionais dos scripts administrativos e de migração.
- Configuração e revisão para implantação em produção.

Essas limitações devem ser confrontadas com os requisitos obrigatórios.
O estado das confirmações e do envio está no
[checklist](docs/entrega/checklist.md) e na
[decisão de qualidade](docs/decisao-qualidade.md).

O banco recursos.db e senhas locais não devem ser enviados ao GitHub.

Sem SECRET_KEY no ambiente, a aplicação gera uma chave temporária.
Reiniciar o servidor nesse modo invalida sessões anteriores.

O servidor de demonstração é de desenvolvimento.
Os resultados apresentados não declaram prontidão para produção.
