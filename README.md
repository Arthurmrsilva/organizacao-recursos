# Organização de Recursos

Projeto da disciplina de Qualidade de Software — ADS, 4º semestre.

Sistema web para reservar salas, professores e materiais, evitar
sobreposições e controlar aprovação, manutenção e movimentação de materiais.

## Integrantes

- Arthur Mendes
- Murilo Henrique
- Nicolas Ferreira
- Robert Oliveira

As contribuições e a decisão final devem ser confirmadas pelos integrantes.

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

Python foi informado como permitido pelo professor. A aceitação das
substituições específicas de Maven e JaCoCo deve ser confirmada.
O projeto não executa Maven nem gera relatório JaCoCo.

## Instalação limpa no Windows

Pré-requisitos: Git e Python 3.14. O ambiente de desenvolvimento
utiliza Python 3.14.6.

### 1. Obter o projeto

```powershell
git clone --single-branch --branch funcionalidade/login https://github.com/Arthurmrsilva/organizacao-recursos.git
cd organizacao-recursos
```

A implementação documentada está na branch funcionalidade/login.
Enquanto o repositório estiver privado, o acesso exige permissão.

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
Não é apresentada como API REST JSON.

| Endereço | Método | Finalidade |
| --- | --- | --- |
| /login | GET e POST | Exibir formulário e autenticar |
| /sair | POST | Encerrar sessão |
| / | GET | Consultar recursos e aplicar filtros |
| /recursos/novo | GET e POST | Cadastrar recurso como administrador |
| /reservas/nova | GET e POST | Criar reserva |
| /reservas | GET | Consultar as próprias reservas |
| /reservas/<id>/cancelar | POST | Cancelar a própria reserva |
| /aprovacoes | GET | Consultar solicitações vinculadas |
| /manutencoes | GET e POST | Consultar e cadastrar manutenção |
| /materiais | GET | Consultar gestão de materiais |
| /auditoria | GET | Consultar eventos como administrador |
| /notificacoes | GET | Consultar os próprios avisos |
| /relatorios | GET | Consultar indicadores como administrador |

Esta tabela apresenta as principais rotas. Edição, avaliação,
movimentação e leitura de notificações são acessadas pelos formulários
das respectivas páginas.

Os formulários POST exigem token CSRF. As operações protegidas
verificam autenticação e permissões.

## Testes Python

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

A suíte registrada contém 292 testes. No commit da93d49,
a execução local terminou aprovada em 116,207 segundos.

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
O checklist e o índice identificam a consolidação pendente.

## Limitações e fechamento

- Gestão completa de usuários e edição/desativação de recursos pela interface.
- Ampliação dos fluxos de navegador e dos cenários de carga autenticados.
- Testes adicionais dos scripts administrativos e de migração.
- Configuração e revisão para implantação em produção.
- Confirmação das equivalências de ferramentas exigidas pela disciplina.
- Revisão real por pares e declaração das contribuições.
- Consolidação documental e validação final em clone limpo.
- CI verde na main avaliada, tag anotada e decisão de qualidade.
- Publicação do repositório e envio no formulário da disciplina.

O banco recursos.db e senhas locais não devem ser enviados ao GitHub.

Sem SECRET_KEY no ambiente, a aplicação gera uma chave temporária.
Reiniciar o servidor nesse modo invalida sessões anteriores.

O servidor de demonstração é de desenvolvimento.
Os resultados apresentados não declaram prontidão para produção.