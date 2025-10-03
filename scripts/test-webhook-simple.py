#!/usr/bin/env python3
"""
Teste Simples do Webhook Typebot
Valida a correção do body com fallbacks
"""
import requests
import json
from datetime import datetime

def test_webhook_fix():
    """Teste da correção do webhook"""
    print("TESTE DA CORRECAO DO WEBHOOK TYPEBOT")
    print("=" * 50)
    
    webhook_url = "https://n8n-inovacao.ar-infra.com.br/webhook/assist/routing"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer dtransforma2026"
    }
    
    # Teste 1: Cenário normal
    print("\n1. Teste: Cenário Normal")
    payload1 = {
        "thread_id": "thread_123",
        "sender": {"id": "u_789", "channel": "typebot"},
        "message": {"text": "Quero orcamento para 1500 emails"},
        "context": {
            "lead_nome": "Luna",
            "fluxo_path": "typebot>duvida",
            "lead_volumetria": "1500",
            "volume_class": "alto"
        }
    }
    
    try:
        response1 = requests.post(webhook_url, json=payload1, headers=headers, timeout=10)
        print(f"   Status: {response1.status_code}")
        if response1.status_code == 200:
            print("   OK: Resposta recebida")
        else:
            print(f"   ERRO: {response1.text}")
    except Exception as e:
        print(f"   ERRO: {e}")
    
    # Teste 2: Fallback ping
    print("\n2. Teste: Fallback Ping")
    payload2 = {
        "thread_id": "thread_abc",
        "sender": {"id": "u_000", "channel": "typebot"},
        "message": {"text": "ping"},
        "context": {
            "lead_nome": "",
            "fluxo_path": "typebot>duvida",
            "lead_volumetria": "",
            "volume_class": ""
        }
    }
    
    try:
        response2 = requests.post(webhook_url, json=payload2, headers=headers, timeout=10)
        print(f"   Status: {response2.status_code}")
        if response2.status_code == 200:
            print("   OK: Resposta recebida")
        else:
            print(f"   ERRO: {response2.text}")
    except Exception as e:
        print(f"   ERRO: {e}")
    
    # Teste 3: Volumetria baixa
    print("\n3. Teste: Volumetria Baixa")
    payload3 = {
        "thread_id": "thread_456",
        "sender": {"id": "u_999", "channel": "typebot"},
        "message": {"text": "Preciso enviar 500 emails"},
        "context": {
            "lead_nome": "Joao",
            "fluxo_path": "typebot>volumetria",
            "lead_volumetria": "500",
            "volume_class": "baixo"
        }
    }
    
    try:
        response3 = requests.post(webhook_url, json=payload3, headers=headers, timeout=10)
        print(f"   Status: {response3.status_code}")
        if response3.status_code == 200:
            print("   OK: Resposta recebida")
        else:
            print(f"   ERRO: {response3.text}")
    except Exception as e:
        print(f"   ERRO: {e}")
    
    print("\n" + "=" * 50)
    print("TESTE CONCLUIDO")
    print("=" * 50)
    
    # Comandos cURL
    print("\nCOMANDOS CURL PARA TESTE MANUAL:")
    print("-" * 30)
    
    curl_basic = """curl -X POST \\
  'https://n8n-inovacao.ar-infra.com.br/webhook/assist/routing' \\
  -H 'Content-Type: application/json' \\
  -H 'Authorization: Bearer dtransforma2026' \\
  -d '{
    "thread_id":"thread_test_cli",
    "sender":{"id":"cli_test","channel":"typebot"},
    "message":{"text":"ping"},
    "context":{"lead_nome":"Luna","fluxo_path":"typebot>duvida"}
  }'"""
    
    print("Teste Basico:")
    print(curl_basic)
    
    curl_volumetria = """curl -X POST \\
  'https://n8n-inovacao.ar-infra.com.br/webhook/assist/routing' \\
  -H 'Content-Type: application/json' \\
  -H 'Authorization: Bearer dtransforma2026' \\
  -d '{
    "thread_id":"thread_volumetria",
    "sender":{"id":"cli_vol","channel":"typebot"},
    "message":{"text":"Quero enviar 1500 emails"},
    "context":{
      "lead_nome":"Joao",
      "fluxo_path":"typebot>volumetria",
      "lead_volumetria":"1500",
      "volume_class":"alto"
    }
  }'"""
    
    print("\nTeste Volumetria:")
    print(curl_volumetria)
    
    print("\nTEMPLATE PARA TYPEBOT:")
    print("-" * 30)
    template = """{
  "thread_id": "{{thread_id}}",
  "sender": {
    "id": "{{user_id}}",
    "channel": "typebot"
  },
  "message": {
    "text": "{{ last_user_message || reply_text || "ping" }}"
  },
  "context": {
    "lead_nome": "{{ lead_nome || "" }}",
    "fluxo_path": "{{ fluxo_path || "typebot>duvida" }}",
    "lead_volumetria": "{{ lead_volumetria || "" }}",
    "volume_class": "{{ volume_class || "" }}"
  }
}"""
    
    print(template)
    
    print("\nCONFIGURACOES:")
    print("-" * 30)
    print("Headers:")
    print("  Content-Type: application/json")
    print("  Authorization: Bearer dtransforma2026")
    print("\nAdvanced:")
    print("  Execute on client: Ativado")
    print("  Timeout: 10s")
    print("  Custom body: Ativado")

if __name__ == "__main__":
    test_webhook_fix()
