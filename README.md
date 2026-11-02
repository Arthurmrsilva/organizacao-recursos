# Organização de Recursos

Projeto da disciplina de Qualidade de Software — ADS, 4º semestre.

Sistema web para organizar reservas de salas, professores e materiais, evitar sobreposições e controlar aprovação, manutenção e movimentação de equipamentos.

## Integrantes

- Arthur Mendes
- Murilo Henrique
- Nicolas Ferreira
- Robert Oliveira

## Funcionalidades

- Login e logout com senhas armazenadas como hash.
- Perfis ADMIN, RESPONSAVEL e SOLICITANTE.
- Proteção CSRF nos formulários POST.
- Cadastro de recursos pelo administrador, com vínculo opcional de responsável.
- Pesquisa por tipo, capacidade, localização, competência e disponibilidade.
- Criação, edição e cancelamento das próprias reservas.
- Bloqueio de sobreposição e permissão de horários consecutivos.
- Aprovação e rejeição pelo responsável vinculado.
- Bloqueio de recursos em manutenção.
- Retirada, devolução e não comparecimento de materiais.
- Auditoria das operações de reserva.
- Notificações internas.
- Relatórios de contagens, horas previstas e conflitos evitados.

A gestão completa de usuários e a edição ou desativação de recursos pela interface ainda precisam de revisão e implementação complementar.

## Tecnologias

| Finalidade | Tecnologia |
| --- | --- |
| Aplicação | Python 3.14 e Flask |
| Persistência | SQLAlchemy Core e SQLite |
| Interface | Jinja, HTML, CSS e JavaScript |
| Testes | unittest e Playwright com Chromium |
| Cobertura | coverage.py |
| Integração contínua | GitHub Actions |
| Análise estática | SonarQube Cloud |
| Desempenho | Apache JMeter |
| Auditoria de dependências | pip-audit |

As versões das dependências estão registradas nos arquivos de requisitos e locks.

## Instalação no Windows

### 1. Obter o projeto

É necessário ter Git e Python 3.14 instalados. O ambiente local utilizado no desenvolvimento possui Python 3.14.6.

```powershell
git clone https://github.com/Arthurmrsilva/organizacao-recursos.git
cd organizacao-recursos
git switch funcionalidade/login
```

A branch acima contém a implementação documentada. O acesso ao repositório depende das permissões da conta GitHub.

### 2. Criar o ambiente virtual

```powershell
py -3.14 -m venv .venv
```

Os comandos seguintes utilizam diretamente o Python do ambiente virtual; não é necessário ativá-lo.

### 3. Instalar dependências

```powershell
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: --require-hashes -r requirements.lock
```

O lock registra versões e hashes dos pacotes esperados.

### 4. Criar a estrutura do banco

```powershell
.\.venv\Scripts\python.exe banco.py
```

O banco SQLite local utiliza o arquivo recursos.db.

A criação das tabelas não substitui migrações de bancos antigos. Para atualizar uma instalação existente, preserve um backup e revise os scripts administrativos antes de executá-los.

### 5. Cadastrar exemplos

Etapa opcional:

```powershell
.\.venv\Scripts\python.exe seed.py
```

O script cadastra Sala 101, Professor Carlos e Projetor 01, verificando se os exemplos já existem.

Os exemplos não configuram automaticamente responsáveis para os recursos que exigem aprovação.

### 6. Criar administrador

```powershell
.\.venv\Scripts\python.exe criar_admin.py
```

O login será admin. O script solicita uma senha de pelo menos oito caracteres e sua confirmação.

A senha não aparece enquanto é digitada. Utilize uma senha exclusiva para a demonstração.

Se admin já existir, o script informa a situação e não altera os dados.

### 7. Iniciar a aplicação

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --port 5003
```

Acesse:

http://127.0.0.1:5003/login

Mantenha o terminal aberto. Para encerrar, pressione Ctrl + C.

Também é possível executar app.py diretamente; nesse caso, a configuração padrão utiliza a porta 5000.

## Perfis e demonstração

| Perfil | Operações principais |
| --- | --- |
| SOLICITANTE | Consultar recursos e gerenciar as próprias reservas |
| RESPONSAVEL | Avaliar solicitações e gerenciar materiais vinculados |
| ADMIN | Cadastrar recursos, registrar manutenção, consultar auditoria e relatórios e gerenciar movimentações |

As permissões também dependem da propriedade da reserva, do vínculo com o recurso, do prazo e do estado da operação.

O script criar_admin.py prepara somente o administrador. A criação de outros usuários e a configuração de recursos existentes dependem dos procedimentos administrativos do projeto.

### Roteiro básico

1. Entrar com o administrador.
2. Consultar os recursos ou cadastrar uma sala comum.
3. Reservar um período futuro válido.
4. Conferir a reserva em Minhas reservas.
5. Tentar uma reserva sobreposta e conferir a recusa.
6. Cancelar a reserva antes do início.
7. Conferir o Histórico, as notificações e a auditoria.

Para demonstrar aprovação, é necessário um usuário RESPONSAVEL ativo vinculado ao recurso.

Recursos restritos e professores aguardam aprovação. Reservas comuns podem ser aprovadas automaticamente.

## Fluxos públicos

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

Edição, avaliação de solicitações, movimentação e leitura de notificações são acessadas pelos formulários das respectivas páginas.

Os formulários POST exigem token CSRF. As rotas verificam autenticação e permissões conforme a operação.

## Executar os testes

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes de persistência utilizam bancos temporários nos cenários preparados. Vários testes de rotas simulam a sessão; outros verificam o login real.

A aplicação possui inicialização de estrutura durante a importação. Execute os testes em ambiente de desenvolvimento e preserve bases importantes.

### Resultados registrados

- Suíte local de 286 testes aprovada em 121,250 segundos.
- Posteriormente, um teste de escape de HTML foi acrescentado e aprovado separadamente, com dois cenários.
- Um teste de navegador executa o fluxo de login, criação, conflito e cancelamento.

Os resultados pertencem às versões verificadas. Consulte RTM.md e os logs da CI para identificar as evidências.

## Medir cobertura

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

Abra htmlcov/index.html para consultar o relatório HTML.

O artefato detalhado conferido apresentou 97,69% de linhas e 95,39% de ramificações no escopo medido. Esses valores são históricos e devem ser associados à execução de origem.

A cobertura Python não inclui HTML, CSS e JavaScript.

## Teste de navegador

Instale as dependências de E2E:

```powershell
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: --require-hashes -r requirements-e2e.lock
```

Instale o Chromium:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
```

