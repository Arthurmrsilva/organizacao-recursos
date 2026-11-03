# Segurança — Organização de Recursos

Atualização: 02/11/2026.

Integrantes: Arthur Mendes, Nicolas Ferreira e Robert Oliveira.

## 1. Objetivo e escopo

Registrar controles implementados, verificações executadas e limitações.

As evidências abrangem autenticação, autorização, CSRF, escape de HTML,
integridade transacional, dependências Python, container de testes
e verificação de backup e restauração SQLite.

Este documento não representa teste de invasão completo,
certificação de segurança ou aprovação para produção.

## 2. Controles implementados

| Controle | Comportamento |
| --- | --- |
| Senhas | Armazenadas como hash |
| Autenticação | Credenciais válidas de usuário ativo |
| Autorização | Perfil, propriedade e vínculo conforme a operação |
| CSRF | Requisições POST exigem token da sessão |
| Renovação de sessão | Login válido limpa a sessão e gera novo token |
| Consultas SQL | SQLAlchemy e parâmetros nas operações verificadas |
| Saída HTML | Escape nos pontos testados |
| Integridade | Operações relacionadas compartilham transação |
| Auditoria | Transições implementadas registram autor e alteração |
| Container | Testes executados com usuário sem privilégios de root |

A presença de controles não comprova eficácia em todos os cenários.

## 3. Autenticação, sessão e CSRF

Verificações nos cenários abrangidos:

- Login válido, credenciais inválidas e usuário inativo.
- Acesso protegido sem autenticação e encerramento de sessão.
- POST com token ausente ou incorreto.
- Token pertencente a outra sessão.
- Renovação do token após login.
- Recusa do token anterior no logout.
- Logout permitido com token atual.
- Tentativas de injeção SQL no login.

Evidências principais:

- tests/test_consulta.py
- tests/test_seguranca_login.py
- e2e/test_fluxo_reserva.py

O teste específico de SQL utiliza três entradas e verifica ausência
de autenticação indevida e preservação dos usuários.

O Chromium verifica login inválido e válido com servidor real
e banco temporário.

Sem SECRET_KEY definida, a aplicação gera chave temporária.
Reiniciar o servidor nesse modo invalida as sessões anteriores.

## 4. Autorização e isolamento

Os testes verificam combinações de:

- ADMIN, RESPONSAVEL e SOLICITANTE.
- Usuários ativos e inativos.
- Proprietário e usuário alheio.
- Responsável vinculado e não vinculado.
- Registros existentes e inexistentes.
- Estados e prazos permitidos.

As evidências estão nos testes de reservas, aprovação, cancelamento,
edição, manutenção, materiais, auditoria, notificações e relatórios.

Consulta e leitura de notificações verificam o destinatário.

Não representam revisão completa de todas as combinações de permissões.
O cliente Flask não executa JavaScript.

## 5. Escape de HTML

Arquivo: tests/test_seguranca_xss.py.

Verifica nome de recurso contendo tag script na página inicial
e no formulário de nova reserva, com saída escapada e ausência
da tag original sem escape nos pontos examinados.

Resultado local histórico: um método aprovado em 0,382 segundo,
com dois cenários; commit 75c7622.

A verificação integra a suíte atual, mas não cobre todos os campos,
contextos de saída ou formas de XSS.

## 6. Integridade e rastreabilidade

Há verificações de persistência, recusas sem alterações indevidas
e falhas simuladas para conferir rollback de operações relacionadas
à auditoria e às notificações.

A concorrência de reservas foi verificada no serviço e por HTTP,
com duas sessões autenticadas.

A disputa entre manutenção e reserva foi verificada no serviço
para SALA, PROFESSOR e MATERIAL.

Esses testes não eliminam todas as condições de corrida possíveis.

## 7. Auditoria de dependências

Ferramenta: pip-audit, em ambiente separado .venv-auditoria.

As execuções registradas utilizaram --require-hashes e --strict.

| Lock | Evidência | Resultado registrado |
| --- | --- | --- |
| requirements.lock | auditoria_dependencias.json | Dez dependências; nenhuma vulnerabilidade conhecida reportada |
| requirements-e2e.lock | auditoria_dependencias_e2e.json | Nenhuma vulnerabilidade conhecida reportada |

A auditoria E2E inclui Playwright 1.64.1 e as dependências Python
listadas no relatório, registrado em 98d26d5.

### Reprodução

