@echo off
REM Script para instalar Redis no Windows

setlocal enabledelayedexpansion

echo ==========================================
echo   Instalacao Redis - Windows
echo ==========================================
echo.

echo [INFO] Baixando Redis para Windows...
echo.

REM Criar diretorio para Redis
if not exist "redis" mkdir redis
cd redis

REM URL do Redis para Windows (versao mais recente)
set REDIS_URL=https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip
set REDIS_FILE=Redis-x64-3.0.504.zip

echo [INFO] Baixando Redis...
echo URL: %REDIS_URL%

REM Tentar baixar com PowerShell
powershell -Command "& {Invoke-WebRequest -Uri '%REDIS_URL%' -OutFile '%REDIS_FILE%'}"

if exist "%REDIS_FILE%" (
    echo [SUCCESS] Redis baixado com sucesso!
    echo.
    echo [INFO] Extraindo arquivos...
    
    REM Extrair arquivo ZIP
    powershell -Command "& {Expand-Archive -Path '%REDIS_FILE%' -DestinationPath '.' -Force}"
    
    echo [SUCCESS] Redis extraido!
    echo.
    echo ==========================================
    echo   Redis Instalado
    echo ==========================================
    echo.
    echo Redis foi instalado em: %CD%
    echo.
    echo Para iniciar Redis:
    echo 1. Execute: redis-server.exe
    echo 2. Ou execute: start-redis.bat
    echo.
    echo Para testar:
    echo redis-cli ping
    echo.
    
    REM Criar script para iniciar Redis
    echo @echo off > start-redis.bat
    echo echo Iniciando Redis... >> start-redis.bat
    echo redis-server.exe >> start-redis.bat
    
    echo [INFO] Script start-redis.bat criado!
    
) else (
    echo [ERROR] Falha ao baixar Redis.
    echo.
    echo ==========================================
    echo   Instalacao Manual
    echo ==========================================
    echo.
    echo Para instalar Redis manualmente:
    echo.
    echo 1. Acesse: https://github.com/microsoftarchive/redis/releases
    echo 2. Baixe a versao mais recente para Windows
    echo 3. Extraia o arquivo ZIP
    echo 4. Execute redis-server.exe
    echo.
    echo Ou use uma das alternativas:
    echo - Redis Cloud: https://redis.com/try-free/
    echo - Upstash Redis: https://upstash.com/
    echo.
)

cd ..

echo.
echo ==========================================
echo   Configuracao Atual
echo ==========================================
echo.
echo O projeto ja esta configurado para Redis:
echo.
echo REDIS_URL=redis://localhost:6379/0
echo REDIS_HOST=localhost
echo REDIS_PORT=6379
echo REDIS_DB=0
echo.
echo Para N8N:
echo Host: localhost
echo Port: 6379
echo Database: 0
echo Password: (deixe vazio)
echo.

pause
