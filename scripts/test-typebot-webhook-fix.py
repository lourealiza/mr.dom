#!/usr/bin/env python3
"""
Teste da Correção do Webhook Typebot
Valida o template de body seguro com fallbacks
"""
import requests
import json
from datetime import datetime

class TypebotWebhookTester:
    """Testador do webhook Typebot com correções"""
    
    def __init__(self):
        self.webhook_url = "https://n8n-inovacao.ar-infra.com.br/webhook/assist/routing"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer dtransforma2026"
        }
    
    def test_scenario_1_normal_user_input(self):
        """Teste 1: Usuário digitou algo (caminho normal)"""
        print("\n" + "="*60)
        print("TESTE 1: USUÁRIO DIGITOU ALGO (CAMINHO NORMAL)")
        print("="*60)
        
        payload = {
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
        
        return self._send_request("Cenário Normal", payload)
    
    def test_scenario_2_fallback_ping(self):
        """Teste 2: Usuário não digitou (fallback aciona)"""
        print("\n" + "="*60)
        print("TESTE 2: USUÁRIO NÃO DIGITOU (FALLBACK PING)")
        print("="*60)
        
        payload = {
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
        
        return self._send_request("Fallback Ping", payload)
    
    def test_scenario_3_volumetria_detected(self):
        """Teste 3: Volumetria detectada"""
        print("\n" + "="*60)
        print("TESTE 3: VOLUMETRIA DETECTADA")
        print("="*60)
        
        payload = {
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
        
        return self._send_request("Volumetria Detectada", payload)
    
    def test_scenario_4_empty_text_fallback(self):
        """Teste 4: Texto vazio com fallback"""
        print("\n" + "="*60)
        print("TESTE 4: TEXTO VAZIO COM FALLBACK")
        print("="*60)
        
        payload = {
            "thread_id": "thread_empty",
            "sender": {
                "id": "u_empty",
                "channel": "typebot"
            },
            "message": {
                "text": ""  # Texto vazio para testar fallback
            },
            "context": {
                "lead_nome": "Maria",
                "fluxo_path": "typebot>duvida",
                "lead_volumetria": "",
                "volume_class": ""
            }
        }
        
        return self._send_request("Texto Vazio", payload)
    
    def test_scenario_5_missing_fields(self):
        """Teste 5: Campos ausentes"""
        print("\n" + "="*60)
        print("TESTE 5: CAMPOS AUSENTES")
        print("="*60)
        
        payload = {
            "thread_id": "thread_missing",
            "sender": {
                "id": "u_missing",
                "channel": "typebot"
            },
            "message": {
                "text": "Teste com campos ausentes"
            },
            "context": {
                "lead_nome": "",
                "fluxo_path": "",
                "lead_volumetria": "",
                "volume_class": ""
            }
        }
        
        return self._send_request("Campos Ausentes", payload)
    
    def _send_request(self, test_name, payload):
        """Enviar requisição e processar resposta"""
        print(f"Enviando: {test_name}")
        print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            print(f"\nStatus Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print("Resposta JSON:")
                    print(json.dumps(response_data, indent=2, ensure_ascii=False))
                    
                    # Validar campos obrigatórios na resposta
                    required_fields = ['thread_id', 'reply_text']
                    missing_fields = [field for field in required_fields if field not in response_data]
                    
                    if missing_fields:
                        print(f"⚠️ Campos obrigatórios ausentes: {missing_fields}")
                        return False
                    else:
                        print("✅ Resposta válida com todos os campos obrigatórios")
                        return True
                        
                except json.JSONDecodeError:
                    print(f"Resposta (texto): {response.text}")
                    print("⚠️ Resposta não é JSON válido")
                    return False
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"Resposta: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Timeout na requisição")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return False
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("TESTE DA CORREÇÃO DO WEBHOOK TYPEBOT")
        print("="*60)
        print(f"Webhook URL: {self.webhook_url}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            ("Usuário Digitou Algo", self.test_scenario_1_normal_user_input),
            ("Fallback Ping", self.test_scenario_2_fallback_ping),
            ("Volumetria Detectada", self.test_scenario_3_volumetria_detected),
            ("Texto Vazio", self.test_scenario_4_empty_text_fallback),
            ("Campos Ausentes", self.test_scenario_5_missing_fields)
        ]
        
        results = []
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                if result:
                    passed += 1
                    print(f"✅ {test_name}: PASSOU")
                else:
                    print(f"❌ {test_name}: FALHOU")
            except Exception as e:
                results.append((test_name, False))
                print(f"❌ {test_name}: ERRO - {e}")
        
        # Resumo final
        print("\n" + "="*60)
        print("RESUMO DOS TESTES")
        print("="*60)
        print(f"Total de testes: {total}")
        print(f"Testes aprovados: {passed}")
        print(f"Testes falharam: {total - passed}")
        print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Correção do webhook funcionando perfeitamente!")
        elif passed >= total * 0.8:
            print("\n👍 MAIORIA DOS TESTES PASSOU!")
            print("⚠️ Verifique os testes que falharam")
        else:
            print("\n⚠️ MUITOS TESTES FALHARAM!")
            print("🔧 Verifique configurações e conectividade")
        
        return results
    
    def generate_curl_commands(self):
        """Gerar comandos cURL para teste manual"""
        print("\n" + "="*60)
        print("COMANDOS CURL PARA TESTE MANUAL")
        print("="*60)
        
        scenarios = [
            {
                "name": "Teste Básico",
                "payload": {
                    "thread_id": "thread_test_cli",
                    "sender": {"id": "cli_test", "channel": "typebot"},
                    "message": {"text": "ping"},
                    "context": {"lead_nome": "Luna", "fluxo_path": "typebot>duvida"}
                }
            },
            {
                "name": "Teste Volumetria",
                "payload": {
                    "thread_id": "thread_volumetria",
                    "sender": {"id": "cli_vol", "channel": "typebot"},
                    "message": {"text": "Quero enviar 1500 emails"},
                    "context": {
                        "lead_nome": "João",
                        "fluxo_path": "typebot>volumetria",
                        "lead_volumetria": "1500",
                        "volume_class": "alto"
                    }
                }
            }
        ]
        
        for scenario in scenarios:
            print(f"\n{scenario['name']}:")
            print("```bash")
            
            curl_command = f"""curl -X POST \\
  '{self.webhook_url}' \\
  -H 'Content-Type: application/json' \\
  -H 'Authorization: Bearer dtransforma2026' \\
  -d '{json.dumps(scenario['payload'], separators=(',', ':'))}'"""
            
            print(curl_command)
            print("```")

def main():
    """Função principal"""
    tester = TypebotWebhookTester()
    
    # Executar testes
    results = tester.run_all_tests()
    
    # Gerar comandos cURL
    tester.generate_curl_commands()
    
    # Salvar relatório
    report = {
        "timestamp": datetime.now().isoformat(),
        "webhook_url": tester.webhook_url,
        "test_results": results,
        "total_tests": len(results),
        "passed_tests": sum(1 for _, result in results if result),
        "success_rate": (sum(1 for _, result in results if result) / len(results)) * 100
    }
    
    filename = f"typebot_webhook_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório salvo: {filename}")

if __name__ == "__main__":
    main()
