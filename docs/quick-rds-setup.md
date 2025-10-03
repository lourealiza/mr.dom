# 🚀 Criação Rápida AWS RDS PostgreSQL

## Passo a Passo Simplificado

### 1. **Acesse o AWS Console**
- Vá para: https://console.aws.amazon.com/
- Faça login na sua conta AWS

### 2. **Navegue para RDS**
- No menu de serviços, procure por **"RDS"**
- Clique em **"Create database"**

### 3. **Configurações Básicas**
```
Engine type: PostgreSQL
Version: PostgreSQL 15.x
Templates: Dev/Test (mais barato)
```

### 4. **Identificação**
```
DB instance identifier: mrdom-sdr-postgres
Master username: app
Master password: mrdom2024
```

### 5. **Configuração da Instância**
```
DB instance class: db.t3.micro (Free tier)
Storage: 20 GB
```

### 6. **Conectividade**
```
VPC: Default VPC
Public access: Yes
VPC security groups: Create new
Security group name: mrdom-postgres-sg
```

### 7. **Configuração Adicional**
```
Initial database name: app
Backup retention: 7 days
```

### 8. **Criar Banco**
- Clique em **"Create database"**
- Aguarde 5-10 minutos para criação

### 9. **Obter Informações de Conexão**
Após criação:
1. Vá para **RDS** → **Databases**
2. Clique no seu banco `mrdom-sdr-postgres`
3. Na aba **"Connectivity & security"**:
   - **Endpoint:** `mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com`
   - **Port:** `5432`

### 10. **Configurar Security Group**
1. Vá para **EC2** → **Security Groups**
2. Encontre `mrdom-postgres-sg`
3. **Edit inbound rules**
4. Adicione:
```
Type: PostgreSQL
Protocol: TCP
Port: 5432
Source: 0.0.0.0/0
```

## 💰 **Custos Estimados**
- **Free Tier:** Gratuito por 12 meses
- **Dev/Test:** ~$15-20/mês
- **Production:** ~$30-40/mês

## ⚡ **Criação Rápida via AWS CLI**

Se você tem AWS CLI configurado:

```bash
aws rds create-db-instance \
    --db-instance-identifier mrdom-sdr-postgres \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username app \
    --master-user-password mrdom2024 \
    --allocated-storage 20 \
    --db-name app \
    --publicly-accessible \
    --storage-type gp3
```

## 🔧 **Verificar Status**

```bash
aws rds describe-db-instances --db-instance-identifier mrdom-sdr-postgres
```

## 📋 **Informações que Você Precisará**

Após criar o RDS, você terá:

```
Host: mrdom-sdr-postgres.xxxxx.us-east-1.rds.amazonaws.com
Port: 5432
Database: app
Username: app
Password: mrdom2024
```

## 🎯 **Próximos Passos**

1. ✅ Criar RDS
2. ✅ Configurar Security Group
3. ✅ Obter endpoint
4. ✅ Executar: `scripts\configure-aws-rds.bat`
5. ✅ Testar conexão
6. ✅ Configurar N8N
