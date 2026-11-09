## Nota de integracao documental - 09/11/2026

Executor identificado: Nicolas Ferreira.
O texto abaixo preserva os resultados informados pelo executor.

Versao informada como testada: f3f2061.
Branch informada pelo executor: test/scripts-administrativos.
O documento foi enviado pelo PR #8, na branch teste-da-branch.
A branch usada para enviar o documento e a versao executada
sao registros distintos; a correspondencia ainda precisa de confirmacao.

O relato informa 21 cenarios: A1 a A15 e R1 a R6.
Nao representa revisao integral do codigo nem validacao de todas
as funcionalidades. Nao atribui execucao ou aprovacao a Robert Oliveira.

Pendencias de identificacao do relato:
- Confirmar o recurso vinculado ao usuario responsavel.
- Confirmar a versao e eventuais alteracoes locais durante a execucao.
- Esclarecer o horario duplicado na segunda reserva descrita.
- Identificar a finalidade da reserva iniciada em 09/11 as 10:30,
  anterior ao horario do trecho de log apresentado.
- Confirmar se o computador do executor era distinto do desenvolvimento.

Os codigos HTTP resumidos sao evidencias complementares.
Sozinhos, nao identificam a mensagem exibida nem comprovam
a regra de negocio ou a conferencia dos valores dos relatorios.

Este registro complementa a documentacao apos a publicacao da rc3.
Nao altera a tag v1.0.0-rc3 nem seus resultados automatizados.

## Relato recebido do executor

# Validação funcional por perfil (ADMIN e RESPONSAVEL)

## Identificação
-Data: [09/11/2026].
Executor: Nicolas Ferreira.
Commit: [f3f2061].
Branch: [test/scripts-administrativos].
Ambiente: Windows, Python [Python 3.14.7] e SQLite.
Origem: projeto local em execução com Flask em 127.0.0.1:5000.
Usuários utilizados: admin (perfil ADMIN) e responsavel (perfil RESPONSAVEL, vinculado a: recurso vinculado nao identificado no relato).
## Objetivo
Verificar o funcionamento básico das telas, das regras de reserva
e das permissões de acesso dos perfis ADMIN e RESPONSAVEL,
com a aplicação já instalada e o banco preparado.

## Procedimento e resultados

                                        PERFIL ADMIN
                Etapa	                                                Resultado observado

A1.  Login com a senha correta	                            |Acesso concedido e página inicial apresentada
A2.  Login com senha incorreta	                            |Acesso negado com a mensagem de login ou senha inválidos
A3.  Filtro de recursos por tipo	                        |Lista filtrada conforme o tipo escolhido
A4.  Cadastro de novo recurso	                            |Recurso cadastrado e apresentado na lista
A5.  Cadastro com campo obrigatório vazio                   |Cadastro recusado com mensagem de validação
A6.  Criação de reserva da Sala 101                         |Reserva registrada e apresentada em Minhas reservas
A7.  Reserva sobreposta no mesmo recurso                    |Reserva recusada por conflito de horário
A8.  Reserva em horário consecutivo	                        |Reserva aceita
A9.  Reserva com término anterior ao início ou no passado   |Reserva recusada com mensagem de validação
A10. Edição e cancelamento de reservas                      |Alterações refletidas em Minhas reservas e nos filtros
A11. Manutenção e reserva no mesmo horário                  |Reserva bloqueada pela manutenção
A12. Consulta da auditoria                                  |Operações realizadas apresentadas na listagem
A13. Consulta dos relatórios                                |Valores coerentes com as reservas realizadas
A14. Consulta das notificações                              |Avisos apresentados e marcação como lida funcionando
A15. Encerramento da sessão	                                |Retorno ao login e páginas internas inacessíveis após sair

 |-----------------------------------------------------------------------------------------------------------------------|

                                        PERFIL RESPONSAVEL
            Etapa                                            Resultado observado

R1. Login	                                                    |Acesso concedido
R2. Tela de Aprovações	                                        |Tela acessada sem erro
R3. Acesso por endereço a telas exclusivas do ADMIN	            |Acesso negado
R4. Tela de Materiais	                                        |Tela acessada sem erro
R5. Reserva de recurso comum	                                |Reserva registrada
R6. Tela de Notificações	                                    |Tela acessada sem erro


| -------------------------------------------------------------------------------------------------------------------------|

## Dados utilizados
Recursos: Sala 101, SALA A305, MARCELINHO (PROFESSOR), JUNIOR(PROFESSOR), NICOLAS SOUZA(PROFESSOR), PROJETOR 01.
Reservas: [Início: 09/11/2026 às 10:30 ÁS Término: 10/11/2026 às 10:30].
Reservas: [Início: 10/11/2026 às 13:41 às 10:30 ÁS Término: 11/11/2026 às 13:41].
Manutenção: [Sala 101 -Início: 13/11/2026 às 14:24 ÁS Término: 20/11/2026 às 13:24 ].

## Evidências
[SEGUE O DECORRER DO TERMINAL ENQUANTO EU FAZIA OS TESTES NO SISTEMA:
Evidências

Registros do terminal do servidor que correspondem aos testes:

Registro	Interpretação
POST /login com 401 (13:13:05)                                  	|Login com senha incorreta recusado (A2)
POST /recursos/novo com 302 (13:17:25) e 400 (13:18:40)         	|Cadastro válido aceito e cadastro inválido recusado (A4 e A5)
POST /reservas/nova com 400 (13:21:27)	                            |Reserva inválida ou conflitante recusada
POST /reservas/11/editar com 400 (13:23:52) e 302 (13:23:58)	    |Edição inválida recusada e edição válida aceita (A10)
POST /manutencoes com 400 (três vezes) e 302 (13:25:48)         	|Manutenções inválidas recusadas e manutenção válida aceita
POST /reservas/nova com 400 (13:26:10)	                            |Reserva no período da manutenção recusada (A11)
GET /recursos/novo, /manutencoes, /auditoria e /relatorios com 403	|Telas do ADMIN negadas ao responsável (R3)

O terminal do servidor foi acompanhado durante os testes e não apresentou erros 500 nem Traceback no trecho registrado.


## Problemas encontrados
Nenhum nos passos executados.

## Limites
A validação ocorreu no mesmo computador do desenvolvimento, com o banco local do projeto.

Esta validação cobre apenas as etapas A1 a A15 e R1 a R6 descritas acima. Não foram registrados aqui o fluxo de aprovação e rejeição entre os dois perfis, nem a retirada, a devolução e o não comparecimento de materiais.

Não representa instalação em outro computador, implantação de produção ou teste manual completo de todas as funcionalidades.

O resultado confirma somente as etapas e o fluxo descritos.
