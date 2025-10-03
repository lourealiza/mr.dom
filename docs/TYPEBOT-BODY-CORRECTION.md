# 🔧 Correção Imediata - Typebot Body

## ⚡ **Problema Identificado**
Garantir texto não-vazio ao montar o Body da requisição para o webhook n8n.

---

## ✅ **Solução Implementada**

### **Template de Body Seguro**

#### **Configuração no Typebot**
- **Tipo**: Custom body
- **Content-Type**: application/json
- **Authorization**: Bearer dtransforma2026

#### **JSON Template (Pronto para Colar)**
```json
{
  "thread_id": "{{thread_id}}",
  "sender": {
    "id": "{{user_id}}",
    "channel": "typebot"
  },
  "message": {
    "text": "{{ last_user_message || reply_text || \"ping\" }}"
  },
  "context": {
    "lead_nome": "{{ lead_nome || \"\" }}",
    "fluxo_path": "{{ fluxo_path || \"typebot>duvida\" }}",
    "lead_volumetria": "{{ lead_volumetria || \"\" }}",
    "volume_class": "{{ volume_class || \"\" }}"
  }
}
```

---

## 🔍 **Explicação dos Fallbacks**

### **Campo `message.text`**
```javascript
{{ last_user_message || reply_text || "ping" }}
```

#### **Hierarquia de Fallbacks**
1. **`last_user_message`**: Última entrada digitada pelo usuário
2. **`reply_text`**: Resposta anterior (casos especiais)
3. **`"ping"`**: Fallback final - nunca string vazia

### **Outros Campos com Fallbacks**
- **`lead_nome`**: `{{ lead_nome || "" }}`
- **`fluxo_path`**: `{{ fluxo_path || "typebot>duvida" }}`
- **`lead_volumetria`**: `{{ lead_volumetria || "" }}`
- **`volume_class`**: `{{ volume_class || "" }}`

---

## ⚙️ **Configuração no Typebot**

### **Headers**
```http
Content-Type: application/json
Authorization: Bearer dtransforma2026
```

### **Advanced Settings**
- **Execute on client**: ✅ Ativado
- **Timeout**: 10s
- **Custom body**: ✅ Ativado

### **URL do Webhook**
```
https://n8n-inovacao.ar-infra.com.br/webhook/assist/routing
```

---

## 📋 **Checklist de Validação**

### **✅ Campos Obrigatórios**
- [ ] `message.text` nunca vazio (tem "ping" como fallback)
- [ ] `sender.id` preenchido com valor estável
- [ ] `thread_id` presente
- [ ] JSON válido (sem vírgulas sobrando)
- [ ] Chaves `{{ }}` entre aspas quando são strings

### **✅ Headers Corretos**
- [ ] `Content-Type: application/json`
- [ ] `Authorization: Bearer dtransforma2026`

### **✅ Configurações Avançadas**
- [ ] Execute on client ativado
- [ ] Timeout configurado (10s)
- [ ] Custom body ativado

---

## 🧪 **Exemplos de Teste**

### **Cenário 1: Usuário Digitou Algo (Normal)**
```json
{
  "thread_id": "thread_123",
  "sender": {
    "id": "u_789",
    "channel": "typebot"
  },
  "message": {
    "text": "Quero orçamento para 1500 emails"
  },
  "context": {
    "lead_nome": "Luna",
    "fluxo_path": "typebot>duvida",
    "lead_volumetria": "1500",
    "volume_class": "alto"
  }
}
```

### **Cenário 2: Usuário Não Digitou (Fallback)**
```json
{
  "thread_id": "thread_abc",
  "sender": {
    "id": "u_000",
    "channel": "typebot"
  },
  "message": {
    "text": "ping"
  },
  "context": {
    "lead_nome": "",
    "fluxo_path": "typebot>duvida",
    "lead_volumetria": "",
    "volume_class": ""
  }
}
```

### **Cenário 3: Volumetria Detectada**
```json
{
  "thread_id": "thread_456",
  "sender": {
    "id": "u_999",
    "channel": "typebot"
  },
  "message": {
    "text": "Preciso enviar 500 emails para minha empresa"
  },
  "context": {
    "lead_nome": "João",
    "fluxo_path": "typebot>volumetria",
    "lead_volumetria": "500",
    "volume_class": "baixo"
  }
}
```

