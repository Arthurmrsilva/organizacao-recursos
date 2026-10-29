# Matriz de Rastreabilidade ÔÇö RTM

**Projeto:** Organiza├º├úo de Recursos  
**├Ültima atualiza├º├úo:** 29/10/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

Esta matriz relaciona requisitos, riscos, testes e evid├¬ncias.

As tabelas descrevem a situa├º├úo atual. Os registros hist├│ricos preservam os resultados das etapas anteriores.

## 1. Legenda

- **Implementado e verificado:** dispon├¡vel e verificado no escopo indicado.
- **Parcial:** parte da implementa├º├úo ou da verifica├º├úo permanece pendente.
- **Pendente:** implementa├º├úo ou verifica├º├úo ainda n├úo realizada.
- Testes planejados n├úo representam resultados aprovados.
- Quantidade de testes e cobertura n├úo representam percentual de conclus├úo.
- Aprova├º├úo dos testes n├úo comprova aus├¬ncia de defeitos.
- Testes com o cliente Flask n├úo equivalem ├á automa├º├úo de navegador ou a testes externos por HTTP.

## 2. Requisitos funcionais

| ID | Requisito | Risco | Testes e evid├¬ncias | Situa├º├úo |
| --- | --- | --- | --- | --- |
| RF01 | Autentica├º├úo e autoriza├º├úo por perfil | Acesso indevido | Testes de consulta, cancelamento, aprova├º├úo, auditoria, manuten├º├úo, edi├º├úo, notifica├º├Áes, relat├│rios, materiais e n├úo comparecimento | Implementado e verificado nas opera├º├Áes atuais; revis├úo geral de seguran├ºa pendente |
| RF02 | Cadastro e consulta de salas, professores e materiais | Dados inv├ílidos | test_consulta.py e cadastro manual | Implementado e verificado; revis├úo por colega pendente |
| RF03 | Pesquisa por tipo, capacidade, localiza├º├úo, compet├¬ncia e disponibilidade | Resultado incorreto | test_consulta.py, test_disponibilidade.py e consulta manual | Implementado e verificado; navegador automatizado pendente |
| RF04 | Criar, alterar e cancelar reservas | Reserva incorreta ou altera├º├úo indevida | Testes de reservas, listagem, cancelamento e edi├º├úo | Implementado e verificado no escopo atual |
| RF05 | Detectar sobreposi├º├úo, inclusive na agenda do professor | Dois usos simult├óneos | Testes de cria├º├úo, aprova├º├úo, disponibilidade e edi├º├úo | Parcial: ampliar cen├írios expl├¡citos por tipo |
| RF06 | Impedir dupla reserva simult├ónea | Duas solicita├º├Áes aceitas | Teste de duas solicita├º├Áes simult├óneas em test_reservas.py | Verificado no servi├ºo com SQLite; concorr├¬ncia por HTTP pendente |
| RF07 | Exigir aprova├º├úo para recursos restritos | Uso sem autoriza├º├úo | Testes de aprova├º├úo, v├¡nculo e nova aprova├º├úo ap├│s edi├º├úo | Implementado e verificado; interface para vincular respons├íveis pendente |
| RF08 | Bloquear recursos em manuten├º├úo | Reserva imposs├¡vel de atender | Testes de manuten├º├úo, disponibilidade e edi├º├úo; consulta manual | Implementado e verificado; concorr├¬ncia entre manuten├º├úo e reserva pendente |
| RF09 | Registrar retirada e devolu├º├úo de materiais | Perda de controle dos equipamentos | test_materiais.py, test_materiais_http.py e fluxo manual da reserva n┬║ 11 | Implementado e verificado no servi├ºo, nas rotas e manualmente; navegador automatizado pendente |
| RF10 | Manter hist├│rico audit├ível | Mudan├ºas sem rastreio | Testes de auditoria, edi├º├úo, materiais e n├úo comparecimento; rollback e confer├¬ncia manual | Implementado nas opera├º├Áes atuais; testes espec├¡ficos de limite e ordena├º├úo da consulta pendentes |
| RF11 | Notifica├º├úo simulada ou integra├º├úo externa | Usu├írio n├úo informado | test_notificacoes.py e fluxo manual de leitura | Implementado como avisos internos para cria├º├úo, edi├º├úo, cancelamento, aprova├º├úo e rejei├º├úo |
| RF12 | Relat├│rios de utiliza├º├úo, horas e conflitos evitados | Indicadores incorretos | test_relatorios.py, test_relatorios_http.py e consultas manuais | Parcial: contagens e horas previstas implementadas; conflitos evitados e tempo real de utiliza├º├úo indispon├¡veis |
| RF13 | Interface responsiva e erros compreens├¡veis | Dificuldade de uso | Testes HTTP e verifica├º├Áes manuais | Parcial: avalia├º├úo em diferentes telas e automa├º├úo de navegador pendentes |
| RF14 | Documenta├º├úo da API ou dos fluxos p├║blicos | Dificuldade de instalar e utilizar | README inicial e esta matriz | Parcial: ampliar instala├º├úo, fluxos e interfaces |

## 3. Regras cr├¡ticas

