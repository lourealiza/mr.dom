@echo off
REM Script para configurar Redis no projeto MrDom SDR

setlocal enabledelayedexpansion

echo ==========================================
echo   Configuracao Redis - MrDom SDR
echo ==========================================
echo.

echo Redis e uma excelente opcao para desenvolvimento!
echo E mais simples que PostgreSQL e perfeito para cache e sessoes.
echo.

echo ==========================================
echo   Opcoes de Instalacao
echo ==========================================
echo.
echo 1. Redis Local (Recomendado)
echo 2. Redis Cloud (Gratuito)
echo 3. Docker Redis (se Docker funcionar)
echo 4. Usar Redis existente
echo.

set /p choice="Escolha uma opcao (1-4): "

if "%choice%"=="1" goto :local_redis
if "%choice%"=="2" goto :cloud_redis
if "%choice%"=="3" goto :docker_redis
if "%choice%"=="4" goto :existing_redis
goto :invalid_choice

:local_redis
echo.
echo ==========================================
echo   Redis Local
echo ==========================================
echo.
echo Para instalar Redis localmente:
echo.
echo 1. Baixe Redis para Windows:
echo    https://github.com/microsoftarchive/redis/releases
echo.
echo 2. Extraia o arquivo ZIP
echo 3. Execute redis-server.exe
echo 4. Redis rodara na porta 6379
echo.
echo Configuracao para o projeto:
echo REDIS_URL=redis://localhost:6379/0
echo REDIS_HOST=localhost
echo REDIS_PORT=6379
echo REDIS_DB=0
echo.
goto :configure_project

:cloud_redis
echo.
echo ==========================================
echo   Redis Cloud
echo ==========================================
echo.
echo Opcoes gratuitas:
echo.
echo 1. Redis Cloud: https://redis.com/try-free/
echo 2. Upstash Redis: https://upstash.com/
echo.
echo Apos criar conta, voce recebera:
echo - Host (endereco do servidor)
echo - Porta (geralmente 6379)
echo - Senha (se necessario)
echo.
echo Configure no projeto com as credenciais recebidas.
echo.
goto :configure_project

:docker_redis
echo.
echo ==========================================
echo   Docker Redis
echo ==========================================
echo.
echo Tentando iniciar Redis com Docker...
echo.

docker run -d --name mrdom-redis -p 6379:6379 redis:7-alpine
if errorlevel 1 (
    echo [ERROR] Docker nao esta funcionando.
    echo Use uma das outras opcoes.
    goto :end
) else (
    echo [SUCCESS] Redis iniciado com Docker!
    echo.
    echo Configuracao:
    echo REDIS_URL=redis://localhost:6379/0
    echo REDIS_HOST=localhost
    echo REDIS_PORT=6379
    echo REDIS_DB=0
)
goto :configure_project

:existing_redis
echo.
echo ==========================================
echo   Redis Existente
echo ==========================================
echo.
echo Se voce ja tem Redis rodando:
echo.
echo Configure manualmente no config.env:
echo REDIS_URL=redis://seu-host:porta/db
echo REDIS_HOST=seu-host
echo REDIS_PORT=sua-porta
echo REDIS_DB=seu-db
echo REDIS_PASSWORD=sua-senha
echo.
goto :configure_project

:configure_project
echo.
echo ==========================================
echo   Configurando Projeto
echo ==========================================
echo.

REM Fazer backup do config.env
if exist config.env (
    copy config.env config.env.backup >nul
    echo [INFO] Backup criado: config.env.backup
)

REM Atualizar config.env para Redis
echo [INFO] Atualizando config.env para Redis...

