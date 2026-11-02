# Registro de defeitos e retestes

**Projeto:** Organização de Recursos  
**Data de consolidação:** 02/11/2026  
**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

## 1. Critérios

Este registro consolida problemas observados durante o desenvolvimento e a verificação.

As prioridades foram atribuídas nesta consolidação e precisam de revisão pelo grupo.

- P1: impede uma operação importante ou uma verificação obrigatória.
- P2: prejudica parte do comportamento, dos testes ou da documentação.
- P3: impacto menor, sem impedir o fluxo principal.

“Corrigido no escopo verificado” significa que existe evidência de correção e reteste dos cenários registrados. Não comprova ausência de outros defeitos.

## 2. Resumo

| ID | Problema | Área | Prioridade | Situação |
| --- | --- | --- | --- | --- |
| DEF01 | Material em uso desaparecia das reservas Ativas após o prazo | Aplicação | P2 | Corrigido no escopo verificado |
| DEF02 | Template compartilhado com nome diferente do include | Aplicação | P1 | Corrigido no escopo verificado |
| DEF03 | Conexões abertas impediam limpeza dos bancos temporários no Windows | Testes | P2 | Corrigido no escopo verificado |
| DEF04 | Sintaxe YAML impedia execução da CI | Pipeline | P1 | Corrigido no escopo verificado |
| DEF05 | Acentos e formatação corrompidos na documentação de rastreabilidade | Documentação | P2 | Corrigido nos trechos conferidos |
| INV01 | Falhas de conexão no ensaio de carga sem pausa | Ambiente ou aplicação: causa não confirmada | P2 | Investigação pendente |

Os registros representam problemas observados. Não constituem uma contagem completa de todos os defeitos do projeto.

## 3. DEF01 — Material em uso desaparecia das Ativas

**Requisitos relacionados:** RF04 e RF09.  
**Regra relacionada:** RC05.  
**Prioridade:** P2.

### Reprodução

1. Preparar uma reserva de material em EM_USO.
2. Considerar horário atual posterior ao término reservado.
3. Consultar Minhas reservas com o filtro Ativas.

### Resultado esperado

O material deve continuar em Ativas enquanto não houver devolução.

### Resultado observado

A reserva deixava de aparecer em Ativas após o término, mesmo permanecendo em EM_USO.

### Correção

- EM_USO passou a permanecer em Ativas independentemente do término.
- SOLICITADA e APROVADA continuam dependendo de término futuro.
- Histórico utiliza a condição complementar.
- A interface apresenta aviso de prazo encerrado.
- Não foi acrescentada devolução automática.

### Reteste e evidências

- Testes de estados, prazo, limite exato, filtros e ordenação.
- Arquivo tests/test_minhas_reservas.py.
- Suíte da etapa: 161 testes aprovados em 54,707 segundos.
- Commit 9e94725.
- Actions #57 e #58 aprovados.

**Situação:** corrigido no escopo verificado.

## 4. DEF02 — Nome incorreto do template compartilhado

**Requisitos relacionados:** RF07, RF09 e RF13.  
**Prioridade:** P1.

### Reprodução

Executar os fluxos e testes que renderizam as páginas de aprovação e gestão de materiais após a extração do trecho compartilhado.

### Resultado esperado

As páginas devem carregar os dados da reserva e seus formulários.

### Resultado observado

O arquivo compartilhado foi criado com nome diferente do utilizado no include. A execução apresentou respostas HTTP 500 e 19 falhas na suíte.

### Correção

Nome do arquivo ajustado para templates/_dados_reserva.html, conforme utilizado pelos templates consumidores.

### Reteste e evidências

- Reteste local informado como aprovado.
- Execuções posteriores da CI aprovadas.
- Templates envolvidos:
  - templates/_dados_reserva.html
  - templates/aprovacoes.html
  - templates/materiais.html

O hash específico da correção não foi individualizado neste registro.

**Situação:** corrigido no escopo verificado.

## 5. DEF03 — Limpeza de banco temporário bloqueada no Windows

**Área:** infraestrutura dos testes de migração.  
**Requisito relacionado:** RF10.  
**Prioridade:** P2.

### Reprodução

Executar os testes da migração da auditoria e remover os bancos temporários após os cenários.

### Resultado esperado

As conexões devem ser encerradas e os arquivos temporários removidos ao final de cada teste.

### Resultado observado

Conexões SQLite permaneciam abertas, provocando PermissionError durante a remoção dos arquivos no Windows.

### Correção

