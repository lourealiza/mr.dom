# Configuração Redis - MrDom SDR

Redis é uma excelente opção para desenvolvimento e testes. É mais simples que PostgreSQL e perfeito para cache, sessões e dados temporários.

## 🚀 **Vantagens do Redis**

- ✅ **Simples de configurar**
- ✅ **Rápido e eficiente**
- ✅ **Perfeito para desenvolvimento**
- ✅ **Suporte nativo no projeto**
- ✅ **Ideal para cache e sessões**

## 📋 **Opções de Instalação**

### **1. Redis Local (Recomendado)**

#### **Windows:**
1. Baixe Redis para Windows: https://github.com/microsoftarchive/redis/releases
2. Extraia e execute `redis-server.exe`
3. Redis rodará na porta 6379

#### **Docker (se funcionar):**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

### **2. Redis Cloud (Gratuito)**

#### **Redis Cloud:**
1. Acesse: https://redis.com/try-free/
2. Crie conta gratuita
3. Crie uma instância gratuita
4. Obtenha as credenciais de conexão

#### **Upstash Redis:**
1. Acesse: https://upstash.com/
2. Crie conta gratuita
3. Crie um banco Redis
4. Obtenha URL de conexão

## 🔧 **Configuração do Projeto**

### **Atualizar config.env:**
```env
# ====== Configurações do Redis ======
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# ====== Configurações do PostgreSQL (Desabilitado) ======
# DB_HOST=postgres
# DB_PORT=5432
# DB_NAME=app
# DB_USER=app
# DB_PASSWORD=mrdom2024
```

### **Para N8N:**
- **Host:** `localhost`
- **Port:** `6379`
- **Database:** `0`
- **Password:** (deixe vazio se local)

## 🛠️ **Scripts de Configuração**

### **Instalar Redis Local:**
```bash
# Baixar Redis para Windows
# https://github.com/microsoftarchive/redis/releases
```

### **Testar Conexão:**
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('test', 'Hello Redis!')
print(r.get('test'))
```

## 📊 **Estrutura de Dados no Redis**

### **Chaves Sugeridas:**
```
conversations:{conversation_id}     # Dados da conversa
messages:{conversation_id}:{msg_id} # Mensagens
contacts:{contact_id}               # Dados do contato
bot_sessions:{session_id}          # Sessões do bot
workflow_executions:{exec_id}       # Execuções de workflow
cache:{key}                        # Cache geral
```

### **Exemplo de Uso:**
```python
# Salvar conversa
r.hset('conversations:123', mapping={
    'id': '123',
    'status': 'open',
    'contact_id': '456',
    'created_at': '2024-01-01T10:00:00Z'
})

# Salvar mensagem
r.lpush('messages:123', {
    'id': 'msg-1',
    'content': 'Olá!',
    'type': 'incoming',
    'timestamp': '2024-01-01T10:00:00Z'
})

# Salvar sessão do bot
r.hset('bot_sessions:session-123', mapping={
    'conversation_id': '123',
    'current_step': 'greeting',
    'state': '{"name": "João"}'
})
```

## 🔍 **Testando Redis**

### **Comando CLI:**
```bash
redis-cli
> ping
PONG
> set test "Hello Redis"
OK
> get test
"Hello Redis"
```

### **Python:**
```python
import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print("✅ Redis conectado!")
    
    # Teste básico
    r.set('test_key', 'test_value')
    value = r.get('test_key')
    print(f"Valor: {value}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
```

## 🚀 **Iniciando Redis**

### **Windows:**
1. Baixe Redis: https://github.com/microsoftarchive/redis/releases
2. Extraia o arquivo ZIP
3. Execute `redis-server.exe`
4. Redis estará rodando em `localhost:6379`

### **Docker (se funcionar):**
```bash
docker run -d --name mrdom-redis -p 6379:6379 redis:7-alpine
```

## 📝 **Configuração para N8N**

### **No N8N:**
1. Vá para **Credentials** → **Redis**
2. Configure:
   - **Host:** `localhost`
   - **Port:** `6379`
   - **Database:** `0`
   - **Password:** (deixe vazio)

### **Teste no N8N:**
1. Crie um nó **Redis**
2. Configure a conexão
3. Teste com comando `PING`

## 💡 **Dicas de Uso**

### **Para Desenvolvimento:**
- Use Redis para cache de respostas
- Armazene sessões de conversa
- Cache de dados do Chatwoot
- Armazenamento temporário de workflows

### **Estrutura Recomendada:**
```
mrdom:conversations:{id}     # Conversas
mrdom:messages:{conv_id}     # Mensagens por conversa
mrdom:contacts:{id}          # Contatos
mrdom:sessions:{id}          # Sessões do bot
mrdom:cache:{key}           # Cache geral
```

## 🔧 **Scripts Úteis**

### **Limpar Redis:**
```bash
redis-cli FLUSHALL
```

### **Ver todas as chaves:**
```bash
redis-cli KEYS "*"
```

### **Monitorar Redis:**
```bash
redis-cli MONITOR
```

## 🎯 **Próximos Passos**

1. ✅ Instalar Redis local
2. ✅ Configurar projeto para usar Redis
3. ✅ Testar conexão
4. ✅ Configurar N8N
5. ✅ Implementar estrutura de dados
6. ✅ Testar funcionalidades

## 🆘 **Solução de Problemas**

### **Redis não conecta:**
- Verifique se Redis está rodando
- Confirme porta 6379
- Verifique firewall

### **Erro de conexão:**
- Teste com `redis-cli ping`
- Verifique configurações de rede
- Confirme se Redis aceita conexões externas
