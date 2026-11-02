# Changelog

## Em preparacao — release candidata 1.0.0

A tag v1.0.0-rc1 ainda nao foi criada.
Esta secao descreve o conteudo preparado para avaliacao do grupo.
Nao representa aprovacao da entrega ou liberacao para producao.

### Funcionalidades

- Autenticacao com senha armazenada como hash e encerramento de sessao.
- Perfis ADMIN, RESPONSAVEL e SOLICITANTE.
- Protecao CSRF nos formularios POST.
- Cadastro e consulta de salas, professores e materiais.
- Filtros por caracteristicas e disponibilidade.
- Criacao, edicao e cancelamento das proprias reservas.
- Verificacao de sobreposicao, permitindo horarios consecutivos.
- Aprovacao e rejeicao de solicitacoes pelo responsavel vinculado.
- Bloqueio de recursos durante manutencao.
- Controle de retirada, devolucao e nao comparecimento de materiais.
- Auditoria de reservas e notificacoes internas.
- Relatorios de contagens, horas previstas e conflitos evitados.

### Testes e verificacoes

- Suite Python com 292 testes nas execucoes registradas.
- Teste separado de concorrencia por HTTP com duas sessoes autenticadas.
- Teste de concorrencia entre manutencao e reserva para os tres tipos de recurso.
- Teste de navegador Chromium com login, criacao, conflito e cancelamento.
- Execucao da suite em container Linux controlado pelo Testcontainers.
- Verificacao de integridade, backup e restauracao SQLite.
- Quatro testes automatizados do verificador de backup.
- Auditorias versionadas das dependencias principais e do navegador.
- Validacao de instalacao em clone separado no commit c84dac2.
- Duas execucoes planejadas de carga sobre GET /login, com resultados JTL.

### Integracao continua

- Workflows para testes Python, cobertura, Chromium e Testcontainers.
- Instalacao das dependencias principais e E2E com verificacao de hashes.
- Metas de cobertura de 80% de linhas e 70% de ramificacoes.
- Publicacao dos relatorios JSON, XML e HTML e do log Testcontainers.
- Analise Sonar e verificacao do Quality Gate nos eventos configurados.

### Correcoes relevantes

- Ajustes no controle de acesso e nas validacoes das reservas.
- Execucao da imagem de testes com usuario sem privilegios de root.
- Copia explicita dos arquivos necessarios para a imagem de testes.
- Classificacao dos testes separados na configuracao do Sonar.
- Exigencia de pacotes binarios na instalacao do Testcontainers.
- Correcao da sintaxe YAML do comando de instalacao.

### Documentacao

- README com instalacao, execucao, testes e limitacoes.
- Matriz de rastreabilidade, arquitetura e diagramas.
- Plano de testes, relatorio de qualidade e registro de defeitos.
- Documentacao de seguranca e validacao de instalacao.
- Relatorio de carga com criterios definidos antes das execucoes.
- Checklist de fechamento e indice de evidencias.

### Limitacoes conhecidas

- Gestao completa de usuarios e edicao/desativacao de recursos pela interface.
- Cobertura de navegador limitada aos fluxos implementados no teste E2E.
- Carga planejada limitada a consulta da pagina de login em ambiente local.
- Scripts administrativos e migracoes sem cobertura integral.
- Testcontainers utiliza SQLite dentro do container; nao ha servidor de banco separado.
- Dependencias externas do Testcontainers sem lock completo com hashes.
- Implantacao de producao nao validada.

### Pendencias para publicar a candidata

- Consolidar os documentos e conferir seus links.
- Confirmar as equivalencias de ferramentas exigidas pela disciplina.
- Registrar revisao real por outro integrante.
- Confirmar nomes completos e contribuicoes dos integrantes.
- Conferir o conteudo antes de tornar o repositorio publico.
- Integrar a alteracao revisada e verificar a CI na main.
- Validar a versao candidata em clone limpo.
- Registrar a decisao de qualidade e os riscos assumidos.
- Criar a tag anotada no commit avaliado.
- Vincular as evidencias finais ao commit da candidata.