Fechamento explícito das conexões em finally e liberação dos recursos antes da limpeza, preservando commit ou rollback.

### Reteste e evidências

- Oito testes específicos aprovados.
- Arquivo tests/test_atualizar_auditoria.py.
- Suíte completa posterior de 283 testes aprovada.
- Cobertura do script incluída nas medições posteriores.

O problema pertence à infraestrutura de teste. Não é apresentado como falha de limpeza observada no uso normal da aplicação.

**Situação:** corrigido no escopo verificado.

## 6. DEF04 — Sintaxe YAML impedia execução da CI

**Área:** integração contínua.  
**Prioridade:** P1.

### Reprodução

Disparar o workflow na versão com sintaxe inválida.

### Resultado esperado

O GitHub Actions deve interpretar o workflow e iniciar as etapas configuradas.

### Resultado observado

A execução #87 foi recusada antes do início dos testes por erro de sintaxe YAML.

### Correção

Ajuste da sintaxe do comando de instalação no workflow.

### Reteste e evidências

- Commit c81e8ae.
- Execuções #88 e #89 aprovadas.

A reprovação anterior não representa uma execução dos testes da aplicação.

**Situação:** corrigido no escopo verificado.

## 7. DEF05 — Documentação com caracteres corrompidos

**Requisito relacionado:** RF14.  
**Prioridade:** P2.

### Reprodução

Abrir a documentação de rastreabilidade afetada e consultar palavras acentuadas, títulos e tabelas.

### Resultado esperado

Texto legível em português e marcação Markdown válida.

### Resultado observado

Apareciam sequências como Organiza├º├úo e ÔÇö. A cópia enviada também apresentava marcação escapada e títulos formatados incorretamente.

### Correção

- RTM.md atualizado com texto e formatação corrigidos.
- RTM_historico.md teve os padrões de caracteres recuperados.
- Backup criado antes da recuperação do histórico.
- Conteúdo histórico mantido separado dos resultados atuais.

### Reteste e evidências

- Conferência visual de palavras acentuadas no VS Code.
- Commit b8b1de9: correção da acentuação do histórico.
- Revisão integral da renderização ainda pode identificar outros problemas de apresentação.

**Situação:** corrigido nos trechos conferidos.

## 8. INV01 — Falhas de conexão sob carga sem pausa

**Área:** ambiente de carga ou aplicação; causa não confirmada.  
**Prioridade proposta:** P2.  
**Situação:** investigação pendente.

### Cenário

- JMeter 5.6.3.
- Dez usuários configurados.
- Ramp-up de cinco segundos.
- Duração configurada de 60 segundos.
- GET /login.
- Sem pausa entre as requisições.
- Cliente e servidor executados na mesma máquina.

### Resultado observado

- 17.633 amostras.
- 16.344 respostas HTTP 200.
- 1.289 falhas, equivalentes a 7,31%.
- java.net.BindException.
- Mensagem: Address already in use: connect.

### Evidência

performance/carga_login_10usuarios_60s_01.jtl.

### Ação posterior

Foi executado outro cenário com pausa de um segundo por usuário:

- 570 amostras.
- Todas com HTTP 200.
- Nenhuma falha registrada.

Evidência: performance/carga_login_10usuarios_60s_pausa_01.jtl.

### Interpretação

A pausa reduziu a carga oferecida e alterou o cenário.

O resultado posterior não confirma a causa das falhas anteriores nem comprova sua correção.

Não havia critério de aceitação de desempenho definido antes do ensaio.

### Investigação proposta

- Correlacionar os horários das falhas com os logs da aplicação.
- Observar conexões e recursos do cliente e do servidor.
- Repetir o cenário em condições controladas.
- Separar o gerador de carga do servidor, quando possível.
- Definir critérios de aceitação antes dos novos ensaios.

Não atribuir o problema à aplicação ou ao gerador de carga sem evidência adicional.

## 9. Encerramento e revisão

Antes da entrega, o grupo deve:

- Revisar prioridade, reprodução e evidências de cada registro.
- Acrescentar responsáveis e datas quando confirmados.
- Conferir os links e versões dos retestes.
- Manter a investigação INV01 identificada como pendente.
- Registrar a revisão por outro integrante.

A inexistência de outros defeitos neste documento não comprova ausência de problemas na aplicação.

## 10. Referências

- [Rastreabilidade](RTM.md)
- [Histórico](RTM_historico.md)
- [Arquitetura](ARQUITETURA.md)
- [Segurança](SEGURANCA.md)
- [Desempenho](performance/README.md)