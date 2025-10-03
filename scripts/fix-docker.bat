@echo off
REM Script para tentar corrigir problemas do Docker Desktop

setlocal enabledelayedexpansion

echo ==========================================
echo   Correcao do Docker Desktop
echo ==========================================
echo.

echo [INFO] Verificando status do Docker...

REM Verificar se Docker Desktop esta rodando
tasklist | findstr "Docker Desktop.exe" >nul
if errorlevel 1 (
    echo [INFO] Docker Desktop nao esta rodando. Tentando iniciar...
    goto :start_docker
) else (
    echo [INFO] Docker Desktop esta rodando. Tentando reiniciar...
    goto :restart_docker
)

:start_docker
echo.
echo [INFO] Tentando iniciar Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo [INFO] Aguardando Docker Desktop inicializar...
timeout /t 30 /nobreak >nul
goto :test_docker

:restart_docker
echo.
echo [INFO] Tentando reiniciar Docker Desktop...

REM Fechar Docker Desktop
taskkill /f /im "Docker Desktop.exe" >nul 2>&1
echo [INFO] Docker Desktop fechado. Aguardando...
timeout /t 10 /nobreak >nul

REM Iniciar Docker Desktop
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo [INFO] Docker Desktop iniciado. Aguardando inicializacao...
timeout /t 45 /nobreak >nul

:test_docker
echo.
echo [INFO] Testando Docker...

REM Testar Docker
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker ainda nao esta funcionando.
    echo.
    echo ==========================================
    echo   Solucoes Alternativas
    echo ==========================================
    echo.
    echo 1. Reinicie o computador
    echo 2. Verifique se a virtualizacao esta habilitada no BIOS
    echo 3. Reinstale o Docker Desktop
    echo 4. Use AWS RDS (recomendado para desenvolvimento)
    echo.
    echo ==========================================
    echo   Configuracao AWS RDS
    echo ==========================================
    echo.
    echo Para configurar AWS RDS:
    echo 1. Execute: scripts\configure-aws-rds.bat
    echo 2. Siga o guia: docs\aws-rds-setup.md
    echo.
    echo Configuracao atual para N8N:
    echo Host: localhost (ou endpoint do RDS)
    echo Porta: 5432
    echo Database: app
    echo Usuario: app
    echo Senha: mrdom2024
    echo.
    goto :end
) else (
    echo [SUCCESS] Docker esta funcionando!
    echo.
    echo ==========================================
    echo   Testando PostgreSQL
    echo ==========================================
    echo.
    
    REM Testar se PostgreSQL esta rodando
    docker ps | findstr postgres >nul
    if errorlevel 1 (
        echo [INFO] PostgreSQL nao esta rodando. Iniciando...
        docker-compose -f compose\docker-compose.yml up -d postgres
        
        echo [INFO] Aguardando PostgreSQL inicializar...
        timeout /t 15 /nobreak >nul
        
        REM Testar conexao
        docker exec mrdom-postgres psql -U app -d app -c "SELECT version();" >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Falha na conexao com PostgreSQL
        ) else (
            echo [SUCCESS] PostgreSQL funcionando!
            echo.
            echo Configuracao para N8N:
            echo Host: localhost
            echo Porta: 5432
            echo Database: app
            echo Usuario: app
            echo Senha: mrdom2024
        )
    ) else (
        echo [SUCCESS] PostgreSQL ja esta rodando!
        echo.
        echo Configuracao para N8N:
        echo Host: localhost
        echo Porta: 5432
        echo Database: app
        echo Usuario: app
        echo Senha: mrdom2024
    )
)

:end
echo.
echo ==========================================
echo   Resumo
echo ==========================================
echo.
echo Se Docker estiver funcionando:
echo - Use localhost:5432 para conectar no N8N
echo - Execute: docker-compose -f compose\docker-compose.yml up -d
echo.
echo Se Docker nao estiver funcionando:
echo - Configure AWS RDS: scripts\configure-aws-rds.bat
echo - Use o endpoint do RDS para conectar no N8N
echo.

pause
