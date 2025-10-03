# ☁️ Configuração Redis Cloud - MrDom SDR

## 🎯 Objetivo

Configurar Redis Cloud para o projeto MrDom SDR, substituindo o Redis local por uma instância gerenciada na nuvem.

## 📋 Pré-requisitos

- Conta no [Redis Cloud](https://cloud.redis.io/) criada com GitHub
- Acesso ao dashboard Redis Cloud
- Projeto MrDom SDR configurado

## 🚀 Passo a Passo

### 1. **Acessar Redis Cloud**

1. Acesse [https://cloud.redis.io/](https://cloud.redis.io/)
2. Faça login com sua conta GitHub
3. Vá para o dashboard da sua conta

### 2. **Localizar Dados de Conexão**

No dashboard Redis Cloud:

1. **Clique em "Databases"** ou **"My Databases"**
2. **Selecione sua database** (se não tiver uma, crie uma nova)
3. **Copie os dados de conexão**:
   - **Endpoint/Host**: Ex: `redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com`
   - **Port**: Ex: `12345`
   - **Password**: Senha gerada automaticamente
   - **Database**: Geralmente `0`

### 3. **Configuração Automática**

Execute o script de configuração:

```bash
python scripts/configure-redis-cloud.py
```

O script irá:
- Solicitar os dados de conexão
- Configurar o arquivo `config.env`
- Testar a conexão
- Configurar dados de teste

### 4. **Configuração Manual**

Se preferir configurar manualmente, edite o arquivo `config.env`:

```ini
# ====== Configuracoes Redis Cloud ======
REDIS_CLOUD_HOST=redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com
REDIS_CLOUD_PORT=12345
REDIS_CLOUD_PASSWORD=sua_senha_aqui
REDIS_CLOUD_DB=0
REDIS_CLOUD_URL=redis://:sua_senha_aqui@redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com:12345/0
```

### 5. **Testar Conexão**

Execute o teste de conexão:

```bash
python scripts/test-redis-cloud.py
```

O teste irá verificar:
- ✅ Ping da conexão
- ✅ Operações básicas (SET/GET)
- ✅ Estruturas de dados (Hash, List, Set)
- ✅ Performance (escrita/leitura em lote)
- ✅ Configuração de dados da trilha

## 🔧 Configuração no n8n

### 1. **Acessar n8n**

1. Acesse sua instância n8n
2. Vá para **Settings** → **Credentials**
3. Clique em **"Add Credential"**

### 2. **Criar Credential Redis**

1. **Selecione "Redis"**
2. **Configure os campos**:
   - **Host**: `redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com`
   - **Port**: `12345`
   - **Password**: `sua_senha_aqui`
   - **Database**: `0`
   - **SSL**: `true` (se disponível)

3. **Teste a conexão**
4. **Salve a credential**

### 3. **Usar em Workflows**

Nos seus workflows n8n:

1. **Adicione um nó Redis**
2. **Selecione a credential criada**
3. **Configure a operação** (SET, GET, HGET, etc.)

## 📊 Configuração nos Testes

### 1. **Atualizar Testes**

Os testes já estão configurados para usar Redis Cloud. Para ativar:

```python
# Em api/tests/test_endpoints.py
import os

# Usar Redis Cloud se configurado
if os.getenv('REDIS_CLOUD_HOST'):
    redis_host = os.getenv('REDIS_CLOUD_HOST')
    redis_port = int(os.getenv('REDIS_CLOUD_PORT'))
    redis_password = os.getenv('REDIS_CLOUD_PASSWORD')
    redis_db = int(os.getenv('REDIS_CLOUD_DB'))
else:
    # Usar Redis local
    redis_host = 'localhost'
    redis_port = 6379
    redis_password = None
    redis_db = 0
```

### 2. **Executar Testes**

```bash
# Executar trilha de testes com Redis Cloud
python scripts/run-trilha-tests.py

# Testar conexão específica
python scripts/test-redis-cloud.py
```

## 🔍 Troubleshooting

### Problemas Comuns

#### ❌ **Erro de Conexão**
```
redis.exceptions.ConnectionError: Error 111 connecting to redis-xxx.cloud.redislabs.com:12345
```

**Soluções**:
- Verifique se o host e port estão corretos
- Confirme se a password está correta
- Verifique se o firewall permite conexão
- Teste a conectividade: `telnet redis-xxx.cloud.redislabs.com 12345`

#### ❌ **Erro de Autenticação**
```
redis.exceptions.AuthenticationError: WRONGPASS invalid username-password pair
```

**Soluções**:
- Verifique se a password está correta
- Confirme se não há espaços extras
- Teste a password no dashboard Redis Cloud

#### ❌ **Erro de Database**
```
redis.exceptions.ResponseError: ERR DB index is out of range
```

**Soluções**:
- Verifique se o database existe (geralmente 0)
- Confirme se a instância suporta múltiplas databases

#### ❌ **Timeout de Conexão**
```
redis.exceptions.TimeoutError: Timeout connecting to server
```

**Soluções**:
- Aumente o timeout de conexão
- Verifique a latência da rede
- Teste de uma rede diferente

### Comandos de Diagnóstico

```bash
# Testar conectividade
telnet redis-xxx.cloud.redislabs.com 12345

# Testar com redis-cli
redis-cli -h redis-xxx.cloud.redislabs.com -p 12345 -a sua_senha ping

# Verificar configuração
python scripts/test-redis-cloud.py
```

## 📈 Monitoramento

### 1. **Dashboard Redis Cloud**

No dashboard Redis Cloud você pode monitorar:
- **Uso de memória**
- **Conexões ativas**
- **Comandos por segundo**
- **Latência**
- **Logs de erro**

### 2. **Métricas dos Testes**

Os testes coletam métricas:
- **Tempo de ping**
- **Performance de escrita/leitura**
- **Taxa de sucesso**
- **Latência média**

### 3. **Alertas**

Configure alertas no Redis Cloud para:
- **Uso de memória > 80%**
- **Conexões > limite**
- **Latência > 100ms**
- **Erros > 5%**

## 💡 Dicas de Otimização

### 1. **Pool de Conexões**

```python
import redis.connection

# Configurar pool de conexões
pool = redis.ConnectionPool(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    db=redis_db,
    max_connections=20,
    socket_timeout=30,
    socket_connect_timeout=30
)

r = redis.Redis(connection_pool=pool)
```

### 2. **Pipeline para Operações em Lote**

```python
# Usar pipeline para múltiplas operações
pipe = r.pipeline()
for i in range(100):
    pipe.set(f"key_{i}", f"value_{i}")
pipe.execute()
```

### 3. **TTL para Dados Temporários**

```python
# Definir TTL para dados de teste
r.set("test:data", "value", ex=3600)  # 1 hora
```

## 🔒 Segurança

### 1. **Password Segura**

- Use passwords geradas automaticamente
- Não compartilhe passwords em logs
- Rotacione passwords regularmente

### 2. **Acesso Restrito**

- Configure IPs permitidos no Redis Cloud
- Use SSL/TLS quando disponível
- Monitore acessos suspeitos

### 3. **Backup**

- Configure backups automáticos
- Teste restauração regularmente
- Mantenha backups em local seguro

## 📚 Recursos Adicionais

- [Documentação Redis Cloud](https://docs.redislabs.com/)
- [Redis Cloud Dashboard](https://cloud.redis.io/)
- [Documentação Redis Python](https://redis-py.readthedocs.io/)
- [Guia de Troubleshooting Redis](https://redis.io/docs/manual/troubleshooting/)

## 🆘 Suporte

Em caso de problemas:

1. **Verifique os logs** em `test_results/logs/`
2. **Execute o teste de conexão**: `python scripts/test-redis-cloud.py`
3. **Consulte a documentação** Redis Cloud
4. **Entre em contato** com o suporte Redis Cloud
5. **Abra uma issue** no repositório do projeto
