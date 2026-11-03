# Validação em clone limpo — 03/11/2026

Executor: Arthur Mendes Ramos da Silva.

Commit avaliado:
b55f1ef87ea97bb5fee3bf076a57cf0555656e74.

## Ambiente e preparação

- Windows, no mesmo computador de desenvolvimento.
- Clone separado em diretório temporário, fora da pasta original.
- Checkout do commit avaliado.
- Ambiente virtual novo com Python 3.14.
- Dependências instaladas pelo requirements.lock, com
  --only-binary=:all: e --require-hashes.
- Banco preparado com banco.py e seed.py.
- Administrador criado com criar_admin.py.
- Aplicação iniciada sem debugger e sem reloader.

Foram seguidos os procedimentos do README, usando a porta 5004
para distinguir esta execução da instalação original.

## Resultados

| Verificação | Resultado |
| --- | --- |
| Instalação das dependências com hashes | Aprovada |
| Suíte Python | 292 testes aprovados em 86,353 segundos |
| Login com administrador | Aprovado |
| Exibição dos recursos de exemplo | Aprovada |
| Criação de reserva para Sala 101 | Reserva nº 1 aprovada |
| Segunda reserva no mesmo recurso e período | Recusada por conflito |
| Cancelamento da reserva nº 1 | Aprovado |
| Consulta do histórico | Reserva nº 1 exibida como Cancelada |

Período utilizado na reserva:
04/11/2026, das 14h às 15h.

A finalidade foi preenchida com texto de teste.

## Limites da verificação

Esta execução confirma a instalação e o fluxo básico descrito acima.
Não representa revisão por outro integrante nem validação em outro
computador.

Os testes de Chromium, concorrência HTTP e Testcontainers não foram
reexecutados nesta verificação local. Seus resultados devem ser
consultados nas execuções de CI correspondentes.

A verificação foi realizada na versão da branch de preparação.
Ainda é necessário conferir a versão integrada na main e identificar
o commit da futura tag.

Não se declara prontidão para produção.