Execute:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s e2e -v
```

O teste inicia seu próprio servidor e banco temporário. Não exige que a aplicação da porta 5003 esteja aberta.

O cenário verifica login inválido e válido, criação, conflito, cancelamento, listas e registros associados.

## Integração contínua

O workflow .github/workflows/testes.yml executa em pushes e pull requests.

As verificações incluem:

- Instalação de dependências com hashes.
- Testes automatizados.
- Cobertura mínima de 80% de linhas e 70% de ramificações.
- Publicação de JSON, XML e HTML no artefato relatorios-cobertura.
- Teste separado de navegador com Chromium.
- Análise Sonar nos pull requests e pushes da main.
- Espera pelo resultado do Quality Gate.

Consulte as execuções em:

https://github.com/Arthurmrsilva/organizacao-recursos/actions

A aprovação da CI não substitui revisão por outro integrante.

## Evidência de TDD

Funcionalidade: controle de acesso ao formulário de cadastro de recursos.

- RED: commit 1ed928d, com testes falhando antes da implementação.
- GREEN: commit 49b42fe, com implementação e testes aprovados.
- Ampliação da suíte e CI: commit 250f9b2.

As evidências históricas estão registradas em RTM_historico.md.

## Segurança

Controles e verificações registrados:

- Hash de senhas.
- Autenticação, perfis e isolamento por usuário.
- Proteção CSRF e renovação do token após login.
- Testes de token de outra sessão.
- Tentativas de injeção SQL no login.
- Escape de HTML no nome do recurso em duas páginas.
- Auditoria das dependências de requirements.lock.

O relatório fornecido do pip-audit apresentou dez dependências sem vulnerabilidades conhecidas reportadas.

Isso não comprova ausência de vulnerabilidades na aplicação. Consulte SEGURANCA.md para escopo e limitações.

## Desempenho

O diretório performance contém o plano JMeter, os resultados e a documentação.

O cenário GET /login utilizou dez usuários, ramp-up de cinco segundos e duração configurada de 60 segundos.

Com pausa de um segundo por usuário:

- 570 respostas HTTP 200.
- Nenhuma falha.
- Média de 5,49 ms.
- Percentil 95 de 8 ms.
- Máximo de 38 ms.

A execução anterior sem pausa registrou 1.289 falhas de conexão em 17.633 amostras. Sua causa não foi confirmada.

O ensaio foi local e exploratório. Não mede autenticação completa, operações de reserva ou capacidade de produção.

Consulte performance/README.md antes de reproduzir os ensaios.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [RTM.md](RTM.md) | Requisitos, regras críticas, testes, métricas e pendências |
| [RTM_historico.md](RTM_historico.md) | Evidências históricas |
| [ARQUITETURA.md](ARQUITETURA.md) | C4, sequências, decisões, riscos e árvore de utilidade |
| [SEGURANCA.md](SEGURANCA.md) | Verificações e limitações de segurança |
| [Auditoria de dependências](auditoria_dependencias.json) | Resultado do pip-audit |
| [Desempenho](performance/README.md) | Ambiente, plano, resultados e limitações de carga |

## Limitações e pendências

- Gestão completa de usuários pela interface.
- Edição e desativação de recursos e alteração de vínculos existentes pela interface.
- Ampliação da concorrência por HTTP e entre manutenção e reserva.
- Banco em container ou alternativa aceita pelo professor.
- Ampliação dos fluxos de navegador.
- Testes dos demais scripts administrativos e de migração.
- Critérios de aceitação e novos cenários de desempenho.
- Revisão de segurança e configuração de implantação.
- Revisão por pares.
- Consolidação do registro de defeitos, relatório final e apresentação.

O detalhamento atualizado está em RTM.md.

## Observações de desenvolvimento

O banco recursos.db é local e não deve ser enviado ao GitHub.

Sem SECRET_KEY no ambiente, a aplicação gera uma chave temporária ao iniciar. Reiniciar o servidor nesse modo invalida as sessões anteriores.

A sessão não deve ser usada para armazenar senhas ou outros dados sensíveis.

O servidor Flask utilizado na demonstração é um servidor de desenvolvimento. Implantação de produção exige configuração própria de servidor, HTTPS, segredos e recuperação de dados.

A implementação em Python foi informada como permitida pelo professor. A aceitação das substituições de ferramentas e demais entregáveis deve ser conferida com os critérios da disciplina.