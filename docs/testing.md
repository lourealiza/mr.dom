# Ambiente de Testes - MrDom SDR

Este documento descreve como configurar e executar o ambiente de testes do sistema MrDom SDR.

## Visão Geral

O ambiente de testes foi projetado para fornecer uma infraestrutura completa e isolada para execução de testes automatizados, incluindo:

- **Testes Unitários**: Testes isolados de componentes individuais
- **Testes de Integração**: Testes que verificam a integração entre componentes
- **Testes End-to-End**: Testes do fluxo completo do sistema
- **Testes de Performance**: Testes de carga e tempo de resposta

## Estrutura do Ambiente

```
├── test.env                          # Configurações específicas para testes
├── pytest.ini                       # Configuração do pytest
├── compose/
│   ├── docker-compose.test.yml      # Docker Compose para testes
│   ├── Dockerfile.test             # Dockerfile para testes
│   ├── init-db.sql                 # Script de inicialização do PostgreSQL
│   └── init-test-db.sql            # Script de inicialização para testes
├── scripts/
│   ├── setup-test-env.sh           # Script de configuração (Linux/Mac)
│   ├── setup-test-env.bat          # Script de configuração (Windows)
│   ├── run-tests.sh                # Script de execução de testes (Linux/Mac)
│   ├── run-tests.bat               # Script de execução de testes (Windows)
│   ├── cleanup-test-env.sh         # Script de limpeza (Linux/Mac)
│   └── cleanup-test-env.bat        # Script de limpeza (Windows)
└── api/tests/
    ├── conftest.py                 # Configurações globais do pytest
    ├── factories.py                # Factories para dados de teste
    ├── test_bot_logic.py           # Testes unitários existentes
    ├── test_n8n_integration.py     # Testes de integração com N8N
    ├── test_chatwoot_integration.py # Testes de integração com Chatwoot
    └── test_end_to_end.py          # Testes end-to-end
```

## Configuração Inicial

### 1. Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Python 3.8+** instalado
- **Git** para clonagem do repositório

### 2. Configuração do Ambiente

#### Linux/Mac:
```bash
# Executar script de configuração
./scripts/setup-test-env.sh
```

#### Windows:
```cmd
# Executar script de configuração
scripts\setup-test-env.bat
```

### 3. Configuração de Variáveis

Edite o arquivo `test.env` com suas configurações:

```env
# Chatwoot
CHATWOOT_BASE_URL=https://seu-chatwoot.com
CHATWOOT_ACCESS_TOKEN=seu_token_aqui
CHATWOOT_ACCOUNT_ID=1

# N8N
N8N_BASE_URL=https://seu-n8n.com
N8N_API_KEY=seu_api_key_aqui

# OpenAI
OPENAI_API_KEY=sk-sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app
DB_USER=app
DB_PASSWORD=change-me
```

## Executando Testes

### Tipos de Teste Disponíveis

1. **Testes Unitários** (`unit`): Testes isolados de componentes
2. **Testes de Integração** (`integration`): Testes de integração com APIs externas
3. **Testes End-to-End** (`e2e`): Testes do fluxo completo
4. **Todos os Testes** (`all`): Executa todos os tipos de teste
5. **Testes com Cobertura** (`coverage`): Testes com relatório de cobertura
6. **Testes em Docker** (`docker`): Executa testes em containers Docker

### Executando Testes

#### Linux/Mac:
```bash
# Testes unitários (padrão)
./scripts/run-tests.sh

# Testes de integração
./scripts/run-tests.sh integration

# Todos os testes com cobertura
./scripts/run-tests.sh coverage --verbose

# Testes em Docker
./scripts/run-tests.sh docker
```

#### Windows:
```cmd
# Testes unitários (padrão)
scripts\run-tests.bat

# Testes de integração
scripts\run-tests.bat integration

# Todos os testes com cobertura
scripts\run-tests.bat coverage --verbose

# Testes em Docker
scripts\run-tests.bat docker
```

### Opções Disponíveis

- `--verbose`: Modo verboso com mais detalhes
- `--parallel`: Executar testes em paralelo
- `--no-cov`: Sem relatório de cobertura
- `--help`: Mostrar ajuda

## Executando Testes Específicos

### Usando pytest diretamente:

```bash
# Ativar ambiente virtual
source venv-test/bin/activate  # Linux/Mac
# ou
venv-test\Scripts\activate.bat  # Windows

# Executar testes específicos
pytest api/tests/test_bot_logic.py -v

# Executar testes com marcadores específicos
pytest -m unit -v
pytest -m integration -v
pytest -m e2e -v

# Executar testes com cobertura
pytest --cov=api --cov-report=html
```

