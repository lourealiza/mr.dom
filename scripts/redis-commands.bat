@echo off
REM Script com comandos úteis para Redis

setlocal enabledelayedexpansion

echo ==========================================
echo   Comandos Redis - MrDom SDR
echo ==========================================
echo.

echo Redis esta rodando! Use estes comandos:
echo.

echo 1. Testar conexao:
echo    redis\redis-cli.exe ping
echo.

echo 2. Ver todas as chaves:
echo    redis\redis-cli.exe keys "*"
echo.

echo 3. Limpar todas as chaves:
echo    redis\redis-cli.exe flushall
echo.

echo 4. Monitorar Redis:
echo    redis\redis-cli.exe monitor
echo.

echo 5. Informacoes do servidor:
echo    redis\redis-cli.exe info
echo.

echo ==========================================
echo   Testando Redis
echo ==========================================
echo.

echo [INFO] Testando conexao...
redis\redis-cli.exe ping

echo.
echo [INFO] Testando operacoes basicas...

REM Testar operacoes basicas
redis\redis-cli.exe set "mrdom:test" "Redis funcionando!"
redis\redis-cli.exe get "mrdom:test"

echo.
echo [INFO] Criando estrutura de dados para o projeto...

REM Criar estrutura basica para o projeto
redis\redis-cli.exe hset "mrdom:conversations:123" "id" "123" "status" "open" "contact_id" "456"
redis\redis-cli.exe lpush "mrdom:messages:123" "Mensagem de teste 1"
redis\redis-cli.exe lpush "mrdom:messages:123" "Mensagem de teste 2"
redis\redis-cli.exe hset "mrdom:contacts:456" "name" "Joao Silva" "email" "joao@teste.com"

echo.
echo [SUCCESS] Estrutura de dados criada!
echo.

echo ==========================================
echo   Configuracao para N8N
echo ==========================================
echo.
echo Use estas configuracoes no N8N:
echo.
echo Host: localhost
echo Port: 6379
echo Database: 0
echo Password: (deixe vazio)
echo.
echo Para testar no N8N:
echo 1. Crie um no Redis
echo 2. Configure a conexao
echo 3. Use comando: PING
echo.

echo ==========================================
echo   Comandos Uteis
echo ==========================================
echo.

echo Para iniciar Redis:
echo start "Redis" redis\redis-server.exe
echo.

echo Para parar Redis:
echo taskkill /f /im redis-server.exe
echo.

echo Para conectar no Redis:
echo redis\redis-cli.exe
echo.

echo ==========================================

pause
