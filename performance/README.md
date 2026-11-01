# Teste de desempenho — página de login

## Objetivo

Medir o tempo de resposta da abertura da página de login
por meio de requisições GET /login, sem autenticação.

## Ambiente e configuração

- Data: 01/11/2026.
- Windows, JMeter 5.6.3 e Java Zulu 25.
- Flask com servidor de desenvolvimento em http://127.0.0.1:5003.
- Aplicação e JMeter executados no mesmo computador.
- 10 usuários virtuais.
- Entrada gradual dos usuários em 5 segundos.
- Duração configurada: 60 segundos.
- Pausa de 1 segundo antes de cada consulta por usuário.
- Execução pelo terminal, sem interface gráfica.
- Verificações: HTTP 200 e presença do texto “Acesso ao sistema”.

## Resultado com pausa

Arquivo: carga_login_10usuarios_60s_pausa_01.jtl

| Métrica | Resultado |
| --- | ---: |
| Consultas | 570 |
| Respostas HTTP 200 | 570 |
| Falhas | 0 |
| Tempo médio | 5,49 ms |
| Mediana | 5 ms |
| Percentil 95 | 8 ms |
| Tempo máximo | 38 ms |
| Pico de usuários virtuais ativos | 10 |

## Execução anterior sem pausa

Arquivo: carga_login_10usuarios_60s_01.jtl

Foram registradas 17.633 consultas, com 16.344 respostas HTTP 200
e 1.289 falhas de conexão (7,31%).

As falhas apresentaram java.net.BindException, com a mensagem
“Address already in use: connect”. O arquivo não permite confirmar
a causa completa nem atribuir essas falhas à aplicação.

Foi criado um novo cenário com pausa para controlar a frequência
das consultas. Os dois resultados foram preservados.

## Limitações e conclusão

O cenário com pausa terminou sem falhas e apresentou percentil 95
de 8 ms nesta execução.

O teste abrange somente o HTML da página de login. Não mede
autenticação, carregamento de arquivos estáticos, criação de
reservas ou capacidade em produção.

Usuários virtuais ativos incluem usuários aguardando a pausa;
isso não significa 10 requisições sendo processadas simultaneamente.

Os resultados são exploratórios. Não foi definido previamente
um limite de tempo de resposta para aprovação.