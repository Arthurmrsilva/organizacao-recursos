# Validação funcional parcial pelos integrantes

Registro elaborado por Arthur Mendes Ramos da Silva em 08/11/2026,
com base no relato recebido de Nicolas Ferreira e Robert Oliveira.

## Participantes e período

Segundo Arthur, ambos participaram dos testes manuais na sexta-feira
anterior à publicação da rc2.

Versão presumida: v1.0.0-rc1, pela cronologia informada.
A tag e o commit efetivamente utilizados ainda precisam ser confirmados.

## Cenários relatados

| Fluxo | Resultado informado a Arthur |
| --- | --- |
| Login | Funcionamento sem falhas relatadas |
| Criação de reserva | Funcionamento sem falhas relatadas |
| Aprovação de reserva | Funcionamento sem falhas relatadas |
| Recusa de reserva | Funcionamento sem falhas relatadas |
| Tentativa de reserva conflitante | Bloqueio informado |
| Consulta ao histórico | Funcionamento sem falhas relatadas |

O conflito considerado pelo sistema é a sobreposição de horários
para o mesmo recurso. Reservas no mesmo dia, em horários sem
sobreposição, podem ser permitidas.

## Alcance do registro

Este documento registra o relato recebido pelo autor.
Não foram apresentados neste registro logs, capturas de tela,
horários utilizados ou a distribuição dos cenários entre os participantes.

Não é atribuído percentual de conclusão, pois não há uma lista completa
de cenários executados que permita calcular essa medida.

Os resultados não demonstram validação integral da aplicação,
revisão do código ou aprovação coletiva da decisão de qualidade.

## Relação com a rc2

A rc2 contém mudanças documentais em relação à rc1, sem alteração
no código da aplicação. Os testes relatados continuam relevantes
para esse código, respeitadas as limitações descritas acima.

## Confirmações pendentes

- Confirmar a versão efetivamente utilizada.
- Identificar quais cenários cada participante executou.
- Complementar os cenários não testados.
- Registrar a revisão do código.
- Registrar a decisão coletiva e o aceite nominal dos riscos.

Este registro complementa os documentos anteriores: a participação
funcional relatada é parcial; as confirmações finais permanecem pendentes.
