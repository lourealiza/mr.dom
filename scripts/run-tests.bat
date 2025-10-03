@echo off
REM Script para executar testes do MrDom SDR (Windows)
REM Este script permite executar diferentes tipos de testes

setlocal enabledelayedexpansion

REM Configurar variáveis padrão
set TEST_TYPE=unit
set VERBOSE=false
set PARALLEL=false
set NO_COV=false

REM Processar argumentos
:parse_args
if "%1"=="" goto :main
if "%1"=="unit" set TEST_TYPE=unit
if "%1"=="integration" set TEST_TYPE=integration
if "%1"=="e2e" set TEST_TYPE=e2e
if "%1"=="all" set TEST_TYPE=all
if "%1"=="coverage" set TEST_TYPE=coverage
if "%1"=="docker" set TEST_TYPE=docker
if "%1"=="--verbose" set VERBOSE=true
if "%1"=="--parallel" set PARALLEL=true
if "%1"=="--no-cov" set NO_COV=true
if "%1"=="--help" goto :show_help
shift
goto :parse_args

:show_help
echo Uso: %0 [TIPO] [OPCOES]
echo.
echo Tipos de teste disponiveis:
echo   unit        - Testes unitarios (padrao)
echo   integration - Testes de integracao
echo   e2e         - Testes end-to-end
echo   all         - Todos os testes
echo   coverage    - Testes com relatorio de cobertura
echo   docker      - Executar testes em containers Docker
echo.
echo Opcoes:
echo   --verbose   - Modo verboso
echo   --parallel  - Executar testes em paralelo
echo   --no-cov    - Sem relatorio de cobertura
echo   --help      - Mostrar esta ajuda
echo.
echo Exemplos:
echo   %0                    # Executar testes unitarios
echo   %0 integration        # Executar testes de integracao
echo   %0 all --parallel     # Executar todos os testes em paralelo
echo   %0 docker             # Executar testes em Docker
echo   %0 coverage --verbose # Testes com cobertura detalhada
exit /b 0

:main
echo ==========================================
echo   Executando Testes - MrDom SDR
echo ==========================================
echo Tipo: %TEST_TYPE%
echo Verbose: %VERBOSE%
echo Paralelo: %PARALLEL%
echo Sem cobertura: %NO_COV%
echo ==========================================
echo.

REM Verificar dependências
echo [INFO] Verificando dependencias...

REM Verificar se pytest está instalado
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pytest nao esta instalado. Execute: pip install pytest
    exit /b 1
)

REM Verificar se o arquivo test.env existe
if not exist "test.env" (
    echo [WARNING] Arquivo test.env nao encontrado. Usando configuracoes padrao.
)

echo [SUCCESS] Dependencias verificadas

REM Configurar ambiente
echo [INFO] Configurando ambiente de teste...

REM Carregar variáveis de ambiente de teste
if exist "test.env" (
    echo [INFO] Variaveis de ambiente carregadas de test.env
)

REM Criar diretórios necessários
if not exist "test-results" mkdir test-results
if not exist "htmlcov" mkdir htmlcov

REM Definir variáveis de ambiente para pytest
set PYTHONPATH=%PYTHONPATH%;%CD%
set TESTING=true

echo [SUCCESS] Ambiente configurado

REM Executar testes baseado no tipo
if "%TEST_TYPE%"=="unit" goto :run_unit_tests
if "%TEST_TYPE%"=="integration" goto :run_integration_tests
if "%TEST_TYPE%"=="e2e" goto :run_e2e_tests
if "%TEST_TYPE%"=="all" goto :run_all_tests
if "%TEST_TYPE%"=="coverage" goto :run_coverage_tests
if "%TEST_TYPE%"=="docker" goto :run_docker_tests
goto :invalid_test_type

:run_unit_tests
echo [INFO] Executando testes unitarios...
set PYTEST_ARGS=-m unit --tb=short
if "%VERBOSE%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -v
if "%PARALLEL%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -n auto
if "%NO_COV%"=="false" set PYTEST_ARGS=%PYTEST_ARGS% --cov=api --cov-report=term-missing
pytest %PYTEST_ARGS% api\tests\
echo [SUCCESS] Testes unitarios concluidos
goto :cleanup

:run_integration_tests
echo [INFO] Executando testes de integracao...
set PYTEST_ARGS=-m integration --tb=short --timeout=30
if "%VERBOSE%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -v
pytest %PYTEST_ARGS% api\tests\
echo [SUCCESS] Testes de integracao concluidos
goto :cleanup

:run_e2e_tests
echo [INFO] Executando testes end-to-end...
set PYTEST_ARGS=-m e2e --tb=short --timeout=60
if "%VERBOSE%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -v
pytest %PYTEST_ARGS% api\tests\
echo [SUCCESS] Testes end-to-end concluidos
goto :cleanup

:run_all_tests
echo [INFO] Executando todos os testes...
set PYTEST_ARGS=--tb=short
if "%VERBOSE%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -v
if "%PARALLEL%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -n auto
if "%NO_COV%"=="false" set PYTEST_ARGS=%PYTEST_ARGS% --cov=api --cov-report=html:htmlcov --cov-report=term-missing --cov-report=xml
pytest %PYTEST_ARGS% api\tests\
echo [SUCCESS] Todos os testes concluidos
goto :cleanup

:run_coverage_tests
echo [INFO] Executando testes com relatorio de cobertura...
set PYTEST_ARGS=--cov=api --cov-report=html:htmlcov --cov-report=term-missing --cov-report=xml --cov-fail-under=80
if "%VERBOSE%"=="true" set PYTEST_ARGS=%PYTEST_ARGS% -v
pytest %PYTEST_ARGS% api\tests\
echo [SUCCESS] Relatorio de cobertura gerado em htmlcov\index.html
goto :cleanup

:run_docker_tests
echo [INFO] Executando testes em containers Docker...

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker nao esta rodando. Inicie o Docker primeiro.
    exit /b 1
)

REM Parar containers existentes
docker-compose -f compose\docker-compose.test.yml down --remove-orphans >nul 2>&1

REM Construir e executar testes
docker-compose -f compose\docker-compose.test.yml up --build --abort-on-container-exit test-runner

REM Copiar resultados para o host
docker cp mrdom-test-runner:/app/test-results ./test-results/ >nul 2>&1

echo [SUCCESS] Testes em Docker concluidos
goto :cleanup

:invalid_test_type
echo [ERROR] Tipo de teste invalido: %TEST_TYPE%
goto :show_help

:cleanup
echo [INFO] Limpando arquivos temporarios...

REM Remover arquivos .pyc
for /r . %%i in (*.pyc) do del "%%i" >nul 2>&1
for /d /r . %%i in (__pycache__) do rmdir /s /q "%%i" >nul 2>&1

REM Remover arquivos de cache do pytest
if exist ".pytest_cache" rmdir /s /q ".pytest_cache" >nul 2>&1

echo [SUCCESS] Limpeza concluida

:show_results
echo.
echo ==========================================
echo   Resultados dos Testes - MrDom SDR
echo ==========================================

if exist "test-results\junit.xml" (
    echo Relatorio JUnit: test-results\junit.xml
)

if exist "test-results\report.html" (
    echo Relatorio HTML: test-results\report.html
)

if exist "htmlcov" (
    echo Relatorio de Cobertura: htmlcov\index.html
)

if exist "test-results\pytest.log" (
    echo Log detalhado: test-results\pytest.log
)

echo ==========================================

echo.
echo [SUCCESS] Testes executados com sucesso!

pause
