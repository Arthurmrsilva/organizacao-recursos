# Resultado 01 — Consulta da pagina de login

## Identificacao

- Data: 02/11/2026.
- Executor: Arthur Mendes.
- Ferramenta: Apache JMeter 5.6.3, executado em modo CLI.
- Plano: performance/consulta_login_10usuarios_60s.jmx.
- Aplicacao: Flask, servidor de desenvolvimento, debug desligado.
- Endereco: http://127.0.0.1:5003/login.
- Ambiente: Windows; aplicacao e gerador de carga no mesmo computador.

## Cenario

Consulta HTTP GET da pagina de login, sem autenticacao.

- 10 usuarios virtuais.
- Subida gradual: 5 segundos.
- Duracao configurada: 60 segundos.
- Pausa: 1 segundo antes de cada consulta.
- Duas execucoes sequenciais.
- Verificacoes: HTTP 200 e presenca do texto "Acesso ao sistema".

## Criterios definidos antes das execucoes

Cada execucao deveria apresentar:

- Zero requisicoes com erro.
- p95 de tempo de resposta de ate 500 ms.
- Pelo menos 500 amostras.

## Evidencias

- [Plano JMeter](../../performance/consulta_login_10usuarios_60s.jmx)
- [Resultados da execucao 1](../../performance/login_planejado_20261102-192309_01.jtl)
- [Resultados da execucao 2](../../performance/login_planejado_20261102-192309_02.jtl)

## Resultados

| Execucao | Amostras | Erros | Media (ms) | p95 (ms) | Maximo (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 565 | 0 | 9,12 | 23 | 85 |
| 2 | 565 | 0 | 8,11 | 19 | 69 |

Os valores foram calculados a partir dos arquivos JTL, usando a coluna
elapsed para o tempo em milissegundos e success para identificar erros.

O p95 foi calculado ordenando os tempos e selecionando a posicao
ceil(0,95 * quantidade), com numeracao iniciada em 1.

## Conclusao

As duas execucoes atenderam aos tres criterios definidos para este cenario.

O resultado evidencia o desempenho observado na consulta local da pagina
de login, sob a carga configurada.

## Limites da avaliacao

- Nao mede login por POST ou navegacao autenticada.
- Nao mede criacao, aprovacao ou cancelamento de reservas.
- Nao representa acesso pela internet ou ambiente de producao.
- Aplicacao e JMeter compartilham os recursos do mesmo computador.
- O servidor utilizado e o servidor de desenvolvimento do Flask.
- Nao determina a capacidade maxima do sistema.
- As execucoes exploratorias anteriores permanecem separadas destas
  duas execucoes com criterios previamente definidos.