---

## 🔧 **Validação Manual com cURL**

### **Teste Básico**
```bash
curl -X POST \
  'https://n8n-inovacao.ar-infra.com.br/webhook/assist/routing' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer dtransforma2026' \
  -d '{
    "thread_id":"thread_test_cli",
    "sender":{"id":"cli_test","channel":"typebot"},
    "message":{"text":"ping"},
    "context":{"lead_nome":"Luna","fluxo_path":"typebot>duvida"}
  }'
```

### **Resposta Esperada**
```json
{
  "thread_id": "thread_test_cli",
  "reply_text": "Olá Luna! Como posso ajudar você hoje?",
  "next_step": "coletar_duvida",
  "fluxo_path": "typebot>duvida",
  "status": "success"
}
```

---

## 🎯 **Mapeamento de Resposta**

### **Variáveis do Typebot para Resposta**
```javascript
// Mapear retornos do n8n para variáveis do Typebot
response.reply_text    → {{response.reply_text}}
response.next_step     → {{response.next_step}}
response.calendar_url  → {{response.calendar_url}}
response.fluxo_path    → {{response.fluxo_path}}
response.status        → {{response.status}}
```

### **Exemplo de Resposta Completa**
```json
{
  "thread_id": "thread_123",
  "reply_text": "Para esse volume de 1500 emails, recomendo uma demonstração personalizada. Posso agendar uma reunião com nossos especialistas?",
  "next_step": "agendar",
  "calendar_url": "https://outlook.office.com/book/EspecialistasAROnline@realizati.com/",
  "fluxo_path": "agendamento",
  "volume_class": "alto",
  "status": "success"
}
```

---

## 🔄 **Correção Alternativa (Backend)**

### **Se Preferir Blindar no n8n/FastAPI**
```javascript
// Pseudo (n8n Code node ou FastAPI):
const text = (req.body?.message?.text || "").trim();
req.body.message.text = text.length ? text : "ping";

// Validação adicional
if (!req.body.sender?.id) {
  req.body.sender.id = "unknown_user";
}

if (!req.body.thread_id) {
  req.body.thread_id = `thread_${Date.now()}`;
}
```

### **Validação no FastAPI**
```python
from pydantic import BaseModel, validator

class WebhookRequest(BaseModel):
    thread_id: str
    sender: dict
    message: dict
    context: dict
    
    @validator('message')
    def validate_message_text(cls, v):
        text = v.get('text', '').strip()
        if not text:
            v['text'] = 'ping'
        return v
    
    @validator('sender')
    def validate_sender_id(cls, v):
        if not v.get('id'):
            v['id'] = 'unknown_user'
        return v
```

---

## 📝 **Dicas Adicionais**

### **Processamento do Nome**
- **Antes**: "O primeiro nome extraído é Luna"
- **Depois**: "Luna"
- **Implementação**: Use pré-processamento no Typebot para manter apenas o primeiro nome

### **Geração de thread_id**
```javascript
// Se não houver thread_id, gerar um
{{ thread_id || `thread_${Date.now()}` }}
```

### **Validação de JSON**
- Sempre teste o JSON antes de usar
- Use ferramentas online para validar sintaxe
- Verifique se todas as chaves estão entre aspas

---

## 🚨 **Problemas Comuns e Soluções**

### **Problema: message.text vazio**
**Solução**: Usar fallback `{{ last_user_message || reply_text || "ping" }}`

### **Problema: sender.id vazio**
**Solução**: Usar `{{user_id}}` ou `{{phone}}` como identificador estável

### **Problema: JSON inválido**
**Solução**: Verificar vírgulas e aspas, usar template fornecido

### **Problema: Timeout**
**Solução**: Verificar se n8n está respondendo, aumentar timeout se necessário

---

## ✅ **Status da Correção**

**✅ TEMPLATE PRONTO PARA USO**

- **Body JSON**: Template seguro com fallbacks
- **Headers**: Configuração correta
- **Validação**: Checklist completo
- **Testes**: Exemplos funcionais
- **Backup**: Correção alternativa no backend

**A correção está implementada e pronta para resolver o problema de texto vazio no webhook! 🎯**
