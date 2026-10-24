# Organização de Recursos

Projeto da disciplina de Qualidade de Software — ADS, 4º semestre.

O objetivo é organizar reservas de salas, professores e materiais,
evitando conflitos de horário e apresentando evidências de qualidade.

## Integrantes

- Arthur Mendes
- Murilo Henrique
- Nicolas Ferreira
- Robert Oliveira

## Situação atual

Projeto em desenvolvimento.

Implementado:

- Login e logout.
- Senhas armazenadas como hash.
- Acesso à página inicial mediante autenticação.
- Cadastro de salas, professores e materiais exclusivo do administrador.
- Validação dos campos no servidor.
- Consulta de recursos ativos com filtro por tipo.
- Proteção CSRF nos formulários.
- 16 testes automatizados.
- GitHub Actions executando testes em pushes e pull requests.

Os perfis SOLICITANTE, RESPONSAVEL e ADMIN estão definidos no banco.
Nesta etapa, a restrição específica implementada é o cadastro de recursos
exclusivo do administrador.

## Tecnologias

- Python 3.14
- Flask
- SQLAlchemy
- SQLite
- HTML e CSS
- unittest
- GitHub Actions

## Instalação no Windows

É necessário ter Python e Git instalados.

Clone o repositório:

```powershell
git clone https://github.com/Arthurmrsilva/organizacao-recursos.git
cd organizacao-recursos
```

Enquanto o Pull Request nº 1 estiver aberto, acesse a implementação com:

```powershell
git switch funcionalidade/login
```

Crie o ambiente virtual:

```powershell
py -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Crie as tabelas:

```powershell
.\.venv\Scripts\python.exe banco.py
```

Cadastre os recursos de exemplo:

```powershell
.\.venv\Scripts\python.exe seed.py
```

Crie a conta de administrador:

```powershell
.\.venv\Scripts\python.exe criar_admin.py
```

O login será `admin`. A senha é definida no terminal e não aparece
enquanto é digitada. Não utilize senhas de contas pessoais.

Execute a aplicação:

```powershell
.\.venv\Scripts\python.exe app.py
```

Abra no navegador:

http://127.0.0.1:5000

Mantenha o terminal aberto enquanto estiver usando o sistema.
Para encerrar, pressione Ctrl + C.

## Executar os testes

Na pasta principal:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes utilizam bancos SQLite temporários separados do banco local.

O GitHub Actions também executa a suíte automaticamente.
O resultado pode ser consultado na aba Actions do repositório.

## Evidência de TDD

Funcionalidade: controle de acesso ao formulário de cadastro de recursos.

- RED: commit `1ed928d`, com os testes falhando antes da implementação.
- GREEN: commit `49b42fe`, com a implementação e os testes aprovados.
- Ampliação da suíte e CI: commit `250f9b2`.
- Pull Request nº 1: revisão por outro integrante pendente.

## Fluxos disponíveis

| Endereço | Método | Comportamento |
| --- | --- | --- |
| `/login` | GET | Exibe o formulário de login |
| `/login` | POST | Verifica as credenciais |
| `/` | GET | Lista recursos para usuários autenticados |
| `/?tipo=SALA` | GET | Filtra recursos por tipo |
| `/recursos/novo` | GET | Exibe o cadastro para administradores |
| `/recursos/novo` | POST | Valida e cadastra um recurso |
| `/sair` | POST | Encerra a sessão |

Os formulários POST exigem um token CSRF.

## Próximas entregas

- Gestão de usuários e demais permissões.
- Edição e desativação de recursos.
- Filtros por capacidade, localização, competência e disponibilidade.
- Reservas e prevenção de conflitos, inclusive em solicitações simultâneas.
- Aprovação, manutenção e estados das reservas.
- Retirada e devolução de materiais.
- Auditoria, notificações e relatórios.
- Testes adicionais, Testcontainers e testes de carga.
- Medição de cobertura e análise estática.
- RTM, diagramas, registros de defeitos e relatório final de qualidade.

## Observações de desenvolvimento

O arquivo `recursos.db` é criado localmente e não é enviado ao GitHub.

Sem a variável de ambiente SECRET_KEY, a aplicação gera uma chave
temporária ao iniciar. Nesse modo, reiniciar o servidor exige novo login.

O servidor utilizado nesta etapa é o servidor local de desenvolvimento
do Flask.

A implementação utiliza Python. A aceitação das ferramentas equivalentes
às especificadas no enunciado deve ser confirmada com o professor.