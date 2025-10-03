@echo off
echo ========================================
echo Criando tabela n8n_chat_histories
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

REM Verificar se psycopg2 está instalado
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando psycopg2...
    pip install psycopg2-binary
    if errorlevel 1 (
        echo ❌ Erro ao instalar psycopg2!
        pause
        exit /b 1
    )
)

echo 🚀 Executando script de criação da tabela...
echo.

REM Executar o script Python
python scripts/create-n8n-table.py

echo.
echo ========================================
echo Processo concluído!
echo ========================================
pause
