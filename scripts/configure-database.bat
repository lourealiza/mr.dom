@echo off
REM Script para configurar banco de dados (RDS, Local, ou outro)

setlocal enabledelayedexpansion

echo ==========================================
echo   Configuracao de Banco de Dados
echo ==========================================
echo.

echo Escolha uma opcao:
echo.
echo 1. AWS RDS (Recomendado)
echo 2. PostgreSQL Local
echo 3. Outro servidor PostgreSQL
echo 4. Usar configuracoes atuais
echo.

set /p choice="Digite sua escolha (1-4): "

if "%choice%"=="1" goto :aws_rds
if "%choice%"=="2" goto :local_postgres
if "%choice%"=="3" goto :other_server
if "%choice%"=="4" goto :current_config
goto :invalid_choice

:aws_rds
echo.
echo ==========================================
echo   AWS RDS
echo ==========================================
echo.
echo Para criar um RDS:
echo 1. Acesse: https://console.aws.amazon.com/rds/
echo 2. Clique em "Create database"
echo 3. Escolha PostgreSQL
echo 4. Use estas configuracoes:
echo    - DB instance identifier: mrdom-sdr-postgres
echo    - Master username: app
echo    - Master password: mrdom2024
echo    - Initial database name: app
echo    - Public access: Yes
echo.
echo Apos criar, execute: scripts\configure-aws-rds.bat
echo.
goto :end

:local_postgres
echo.
echo ==========================================
echo   PostgreSQL Local
echo ==========================================
echo.
echo Para instalar PostgreSQL localmente:
echo 1. Baixe em: https://www.postgresql.org/download/windows/
echo 2. Instale com:
echo    - Porta: 5432
echo    - Usuario: app
echo    - Senha: mrdom2024
echo    - Database: app
echo.
echo 3. Apos instalacao, execute:
echo    scripts\configure-local-postgres.bat
echo.
goto :end

:other_server
echo.
echo ==========================================
echo   Outro Servidor PostgreSQL
echo ==========================================
echo.
echo Configure manualmente o config.env:
echo.
echo DB_HOST=seu-servidor.com
echo DB_PORT=5432
echo DB_NAME=app
echo DB_USER=seu-usuario
echo DB_PASSWORD=sua-senha
echo DATABASE_URL=postgresql://seu-usuario:sua-senha@seu-servidor.com:5432/app
echo.
echo Depois execute: scripts\test-rds-connection.py
echo.
goto :end

:current_config
echo.
echo ==========================================
echo   Configuracao Atual
echo ==========================================
echo.
echo Suas configuracoes atuais:
echo.
type config.env | findstr "DB_"
echo.
echo Para N8N, use:
echo Host: localhost (ou DB_HOST do config.env)
echo Port: 5432 (ou DB_PORT do config.env)
echo Database: app (ou DB_NAME do config.env)
echo Usuario: app (ou DB_USER do config.env)
echo Senha: mrdom2024 (ou DB_PASSWORD do config.env)
echo.
goto :end

:invalid_choice
echo Opcao invalida!
goto :end

:end
echo.
echo ==========================================
echo   Resumo
echo ==========================================
echo.
echo Para conectar no N8N, voce precisa de:
echo - Host (endereco do servidor)
echo - Porta (geralmente 5432)
echo - Database (nome do banco)
echo - Usuario
echo - Senha
echo.
echo Se nao tem essas informacoes:
echo 1. Crie um AWS RDS (mais facil)
echo 2. Instale PostgreSQL localmente
echo 3. Use um servidor existente
echo.

pause
