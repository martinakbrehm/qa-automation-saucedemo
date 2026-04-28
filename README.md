# Automation Testing — SauceDemo E2E

Framework de testes end-to-end para o e-commerce [SauceDemo](https://www.saucedemo.com), construído com **Python**, **Selenium WebDriver** e **pytest**, aplicando conceitos de **Engenharia de Dados** — data-driven testing, logging estruturado em JSON, análise de resultados com pandas e orquestração de pipeline com Prefect.

---

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Casos de Teste](#casos-de-teste)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Executando os Testes](#executando-os-testes)
- [Orquestração com Prefect](#orquestração-com-prefect)
- [Análise de Resultados](#análise-de-resultados)
- [CI/CD com GitHub Actions](#cicd-com-github-actions)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Boas Práticas Adotadas](#boas-práticas-adotadas)

---

## Sobre o Projeto

Este projeto implementa uma suíte de testes automatizados para validar os fluxos críticos de um e-commerce, cobrindo autenticação, carrinho e checkout. Além das práticas de QA Automation com **Page Object Model**, o projeto integra conceitos de **Engenharia de Dados**:

- **Data-driven testing:** cenários alimentados por arquivos JSON externos (`data/`), separando dados de lógica exatamente como um pipeline de ingestão
- **Logging estruturado JSON:** todos os eventos de teste são logados em formato JSON compatível com Elasticsearch, Datadog e similares
- **Análise de resultados com pandas:** script que transforma o relatório JSON em métricas de qualidade (taxa de sucesso, duração média, top falhas) e exporta CSV
- **Pipeline Prefect:** orquestra a suíte como um DAG com retries, quality gate e consolidação de relatórios
- **CI/CD GitHub Actions:** execução automática em push, PR e agendamento diário

---

## Tecnologias

| Tecnologia    | Versão | Função                                 |
| ------------- | ------ | -------------------------------------- |
| Python        | 3.10+  | Linguagem base                         |
| Selenium      | 4.10.0 | Automação do navegador                 |
| pytest        | 7.4.0  | Framework de testes                    |
| pytest-json-report | 1.5.0 | Export de resultados em JSON        |
| python-dotenv | 1.0.0  | Gerenciamento de variáveis de ambiente |
| pandas        | 2.1.0  | Análise de resultados e export CSV     |
| Prefect       | 2.14.0 | Orquestração do pipeline de testes     |
| GitHub Actions | —     | CI/CD e execução agendada             |
| ChromeDriver  | —      | Driver para Google Chrome              |

---

## Arquitetura

O projeto segue o padrão **Page Object Model (POM)**, que separa a lógica de interação com a UI da lógica dos testes, promovendo reutilização e manutenibilidade.

```
┌─────────────────────────────────────────┐
│              Tests (pytest)             │  ← Orquestram o fluxo e fazem asserções
└───────────────┬─────────────────────────┘
                │ usa
┌───────────────▼─────────────────────────┐
│            Page Objects                 │  ← Encapsulam elementos e ações de cada tela
│  LoginPage / HomePage / CarrinhoPage    │
└───────────────┬─────────────────────────┘
                │ herda
┌───────────────▼─────────────────────────┐
│              BasePage                   │  ← Ações genéricas e waits reutilizáveis
└───────────────┬─────────────────────────┘
                │ usa
┌───────────────▼─────────────────────────┐
│          Selenium WebDriver             │  ← Controla o navegador
└─────────────────────────────────────────┘
```

O `driver` é criado como um **pytest fixture** em `conftest.py` e injetado nas classes de página via construtor — eliminando variáveis globais e tornando os testes isolados e paralelos.

---

## Casos de Teste

| ID      | Categoria | Descrição                                                          | Status |
| ------- | --------- | ------------------------------------------------------------------ | ------ |
| CT01    | Carrinho  | Adicionar dois produtos ao carrinho e validar persistência e badge | ✅      |
| CT02    | Login     | Login válido deve redirecionar para a tela de inventário           | ✅      |
| CT03a   | Login     | Login com credenciais incorretas exibe mensagem de erro            | ✅      |
| CT03b   | Login     | Usuário bloqueado exibe mensagem específica                        | ✅      |
| CT03c   | Login     | Campos vazios exibem erro de username obrigatório                  | ✅      |
| CT03d   | Login     | Senha vazia exibe erro de password obrigatório                     | ✅      |
| CT04    | Carrinho  | Remover o único produto do carrinho valida que ele some            | ✅      |
| CT05    | Carrinho  | Remover um de dois produtos mantém o outro no carrinho             | ✅      |
| CT06    | Checkout  | Fluxo completo de checkout exibe confirmação do pedido             | ✅      |
| CT07    | Checkout  | Avançar no checkout sem formulário exibe erro de primeiro nome     | ✅      |
| CT08    | Checkout  | Avançar no checkout sem sobrenome exibe erro correspondente        | ✅      |

---

## Pré-requisitos

- Python 3.10 ou superior
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome (ou gerenciado automaticamente pelo Selenium Manager >= 4.6)

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/martinakbrehm/qa-automation-saucedemo.git
cd qa-automation-saucedemo

# 2. Crie e ative um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## Configuração

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS
```

| Variável        | Padrão                      | Descrição                                   |
| --------------- | --------------------------- | ------------------------------------------- |
| `BASE_URL`      | `https://www.saucedemo.com` | URL da aplicação sob teste                  |
| `HEADLESS`      | `false`                     | Executa o Chrome sem interface gráfica      |
| `IMPLICIT_WAIT` | `5`                         | Tempo máximo de espera implícita (segundos) |

> **Segurança:** o arquivo `.env` está no `.gitignore` e **nunca** deve ser versionado.
> Use `.env.example` como referência das variáveis necessárias para novos ambientes.

---

## Executando os Testes

```bash
# Executar toda a suíte
pytest

# Executar apenas testes de login
pytest -m login

# Executar apenas testes de checkout
pytest -m checkout

# Executar apenas testes de carrinho
pytest -m carrinho

# Executar um arquivo específico
pytest tests/test_login_valido.py

# Executar em modo headless
$env:HEADLESS="true"; pytest   # Windows PowerShell
HEADLESS=true pytest           # Linux/macOS

# Gerar relatório JSON (necessário para análise e pipeline)
pytest --json-report --json-report-file=reports/results.json

# Gerar relatório HTML (requer pytest-html)
pytest --html=reports/report.html --self-contained-html
```

---

## Estrutura de Diretórios

```
.
├── .github/
│   └── workflows/
│       └── tests.yml             # Pipeline CI/CD GitHub Actions
├── data/
│   ├── usuarios.json         # Dataset de usuários válidos
│   ├── produtos.json         # Catalogo de produtos para testes
│   └── cenarios_login_invalido.json  # Cenários de falha de login
├── logs/                         # Logs JSON gerados em cada execução
├── pages/
│   ├── base_page.py          # Ações genéricas (clicar, escrever, esperar, etc.)
│   ├── login_page.py         # Interações com a tela de login
│   ├── home_page.py          # Interações com a tela de inventário
│   ├── carrinho_page.py      # Interações com a tela do carrinho
│   └── checkout_page.py      # Interações com o fluxo de checkout
├── pipeline/
│   └── quality_pipeline.py   # Orquestração Prefect (DAG, retries, quality gate)
├── reports/                      # Relatórios JSON/CSV gerados após cada execução
├── scripts/
│   └── analyze_results.py    # Análise de métricas de qualidade com pandas
├── tests/
│   ├── test_login_valido.py
│   ├── test_login_invalido.py
│   ├── test_adicionar_produtos_carrinho.py
│   ├── test_remover_produto_carrinho.py
│   └── test_checkout.py
├── conftest.py               # Fixture do WebDriver + logging JSON
├── pytest.ini                # Configuração do pytest e marcadores
├── requirements.txt          # Dependências do projeto
├── .env.example              # Modelo de variáveis de ambiente
├── .gitignore
└── README.md
```

---

## Orquestração com Prefect

O arquivo [pipeline/quality_pipeline.py](pipeline/quality_pipeline.py) orquestra a suíte como um pipeline de dados:

```
[login suite] ─┐
                ├─▶ [consolidar relatórios] ─▶ [analisar com pandas] ─▶ [quality gate]
[carrinho]  ──┤
[checkout]  ──┘
```

```bash
# 1. Iniciar o servidor Prefect (em outro terminal)
prefect server start

# 2. Executar o pipeline
python pipeline/quality_pipeline.py
```

O **quality gate** falha o pipeline inteiro se qualquer suite tiver testes reprovados — o mesmo comportamento de um pipeline de dados que rejeita dados inválidos.

---

## Análise de Resultados

Após gerar o relatório JSON, o script pandas produz métricas de qualidade:

```bash
# 1. Gerar relatório
pytest --json-report --json-report-file=reports/results.json

# 2. Analisar
python scripts/analyze_results.py
```

Saída do script:
```
============================== QUALITY GATE REPORT ==============================
[Resumo por resultado]
 outcome  total
  passed     11

[Duração média por módulo de teste]
                                    testes  media_s  total_s
test_adicionar_produtos_carrinho.py       1    3.251    3.251
test_checkout.py                          3    4.102   12.306
test_login_invalido.py                    4    1.034    4.136
test_login_valido.py                      2    1.521    3.042
test_remover_produto_carrinho.py          2    2.871    5.742

[✓ Todos os testes passaram]
[Taxa de sucesso: 100.0% (11/11)]
```

Também exporta `reports/results_summary.csv` para auditoria ou ingestão em outras ferramentas.

---

## CI/CD com GitHub Actions

O workflow [.github/workflows/tests.yml](.github/workflows/tests.yml) executa automaticamente:

| Gatilho | Quando ocorre |
|---|---|
| `push` | Em qualquer push para `main` ou `develop` |
| `pull_request` | Em PRs para `main` |
| `schedule` | De segunda a sexta às 08:00 UTC |
| `workflow_dispatch` | Execução manual pela interface do GitHub |

Artefatos gerados: relatórios JSON/CSV e logs, retidos por 30 dias.

---

## Boas Práticas Adotadas

- **Page Object Model (POM):** separação total entre lógica de UI e lógica de teste.
- **Data-driven testing:** cenários são definidos em `data/*.json` — adicionar um novo caso é só adicionar uma linha no JSON, sem tocar no código de teste.
- **Injeção de dependência via fixture:** o `driver` é injetado pelo pytest — sem variáveis globais, cada teste é 100% isolado.
- **Logging estruturado JSON:** compatível com qualquer stack de observabilidade (ELK, Datadog, Cloud Logging).
- **Análise com pandas:** resultados tratados como dataset, com agregações, métricas e export CSV.
- **Orquestração Prefect:** pipeline com retries por task, quality gate e consolidação de relatórios.
- **CI/CD com GitHub Actions:** execução automática, agendada e com upload de artefatos.
- **Type hints e docstrings:** código autodocumentado e suporte completo a IDEs.
- **Variáveis de ambiente:** dados de configuração externalizados via `.env`, nunca hardcoded.
- **Sem código comentado:** histórico de mudanças gerenciado pelo Git.
- **Marcadores pytest:** execução seletiva por domínio (`login`, `carrinho`, `checkout`) em pipelines CI/CD.
- **Teardown garantido:** o fixture usa `yield`, garantindo que `driver.quit()` seja sempre chamado.