| ID | Regra | Risco | Verifica├º├úo | Situa├º├úo |
| --- | --- | --- | --- | --- |
| RC01 | T├®rmino posterior ao in├¡cio | Per├¡odo inv├ílido | Valida├º├úo no servi├ºo e banco; testes expl├¡citos de edi├º├úo e disponibilidade | Verificado nesses fluxos; ampliar testes expl├¡citos de cria├º├úo |
| RC02 | Mesmo recurso sem sobreposi├º├úo | Conflito de utiliza├º├úo | Cria├º├úo, aprova├º├úo, edi├º├úo, disponibilidade e hor├írios consecutivos | Parcial: ampliar cen├írios por tipo |
| RC03 | Solicita├º├Áes simult├óneas com uma ├║nica aceita | Dupla reserva | Teste de concorr├¬ncia no servi├ºo | Verificado no servi├ºo; concorr├¬ncia por HTTP pendente |
| RC04 | Recurso em manuten├º├úo indispon├¡vel | Reserva imposs├¡vel de atender | Testes de manuten├º├úo, edi├º├úo e disponibilidade; consulta manual | Implementado e verificado; concorr├¬ncia espec├¡fica pendente |
| RC05 | SOLICITADA ÔåÆ APROVADA ÔåÆ EM_USO ÔåÆ CONCLUIDA | Estado inconsistente | Aprova├º├úo e materiais nos servi├ºos e rotas; fluxo manual da reserva n┬║ 11 | Implementado e verificado para materiais |
| RC06 | Estados alternativos REJEITADA, CANCELADA e NAO_COMPARECEU | Hist├│rico incorreto | Aprova├º├úo, cancelamento e testes de n├úo comparecimento; reserva n┬║ 12 | Verificado no escopo atual; n├úo comparecimento implementado somente para materiais |
| RC07 | Somente respons├ível vinculado aprova recurso restrito | Aprova├º├úo indevida | Testes de perfil, v├¡nculo, prazo e estado | Implementado e verificado |
| RC08 | Reservas iniciadas n├úo podem ser apagadas | Perda de hist├│rico | Sem exclus├úo f├¡sica dispon├¡vel; edi├º├úo e cancelamento ap├│s in├¡cio bloqueados | Verificado nas opera├º├Áes existentes |
| RC09 | Toda mudan├ºa de estado gera auditoria | Aus├¬ncia de rastreabilidade | Cria├º├úo, altera├º├úo, cancelamento, aprova├º├úo, rejei├º├úo, retirada, devolu├º├úo e n├úo comparecimento | Verificado nas transi├º├Áes atuais; novas transi├º├Áes exigir├úo novos testes |

## 4. Testes automatizados

### Resultado local mais recente

- Data: 29/10/2026.
- Su├¡te completa: **257 testes aprovados**.
- Resultado: **OK**.
- Dura├º├úo: **84,677 segundos**.
- Execu├º├úo com unittest, sem uma nova medi├º├úo local de cobertura nessa execu├º├úo.
- Evid├¬ncia: imagem do terminal apresentada pelo executor.
- Commit funcional associado: **f1d0af2**.
- Esse resultado precede o ajuste posterior do r├│tulo em auditoria.html.

### Evolu├º├úo recente

| Etapa | Resultado |
| --- | --- |
| Relat├│rios administrativos | 213 testes em 58,742 segundos, com cobertura |
| Testes HTTP de materiais | 231 testes em 70,820 segundos |
| Servi├ºo de n├úo comparecimento | 14 testes espec├¡ficos em 3,476 segundos |
| N├úo comparecimento antes dos testes HTTP espec├¡ficos | 245 testes em 69,067 segundos |
| Testes HTTP de n├úo comparecimento | 12 testes espec├¡ficos aprovados, conforme confirma├º├úo do executor |
| Su├¡te completa ap├│s os novos testes | 257 testes em 84,677 segundos |

Alguns m├®todos utilizam `subTest` para verificar v├írios cen├írios.

Testes de servi├ºo com persist├¬ncia real tamb├®m verificam integra├º├úo com SQLite. N├úo devem ser classificados integralmente como testes unit├írios isolados.

### Arquivos de teste

| Arquivo | Escopo |
| --- | --- |
| tests/test_consulta.py | Login, logout, usu├írio inativo, CSRF, autoriza├º├úo, cadastro, persist├¬ncia e filtros |
| tests/test_reservas.py | Cria├º├úo, conflitos, hor├írios consecutivos, concorr├¬ncia e cancelamento |
| tests/test_minhas_reservas.py | Login, isolamento, filtros, prazo, atraso e ordena├º├úo |
| tests/test_cancelamento_http.py | Autentica├º├úo, autoriza├º├úo e CSRF no cancelamento |
| tests/test_aprovacoes.py | Aprova├º├úo, rejei├º├úo, v├¡nculo, prazo, estado e conflito |
| tests/test_aprovacoes_http.py | Rotas, perfis, CSRF e isolamento por respons├ível |
| tests/test_auditoria.py | Registro das opera├º├Áes, autor e rollback |
| tests/test_auditoria_http.py | Login, permiss├Áes e visibilidade do bot├úo |
| tests/test_manutencoes.py | Per├¡odos, conflitos e bloqueio de reservas |
| tests/test_manutencoes_http.py | Permiss├Áes, CSRF, cadastro e consulta |
| tests/test_materiais.py | Retirada, devolu├º├úo, permiss├Áes, hor├írios, estados, manuten├º├úo e auditoria |
| tests/test_materiais_http.py | Listagem, isolamento, retirada, devolu├º├úo, permiss├Áes, CSRF e recusas |
| tests/test_disponibilidade.py | Per├¡odos, sobreposi├º├úo, estados, manuten├º├úo, limites e filtros combinados |
| tests/test_edicao_reservas.py | Edi├º├úo, permiss├Áes, valida├º├Áes, conflitos, manuten├º├úo, aprova├º├úo, auditoria e rollback |
| tests/test_edicao_http.py | Formul├írio, persist├¬ncia, auditoria, CSRF e recusas |
| tests/test_notificacoes.py | Gera├º├úo, destinat├írio, leitura, isolamento, CSRF, ordena├º├úo, escape e rollback |
| tests/test_relatorios.py | Permiss├Áes, datas, contagens, agrupamento, horas, limites e arredondamento |
| tests/test_relatorios_http.py | Login, perfis, filtros, erros, campos, resultados vazios e consulta sem altera├º├úo |
| tests/test_nao_comparecimento.py | Permiss├Áes, prazo, estados, recurso inativo, repeti├º├úo, auditoria e rollback |
| tests/test_nao_comparecimento_http.py | Rota, bot├úo, perfis, CSRF, prazo, repeti├º├úo, mensagem e persist├¬ncia |

### Execu├º├úo

Na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Limita├º├Áes

- Persist├¬ncia testada com bancos SQLite tempor├írios.
- Rotas testadas com o cliente Flask.
- Sess├úo simulada em v├írios testes; login e senha possuem testes pr├│prios.
- O cliente Flask n├úo executa JavaScript nem a confirma├º├úo dos bot├Áes.
- HTTP externo, navegador automatizado e carga permanecem pendentes.
- Verifica├º├úo com banco em container permanece pendente.
- Scripts de migra├º├úo ainda n├úo possuem testes automatizados.
- A cobertura medida nos m├│dulos Python n├úo abrange HTML, CSS e JavaScript.

