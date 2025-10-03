@echo off
REM Script para configurar AWS RDS no projeto MrDom SDR

setlocal enabledelayedexpansion

echo ==========================================
echo   Configuracao AWS RDS - MrDom SDR
echo ==========================================
echo.

echo Este script ira te ajudar a configurar as variaveis
echo de ambiente para conectar com o AWS RDS PostgreSQL.
echo.

echo ==========================================
echo   Informacoes Necessarias
echo ==========================================
echo.
echo Voce precisara das seguintes informacoes do seu RDS:
echo - Endpoint (hostname)
echo - Porta (geralmente 5432)
echo - Nome do database
echo - Usuario
echo - Senha
echo.

echo ==========================================
echo   Coletando Informacoes
echo ==========================================
echo.

set /p rds_endpoint="Digite o endpoint do RDS (ex: mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com): "
set /p rds_port="Digite a porta (padrao: 5432): "
set /p rds_database="Digite o nome do database (padrao: app): "
set /p rds_user="Digite o usuario (padrao: app): "
set /p rds_password="Digite a senha: "

REM Definir valores padrao se vazios
if "%rds_port%"=="" set rds_port=5432
if "%rds_database%"=="" set rds_database=app
if "%rds_user%"=="" set rds_user=app

echo.
echo ==========================================
echo   Configuracao Atual
echo ==========================================
echo.
echo Endpoint: %rds_endpoint%
echo Porta: %rds_port%
echo Database: %rds_database%
echo Usuario: %rds_user%
echo Senha: [OCULTA]
echo.

echo ==========================================
echo   Atualizando config.env
echo ==========================================
echo.

REM Fazer backup do config.env atual
if exist config.env (
    copy config.env config.env.backup >nul
    echo [INFO] Backup criado: config.env.backup
)

REM Atualizar config.env
echo [INFO] Atualizando config.env...

REM Usar PowerShell para atualizar o arquivo
powershell -Command "& {
    $content = Get-Content 'config.env' -Raw
    $content = $content -replace 'DB_HOST=.*', 'DB_HOST=%rds_endpoint%'
    $content = $content -replace 'DB_PORT=.*', 'DB_PORT=%rds_port%'
    $content = $content -replace 'DB_NAME=.*', 'DB_NAME=%rds_database%'
    $content = $content -replace 'DB_USER=.*', 'DB_USER=%rds_user%'
    $content = $content -replace 'DB_PASSWORD=.*', 'DB_PASSWORD=%rds_password%'
    $content = $content -replace 'DATABASE_URL=.*', 'DATABASE_URL=postgresql://%rds_user%:%rds_password%@%rds_endpoint%:%rds_port%/%rds_database%'
    Set-Content 'config.env' $content
}"

echo [SUCCESS] config.env atualizado!

echo.
echo ==========================================
echo   Configuracao para N8N
echo ==========================================
echo.
echo Use estas configuracoes no N8N:
echo.
echo Host: %rds_endpoint%
echo Port: %rds_port%
echo Database: %rds_database%
echo Username: %rds_user%
echo Password: %rds_password%
echo SSL Mode: require
echo.

echo ==========================================
echo   Testando Conexao
echo ==========================================
echo.

echo [INFO] Testando conexao com o banco...

REM Verificar se psql esta disponivel
where psql >nul 2>&1
if errorlevel 1 (
    echo [WARNING] psql nao encontrado. Instale PostgreSQL client para testar conexao.
    echo.
    echo Para testar manualmente:
    echo psql -h %rds_endpoint% -p %rds_port% -U %rds_user% -d %rds_database%
) else (
    echo [INFO] Executando teste de conexao...
    echo [INFO] Digite a senha quando solicitado...
    psql -h %rds_endpoint% -p %rds_port% -U %rds_user% -d %rds_database% -c "SELECT version();"
    if errorlevel 1 (
        echo [ERROR] Falha na conexao. Verifique as configuracoes.
    ) else (
        echo [SUCCESS] Conexao bem-sucedida!
    )
)

echo.
echo ==========================================
echo   Configuracao Concluida
echo ==========================================
echo.
echo Suas configuracoes foram salvas em config.env
echo.
echo Proximos passos:
echo 1. Configure o N8N com as informacoes acima
echo 2. Teste a conexao no N8N
echo 3. Execute os scripts de inicializacao do banco
echo 4. Configure o ambiente de testes se necessario
echo.

echo ==========================================

pause
