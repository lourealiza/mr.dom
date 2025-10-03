# MrDom SDR AgentOS - Enterprise Platform

🚀 **Sistema enterprise completo para Sales Development Representatives (SDR)** 

Plataforma de automação inteligente para qualificação e prospecção de leads usando AgentOS com Model Context Protocol (MCP), arquitetura enterprise Kubernetes-ready e monitoramento avançado.

## ✨ Funcionalidades Enterprise

### 🤖 **AgentOS Integration**
- **Agentes especializados**: Lead Qualification, Sales SDR, Customer Success
- **AWS Bedrock**: Models Cloude 3 e Amazon Titan para máxima performance
- **Model Context Protocol**: Comunicação padronizada entre agentes
- **Escalabilidade**: Multi-agent architecture com load balancing

### 🔄 **Automação Inteligente**
- **N8N Workflows**: Integração completa com workflows automatizados
- **Chatwoot Integration**: Webhooks e respostas automáticas inteligentes
- **Qualificação BANT**: Análise automatizada (Budget, Authority, Need, Timeline)
- **Escalação inteligente**: Transfer automática para humanos quando necessário

### 📊 **Monitoramento Enterprise**
- **40+ Dashboards Grafana**: Métricas especializadas por categoria
- **Prometheus Metrics**: Coleta avançada de métricas
- **Business Intelligence**: Dashboards de vendas, performance, qualidade
- **Security Monitoring**: Compliance e segurança automatizada

### 🏗️ **Infraestrutura Ready**
- **Kubernetes**: Deploy completo (Pod, Service, Ingress, ConfigMap)
- **Docker**: Containerização otimizada
- **CI/CD**: GitHub Actions automatizado
- **Ambientes**: Dev/Staging/Production configurados

## 📁 Arquitetura do Projeto

```
mrdom-agentos-mcp/
├─ src/mrdom/                     # Core AgentOS Library
│  ├─ agents/                     # AgentOS Agents
│  │  └─ bedrock_agent.py         # AWS Bedrock configured agents
│  └─ api/routes/                 # FastAPI Routes
│     ├─ agents.py                # AgentOS endpoints (/api/v1/agents/*)
│     ├─ health.py                # Health/readiness checks
│     └─ webhooks.py              # Webhook handlers
├─ k8s/                           # Kubernetes Configurations
│  ├─ deployment.yaml            # Main deployment
│  ├─ service.yaml                # Kubernetes service
│  ├─ ingress.yaml                # External access
│  ├─ secrets.yaml                # Secrets management
│  ├─ hpa.yaml                    # Horizontal Pod Autoscaler
│  └─ servicemonitor.yaml         # Prometheus monitoring
├─ monitoring/grafana/dashboards/ # Grafana Dashboards (40+)
│  ├─ business-metrics-dashboard.json
│  ├─ security-metrics-dashboard.json
│  ├─ performance-metrics-dashboard.json
│  ├─ *-excellence-dashboard.json # Excellence frameworks
│  └─ dashboard-provider.yml     # Grafana provisioning
├─ monitoring/prometheus.yml      # Prometheus configuration
├─ .github/workflows/ci.yml       # CI/CD pipeline
├─ Dockerfile                     # Container image
├─ docker-compose.yml             # Multi-service orchestration
├─ pyproject.toml                 # Modern Python packaging
├─ requirements.txt               # Dependencies (AgentOS + AWS Bedrock)
└─ README.md                      # This documentation
```

## 🚀 Quick Start

### 1. **Docker (Recommended)**
```bash
# Clone and start
git clone https://github.com/DOM-360/mrdom-agentos-mcp.git
cd mrdom-agentos-mcp
cp env.example .env

# Configure your AWS Bedrock credentials
# Edit .env with your credentials

# Start with Docker Compose
docker-compose up -d --build
```

### 2. **Kubernetes Deployment**
```bash
# Configure your cluster
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment
kubectl get pods -n mrdom-agentos
```

### 3. **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your settings

# Run AgentOS API
python main.py --reload
```

## ⚙️ Configuração Enterprise

### **Core Settings**
```bash
# AWS Bedrock Models
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# AgentOS Configuration
AGENT_MAX_TOKENS=4096
AGENT_TEMPERATURE=0.7
AGENTOS_ENABLED=true

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:pass@localhost/mrdom_agentos

# Monitoring
PROMETHEUS_EXPORT_PORT=9090
GRAFANA_ENABLED=true
```

### **Integration Settings**
```bash
# Chatwoot
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_ACCESS_TOKEN=your_token
CHATWOOT_ACCOUNT_ID=your_account_id

# N8N Workflows
N8N_BASE_URL=https://your-n8n-instance.com
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/mrdom
```

## 🔗 API Endpoints

### **AgentOS Agents**
```bash
GET    /api/v1/agents/status       # AgentOS status
GET    /api/v1/agents/list         # Available agents
POST   /api/v1/agents/process      # Process with specific agent
POST   /api/v1/agents/process-best # Auto-select best agent
POST   /api/v1/agents/suggest      # Suggest best agent
```

### **Health & Monitoring**
```bash
GET    /health                     # Health check
GET    /metrics                    # Prometheus metrics
GET    /api/v1/webhooks/chatwoot   # Chatwoot webhook handler
```

## 📊 **Monitoring Dashboards**

### **Core Metrics**
- **Business Metrics**: Leads, conversions, revenue
- **Performance Metrics**: Response time, throughput
- **Security Metrics**: Authentication, access control
- **System Metrics**: CPU, memory, disk usage

### **Excellence Dashboards**
- **Leadership Excellence**: Management KPIs
- **Process Excellence**: Operational efficiency
- **Innovation Excellence**: R&D metrics
- **Sustainability Excellence**: Environmental impact

## 🧪 Testing & Quality

```bash
# Run tests
pytest tests/

# Coverage report
pytest --cov=src/

# Load testing
pytest tests/load/

# Integration tests
pytest tests/integration/
```

## 🚀 CI/CD Pipeline

O projeto inclui pipeline GitHub Actions completo:

- **Automated Testing**: pytest + coverage
- **Security Scanning**: SAST and dependency scanning  
- **Container Build**: Multi-stage Docker optimization
- **Kubernetes Deploy**: Automated cluster deployment
- **Monitoring**: Prometheus metrics collection

## 📈 **Production Deployment**

### **Kubernetes Production**
```bash
# Production namespace
kubectl apply -f k8s/namespace.yaml

# Secrets (replace with actual values)
kubectl create secret generic mrdom-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=bedrock-access-key=$AWS_ACCESS_KEY_ID \
  --from-literal=bedrock-secret-key=$AWS_SECRET_ACCESS_KEY

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n mrdom-agentos
kubectl logs -f deployment/mrdom-agentos -n mrdom-agentos
```

## 🔒 **Security & Compliance**

- **AWS IAM**: Role-based access control
- **Encryption**: TLS/SSL for all communication
- **Secrets**: Kubernetes Secrets management
- **Monitoring**: Security metrics dashboards
- **Compliance**: Audit trails and logging

## 📚 **Documentation**

- **API Documentation**: Available at `/docs` (Swagger UI)
- **AgentOS Guide**: `docs/agentos-integration.md`
- **AWS Bedrock Setup**: `docs/bedrock-agentos-integration.md`
- **Deployment Guide**: `docs/deployment.md`
- **Grafana Dashboards**: `monitoring/grafana/dashboards/README.md`

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 **Support**

- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Documentation**: Check `/docs` directory

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🚀 **MrDom SDR AgentOS Enterprise** - De MVP a plataforma enterprise em uma solução completa!