## 5. Evid├¬ncias

### Hist├│rico preservado

| ID | Evid├¬ncia |
| --- | --- |
| EV01 | Commit 1ed928d: etapa RED do acesso ao cadastro |
| EV02 | Commit 49b42fe: etapa GREEN do cadastro |
| EV03 | Commit 250f9b2: 16 testes e GitHub Actions |
| EV04 | 16 testes aprovados em 6,098 segundos |
| EV05 | Actions do commit 250f9b2 aprovado em 21 segundos |
| EV06 | Cadastro manual da Sala 202 |
| EV07 | PR n┬║ 1 aberto; revis├úo por outro integrante pendente |
| EV08 | Commit 940a392: reservas, conflitos, hor├írios consecutivos e concorr├¬ncia |
| EV09 | 22 testes em 7,883 segundos |
| EV10 | Actions #13 e #14 aprovados |
| EV11 | Commit ecb0eb7: cancelamento; 31 testes em 9,850 segundos |
| EV12 | Reserva n┬║ 3 cancelada e n┬║ 4 aprovada no mesmo per├¡odo |
| EV13 | Commit 7ae60b7: testes HTTP de cancelamento |
| EV14 | Commit cca4432: aprova├º├úo, v├¡nculo e temas por perfil |
| EV15 | Commit 9946585: testes HTTP de aprova├º├úo; 56 testes |
| EV16 | Actions #27 e #28 aprovados |
| EV17 | Reserva n┬║ 6 aprovada e cancelada; n┬║ 7 rejeitada |
| EV18 | Commit 1515dcd: auditoria no servi├ºo e testes |
| EV19 | Commit 0fc4cf5: consulta de auditoria e filtros; 62 testes |
| EV20 | Commit 6ac9d65: bot├úo de auditoria |
| EV21 | Confer├¬ncia manual de autor, hor├írio e situa├º├Áes |
| EV22 | Respons├ível bloqueado em /auditoria |
| EV23 | Commit db1e5e8: 65 testes; Actions #37 aprovado |
| EV24 | Manuten├º├úo: 86 testes em 21,313 segundos |
| EV25 | Manuten├º├úo n┬║ 1 da Sala 101 em 01/11/2026, das 14h ├ás 16h; reserva n┬║ 9 aceita a partir das 16h |
| EV26 | Fluxo de materiais da reserva n┬║ 11 em 26/10/2026 |
| EV27 | Retirada ├ás 20:17:10 e devolu├º├úo ├ás 20:18:04 na auditoria |
| EV28 | 103 testes em 28,560 segundos |
| EV29 | Commit 22014eb: materiais, auditoria e testes; push confirmado |
| EV30 | Actions #45 aprovado em 17 segundos |
| EV31 | Actions #46 aprovado em 23 segundos |
| EV32 | Cobertura hist├│rica: 89,87% de linhas e 85,16% de ramifica├º├Áes |
| EV33 | Commit 400b119: registro da cobertura |
| EV34 | Commit 6b8d472: disponibilidade com 15 testes |
| EV35 | 118 testes em 48,257 segundos |
| EV36 | Consulta excluiu Sala 101 durante manuten├º├úo e permitiu per├¡odo consecutivo |
| EV37 | Per├¡odo invertido recusado na busca |
| EV38 | Migra├º├úo para detalhes de altera├º├úo com backup e 9 registros preservados |
| EV39 | Finalidade da reserva n┬║ 9 alterada, mantendo 01/11/2026, das 16h ├ás 17h |
| EV40 | Edi├º├úo para 14:30ÔÇô15:30 recusada por manuten├º├úo; per├¡odo preservado |
| EV41 | Evento n┬║ 10 com finalidade anterior e nova |
| EV42 | 118 testes em 32,354 segundos ap├│s mudan├ºas de edi├º├úo |
| EV43 | 24 testes de edi├º├úo; su├¡te de 142 informada como aprovada |
| EV44 | Commit 35b5fe5: edi├º├úo, auditoria e testes |
| EV45 | Actions #53 aprovado em 24 segundos |
| EV46 | Actions #54 aprovado em 23 segundos |
| EV47 | 12 testes HTTP de edi├º├úo aprovados |
| EV48 | Commit b9d752d: testes HTTP e RTM |
| EV49 | Actions #55 em 23 segundos e #56 em 25 segundos |
| EV50 | 10 testes de filtros, incluindo 7 novos |
| EV51 | 161 testes em 54,707 segundos |
| EV52 | Commit 9e94725: EM_USO nas Ativas e testes |
| EV53 | Actions #57 e #58 aprovados |
| EV54 | Tabela notificacoes criada |
| EV55 | Tela sem notifica├º├Áes apresentada corretamente |
| EV56 | Edi├º├úo da reserva n┬║ 9 gerou aviso em 28/10/2026 ├ás 19:10:08 |
| EV57 | Aviso marcado como Lida e preservado |
| EV58 | Bot├úo Notifica├º├Áes confirmado no menu |
| EV59 | 24 testes de notifica├º├Áes aprovados |
| EV60 | Su├¡te de 185 testes informada como aprovada |
| EV61 | Commit 5a18890: notifica├º├Áes, leitura e testes |
| EV62 | Actions de 5a18890 informado como aprovado |
| EV63 | 16 testes de relat├│rios; su├¡te de 201 informada como aprovada |
| EV64 | Relat├│rio sem datas: 11 reservas e 4,33 horas previstas |
| EV65 | Relat├│rio de 01/11/2026: uma reserva da Sala 101 e 1,00 hora prevista |
| EV66 | Datas invertidas recusadas, com campos preservados |
| EV67 | 12 testes HTTP de relat├│rios em 2,484 segundos |
| EV68 | Commit 2ae1f0c: relat├│rios, filtros e testes |
| EV69 | Actions de relat├│rios informado como aprovado; posteriormente conferidos #63 e #64 verdes |
| EV70 | 213 testes com cobertura em 58,742 segundos |
| EV71 | Medi├º├úo de 28/10/2026: 93,31% de linhas e 90,23% de ramifica├º├Áes |
| EV72 | servico_relatorios.py com 100% de cobertura combinada nessa medi├º├úo |
| EV73 | coverage.json gerado e percentuais separados conferidos |