Com o ambiente de auditoria previamente preparado:

    .\.venv-auditoria\Scripts\python.exe -m pip_audit -r requirements.lock --require-hashes --strict -f json -o auditoria_dependencias.json

    .\.venv-auditoria\Scripts\python.exe -m pip_audit -r requirements-e2e.lock --require-hashes --strict -f json -o auditoria_dependencias_e2e.json

### Limites

- Resultados dependem das versões e da base consultada na execução.
- Não abrangem automaticamente o binário Chromium ou a imagem Docker.
- Não abrangem as dependências externas do ambiente Testcontainers.
- Ausência de vulnerabilidades conhecidas reportadas não comprova segurança completa.

## 8. Docker e Testcontainers

Arquivos: Dockerfile.testes, .dockerignore e teste_testcontainers.py.

A imagem:

- Executa testes com usuário sem privilégios de root.
- Copia explicitamente os arquivos e diretórios necessários.
- Instala requirements.lock com verificação de hashes.
- Exclui banco local, ambientes virtuais, backups e arquivos de ambiente
  do contexto conforme .dockerignore.

Os comandos documentados não montam o banco local no container.

O Testcontainers controla o ciclo de vida da imagem de testes
e verifica término com sucesso e os 292 testes esperados.

A CI foi informada como aprovada após a correção YAML em 1e42442.
O print do commit 3a76227 confirma os sete checks verdes.

A instalação externa do Testcontainers exige pacotes binários
e fixa as versões diretas testcontainers==4.15.0 e docker==7.2.0.
Ainda não possui lock completo com hashes das dependências transitivas.

A imagem-base não está fixada por digest.
Essa imagem é destinada aos testes, não à implantação em produção.

## 9. Análise estática

Referência conferida: commit 3a76227, pull request nº 1.

| Indicador | Resultado |
| --- | --- |
| Quality Gate | Aprovado |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Security Hotspots | 0 |
| Cobertura no código novo | 84,1% |
| Duplicação no código novo | 0,0% |

Correções anteriores:

- 02737a6: usuário do container, cópias explícitas e classificação do teste HTTP.
- 047995b: exigência de pacotes binários na instalação Testcontainers.
- 1e42442: correção YAML do comando de instalação.

A aprovação no pull request não representa análise da main após merge.
Zero problemas ou hotspots não comprova ausência de vulnerabilidades.

## 10. Regressão

Referência detalhada: da93d49.

- Suíte local: 292 testes aprovados em 116,207 segundos.
- CI principal aprovada na execução #160.
- Concorrência HTTP e Chromium aprovados.
- Cobertura de linhas: 97,46%.
- Cobertura de ramificações: 94,83%.

O commit documental 3a76227 também apresentou sete checks verdes.

Os 292 testes incluem cenários funcionais e de integração.
Não são 292 testes exclusivos de segurança.

A cobertura sobre código novo do Sonar é uma métrica distinta.

## 11. Backup e restauração

O script validar_backup.py verifica integridade, cria backup temporário,
restaura para outro arquivo e compara estrutura e dados.

A execução registrada utilizou o banco do clone de validação,
com sete tabelas da aplicação e origem aberta somente para leitura.

tests/test_validar_backup.py contém quatro testes:

- Preservação de estrutura e dados, sem alterar a origem.
- Arquivo inexistente recusado sem criação.
- Diretório recusado.
- Arquivo inválido recusado sem alteração.

Não representa backup persistente, recuperação completa após desastre
ou teste de indisponibilidade da aplicação.

## 12. Limitações e fechamento

- Revisão completa de segurança pelo grupo.
- Configuração de HTTPS, segredos e cookies para implantação.
- Avaliação de limitação de tentativas de login.
- Ampliação dos campos e páginas verificados contra XSS.
- Auditoria específica de Chromium, imagem Docker e ambiente Testcontainers.
- Conferência das proteções da main.
- Validação do commit final e das evidências da release.
- Revisão real por outro integrante.

O servidor Flask local é de desenvolvimento.
As evidências não declaram prontidão para produção.

## 13. Referências

- [Índice de evidências](docs/evidencias/README.md)
- [Checklist](docs/entrega/checklist.md)
- [Rastreabilidade](RTM.md)
- [Plano de testes](PLANO_TESTES.md)
- [Relatório de qualidade](RELATORIO_QUALIDADE.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Auditoria principal](auditoria_dependencias.json)
- [Auditoria E2E](auditoria_dependencias_e2e.json)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Sonar do PR](https://sonarcloud.io/dashboard?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)