# Changelog

## Em preparação — v1.0.0-rc1

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