REM Criar novo config.env focado em Redis
echo # ====== Chatwoot API ====== > config.env
echo CHATWOOT_BASE_URL=https://chatwootdev.domineseunegocio.com.br >> config.env
echo CHATWOOT_ACCESS_TOKEN=bDdDRz2RbrgvHjscdXgtVYQ8 >> config.env
echo CHATWOOT_ACCOUNT_ID=1 >> config.env
echo. >> config.env
echo # Seguranca do webhook do Agent Bot >> config.env
echo CHATWOOT_BOT_TOKEN=bDdDRz2RbrgvHjscdXgtVYQ8 >> config.env
echo CHATWOOT_HMAC_SECRET=aYmuHEPax3xWb2UboHC6J4J9 >> config.env
echo. >> config.env
echo # ====== n8n ====== >> config.env
echo N8N_BASE_URL=https://n8n-inovacao.ar-infra.com.br >> config.env
echo N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxYmJhM2U0Mi03MDVmLTRkYjktOGZjMC04NmUxYjA5YzVlODEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2OTE4NDI5fQ.3NHagASdkW_O_Hc-LrDrxUEnXK8LqtdJFNQaXO_tWq8 >> config.env
echo N8N_USER=cursor >> config.env
echo N8N_PASSWORD=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxYmJhM2U0Mi03MDVmLTRkYjktOGZjMC04NmUxYjA5YzVlODEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2OTE4NDI5fQ.3NHagASdkW_O_Hc-LrDrxUEnXK8LqtdJFNQaXO_tWq8 >> config.env
echo. >> config.env
echo # ====== OpenAI ====== >> config.env
echo OPENAI_API_KEY=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 >> config.env
echo OPENAI_MODEL=gpt-4o-mini >> config.env
echo. >> config.env
echo # ====== Configuracoes do Bot ====== >> config.env
echo BOT_WELCOME_MESSAGE=Ola! 👋 Sou o assistente virtual da MrDom. Como posso ajuda-lo hoje? >> config.env
echo ESCALATION_KEYWORDS=["falar com humano", "atendente", "supervisor", "quero falar com alguem"] >> config.env
echo AUTO_RESPONSE_ENABLED=true >> config.env
echo QUALIFICATION_QUESTIONS=["Qual e o seu principal desafio?", "Qual o tamanho da sua empresa?", "Qual o seu orcamento aproximado?"] >> config.env
echo BUSINESS_HOURS={"start": "09:00", "end": "18:00"} >> config.env
echo TIMEZONE=America/Sao_Paulo >> config.env
echo. >> config.env
echo # ====== Configuracoes de Log ====== >> config.env
echo LOG_LEVEL=INFO >> config.env
echo LOG_FORMAT=json >> config.env
echo. >> config.env
echo # ====== Configuracoes de Seguranca ====== >> config.env
echo SECRET_KEY=sua_chave_secreta_aqui >> config.env
echo ALLOWED_HOSTS=["localhost", "127.0.0.1", "0.0.0.0"] >> config.env
echo. >> config.env
echo # ====== Configuracoes do Redis ====== >> config.env
echo REDIS_URL=redis://localhost:6379/0 >> config.env
echo REDIS_HOST=localhost >> config.env
echo REDIS_PORT=6379 >> config.env
echo REDIS_DB=0 >> config.env
echo REDIS_PASSWORD= >> config.env
echo. >> config.env
echo # ====== Configuracoes de Desenvolvimento ====== >> config.env
echo DEBUG=true >> config.env
echo RELOAD=true >> config.env

echo [SUCCESS] config.env atualizado para Redis!

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
echo Password: (deixe vazio se local)
echo.

echo ==========================================
echo   Testando Redis
echo ==========================================
echo.

echo [INFO] Testando conexao com Redis...

REM Verificar se redis-cli esta disponivel
where redis-cli >nul 2>&1
if errorlevel 1 (
    echo [WARNING] redis-cli nao encontrado.
    echo Instale Redis para testar conexao.
    echo.
    echo Para testar manualmente:
    echo redis-cli ping
) else (
    echo [INFO] Testando conexao...
    redis-cli ping >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Redis nao esta rodando.
        echo Inicie Redis antes de continuar.
    ) else (
        echo [SUCCESS] Redis esta funcionando!
    )
)

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
echo Redis configurado para o projeto!
echo.
echo Proximos passos:
echo 1. Instale Redis (se ainda nao instalou)
echo 2. Configure N8N com as informacoes acima
echo 3. Teste a conexao
echo 4. Execute o projeto
echo.
echo Para mais informacoes:
echo docs\redis-setup.md
echo.

pause
