# Configuração do Supabase

## 🔗 Conectando com a API do Supabase

### 1. Acesse o Dashboard do Supabase
- URL: https://fqelsdkaqtjsuxqyvukh.supabase.co
- Faça login no seu projeto

### 2. Obtenha as Credenciais

#### **API Keys:**
1. Vá para **Settings** → **API**
2. Copie as seguintes chaves:
   - **anon/public key** (para operações do cliente)
   - **service_role key** (para operações do servidor)

#### **Database URL:**
1. Vá para **Settings** → **Database**
2. Copie a **Connection string** (URI)
3. Substitua `[YOUR-PASSWORD]` pela senha do seu banco

### 3. Configure o arquivo `config.env`

```env
# ====== Configuracoes do Supabase ======
SUPABASE_URL=https://fqelsdkaqtjsuxqyvukh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.fqelsdkaqtjsuxqyvukh.supabase.co:5432/postgres
```

### 4. Instalar Dependências

```bash
pip install supabase
```

### 5. Exemplo de Uso

```python
from supabase import create_client, Client
from app.core.settings import settings

# Inicializar cliente Supabase
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)

# Exemplo de operação
def get_user_data(user_id: str):
    response = supabase.table('users').select('*').eq('id', user_id).execute()
    return response.data
```

### 6. Configurações de Segurança

- **anon key**: Use para operações do frontend
- **service_role key**: Use apenas no backend (tem acesso total)
- **Database URL**: Use para conexões diretas com PostgreSQL

### 7. Integração com N8N

Para integrar com o N8N do Mr. DOM:

- **N8N URL**: https://autodevchat.domineseunegocio.com.br
- **Tabela**: `n8n_chat_histories` (já criada no banco)
- **Credenciais PostgreSQL**: 
  - Host: `localhost` (ou `postgres` se Docker)
  - Port: `5432`
  - Database: `app`
  - User: `app`
  - Password: `mrdom2024`

### 7. Teste de Conexão

```python
# Teste simples
try:
    response = supabase.table('test_table').select('*').limit(1).execute()
    print("✅ Conexão com Supabase funcionando!")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
```

## 📋 Checklist de Configuração

- [ ] Obter anon key do dashboard
- [ ] Obter service_role key do dashboard  
- [ ] Obter database URL com senha
- [ ] Atualizar config.env com as credenciais
- [ ] Instalar dependência `supabase`
- [ ] Testar conexão
- [ ] Configurar tabelas necessárias no Supabase
