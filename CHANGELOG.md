# Changelog

## rc5 — em preparação, 10/11/2026

- Alinha checklist, índice de evidências, README e decisão de qualidade.
- Remove indicações desatualizadas de revisão e concordância pendentes.
- Identifica a CI e os anexos da rc4 pelo commit de origem.
- Separa evidências históricas do fechamento da próxima candidata.
- Preserva as ressalvas técnicas e não antecipa o envio pelo formulário.
- Alterações apenas documentais; publicação e CI da rc5 ainda serão conferidas.

## v1.0.0-rc4 — publicada em 10/11/2026

- Commit: ca08ea6132c462fec7228d22892f50ad8ae82926.
- Inclui o relato funcional de Nicolas e as contribuições dos integrantes.
- Registra as revisões e a concordância dos três com a entrega com ressalvas.
- CI da tag: testes automatizados #245 e Testcontainers #83 aprovados.
- Relatórios preservados na [release rc4](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc4).
- Checklist e índice ainda continham referências antigas, corrigidas na preparação da rc5.

## v1.0.0-rc3 — publicada

- Commit: b2949306587d37801be304101d36bf6974bcb6f0.
- Consolidação documental anterior às confirmações e contribuições posteriores.
- CI e anexos preservados na [release rc3](https://github.com/Arthurmrsilva/organizacao-recursos/releases/tag/v1.0.0-rc3).

## Histórico anterior à rc3

As seções seguintes preservam os resultados e as pendências das datas
originais; não representam o estado atual das confirmações do grupo.

## Complemento posterior à rc2 — PR #4

- Registra testes funcionais parciais relatados por Nicolas e Robert.
- Vincula o relato à decisão de qualidade e ao índice de evidências.
- Commit de integração: d937c1e.
- CI #211 e #49 aprovada.
- Alterações somente documentais.

## v1.0.0-rc2 — publicada

- Commit: 12fae65.
- Acrescenta o registro de fechamento e referências documentais.
- CI da tag #208 e #46 aprovada.
- Relatórios preservados na release.
- Sem alterações no código da aplicação em relação à rc1.

## Histórico de preparação da rc1 — 03/11/2026

O conteúdo abaixo preserva o registro anterior à publicação.
A rc1 foi posteriormente publicada no commit 3a1ef85.
As pendências descritas nessa seção representam aquela data.

Atualização: 03/11/2026.

O pull request #1 foi integrado na main.
O repositório está público.
A tag v1.0.0-rc1 ainda não foi criada.

### Funcionalidades

- Login com senha armazenada como hash e encerramento de sessão.
- Perfis ADMIN, RESPONSAVEL e SOLICITANTE.
- Proteção CSRF nos formulários POST.
- Cadastro e consulta de salas, professores e materiais.
- Filtros por características e disponibilidade.
- Criação, edição e cancelamento das próprias reservas.
- Bloqueio de reservas com horários sobrepostos.
- Permissão para horários consecutivos.
- Aprovação e rejeição pelo responsável vinculado.
- Bloqueio de recursos durante manutenção.
- Retirada, devolução e registro de não comparecimento de materiais.
- Auditoria de reservas e notificações internas.
- Relatórios de contagens, horas previstas e conflitos evitados.

### Testes e verificações

- Suíte Python com 292 testes nas execuções registradas.
- Teste separado de concorrência por HTTP.
- Testes de concorrência entre manutenção e reserva.
- Teste Chromium com login, criação, conflito e cancelamento.
- Execução da suíte em container Linux com Testcontainers.
- Verificação de integridade, backup e restauração SQLite.
- Quatro testes automatizados do verificador de backup.
- Auditorias das dependências principais e do navegador.
- Duas execuções planejadas de carga sobre GET /login.

### Validação de 03/11/2026

- Clone separado no mesmo computador, com ambiente virtual novo.
- Instalação das dependências com arquivo de lock e hashes.
- 292 testes aprovados em 86,353 segundos.
- Login e consulta dos recursos verificados manualmente.
- Criação de reserva verificada.
- Tentativa de reserva no mesmo recurso e horário bloqueada.
- Cancelamento e consulta no histórico verificados.
- Registro em docs/entrega/validacao-2026-11-03.md.

Commit utilizado na validação:

b55f1ef87ea97bb5fee3bf076a57cf0555656e74

Essa execução foi realizada por Arthur.
Não representa revisão por outro integrante nem teste em outro computador.

### Integração contínua

- Workflows para testes Python, cobertura, Chromium e Testcontainers.
- Dependências principais e E2E instaladas com verificação de hashes.
- Metas de cobertura: 80% de linhas e 70% de ramificações.
- Publicação de relatórios JSON, XML e HTML.
- Publicação do log da execução Testcontainers.
- Análise Sonar com verificação do Quality Gate.

Após a integração do pull request #1, no commit f22d2c9:

- Testes automatizados #200: aprovado.
- Testes com Testcontainers #38: aprovado.

A comparação com b55f1ef mostrou somente a inclusão do documento
de validação, sem alterações no código.

### Correções relevantes

- Ajustes no controle de acesso e nas validações das reservas.
- Execução da imagem de testes com usuário sem privilégios de root.
- Cópia explícita dos arquivos necessários para a imagem de testes.
- Classificação dos testes separados na configuração do Sonar.
- Exigência de pacotes binários na instalação do Testcontainers.
- Correção da sintaxe YAML do comando de instalação.
- Correção dos integrantes nos documentos e rodapés das páginas.

### Documentação

- README com instalação, execução, rotas HTTP e limitações.
- Matriz de rastreabilidade.
- Arquitetura e diagramas.
- Plano de testes e relatório de qualidade.
- Registro de defeitos.
- Documentação de segurança.
- Relatório de carga com critérios definidos antes das execuções.
- Registro da validação em clone limpo.
- Caminhos docs/rtm.md, docs/relatorio-qualidade.md e docs/defeitos/.
- Checklist de entrega e índice de evidências.
- Rascunho da decisão de qualidade.

### Limitações conhecidas

- Gestão completa de usuários e edição/desativação de recursos pela interface
  ainda não implementadas.
- Teste de navegador limitado aos cenários presentes no teste E2E.
- Carga planejada limitada à consulta da página de login em ambiente local.
- Scripts administrativos e migrações sem cobertura integral.
- Testcontainers utiliza SQLite dentro do container, sem servidor de banco separado.
- Dependências do ambiente Testcontainers sem lock completo com hashes.
- Implantação de produção não validada.

### Pendências para publicar a candidata

- Concluir a revisão dos documentos e links.
- Registrar as contribuições reais dos integrantes.
- Registrar revisão por outro integrante.
- Finalizar a decisão de qualidade e os responsáveis pelos riscos.
- Integrar as alterações finais e conferir a CI do commit avaliado.
- Preservar os relatórios da execução final.
- Criar a tag anotada v1.0.0-rc1.
- Vincular as evidências finais ao commit da tag.

A publicação da candidata não representa liberação para produção.
