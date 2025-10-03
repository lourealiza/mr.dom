@echo off
REM Script rápido para executar trilha de testes MrDom SDR

echo 🚀 Trilha de Testes MrDom SDR - Execução Rápida
echo ================================================

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

REM Verificar se Redis está rodando
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Redis não está rodando. Tentando iniciar...
    start /B redis-server
    timeout /t 3 /nobreak >nul
    redis-cli ping >nul 2>&1
    if errorlevel 1 (
        echo ❌ Não foi possível conectar ao Redis.
        echo    Instale Redis ou execute: redis-server
        pause
        exit /b 1
    )
)

echo ✅ Redis conectado

REM Executar configuração do ambiente se necessário
if not exist "api\tests\test_data\test_config.json" (
    echo 📋 Configurando ambiente de teste...
    python scripts\setup-test-environment.py
    if errorlevel 1 (
        echo ❌ Erro na configuração do ambiente
        pause
        exit /b 1
    )
)

REM Executar testes
echo 🧪 Executando trilha de testes...
python scripts\run-trilha-tests.py

if errorlevel 1 (
    echo ❌ Alguns testes falharam. Verifique os logs.
) else (
    echo ✅ Todos os testes passaram!
)

echo.
echo 📁 Resultados salvos em: test_results\
echo 📖 Documentação: docs\trilha-testes.md
echo.
pause
