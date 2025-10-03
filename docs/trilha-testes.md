# Trilha de Testes – MrDom SDR

> **Objetivo**: Validar ponta a ponta a jornada do lead — da primeira mensagem até o agendamento e reengajamento — garantindo que mensagens, dados e eventos fluam corretamente entre canais, n8n e CRM.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Execução dos Testes](#execução-dos-testes)
4. [Cenários de Teste](#cenários-de-teste)
5. [Critérios de Aprovação](#critérios-de-aprovação)
6. [Relatórios e Evidências](#relatórios-e-evidências)
7. [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

A trilha de testes do MrDom SDR valida a jornada completa do lead através de múltiplos canais:

- **Canais**: WhatsApp, Site/Widget, Instagram DM, Telegram
- **Fluxos**: Inbound → Qualificação → Pitch → CTA de agenda → Confirmação → Lembretes → Pós‑não‑venda
- **Integrações**: n8n (webhooks), CRM (upsert lead), Calendário, Mensageria, Analytics

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.8+
- Redis rodando localmente
- Docker e Docker Compose (opcional)
- n8n (opcional, para testes de integração)

### Configuração Automática

```bash
# Executar configuração automática
python scripts/setup-test-environment.py
```

### Configuração Manual

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-mock redis
   ```

2. **Configurar Redis**:
   ```bash
   # Iniciar Redis
   redis-server
   
   # Verificar conexão
   redis-cli ping
   ```

3. **Configurar variáveis de ambiente**:
   ```bash
   cp env.example .env
   # Editar .env com suas configurações
   ```

## 🚀 Execução dos Testes

### Execução Completa

```bash
# Executar toda a trilha
python scripts/run-trilha-tests.py

# Executar cenários específicos
python scripts/run-trilha-tests.py --scenarios WPP-01 SITE-01

# Pular testes específicos
python scripts/run-trilha-tests.py --skip-validations --skip-n8n
```

### Execução com Pytest

```bash
# Executar todos os testes
pytest api/tests/test_trilha_completa.py -v

# Executar por marcador
pytest -m "wpp" -v
pytest -m "n8n" -v
pytest -m "validation" -v

# Executar com relatório detalhado
pytest --html=test_results/report.html --self-contained-html
```

### Execução de Cenários Específicos

```bash
# WhatsApp completo
pytest api/tests/test_trilha_completa.py::TestTrilhaCompleta::test_wpp_01_jornada_completa -v

# Validação de email
pytest api/tests/test_trilha_completa.py::TestTrilhaCompleta::test_val_email_invalido -v

# Testes de n8n
pytest api/tests/test_trilha_completa.py::TestTrilhaCompleta::test_n8n_create_lead -v
```

## 📊 Cenários de Teste

### Cenários Principais

| ID | Descrição | Canal | Status |
|----|-----------|-------|--------|
| WPP-01 | Jornada completa WhatsApp | WhatsApp | ✅ |
| WPP-02 | Normalização telefone | WhatsApp | ✅ |
| SITE-01 | Widget do site | Site | ✅ |
| IG-01 | Instagram DM | Instagram | ✅ |
| TG-01 | Telegram completo | Telegram | ✅ |

### Testes de Validação

| ID | Descrição | Validação |
|----|-----------|-----------|
| VAL-E-MAIL-01 | Email inválido | Formato correto |
| VAL-FONE-01 | Telefone sem DDI/DDD | Normalização E.164 |
| VAL-OBRIG-01 | Campos obrigatórios | Bloqueio sem dados |

### Testes de Integração n8n

| ID | Descrição | Endpoint |
|----|-----------|----------|
| N8N-CL-01 | Criação de lead | POST /create_lead |
| N8N-AG-01 | Agendamento | POST /schedule_meeting |
| N8N-LOG-01 | Log de evento | POST /log_event |
| N8N-FU-01 | Follow-up | POST /send_followup |

### Testes de Follow-up

| ID | Descrição | Timing |
|----|-----------|--------|
| CAD-D0 | Reengajamento imediato | Imediato |
| CAD-D2 | Follow-up D+2 | 2 dias |
| CAD-D7 | Follow-up D+7 | 7 dias |
| CAD-D14 | Follow-up D+14 | 14 dias |

## ✅ Critérios de Aprovação (DoD)

### Métricas Obrigatórias

- **Conversão**: ≥80% das jornadas completam até confirmação
- **Dados**: 100% de leads válidos com campos obrigatórios
- **Calendário**: 100% dos eventos criados com link e ICS
- **Rastreamento**: 100% dos eventos logados corretamente
- **Mensageria**: 100% dos templates corretos por etapa
- **Robustez**: Tratamento de erros com mensagem amigável

### Checklist de Validação

- [ ] Placeholders preenchidos ({{nome}}, {{horario1}}, {{horario2}})
- [ ] Origem do canal preservada até CRM
- [ ] Normalização de telefone E.164 (+55...)
- [ ] Validação de email e campos obrigatórios
- [ ] Evento criado no calendário correto
- [ ] Confirmação enviada (WhatsApp + email)
- [ ] Lembretes T-24h e T-2h disparados
- [ ] Cadência pós-não-venda aplicada
- [ ] Eventos logados corretamente

## 📈 Relatórios e Evidências

### Relatórios Automáticos

Os testes geram automaticamente:

- **Relatório JSON**: `test_results/trilha_test_results_YYYYMMDD_HHMMSS.json`
- **Relatório CSV**: `test_results/test_results_YYYYMMDD_HHMMSS.csv`
- **Logs detalhados**: `test_results/logs/pytest.log`
- **Screenshots**: `test_results/screenshots/` (quando aplicável)

### Estrutura do Relatório

```json
{
  "summary": {
    "total_tests": 15,
    "passed_tests": 14,
    "failed_tests": 1,
    "success_rate": 93.33,
    "criteria_met": {
      "conversion_rate": true,
      "data_validation": true,
      "calendar_integration": true,
      "tracking": true,
      "messaging": true,
      "robustness": true
    },
    "overall_status": "PASSED"
  },
  "detailed_results": {
    "scenarios": {
      "WPP-01": {
        "status": "passed",
        "steps": [...],
        "duration": "00:02:15"
      }
    }
  },
  "recommendations": [
    "Taxa de conversão abaixo de 80%. Revisar fluxo de qualificação."
  ]
}
```

### Evidências Coletadas

- **Capturas de tela**: Conversas, payloads, eventos
- **IDs de rastreamento**: message_id, lead_id, event_id
- **Logs de execução**: n8n, Redis, aplicação
- **Métricas de performance**: Tempo de resposta, taxa de erro

## 🔧 Troubleshooting

### Problemas Comuns

#### Redis não conecta
```bash
# Verificar se Redis está rodando
redis-cli ping

# Iniciar Redis
redis-server

# Verificar porta
netstat -an | grep 6379
```

#### Testes falham por timeout
```bash
# Aumentar timeout
pytest --timeout=600

# Executar testes individuais
pytest api/tests/test_trilha_completa.py::TestTrilhaCompleta::test_wpp_01_jornada_completa -v
```

#### Erro de importação
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Instalar dependências
pip install -r requirements.txt
```

#### n8n não responde
```bash
# Verificar se n8n está rodando
curl http://localhost:5678/healthz

# Verificar logs do n8n
docker logs mrdom-n8n
```

### Logs de Debug

```bash
# Executar com logs detalhados
pytest -v -s --log-cli-level=DEBUG

# Verificar logs específicos
tail -f test_results/logs/pytest.log
```

### Limpeza do Ambiente

```bash
# Limpar dados de teste
python scripts/setup-test-environment.py --cleanup

# Limpar Redis
redis-cli FLUSHDB

# Limpar arquivos antigos
find test_results -name "*.json" -mtime +7 -delete
```

## 📚 Documentação Adicional

- [Configuração do Redis](redis-setup.md)
- [Configuração do n8n](n8n-setup.md)
- [Templates de Mensagem](message-templates.md)
- [API de Testes](api-tests.md)

## 🤝 Contribuição

Para adicionar novos cenários de teste:

1. Adicione o cenário em `api/tests/test_data/trilha_test_data.json`
2. Implemente o teste em `api/tests/test_trilha_completa.py`
3. Atualize a documentação
4. Execute os testes para validar

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs em `test_results/logs/`
2. Consulte a seção [Troubleshooting](#troubleshooting)
3. Abra uma issue no repositório
4. Entre em contato com a equipe de desenvolvimento
