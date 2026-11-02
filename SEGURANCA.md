# Segurança — Organização de Recursos

**Atualização:** 02/11/2026

**Integrantes:** Arthur Mendes, Robert Oliveira, Nicolas Ferreira e Murilo Henrique.

## 1. Objetivo e escopo

Registrar os controles implementados, as verificações executadas e as limitações conhecidas.

As evidências incluem testes de autenticação, autorização, CSRF, escape de HTML, dependências Python e configuração do container de testes.

Este documento não representa um teste de invasão completo nem uma certificação de segurança.

## 2. Controles implementados

| Controle | Comportamento |
| --- | --- |
| Senhas | Armazenadas como hash |
| Autenticação | Login exige credenciais válidas de usuário ativo |
| Autorização | Operações verificam perfil, propriedade ou vínculo conforme o fluxo |
| CSRF | Requisições POST exigem token da sessão |
| Renovação de sessão | Login válido limpa a sessão anterior e gera novo token |
| Consultas SQL | Uso de SQLAlchemy e parâmetros nas operações verificadas |
| Saída HTML | Escape de conteúdo nos pontos testados |
| Integridade | Operações relacionadas compartilham transação |
| Auditoria | Transições implementadas registram autor e alteração |
| Container de testes | Execução como usuário sem privilégios de root |

A presença de um controle não comprova sua eficácia em todos os cenários possíveis.

## 3. Autenticação e sessão

### Verificações

- Login válido.
- Credenciais inválidas.
- Usuário inativo.
- Acesso a páginas protegidas sem autenticação.
- Logout.
- Token CSRF pertencente a outra sessão.
- Renovação do token após login.
- Recusa do token anterior no logout.
- Logout permitido com o token atual.
- Tentativas de injeção SQL no login.

### Evidências

- tests/test_consulta.py
- tests/test_seguranca_login.py
- e2e/test_fluxo_reserva.py

O teste de segurança do login utiliza três entradas de tentativa de injeção SQL e verifica ausência de autenticação indevida e preservação dos usuários.

Commit dos testes específicos: 003cc82.

O fluxo Chromium verifica login inválido e válido com servidor HTTP e banco temporário.

## 4. Autorização e isolamento

Os testes das operações verificam combinações de:

- Administrador, responsável e solicitante.
- Usuário ativo e inativo.
- Proprietário e usuário alheio.
- Responsável vinculado e não vinculado.
- Reserva existente e inexistente.
- Estado e prazo permitidos.

As verificações estão distribuídas pelos testes de consulta, reservas, cancelamento, aprovação, manutenção, edição, materiais, auditoria, notificações e relatórios.

A consulta de notificações é limitada ao destinatário. A marcação de leitura também verifica o vínculo do aviso com o usuário conectado.

Esses resultados não representam uma revisão completa de todas as rotas e combinações de permissões.

## 5. Proteção CSRF

Os formulários POST exigem token da sessão.

Os testes verificam, nos fluxos abrangidos:

- Token ausente.
- Token incorreto.
- Token de outra sessão.
- Renovação após autenticação.
- Recusa do token anterior após login.

O cliente Flask verifica as respostas e os efeitos persistidos. Ele não executa JavaScript.

## 6. Escape de HTML

Arquivo: tests/test_seguranca_xss.py.

O teste utiliza nome de recurso contendo uma tag script e verifica:

- Página inicial.
- Formulário de nova reserva.
- Respostas HTTP 200.
- Conteúdo escapado no HTML.
- Ausência da tag original sem escape nos pontos examinados.

Resultado local registrado: um teste aprovado em 0,382 segundo, com dois cenários.

Commit: 75c7622.

Essa verificação não cobre todos os campos, contextos de saída ou formas de XSS. Também não executa um conjunto completo de ataques no navegador.

## 7. Integridade e rastreabilidade

Os testes verificam persistência e ausência de alterações indevidas nas recusas abrangidas.

Também existem falhas simuladas para verificar rollback de operações relacionadas à auditoria e às notificações.

A concorrência de reservas foi verificada no serviço e em um cenário HTTP com duas sessões autenticadas.

A disputa entre manutenção e reserva foi verificada no serviço para SALA, PROFESSOR e MATERIAL.

Essas verificações apoiam a integridade dos registros, mas não substituem uma análise completa de segurança.

## 8. Auditoria de dependências Python

Ferramenta: pip-audit, executada em ambiente separado .venv-auditoria.

Foram utilizadas as opções --require-hashes e --strict.

