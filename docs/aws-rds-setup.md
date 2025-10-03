# Configuração AWS RDS PostgreSQL - MrDom SDR

Este guia te ajudará a configurar um banco PostgreSQL no AWS RDS para o projeto MrDom SDR.

## 📋 Pré-requisitos

- Conta AWS ativa
- Acesso ao AWS Console
- Conhecimento básico de AWS

## 🚀 Passo a Passo

### 1. Acessar o AWS RDS

1. Faça login no [AWS Console](https://console.aws.amazon.com/)
2. Navegue para **RDS** (Relational Database Service)
3. Clique em **"Create database"**

### 2. Configurar o Banco de Dados

#### **Engine Options**
- **Engine type:** PostgreSQL
- **Version:** PostgreSQL 15.x (recomendado)

#### **Templates**
- **Production:** Para ambiente de produção
- **Dev/Test:** Para desenvolvimento e testes (mais barato)
- **Free tier:** Para testes (limitado)

#### **Settings**
- **DB instance identifier:** `mrdom-sdr-postgres`
- **Master username:** `app`
- **Master password:** `mrdom2024` (ou uma senha mais segura)

#### **Instance Configuration**
- **DB instance class:** 
  - **Free tier:** `db.t3.micro` (1 vCPU, 1 GB RAM)
  - **Dev/Test:** `db.t3.small` (2 vCPU, 2 GB RAM)
  - **Production:** `db.t3.medium` ou maior

#### **Storage**
- **Storage type:** General Purpose SSD (gp3)
- **Allocated storage:** 20 GB (mínimo)
- **Storage autoscaling:** Habilitado (recomendado)

#### **Connectivity**
- **VPC:** Default VPC
- **Subnet group:** Default
- **Public access:** **Yes** (para facilitar conexão)
- **VPC security groups:** Create new
- **Security group name:** `mrdom-sdr-postgres-sg`

#### **Database Authentication**
- **Database authentication:** Password authentication

#### **Additional Configuration**
- **Initial database name:** `app`
- **Backup retention period:** 7 days
- **Backup window:** Default
- **Maintenance window:** Default
- **Monitoring:** Enhanced monitoring (opcional)

### 3. Configurar Security Group

Após criar o banco, configure o Security Group:

1. Vá para **EC2** → **Security Groups**
2. Encontre o grupo `mrdom-sdr-postgres-sg`
3. Clique em **"Edit inbound rules"**
4. Adicione as regras:

```
Type: PostgreSQL
Protocol: TCP
Port: 5432
Source: 0.0.0.0/0 (para desenvolvimento)
```

**⚠️ Para produção, use IPs específicos em vez de 0.0.0.0/0**

### 4. Obter Informações de Conexão

Após criar o banco:

1. Vá para **RDS** → **Databases**
2. Clique no seu banco `mrdom-sdr-postgres`
3. Na aba **"Connectivity & security"**, você encontrará:
   - **Endpoint:** `mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com`
   - **Port:** `5432`

### 5. Configurar o Projeto

Atualize o arquivo `config.env`:

```env
# ====== Configurações do PostgreSQL (AWS RDS) ======
DB_HOST=mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=app
DB_USER=app
DB_PASSWORD=mrdom2024
DATABASE_URL=postgresql://app:mrdom2024@mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432/app
```

### 6. Configurar N8N

No N8N, configure a conexão PostgreSQL:

- **Host:** `mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com`
- **Port:** `5432`
- **Database:** `app`
- **Username:** `app`
- **Password:** `mrdom2024`
- **SSL Mode:** `require` (recomendado para AWS)

### 7. Testar Conexão

#### **Usando psql (se instalado):**
```bash
psql -h mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com -p 5432 -U app -d app
```

#### **Usando Python:**
```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com",
        port=5432,
        database="app",
        user="app",
        password="mrdom2024"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro de conexão: {e}")
```

## 💰 Custos Estimados

### **Free Tier (12 meses):**
- **db.t3.micro:** Gratuito (750 horas/mês)
- **Storage:** 20 GB gratuito
- **Backup:** 20 GB gratuito

### **Dev/Test:**
- **db.t3.small:** ~$15-20/mês
- **Storage:** ~$2-3/mês por 20 GB
- **Backup:** ~$1-2/mês

### **Production:**
- **db.t3.medium:** ~$30-40/mês
- **Storage:** ~$2-3/mês por 20 GB
- **Backup:** ~$1-2/mês
- **Multi-AZ:** +100% do custo

## 🔒 Segurança

### **Recomendações:**

1. **Senhas Fortes:**
   - Use senhas complexas
   - Considere usar AWS Secrets Manager

2. **Security Groups:**
   - Restrinja acesso por IP
   - Use VPN ou bastion host

3. **SSL/TLS:**
   - Sempre use SSL em produção
   - Configure certificados SSL

4. **Backups:**
   - Configure backups automáticos
   - Teste restauração regularmente

5. **Monitoring:**
   - Use CloudWatch para monitoramento
   - Configure alertas

## 🛠️ Comandos Úteis

### **Conectar via AWS CLI:**
```bash
aws rds describe-db-instances --db-instance-identifier mrdom-sdr-postgres
```

### **Criar snapshot:**
```bash
aws rds create-db-snapshot --db-instance-identifier mrdom-sdr-postgres --db-snapshot-identifier mrdom-sdr-backup-$(date +%Y%m%d)
```

### **Listar snapshots:**
```bash
aws rds describe-db-snapshots --db-instance-identifier mrdom-sdr-postgres
```

## 🔧 Troubleshooting

### **Problemas Comuns:**

1. **Conexão recusada:**
   - Verifique Security Group
   - Confirme se o banco está público
   - Verifique firewall local

2. **Timeout de conexão:**
   - Verifique região AWS
   - Confirme endpoint correto
   - Teste conectividade de rede

3. **Erro de autenticação:**
   - Verifique usuário/senha
   - Confirme database name
   - Verifique permissões

### **Logs e Debugging:**

1. **CloudWatch Logs:**
   - Vá para CloudWatch → Logs
   - Procure por `/aws/rds/instance/mrdom-sdr-postgres/postgresql`

2. **RDS Events:**
   - Vá para RDS → Databases → Events
   - Verifique eventos recentes

## 📞 Suporte

- **AWS Documentation:** [RDS PostgreSQL](https://docs.aws.amazon.com/rds/latest/userguide/CHAP_PostgreSQL.html)
- **AWS Support:** Para problemas técnicos
- **Community:** AWS Forums

## 🎯 Próximos Passos

Após configurar o RDS:

1. ✅ Testar conexão
2. ✅ Configurar N8N
3. ✅ Executar migrações (se houver)
4. ✅ Configurar backups
5. ✅ Monitorar performance
6. ✅ Configurar alertas
