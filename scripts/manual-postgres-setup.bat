@echo off
REM Script manual para configurar PostgreSQL sem Docker
REM Este script fornece instruções para configurar PostgreSQL manualmente

setlocal enabledelayedexpansion

echo ==========================================
echo   Configuracao Manual do PostgreSQL
echo ==========================================
echo.
echo Como o Docker Desktop nao esta funcionando, vamos configurar
echo o PostgreSQL manualmente ou usar uma instancia local.
echo.

echo Opcoes disponiveis:
echo.
echo 1. Instalar PostgreSQL localmente
echo 2. Usar PostgreSQL em servidor externo
echo 3. Usar Docker quando estiver funcionando
echo.

set /p choice="Escolha uma opcao (1-3): "

if "%choice%"=="1" goto :local_install
if "%choice%"=="2" goto :external_server
if "%choice%"=="3" goto :docker_wait
goto :invalid_choice

:local_install
echo.
echo ==========================================
echo   Instalacao Local do PostgreSQL
echo ==========================================
echo.
echo Para instalar PostgreSQL localmente:
echo.
echo 1. Baixe o PostgreSQL em: https://www.postgresql.org/download/windows/
echo 2. Instale com as seguintes configuracoes:
echo    - Porta: 5432
echo    - Usuario: app
echo    - Senha: mrdom2024
echo    - Database: app
echo.
echo 3. Apos a instalacao, execute os comandos SQL:
echo    CREATE DATABASE app;
echo    CREATE USER app WITH PASSWORD 'mrdom2024';
echo    GRANT ALL PRIVILEGES ON DATABASE app TO app;
echo.
echo 4. Configure as variaveis de ambiente:
echo    DB_HOST=localhost
echo    DB_PORT=5432
echo    DB_NAME=app
echo    DB_USER=app
echo    DB_PASSWORD=mrdom2024
echo.
goto :end

:external_server
echo.
echo ==========================================
echo   PostgreSQL em Servidor Externo
echo ==========================================
echo.
echo Para usar um servidor PostgreSQL externo:
echo.
echo 1. Configure as variaveis de ambiente no config.env:
echo    DB_HOST=seu-servidor-postgres.com
echo    DB_PORT=5432
echo    DB_NAME=app
echo    DB_USER=seu-usuario
echo    DB_PASSWORD=sua-senha
echo.
echo 2. Certifique-se de que o servidor permite conexoes externas
echo 3. Teste a conexao com:
echo    psql -h seu-servidor-postgres.com -U seu-usuario -d app
echo.
goto :end

:docker_wait
echo.
echo ==========================================
echo   Aguardando Docker Desktop
echo ==========================================
echo.
echo Para usar Docker:
echo.
echo 1. Inicie o Docker Desktop manualmente
echo 2. Aguarde ate que esteja completamente carregado
echo 3. Execute: scripts\reset-postgres.bat
echo.
echo Se o Docker Desktop nao iniciar:
echo - Reinicie o computador
echo - Verifique se a virtualizacao esta habilitada no BIOS
echo - Reinstale o Docker Desktop se necessario
echo.
goto :end

:invalid_choice
echo Opcao invalida!
goto :end

:end
echo.
echo ==========================================
echo   Configuracao Atual
echo ==========================================
echo.
echo As configuracoes atuais estao em config.env:
echo.
type config.env | findstr "DB_"
echo.
echo Para o N8N, use estas configuracoes:
echo   Host: localhost (ou seu servidor)
echo   Porta: 5432
echo   Database: app
echo   Usuario: app
echo   Senha: mrdom2024
echo.
echo ==========================================

pause