| Lock verificado | Evidência | Resultado |
| --- | --- | --- |
| requirements.lock | auditoria_dependencias.json | Dez dependências; nenhuma vulnerabilidade conhecida reportada |
| requirements-e2e.lock | auditoria_dependencias_e2e.json | Nenhuma vulnerabilidade conhecida reportada |

A auditoria de E2E inclui Playwright 1.64.1 e as dependências Python presentes no relatório.

O JSON de E2E foi enviado no commit 98d26d5.

### Reprodução

Na raiz do projeto, com o ambiente de auditoria preparado:

```powershell
.\.venv-auditoria\Scripts\python.exe -m pip_audit -r requirements.lock --require-hashes --strict -f json -o auditoria_dependencias.json
```

```powershell
.\.venv-auditoria\Scripts\python.exe -m pip_audit -r requirements-e2e.lock --require-hashes --strict -f json -o auditoria_dependencias_e2e.json
```

### Limites

- Os resultados dependem das versões e da base consultada no momento da execução.
- Ausência de vulnerabilidades conhecidas reportadas não comprova ausência de vulnerabilidades.
- A auditoria dos pacotes Python não equivale à auditoria do binário Chromium.
- Não representa análise das dependências do sistema operacional da imagem Docker.
- O ambiente de auditoria está separado do ambiente principal e excluído do Git e do Sonar.

## 9. Container de testes

Arquivos: Dockerfile.testes e .dockerignore.

O ajuste registrado no commit 02737a6:

- Define usuário sem privilégios de root para executar os testes.
- Substitui COPY de todo o diretório por cópias dos arquivos e diretórios necessários.
- Instala dependências com hashes.
- Utiliza exclusões do contexto de construção para banco local, ambientes virtuais, backups e arquivos de ambiente.

Os comandos utilizados não montam o banco local dentro do container.

A suíte executada após o ajuste apresentou 287 testes aprovados em 180,651 segundos.

Essa imagem é destinada aos testes. Não representa uma configuração completa de implantação em produção.

A imagem-base utiliza tag e ainda não está fixada por digest.

## 10. Análise estática

Última análise conferida: commit 02737a6, no Pull Request nº 1.

| Indicador | Resultado |
| --- | --- |
| Quality Gate | Aprovado |
| Novos problemas | 0 |
| Problemas aceitos | 0 |
| Security Hotspots | 0 |
| Cobertura no código novo | 83,8% |
| Duplicação no código novo | 0,0% |

O commit anterior 73a556e havia apresentado reprovação do Quality Gate.

Após a correção do Dockerfile e a classificação do teste HTTP como arquivo de teste, a análise conferida foi aprovada.

Os resultados pertencem à versão indicada. A análise do commit final da entrega deve ser conferida.

Zero novos problemas e zero hotspots não comprovam ausência de vulnerabilidades.

## 11. Resultado da regressão

Na execução GitHub Actions #146, commit 67b3d00:

- 288 testes da suíte principal aprovados em 15,349 segundos.
- Teste separado de concorrência HTTP aprovado.
- Fluxo Chromium aprovado.
- Cobertura de linhas: 97,69%.
- Cobertura de ramificações: 95,74%.

A suíte inclui verificações funcionais, de integração e de segurança. Não representa 288 testes exclusivos de segurança.

## 12. Limitações e próximas verificações

- Revisão completa de segurança pelo grupo.
- Configuração de HTTPS e cookies para implantação.
- Avaliação de limitação de tentativas de login.
- Ampliação dos campos e páginas verificados contra XSS.
- Revisão de segredos e configuração antes de implantação.
- Auditoria específica do navegador e da imagem Docker.
- Verificação de restauração de backup.
- Conferência das proteções da branch principal.
- Análise Sonar da versão final.

Sem SECRET_KEY definida, a aplicação utiliza chave temporária ao iniciar. O reinício invalida as sessões anteriores.

O servidor local de desenvolvimento não representa uma implantação de produção.

## 13. Referências

- [Rastreabilidade](RTM.md)
- [Plano de testes](PLANO_TESTES.md)
- [Relatório de qualidade](RELATORIO_QUALIDADE.md)
- [Arquitetura](ARQUITETURA.md)
- [Defeitos](DEFEITOS.md)
- [Auditoria da aplicação](auditoria_dependencias.json)
- [Auditoria de E2E](auditoria_dependencias_e2e.json)
- [GitHub Actions](https://github.com/Arthurmrsilva/organizacao-recursos/actions)
- [Sonar do PR](https://sonarcloud.io/summary/overall?id=Arthurmrsilva_organizacao-recursos&pullRequest=1)