## Marcadores de Teste

Os testes são organizados usando marcadores do pytest:

- `@pytest.mark.unit`: Testes unitários
- `@pytest.mark.integration`: Testes de integração
- `@pytest.mark.e2e`: Testes end-to-end
- `@pytest.mark.slow`: Testes que demoram para executar
- `@pytest.mark.external`: Testes que dependem de serviços externos
- `@pytest.mark.database`: Testes que usam banco de dados
- `@pytest.mark.redis`: Testes que usam Redis
- `@pytest.mark.chatwoot`: Testes que usam Chatwoot
- `@pytest.mark.n8n`: Testes que usam N8N
- `@pytest.mark.openai`: Testes que usam OpenAI
- `@pytest.mark.mock`: Testes que usam mocks
- `@pytest.mark.real_api`: Testes que usam APIs reais

## Estrutura dos Testes

### Testes Unitários (`test_bot_logic.py`)
- Testam componentes isolados
- Usam mocks para dependências externas
- Execução rápida
- Alta cobertura de código

### Testes de Integração (`test_*_integration.py`)
- Testam integração com APIs externas
- Podem usar APIs reais ou mocks
- Verificam contratos de API
- Testam tratamento de erros

### Testes End-to-End (`test_end_to_end.py`)
- Testam fluxos completos do sistema
- Simulam interações reais do usuário
- Verificam integração entre todos os componentes
- Mais lentos e complexos

## Relatórios e Resultados

### Localização dos Relatórios

- **Relatório HTML**: `htmlcov/index.html`
- **Relatório JUnit**: `test-results/junit.xml`
- **Relatório pytest HTML**: `test-results/report.html`
- **Log detalhado**: `test-results/pytest.log`
- **Cobertura XML**: `coverage.xml`

### Interpretando os Resultados

1. **Cobertura de Código**: Deve ser >= 80%
2. **Testes Falhando**: Verificar logs para detalhes
3. **Testes Lentos**: Identificados com marcador `@pytest.mark.slow`
4. **APIs Externas**: Testes podem ser pulados se APIs não estiverem disponíveis

## Limpeza do Ambiente

### Limpeza Completa

#### Linux/Mac:
```bash
./scripts/cleanup-test-env.sh --all --force
```

#### Windows:
```cmd
scripts\cleanup-test-env.bat --all --force
```

### Limpeza Parcial

```bash
# Apenas containers
./scripts/cleanup-test-env.sh --containers

# Apenas volumes
./scripts/cleanup-test-env.sh --volumes

# Apenas arquivos temporários
./scripts/cleanup-test-env.sh --files
```

## Solução de Problemas

### Problemas Comuns

1. **Docker não está rodando**
   ```bash
   # Verificar status do Docker
   docker info
   ```

2. **Portas em uso**
   ```bash
   # Verificar portas em uso
   netstat -tulpn | grep :8001  # Linux
   netstat -an | findstr :8001  # Windows
   ```

3. **Dependências não instaladas**
   ```bash
   # Reinstalar dependências
   pip install -r requirements.txt
   pip install pytest pytest-asyncio pytest-cov
   ```

4. **Variáveis de ambiente não configuradas**
   ```bash
   # Verificar arquivo test.env
   cat test.env
   ```

### Logs e Debug

- **Logs do Docker**: `docker-compose -f compose/docker-compose.test.yml logs`
- **Logs do pytest**: `test-results/pytest.log`
- **Logs da aplicação**: `logs/`

## Integração Contínua

### GitHub Actions

Exemplo de workflow para CI:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
      - name: Run tests
        run: |
          cp env.example test.env
          pytest --cov=api --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Contribuindo

### Adicionando Novos Testes

1. **Testes Unitários**: Adicione em arquivos `test_*.py` existentes
2. **Testes de Integração**: Crie arquivos `test_*_integration.py`
3. **Testes E2E**: Adicione em `test_end_to_end.py`

### Convenções

- Use fixtures do `conftest.py` quando possível
- Use factories do `factories.py` para dados de teste
- Marque testes com marcadores apropriados
- Mantenha testes independentes e determinísticos
- Documente testes complexos

### Exemplo de Teste

```python
@pytest.mark.unit
async def test_example_function():
    """Teste de exemplo com documentação"""
    # Arrange
    input_data = {"test": "data"}
    
    # Act
    result = await example_function(input_data)
    
    # Assert
    assert result is not None
    assert result["status"] == "success"
```

## Recursos Adicionais

- [Documentação do pytest](https://docs.pytest.org/)
- [Documentação do pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Documentação do pytest-cov](https://pytest-cov.readthedocs.io/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org/docs/)

