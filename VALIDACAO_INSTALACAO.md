# Validação da instalação limpa

## Identificação

- Data: 02/11/2026.
- Executor: Arthur Mendes.
- Commit: c84dac2.
- Branch: funcionalidade/login.
- Ambiente: Windows, Python 3.14 e SQLite.
- Origem: novo clone do repositório em diretório temporário.
- Ambiente virtual e banco criados nessa cópia.

## Objetivo

Verificar a instalação das dependências, a preparação inicial
do banco e o funcionamento básico da aplicação em uma nova cópia.

## Procedimento e resultados

| Etapa | Resultado observado |
| --- | --- |
| Clonar a branch | Concluído |
| Criar ambiente virtual | Concluído |
| Instalar requirements.lock com hashes | Concluído sem erro apresentado |
| Executar banco.py | Tabelas verificadas e criadas |
| Executar seed.py | Sala 101, Professor Carlos e Projetor 01 cadastrados |
| Executar criar_admin.py | Administrador criado com senha definida no terminal |
| Iniciar Flask na porta 5004 | Aplicação acessível no navegador |
| Autenticar como administrador | Página inicial apresentada |
| Criar reserva da Sala 101 | Reserva nº 1 registrada |
| Consultar Minhas reservas | Reserva apresentada como Aprovada |

## Reserva utilizada

- Recurso: Sala 101.
- Início: 03/11/2026 às 14h.
- Término: 03/11/2026 às 15h.
- Finalidade: Validacao da instalacao limpa.
- Situação observada: Aprovada.

## Evidências

Foram apresentados registros do terminal e capturas da página
inicial, da confirmação de criação e da listagem da reserva.

Essas capturas foram conferidas durante a validação, mas ainda
não estão anexadas a este documento no repositório.

A versão da cópia foi conferida com git rev-parse --short HEAD.

## Encerramento

O servidor foi encerrado e o terminal retornou à pasta original.

## Limites

A validação ocorreu no mesmo computador do desenvolvimento,
com novo ambiente virtual e banco separado.

Não representa instalação em outro computador, implantação
de produção ou teste manual completo de todas as funcionalidades.

O resultado confirma somente as etapas e o fluxo descritos.