### Evid├¬ncias acrescentadas nesta atualiza├º├úo

| ID | Evid├¬ncia |
| --- | --- |
| EV74 | HTML da cobertura gerado e aberto; cinco m├│dulos e total combinado de 92% |
| EV75 | Commit d776bd7: RTM e cobertura com 213 testes; push confirmado |
| EV76 | Actions #65 e #66 aprovados, conforme imagem |
| EV77 | Commit 4062de2: workflow com medi├º├úo e metas separadas de cobertura |
| EV78 | Execu├º├Áes do workflow com metas informadas como verdes pelo executor |
| EV79 | 18 testes HTTP de materiais informados como aprovados |
| EV80 | 231 testes aprovados em 70,820 segundos |
| EV81 | Commit 4ca4689: testes HTTP de materiais; push confirmado |
| EV82 | Actions da etapa de materiais informado como aprovado |
| EV83 | Migra├º├úo para a├º├úo NAO_COMPARECEU conclu├¡da em 28/10/2026, com backup e 11 registros preservados |
| EV84 | 14 testes do servi├ºo de n├úo comparecimento aprovados em 3,476 segundos |
| EV85 | 245 testes aprovados em 69,067 segundos |
| EV86 | 12 testes HTTP de n├úo comparecimento informados como aprovados |
| EV87 | 257 testes aprovados em 84,677 segundos, em 29/10/2026 |
| EV88 | Commit f1d0af2: n├úo comparecimento com auditoria, migra├º├úo e testes; push confirmado |
| EV89 | GitHub Actions de f1d0af2 informado como aprovado; n├║mero e dura├º├úo n├úo registrados |
| EV90 | Reserva n┬║ 12 do Projetor 01 criada; evento n┬║ 12 em 29/10/2026 ├ás 17:44:15 |
| EV91 | Reserva n┬║ 12 aprovada pelo Respons├ível de Recursos; evento n┬║ 13 ├ás 17:45:05 |
| EV92 | Interface confirmou n├úo comparecimento da reserva n┬║ 12 e removeu o cart├úo da gest├úo |
| EV93 | Evento n┬║ 14: Administrador do projeto registrou Aprovada ÔåÆ N├úo compareceu em 29/10/2026 ├ás 17:54:06 |
| EV94 | R├│tulo ÔÇ£N├úo compareceuÔÇØ apresentado corretamente no t├¡tulo da auditoria ap├│s ajuste do template |

O hash e o push do ajuste posterior de auditoria.html ainda n├úo foram conferidos nesta matriz.

### Links

