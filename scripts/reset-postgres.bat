@echo off
REM Script para resetar o PostgreSQL com novas configurações (Windows)
REM Este script remove o volume do PostgreSQL e recria com as novas configurações

setlocal enabledelayedexpansion

echo ==========================================
echo   Reset do PostgreSQL - MrDom SDR
echo ==========================================
echo.

REM Confirmar ação
set /p response="Tem certeza que deseja resetar o PostgreSQL? Isso ira apagar todos os dados. (y/N): "
if /i not "%response%"=="y" (
    if /i not "%response%"=="yes" (
        echo Operacao cancelada.
        exit /b 0
    )
)

echo Continuando com o reset...

REM Parar containers
echo [INFO] Parando containers...
docker-compose -f compose\docker-compose.yml down >nul 2>&1
docker-compose -f compose\docker-compose.test.yml down >nul 2>&1

REM Remover volume do PostgreSQL
echo [INFO] Removendo volume do PostgreSQL...
docker volume rm mrdom-postgres_data >nul 2>&1

REM Remover container do PostgreSQL se existir
echo [INFO] Removendo container do PostgreSQL...
docker rm mrdom-postgres >nul 2>&1

REM Recriar e iniciar PostgreSQL
echo [INFO] Recriando PostgreSQL com novas configuracoes...
docker-compose -f compose\docker-compose.yml up -d postgres

REM Aguardar PostgreSQL inicializar
echo [INFO] Aguardando PostgreSQL inicializar...
timeout /t 10 /nobreak >nul

REM Verificar se PostgreSQL está rodando
echo [INFO] Verificando status do PostgreSQL...
docker ps | findstr mrdom-postgres >nul
if errorlevel 1 (
    echo [ERROR] PostgreSQL nao esta rodando!
    exit /b 1
) else (
    echo [SUCCESS] PostgreSQL esta rodando!
)

REM Testar conexão
echo [INFO] Testando conexao com PostgreSQL...
docker exec mrdom-postgres psql -U app -d app -c "SELECT version();" >nul 2>&1

if errorlevel 1 (
    echo [ERROR] Falha na conexao com PostgreSQL!
    exit /b 1
) else (
    echo [SUCCESS] Conexao com PostgreSQL bem-sucedida!
)

echo.
echo ==========================================
echo [SUCCESS] PostgreSQL resetado com sucesso!
echo ==========================================
echo.
echo Nova configuracao:
echo   Host: postgres (ou localhost)
echo   Porta: 5432
echo   Database: app
echo   Usuario: app
echo   Senha: mrdom2024
echo.
echo Para conectar no N8N ou outras ferramentas:
echo   Host: localhost
echo   Porta: 5432
echo   Database: app
echo   Usuario: app
echo   Senha: mrdom2024
echo.

pause