- [Reposit├│rio](https://github.com/Arthurmrsilva/organizacao-recursos)
- [Pull Request n┬║ 1](https://github.com/Arthurmrsilva/organizacao-recursos/pull/1)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Materiais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/22014eb)
- [Disponibilidade](https://github.com/Arthurmrsilva/organizacao-recursos/commit/6b8d472)
- [Edi├º├úo](https://github.com/Arthurmrsilva/organizacao-recursos/commit/35b5fe5)
- [Testes HTTP de edi├º├úo](https://github.com/Arthurmrsilva/organizacao-recursos/commit/b9d752d)
- [Corre├º├úo dos filtros](https://github.com/Arthurmrsilva/organizacao-recursos/commit/9e94725)
- [Notifica├º├Áes](https://github.com/Arthurmrsilva/organizacao-recursos/commit/5a18890)
- [Relat├│rios](https://github.com/Arthurmrsilva/organizacao-recursos/commit/2ae1f0c)
- [RTM e cobertura](https://github.com/Arthurmrsilva/organizacao-recursos/commit/d776bd7)
- [Metas na CI](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4062de2)
- [Testes HTTP de materiais](https://github.com/Arthurmrsilva/organizacao-recursos/commit/4ca4689)
- [N├úo comparecimento](https://github.com/Arthurmrsilva/organizacao-recursos/commit/f1d0af2)

### Organiza├º├úo das evid├¬ncias

Os prints da entrega devem identificar cen├írio, data, resultado esperado, resultado observado, requisito relacionado e commit, quando aplic├ível.

As contagens hist├│ricas s├úo preservadas.

A aprova├º├úo do workflow n├úo substitui revis├úo por outro integrante.

## 6. Metas e verifica├º├Áes de qualidade

| Item | Meta ou exig├¬ncia | Situa├º├úo |
| --- | --- | --- |
| Cobertura de linhas | Pelo menos 80% | 93,31% na medi├º├úo detalhada de 213 testes; CI atual informada como aprovada |
| Cobertura de ramifica├º├Áes | Pelo menos 70% | 90,23% na medi├º├úo detalhada de 213 testes; CI atual informada como aprovada |
| Rastreabilidade cr├¡tica | 100% das regras cr├¡ticas ligadas a testes e evid├¬ncias | Parcial; consolidar revis├úo dos cen├írios cr├¡ticos |
| Defeitos e vulnerabilidades cr├¡ticas | Nenhum conhecido pendente na entrega | Verifica├º├úo completa pendente |
| Testes unit├írios isolados | Regras sem depend├¬ncias reais | Amplia├º├úo pendente; servi├ºos utilizam persist├¬ncia real nos testes |
| Integra├º├úo | Persist├¬ncia e integra├º├úo das camadas | Verificada no escopo testado com SQLite e cliente Flask |
| Testes em container | Banco com Testcontainers | Pendente |
| Integra├º├úo externa | WireMock quando aplic├ível | Sem integra├º├úo externa; notifica├º├Áes internas adotadas para RF11 |
| HTTP em caixa-preta | Acesso externo por HTTP | Pendente |
| Ponta a ponta | Automa├º├úo no navegador | Pendente |
| Concorr├¬ncia | Uma ├║nica reserva aceita no mesmo per├¡odo | Verificada no servi├ºo; HTTP e carga pendentes |
| TDD ou BDD | Funcionalidade com evid├¬ncias | RED e GREEN registrados; consolidar documenta├º├úo |
| CI | Testes em push e Pull Requests | Implementada, com medi├º├úo e metas separadas de cobertura |
| An├ílise est├ítica | SonarCloud | Pendente |
| Carga | Plano e resultados com JMeter | Pendente |
| Revis├úo por pares | Revis├úo de outro integrante | Pendente |
| Arquitetura | C4, sequ├¬ncias, utility tree, riscos, trade-offs e ADRs | Pendente |
| Gest├úo de defeitos | Registro, prioridade, corre├º├úo e reteste | Parcial: corre├º├úo do filtro registrada; consolidar documento |
| Relat├│rio final | Evid├¬ncias, m├®tricas e decis├úo de qualidade | Pendente |
| Apresenta├º├úo | Demonstra├º├úo e dom├¡nio pelo grupo | Pendente |

A confirma├º├úo de aceita├º├úo de Python e das ferramentas equivalentes ├ás citadas no enunciado permanece pendente de registro.

## 7. Hist├│rico ÔÇö Cancelamento

**Data:** 25/10/2026.

- Consulta das pr├│prias reservas.
- Cancelamento pelo propriet├írio antes do in├¡cio.
- Situa├º├Áes permitidas: SOLICITADA e APROVADA.
- Registro preservado e per├¡odo liberado.
- 31 testes em 9,850 segundos.
- Commit ecb0eb7.

Edi├º├úo, auditoria e notifica├º├Áes foram acrescentadas posteriormente.

## 8. Hist├│rico ÔÇö Aprova├º├úo

**Data:** 25/10/2026.

- Respons├ível vinculado ao recurso por script local.
- Aprova├º├úo e rejei├º├úo das solicita├º├Áes vinculadas.
- Verifica├º├úo de perfil, v├¡nculo, prazo, recurso ativo e conflito.
- Administrador azul, respons├ível roxo e solicitante verde.
- 56 testes; commits cca4432 e 9946585.
- Actions #27 e #28 aprovados.

A interface para vincular respons├íveis permanece pendente.

Avisos ao solicitante foram acrescentados em 28/10/2026.

## 9. Auditoria e filtros de reservas

**Implanta├º├úo inicial:** 25/10/2026.

Opera├º├Áes auditadas atualmente:

- Cria├º├úo.
- Altera├º├úo.
- Cancelamento.
- Aprova├º├úo.
- Rejei├º├úo.
- Retirada.
- Devolu├º├úo.
- N├úo comparecimento de materiais.

Cada evento registra reserva, autor, a├º├úo, hor├írio e situa├º├Áes anterior e nova.

A auditoria usa a mesma transa├º├úo da opera├º├úo. Falhas provocam rollback conjunto.

A consulta ├® exclusiva do administrador e apresenta os 100 eventos mais recentes.

### Filtros das pr├│prias reservas

- **Ativas:** todas em EM_USO; SOLICITADA e APROVADA somente com t├®rmino futuro.
- **Hist├│rico:** complemento da condi├º├úo de Ativas.
- **Todas:** todos os registros do usu├írio conectado.
- Ativas: in├¡cio e ID crescentes.
- Hist├│rico e Todas: in├¡cio e ID decrescentes.

O encerramento do per├¡odo n├úo altera automaticamente a situa├º├úo.

EM_USO continua em Ativas at├® a devolu├º├úo, com aviso ap├│s o prazo.

### Limita├º├Áes

- Eventos anteriores ├á implanta├º├úo n├úo s├úo reconstru├¡dos.
- Hor├írios seguem o rel├│gio local do servidor.
- Consulta sem pagina├º├úo.
- Nome exibido corresponde ao recurso atual da reserva.
- Altera├º├Áes preservam dados anteriores e novos na coluna detalhes.
- Limite de 100 eventos e ordena├º├úo da auditoria precisam de testes espec├¡ficos.
- Novas opera├º├Áes exigir├úo novos eventos e testes.

## 10. Hist├│rico ÔÇö Manuten├º├úo

**Data:** 25/10/2026.

- Cadastro e consulta pelo administrador.
- Per├¡odo futuro e t├®rmino posterior ao in├¡cio.
- Motivo obrigat├│rio de at├® 200 caracteres.
- Bloqueio de sobreposi├º├úo com manuten├º├úo ou reserva ativa.
- Cria├º├úo e aprova├º├úo de reserva bloqueadas durante manuten├º├úo.
- Hor├írios consecutivos permitidos.
- Prote├º├úo CSRF.
- 12 testes de servi├ºo e 9 de rotas.
- Su├¡te hist├│rica: 86 testes em 21,313 segundos.

Autor e data ficam na tabela de manuten├º├úo. O cadastro n├úo gera evento na auditoria de reservas.

Pend├¬ncias: edi├º├úo e desativa├º├úo pela interface, manuten├º├úo imediata e concorr├¬ncia espec├¡fica.

## 11. Materiais ÔÇö Retirada e devolu├º├úo

**Implanta├º├úo inicial:** 26/10/2026.

- Administrador gerencia movimenta├º├Áes.
- Respons├ível gerencia materiais vinculados.
- Retirada de reserva APROVADA durante o per├¡odo permitido.
- Bloqueio de recurso inativo, em manuten├º├úo ou j├í em uso.
- Retirada: APROVADA ÔåÆ EM_USO.
- Devolu├º├úo: EM_USO ÔåÆ CONCLUIDA.
- Devolu├º├úo permitida ap├│s o prazo e com recurso inativo.
- Auditoria das movimenta├º├Áes.

### Testes

- test_materiais.py: 17 m├®todos.
- test_materiais_http.py: 18 m├®todos.
- Permiss├Áes, isolamento por respons├ível, CSRF, estados e persist├¬ncia.
- Materiais atrasados em uso continuam vis├¡veis.
- Opera├º├úo por GET n├úo realiza movimenta├º├úo.
- A├º├Áes inv├ílidas e reservas inexistentes s├úo recusadas.
- Recusas verificadas sem altera├º├úo de estado ou cria├º├úo de auditoria.

Commit dos testes HTTP: 4ca4689.

### Fluxo manual hist├│rico

Reserva n┬║ 11 do Projetor 01, em 26/10/2026, das 20:15 ├ás 21:15:

1. Solicita├º├úo aprovada.
2. Material apresentado na gest├úo.
3. Retirada ├ás 20:17:10 pelo Administrador do projeto.
4. Situa├º├úo alterada para EM_USO.
5. Devolu├º├úo ├ás 20:18:04 pelo mesmo administrador.
6. Situa├º├úo alterada para CONCLUIDA.
7. Cart├úo removido das movimenta├º├Áes em andamento.
8. Eventos n┬║ 8 e n┬║ 9 conferidos na auditoria.

Su├¡te hist├│rica inicial: 103 testes em 28,560 segundos.
Commit 22014eb; Actions #45 e #46 aprovados.

Pend├¬ncias: automa├º├úo de navegador e revis├úo por colega.

## 12. Cobertura de testes

### ├Ültima medi├º├úo com percentuais detalhados conferidos

**Data:** 28/10/2026.  
**Base funcional:** commit 2ae1f0c.

- Ferramenta: coverage.py 7.17.0.
- Execu├º├úo: 213 testes em 58,742 segundos.
- Linhas executadas: **628 de 673 ÔÇö 93,31%**.
- Ramifica├º├Áes executadas: **231 de 256 ÔÇö 90,23%**.
- Cobertura combinada exibida: **92%**.
- coverage.json gerado.
- Relat├│rio HTML posteriormente gerado e aberto.

| M├│dulo | Cobertura combinada |
| --- | --- |
| app.py | 89% |
| banco.py | 84% |
| servico_materiais.py | 97% |
| servico_relatorios.py | 100% |
| servico_reservas.py | 95% |
| Total | 92% |

Esses valores pertencem ├á vers├úo de 213 testes. N├úo s├úo apresentados como os percentuais exatos da vers├úo de 257 testes.

### Situa├º├úo da vers├úo atual

O workflow passou a medir os mesmos cinco m├│dulos e verificar separadamente:

- Pelo menos 80% de linhas.
- Pelo menos 70% de ramifica├º├Áes.

As execu├º├Áes ap├│s f1d0af2 foram informadas como aprovadas pelo executor.

Os percentuais exatos dessa execu├º├úo ainda precisam ser transcritos do resumo ou de uma nova medi├º├úo local.

### Escopo e limites

M├│dulos medidos:

- app.py.
- banco.py.
- servico_reservas.py.
- servico_materiais.py.
- servico_relatorios.py.

N├úo inclui templates, CSS, JavaScript nem scripts administrativos e de migra├º├úo.

Cobertura combinada considera linhas e ramifica├º├Áes.

100% em um m├│dulo n├úo comprova aus├¬ncia de defeitos ou teste de todas as entradas poss├¡veis.

### Medi├º├úo hist├│rica anterior

**Data:** 26/10/2026.

- 103 testes em 26,625 segundos.
- Quatro m├│dulos, sem servico_relatorios.py.
- Linhas: 417 de 464 ÔÇö 89,87%.
- Ramifica├º├Áes: 155 de 182 ÔÇö 85,16%.
- Commit 400b119.

### Como medir

```powershell
.\.venv\Scripts\python.exe -m coverage run --branch --source=app,banco,servico_reservas,servico_materiais,servico_relatorios -m unittest discover -s tests -v
```

```powershell
.\.venv\Scripts\python.exe -m coverage report -m
```

```powershell
.\.venv\Scripts\python.exe -m coverage json -o coverage.json
```

```powershell
.\.venv\Scripts\python.exe -c "import json; t=json.load(open('coverage.json'))['totals']; print('Linhas: {:.2f}%'.format(100*t['covered_lines']/t['num_statements'])); print('Ramificacoes: {:.2f}%'.format(100*t['covered_branches']/t['num_branches']))"
```

```powershell
.\.venv\Scripts\python.exe -m coverage html
```

Os relat├│rios precisam ser regenerados ap├│s uma nova execu├º├úo para representar seus resultados.

## 13. Pesquisa por disponibilidade

**Data:** 27/10/2026.

- In├¡cio e t├®rmino opcionais, preenchidos em conjunto.
- Valida├º├úo de datas e ordem do per├¡odo.
- Exclus├úo de recursos com reservas sobrepostas em SOLICITADA, APROVADA ou EM_USO.
- Exclus├úo de recursos com manuten├º├úo ativa sobreposta.
- Hor├írios consecutivos permitidos.
- Combina├º├úo com os demais filtros.
- Consulta de per├¡odos passados permitida.
- Atualiza├º├úo da lista sem subir a p├ígina.
- Limpeza tamb├®m remove o per├¡odo.

Evid├¬ncias: 15 testes, su├¡te hist├│rica de 118 em 48,257 segundos, commit 6b8d472 e verifica├º├Áes manuais da Sala 101.

## 14. Edi├º├úo e detalhes de auditoria

**Data:** 27/10/2026.

- Edi├º├úo pelo propriet├írio ativo e autenticado.
- Permitida em SOLICITADA ou APROVADA antes do in├¡cio.
- Altera├º├úo de recurso, per├¡odo e finalidade.
- Valida├º├úo de recurso ativo, datas e finalidade.
- Verifica├º├úo de manuten├º├úo e conflitos, excluindo a pr├│pria reserva.
- Recursos restritos e professores voltam para SOLICITADA.
- Recursos comuns ficam em APROVADA.
- Solicita├º├úo sem mudan├ºa ├® recusada.
- Auditoria ALTERACAO com dados anteriores e novos.
- Edi├º├úo e auditoria na mesma transa├º├úo.
- Interface apresenta antes e depois.

### Migra├º├úo

- Coluna detalhes e a├º├úo ALTERACAO acrescentadas.
- Backup e preserva├º├úo de 9 registros.
- Eventos antigos permanecem sem detalhes.
- Testes automatizados da migra├º├úo pendentes.

### Verifica├º├úo

- 24 testes de servi├ºo e 12 de rotas.
- Reserva n┬║ 9 alterada, mantendo 01/11/2026, das 16h ├ás 17h.
- Tentativa de 14:30ÔÇô15:30 recusada por manuten├º├úo.
- Evento n┬║ 10 conferido manualmente.
- Commits 35b5fe5 e b9d752d.
- Actions #53 a #56 aprovados.

## 15. Corre├º├úo ÔÇö Materiais em uso ap├│s o prazo

**Data:** 28/10/2026.

Problema: EM_USO sa├¡a das Ativas ap├│s o t├®rmino, mesmo sem devolu├º├úo.

Corre├º├úo:

- EM_USO permanece em Ativas.
- SOLICITADA e APROVADA dependem de t├®rmino futuro.
- Hist├│rico utiliza a condi├º├úo complementar.
- Aviso de prazo encerrado na interface.
- Nenhuma devolu├º├úo autom├ítica.

Verifica├º├úo:

- 7 m├®todos novos; arquivo passou de 3 para 10.
- Distribui├º├úo por estado e prazo.
- Limite exato com rel├│gio fixo.
- Aviso, filtro inv├ílido e ordena├º├úo.
- 161 testes em 54,707 segundos.
- Commit 9e94725; Actions #57 e #58 aprovados.

## 16. Notifica├º├Áes internas

**Data:** 28/10/2026.

Avisos persistidos no banco simulam notifica├º├Áes ao dono da reserva.

| Opera├º├úo | Aviso |
| --- | --- |
| Cria├º├úo comum | Criada e aprovada automaticamente |
| Cria├º├úo restrita ou professor | Aguardando aprova├º├úo |
| Edi├º├úo comum | Alterada e aprovada |
| Edi├º├úo restrita ou professor | Aguardando nova aprova├º├úo |
| Cancelamento | Reserva cancelada |
| Aprova├º├úo | Aprovada pelo respons├ível |
| Rejei├º├úo | Rejeitada pelo respons├ível |

### Persist├¬ncia

- Destinat├írio, reserva, mensagem, data e leitura.
- Avisos novos n├úo lidos.
- Reserva, auditoria e aviso na mesma transa├º├úo.
- Falha no aviso desfaz a opera├º├úo.
- Recusas n├úo geram avisos de sucesso.
- Eventos anteriores n├úo s├úo reconstru├¡dos.

### Rotas

- GET /notificacoes exige login e lista somente os pr├│prios avisos.
- Ordena├º├úo por data e ID decrescentes.
- POST /notificacoes/<id>/ler exige login e CSRF.
- UPDATE vinculado ao destinat├írio.
- Aviso inexistente ou alheio retorna 404.
- GET n├úo marca leitura.
- Repeti├º├úo n├úo duplica registros.
- Avisos lidos permanecem na lista.

### Verifica├º├úo e limita├º├Áes

- 24 testes de gera├º├úo, destinat├írio, leitura, isolamento, CSRF, escape e rollback.
- Fluxo manual da reserva n┬║ 9.
- Commit 5a18890; CI informada como aprovada.
- Sem e-mail, SMS, integra├º├úo externa ou atualiza├º├úo em tempo real.
- Sem pagina├º├úo, contador de n├úo lidas ou aviso ao respons├ível.
- Retirada, devolu├º├úo e n├úo comparecimento ainda n├úo geram notifica├º├Áes.
- Testes espec├¡ficos de usu├írio inativo nessas rotas podem ser ampliados.

## 17. Relat├│rios administrativos

**Data:** 28/10/2026.  
**Commit:** 2ae1f0c.

### Acesso

- GET /relatorios.
- Somente administrador ativo.
- Servi├ºo tamb├®m verifica permiss├úo.
- Outros perfis recebem 403.
- Usu├írio inativo ├® redirecionado ao login.
- Consulta sem altera├º├úo das reservas.

### Per├¡odo

- Duas datas opcionais, preenchidas em conjunto.
- Datas iguais permitidas.
- Data final inclu├¡da por inteiro.
- Limite final interno no in├¡cio do dia seguinte.
- Reservas sobrepostas ao per├¡odo s├úo consideradas.
- Contato sem sobreposi├º├úo nos limites ├® exclu├¡do.
- Erros retornam 400 e preservam os campos.

### Indicadores

- Total de reservas.
- Contagem das sete situa├º├Áes.
- Agrupamento por recurso.
- Quantidade de reservas por recurso.
- Quantidade considerada no c├ílculo de horas.
- Horas previstas por recurso e no total.
- Recursos inativos inclu├¡dos quando possuem reservas.
- Recursos sem reservas no per├¡odo n├úo aparecem.

Horas previstas consideram APROVADA, EM_USO e CONCLUIDA.

As demais situa├º├Áes entram nas contagens, mas n├úo somam horas.

Somente a parte do per├¡odo sobreposta ao filtro ├® somada. O arredondamento ocorre depois da soma.

O indicador representa tempo reservado, n├úo tempo real de utiliza├º├úo.

### Conflitos evitados

- Indicador ainda indispon├¡vel.
- Tentativas recusadas n├úo s├úo persistidas para essa finalidade.
- Aus├¬ncia de dados n├úo ├® apresentada como zero.
- Tentativas anteriores n├úo podem ser reconstru├¡das com precis├úo.
- Implementa├º├úo, defini├º├úo do per├¡odo e testes pendentes.

### Verifica├º├úo

- 16 testes de servi├ºo e 12 de rotas.
- Permiss├Áes, datas, limites, contagens, agrupamento e arredondamento.
- Sem datas: 11 reservas e 4,33 horas previstas na base daquele teste manual.
- Em 01/11/2026: uma reserva e 1,00 hora prevista.
- Datas invertidas recusadas.
- Actions #63 e #64 aprovados, conforme imagem posterior.

Limita├º├Áes: conflitos evitados, tempo real de utiliza├º├úo, exporta├º├úo, pagina├º├úo e navegador automatizado.

RF12 permanece parcial.

## 18. Integra├º├úo cont├¡nua e metas de cobertura

**Workflow:** .github/workflows/testes.yml  
**Commit da altera├º├úo:** 4062de2.

- Executa em push e Pull Requests.
- Ubuntu e Python 3.14.
- Instala depend├¬ncias de requirements.txt.
- Instala coverage.py 7.17.0.
- Executa unittest com medi├º├úo de linhas e ramifica├º├Áes.
- Mede os cinco m├│dulos definidos na se├º├úo 12.
- Mostra relat├│rio no log.
- Gera coverage.json na execu├º├úo.
- Calcula percentuais separados.
- Escreve a tabela no resumo do GitHub Actions.
- Falha se algum teste falhar.
- Falha com linhas abaixo de 80% ou ramifica├º├Áes abaixo de 70%.
- Falha se a medi├º├úo n├úo contiver linhas ou ramifica├º├Áes.

O workflow gera o JSON durante a execu├º├úo, mas ainda n├úo publica os relat├│rios como artefatos para download.

As execu├º├Áes foram informadas como verdes ap├│s a altera├º├úo e ap├│s a etapa de n├úo comparecimento.

## 19. N├úo comparecimento de materiais

**Implementa├º├úo iniciada:** 28/10/2026.  
**Verifica├º├úo manual:** 29/10/2026.  
**Commit funcional:** f1d0af2.

### Regra implementada

- Exclusiva para recursos do tipo MATERIAL.
- Reserva deve estar APROVADA.
- Hor├írio atual deve ser igual ou posterior ao t├®rmino.
- Administrador ativo pode registrar.
- Respons├ível ativo pode registrar somente em recurso vinculado.
- Solicitante e respons├ível alheio n├úo podem registrar.
- Recurso inativo n├úo impede o registro hist├│rico.
- Reserva EM_USO exige devolu├º├úo e n├úo pode receber n├úo comparecimento.
- A├º├úo manual; n├úo existe altera├º├úo autom├ítica ao vencer o per├¡odo.
- Mudan├ºa: APROVADA ÔåÆ NAO_COMPARECEU.
- Repeti├º├úo ├® recusada e n├úo duplica auditoria.

### Banco e migra├º├úo

- A├º├úo NAO_COMPARECEU adicionada ├á restri├º├úo da auditoria.
- Situa├º├úo NAO_COMPARECEU j├í existia nas reservas.
- Script atualizar_auditoria_nao_comparecimento.py.
- Backup completo antes da migra├º├úo.
- Migra├º├úo manual conclu├¡da com 11 registros preservados.
- C├│pia dos registros conferida antes da troca de tabela.
- ├ìndices e gatilhos existentes recriados.
- V├¡nculos da tabela de auditoria conferidos.
- Testes automatizados da migra├º├úo pendentes.

### Servi├ºo, rota e interface

- Fun├º├úo registrar_nao_comparecimento em servico_materiais.py.
- Atualiza├º├úo e auditoria na mesma transa├º├úo.
- Falha na auditoria desfaz a mudan├ºa.
- POST /materiais/<id>/movimentar com acao=NAO_COMPARECEU.
- Login, perfil e CSRF exigidos.
- Servi├ºo verifica v├¡nculo, prazo e situa├º├úo.
- Bot├úo aparece para reserva APROVADA com per├¡odo encerrado.
- Confirma├º├úo antes do envio.
- Sucesso apresenta mensagem e remove o cart├úo da gest├úo.
- Registro continua no banco e no hist├│rico.
- Auditoria exibe o r├│tulo ÔÇ£N├úo compareceuÔÇØ.
- N├úo h├í notifica├º├úo interna dessa opera├º├úo.

### Testes

- test_nao_comparecimento.py: 14 m├®todos.
- test_nao_comparecimento_http.py: 12 m├®todos.
- Administrador e respons├ível vinculado.
- Usu├írio inativo, inexistente, solicitante e respons├ível alheio.
- Reserva inexistente.
- Antes do t├®rmino e instante exato do t├®rmino.
- Bloqueio dos demais estados.
- Recurso inativo.
- Recusa de sala e professor.
- Repeti├º├úo sem duplicar auditoria.
- Rollback ap├│s falha simulada na auditoria.
- CSRF ausente e incorreto.
- Exibi├º├úo do bot├úo e mensagem de sucesso.
- Preserva├º├úo dos dados nas recusas.

### Fluxo manual da reserva n┬║ 12

**Recurso:** Projetor 01.

1. Cria├º├úo pelo Administrador do projeto.
2. Evento n┬║ 12: 29/10/2026 ├ás 17:44:15, aguardando aprova├º├úo.
3. Aprova├º├úo pelo Respons├ível de Recursos.
4. Evento n┬║ 13: 29/10/2026 ├ás 17:45:05.
5. Nenhuma retirada registrada.
6. Ap├│s o t├®rmino, bot├úo de n├úo comparecimento utilizado.
7. Mensagem ÔÇ£N├úo comparecimento da reserva n┬║ 12 registrado!ÔÇØ.
8. Cart├úo removido da gest├úo de materiais.
9. Evento n┬║ 14: 29/10/2026 ├ás 17:54:06.
10. Autor: Administrador do projeto.
11. Situa├º├úo anterior: Aprovada.
12. Nova situa├º├úo: N├úo compareceu.
13. T├¡tulo do evento apresentado como ÔÇ£N├úo compareceuÔÇØ.

### Limites

- Implementado somente para materiais.
- Sem registro autom├ítico.
- Sem notifica├º├úo ao solicitante.
- Sem automa├º├úo de navegador.
- Migra├º├úo ainda sem testes automatizados.
- Ajuste posterior do r├│tulo do template verificado manualmente; hash e push ainda n├úo conferidos nesta atualiza├º├úo.

## 20. Pr├│ximas verifica├º├Áes

- Confirmar commit e push do ajuste de auditoria.html.
- Registrar os percentuais exatos da cobertura da vers├úo atual.
- Atualizar os relat├│rios locais de cobertura quando necess├írio.
- Implementar registro de conflitos recusados e indicador verific├ível.
- Revisar o escopo de n├úo comparecimento para outros tipos, conforme enunciado.
- Testar as migra├º├Áes da auditoria.
- Ampliar cen├írios expl├¡citos de conflitos por tipo.
- Testar concorr├¬ncia entre manuten├º├úo e reserva.
- Acrescentar HTTP externo, navegador e carga.
- Completar README de instala├º├úo e fluxos.
- Consolidar evid├¬ncias TDD ou BDD.
- Completar arquitetura, an├ílise est├ítica e revis├úo de seguran├ºa.
- Consolidar registro de defeitos e retestes.
- Obter revis├úo por outro integrante.
- Preparar relat├│rio final e apresenta├º├úo.
