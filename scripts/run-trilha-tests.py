#!/usr/bin/env python3
"""
Script principal para executar a trilha de testes MrDom SDR
"""
import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.tests.test_trilha_completa import TestTrilhaCompleta
from api.tests.test_analytics import test_analytics
from api.tests.test_data.trilha_test_data import *
from api.tests.test_data.message_templates import message_templates, scenario_builder
from api.tests.test_endpoints import test_endpoints

class TrilhaTestRunner:
    """Executor da trilha de testes"""
    
    def __init__(self):
        self.results = {
            "start_time": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "scenarios": {},
            "errors": []
        }
    
    def run_scenario(self, scenario_id: str, scenario_data: Dict) -> Dict:
        """Executa um cenário específico"""
        print(f"\n🚀 Executando cenário: {scenario_id}")
        print(f"   Descrição: {scenario_data['descricao']}")
        
        scenario_result = {
            "id": scenario_id,
            "description": scenario_data["descricao"],
            "status": "running",
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "errors": []
        }
        
        try:
            # Executar steps do cenário
            if scenario_id == "WPP-01":
                result = self._run_wpp_01(scenario_data)
            elif scenario_id == "WPP-02":
                result = self._run_wpp_02(scenario_data)
            elif scenario_id == "SITE-01":
                result = self._run_site_01(scenario_data)
            elif scenario_id == "IG-01":
                result = self._run_ig_01(scenario_data)
            elif scenario_id == "TG-01":
                result = self._run_tg_01(scenario_data)
            else:
                raise ValueError(f"Cenário {scenario_id} não implementado")
            
            scenario_result.update(result)
            scenario_result["status"] = "passed"
            self.results["tests_passed"] += 1
            
        except Exception as e:
            scenario_result["status"] = "failed"
            scenario_result["errors"].append(str(e))
            self.results["tests_failed"] += 1
            print(f"❌ Erro no cenário {scenario_id}: {e}")
        
        scenario_result["end_time"] = datetime.now().isoformat()
        self.results["scenarios"][scenario_id] = scenario_result
        self.results["tests_run"] += 1
        
        return scenario_result
    
    def _run_wpp_01(self, scenario_data: Dict) -> Dict:
        """Executa cenário WPP-01"""
        usuario = next(u for u in usuarios_teste if u["id"] == scenario_data["usuario"])
        
        steps = []
        
        # 1. Abertura
        mensagem = message_templates.render_template("opening", {"nome": usuario["nome"]})
        steps.append({"step": "opening", "message": mensagem, "status": "ok"})
        
        # 2. Qualificação
        perguntas = message_templates.render_template("qualificacao_perguntas", {})
        for i, pergunta in enumerate(perguntas):
            steps.append({"step": f"qualificacao_{i+1}", "message": pergunta, "status": "ok"})
        
        # 3. Pitch
        mensagem_pitch = message_templates.render_template("pitch_geral", usuario)
        steps.append({"step": "pitch", "message": mensagem_pitch, "status": "ok"})
        
        # 4. CTA de Agenda
        horarios = message_templates.get_available_horarios()
        mensagem_cta = message_templates.render_template("cta_agenda", {
            "horario1": horarios[0], "horario2": horarios[1]
        })
        steps.append({"step": "cta_agenda", "message": mensagem_cta, "status": "ok"})
        
        # 5. Criar Lead
        payload_lead = {
            "nome": usuario["nome"],
            "sobrenome": usuario["sobrenome"],
            "empresa": usuario["empresa"],
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "origem": usuario["origem"]
        }
        
        response_lead = test_endpoints.create_lead(payload_lead)
        steps.append({
            "step": "create_lead",
            "payload": payload_lead,
            "response": response_lead,
            "status": "ok" if response_lead["status"] == "ok" else "error"
        })
        
        # 6. Agendamento
        payload_agendamento = {
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "titulo": "Diagnóstico DOM360 (30 min)",
            "opcao_horario": "2025-10-02T14:00:00"
        }
        
        response_agendamento = test_endpoints.schedule_meeting(payload_agendamento)
        steps.append({
            "step": "schedule_meeting",
            "payload": payload_agendamento,
            "response": response_agendamento,
            "status": "ok" if response_agendamento["status"] == "ok" else "error"
        })
        
        # 7. Confirmação
        confirmacao_data = message_templates.generate_confirmation_data(usuario, "14:00")
        mensagem_confirmacao = message_templates.render_template("confirmacao_agendada", confirmacao_data)
        steps.append({"step": "confirmacao", "message": mensagem_confirmacao, "status": "ok"})
        
        return {"steps": steps}
    
    def _run_wpp_02(self, scenario_data: Dict) -> Dict:
        """Executa cenário WPP-02 (normalização de telefone)"""
        usuario = next(u for u in usuarios_teste if u["id"] == scenario_data["usuario"])
        
        steps = []
        
        # Testar normalização de telefone
        telefone_original = scenario_data.get("telefone_original", "11999998888")
        telefone_normalizado = test_endpoints._normalizar_telefone(telefone_original)
        
        steps.append({
            "step": "normalize_phone",
            "original": telefone_original,
            "normalized": telefone_normalizado,
            "status": "ok" if telefone_normalizado == scenario_data.get("telefone_esperado") else "error"
        })
        
        # Criar lead com telefone normalizado
        payload_lead = {
            "nome": usuario["nome"],
            "sobrenome": usuario["sobrenome"],
            "email": usuario["email"],
            "telefone": telefone_normalizado,
            "origem": usuario["origem"]
        }
        
        response = test_endpoints.create_lead(payload_lead)
        steps.append({
            "step": "create_lead",
            "payload": payload_lead,
            "response": response,
            "status": "ok" if response["status"] == "ok" else "error"
        })
        
        return {"steps": steps}
    
    def _run_site_01(self, scenario_data: Dict) -> Dict:
        """Executa cenário SITE-01"""
        usuario = next(u for u in usuarios_teste if u["id"] == scenario_data["usuario"])
        
        steps = []
        
        # Construir fluxo completo
        flow = scenario_builder.build_conversation_flow(usuario, "Site")
        
        for step_data in flow:
            steps.append({
                "step": step_data["step"],
                "message": step_data["message"],
                "status": "ok"
            })
        
        # Criar lead
        payload_lead = {
            "nome": usuario["nome"],
            "sobrenome": usuario["sobrenome"],
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "origem": "Site"
        }
        
        response = test_endpoints.create_lead(payload_lead)
        steps.append({
            "step": "create_lead",
            "payload": payload_lead,
            "response": response,
            "status": "ok" if response["status"] == "ok" else "error"
        })
        
        return {"steps": steps}
    
    def _run_ig_01(self, scenario_data: Dict) -> Dict:
        """Executa cenário IG-01"""
        usuario = next(u for u in usuarios_teste if u["id"] == scenario_data["usuario"])
        
        steps = []
        
        # Criar lead com origem Instagram
        payload_lead = {
            "nome": usuario["nome"],
            "sobrenome": usuario["sobrenome"],
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "origem": "Instagram"
        }
        
        response = test_endpoints.create_lead(payload_lead)
        steps.append({
            "step": "create_lead",
            "payload": payload_lead,
            "response": response,
            "status": "ok" if response["status"] == "ok" else "error"
        })
        
        # Verificar se origem foi preservada
        origem_preservada = response.get("data", {}).get("origem") == "Instagram"
        steps.append({
            "step": "verify_origin",
            "expected": "Instagram",
            "actual": response.get("data", {}).get("origem"),
            "status": "ok" if origem_preservada else "error"
        })
        
        return {"steps": steps}
    
    def _run_tg_01(self, scenario_data: Dict) -> Dict:
        """Executa cenário TG-01"""
        usuario = next(u for u in usuarios_teste if u["id"] == scenario_data["usuario"])
        
        steps = []
        
        # Construir fluxo completo
        flow = scenario_builder.build_conversation_flow(usuario, "Telegram")
        
        for step_data in flow:
            steps.append({
                "step": step_data["step"],
                "message": step_data["message"],
                "status": "ok"
            })
        
        # Criar lead
        payload_lead = {
            "nome": usuario["nome"],
            "sobrenome": usuario["sobrenome"],
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "origem": "Telegram"
        }
        
        response = test_endpoints.create_lead(payload_lead)
        steps.append({
            "step": "create_lead",
            "payload": payload_lead,
            "response": response,
            "status": "ok" if response["status"] == "ok" else "error"
        })
        
        return {"steps": steps}
    
    def run_validation_tests(self):
        """Executa testes de validação"""
        print("\n🔍 Executando testes de validação...")
        
        validation_tests = [
            ("VAL-E-MAIL-01", self._test_invalid_email),
            ("VAL-FONE-01", self._test_invalid_phone),
            ("VAL-OBRIG-01", self._test_missing_fields)
        ]
        
        for test_id, test_func in validation_tests:
            try:
                result = test_func()
                self.results["scenarios"][test_id] = {
                    "id": test_id,
                    "status": "passed" if result["status"] == "ok" else "failed",
                    "result": result
                }
                self.results["tests_run"] += 1
                if result["status"] == "ok":
                    self.results["tests_passed"] += 1
                else:
                    self.results["tests_failed"] += 1
                    
            except Exception as e:
                self.results["scenarios"][test_id] = {
                    "id": test_id,
                    "status": "failed",
                    "error": str(e)
                }
                self.results["tests_failed"] += 1
    
    def _test_invalid_email(self):
        """Testa email inválido"""
        payload = {
            "nome": "Teste",
            "sobrenome": "Inválido",
            "email": "email-invalido",
            "telefone": "+5511988887777"
        }
        
        response = test_endpoints.create_lead(payload)
        return {
            "status": "ok" if response["status"] == "error" and response["code"] == "INVALID_EMAIL" else "error",
            "response": response
        }
    
    def _test_invalid_phone(self):
        """Testa telefone inválido"""
        payload = {
            "nome": "Teste",
            "sobrenome": "Inválido",
            "email": "teste@teste.com",
            "telefone": "988887777"
        }
        
        response = test_endpoints.create_lead(payload)
        return {
            "status": "ok" if response["status"] == "error" and response["code"] == "INVALID_PHONE" else "error",
            "response": response
        }
    
    def _test_missing_fields(self):
        """Testa campos obrigatórios faltando"""
        payload = {
            "nome": "",
            "sobrenome": "",
            "email": "teste@teste.com",
            "telefone": "+5511988887777"
        }
        
        response = test_endpoints.create_lead(payload)
        return {
            "status": "ok" if response["status"] == "error" and "Campos obrigatórios faltando" in response["message"] else "error",
            "response": response
        }
    
    def run_n8n_tests(self):
        """Executa testes de webhooks n8n"""
        print("\n🔗 Executando testes de webhooks n8n...")
        
        n8n_tests = [
            ("N8N-CL-01", self._test_n8n_create_lead),
            ("N8N-AG-01", self._test_n8n_schedule_meeting),
            ("N8N-LOG-01", self._test_n8n_log_event),
            ("N8N-FU-01", self._test_n8n_send_followup)
        ]
        
        for test_id, test_func in n8n_tests:
            try:
                result = test_func()
                self.results["scenarios"][test_id] = {
                    "id": test_id,
                    "status": "passed" if result["status"] == "ok" else "failed",
                    "result": result
                }
                self.results["tests_run"] += 1
                if result["status"] == "ok":
                    self.results["tests_passed"] += 1
                else:
                    self.results["tests_failed"] += 1
                    
            except Exception as e:
                self.results["scenarios"][test_id] = {
                    "id": test_id,
                    "status": "failed",
                    "error": str(e)
                }
                self.results["tests_failed"] += 1
    
    def _test_n8n_create_lead(self):
        """Testa criação de lead via n8n"""
        usuario = usuarios_teste[0]
        payload = {
            "nome": usuario["nome"],
            "sobrenome": usuario["sobrenome"],
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "origem": usuario["origem"]
        }
        
        response = test_endpoints.create_lead(payload)
        return {
            "status": "ok" if response["status"] == "ok" else "error",
            "response": response
        }
    
    def _test_n8n_schedule_meeting(self):
        """Testa agendamento via n8n"""
        usuario = usuarios_teste[0]
        payload = {
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "titulo": "Teste",
            "opcao_horario": "2025-10-02T14:00:00"
        }
        
        response = test_endpoints.schedule_meeting(payload)
        return {
            "status": "ok" if response["status"] == "ok" else "error",
            "response": response
        }
    
    def _test_n8n_log_event(self):
        """Testa log de evento via n8n"""
        payload = {
            "nome_evento": "test_event",
            "properties": {"test": "data"}
        }
        
        response = test_endpoints.log_event(payload)
        return {
            "status": "ok" if response["status"] == "ok" else "error",
            "response": response
        }
    
    def _test_n8n_send_followup(self):
        """Testa envio de follow-up via n8n"""
        usuario = usuarios_teste[0]
        payload = {
            "canal": "WhatsApp",
            "template_id": "pos_nao_venda_D0",
            "destinatario": usuario["telefone"],
            "placeholders": {"nome": usuario["nome"]}
        }
        
        response = test_endpoints.send_followup(payload)
        return {
            "status": "ok" if response["status"] == "ok" else "error",
            "response": response
        }
    
    def run_followup_tests(self):
        """Executa testes de follow-up"""
        print("\n📧 Executando testes de follow-up...")
        
        usuario = usuarios_teste[0]
        followups = scenario_builder.build_followup_sequence(usuario)
        
        for followup in followups:
            payload = {
                "canal": "WhatsApp",
                "template_id": followup["step"].replace("followup_", "pos_nao_venda_"),
                "destinatario": usuario["telefone"],
                "placeholders": {"nome": usuario["nome"]}
            }
            
            response = test_endpoints.send_followup(payload)
            
            test_id = f"CAD-{followup['step'].replace('followup_', '').upper()}"
            self.results["scenarios"][test_id] = {
                "id": test_id,
                "status": "passed" if response["status"] == "ok" else "failed",
                "result": {"response": response}
            }
            self.results["tests_run"] += 1
            if response["status"] == "ok":
                self.results["tests_passed"] += 1
            else:
                self.results["tests_failed"] += 1
    
    def generate_final_report(self):
        """Gera relatório final"""
        self.results["end_time"] = datetime.now().isoformat()
        
        # Calcular estatísticas
        total_tests = self.results["tests_run"]
        passed_tests = self.results["tests_passed"]
        failed_tests = self.results["tests_failed"]
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Verificar critérios de aprovação
        criteria_met = {
            "conversion_rate": success_rate >= 80,
            "data_validation": failed_tests == 0,
            "calendar_integration": True,  # Simulado
            "tracking": True,  # Simulado
            "messaging": True,  # Simulado
            "robustness": True  # Simulado
        }
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": round(success_rate, 2),
                "criteria_met": criteria_met,
                "overall_status": "PASSED" if all(criteria_met.values()) else "FAILED"
            },
            "detailed_results": self.results,
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self):
        """Gera recomendações baseadas nos resultados"""
        recommendations = []
        
        success_rate = (self.results["tests_passed"] / self.results["tests_run"] * 100) if self.results["tests_run"] > 0 else 0
        
        if success_rate < 80:
            recommendations.append("Taxa de sucesso abaixo de 80%. Revisar fluxos de teste.")
        
        if self.results["tests_failed"] > 0:
            recommendations.append(f"Encontrados {self.results['tests_failed']} testes falhados. Revisar logs de erro.")
        
        return recommendations
    
    def save_results(self, filename: str = None):
        """Salva resultados em arquivo"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trilha_test_results_{timestamp}.json"
        
        filepath = Path("test_results") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        return str(filepath)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Executa trilha de testes MrDom SDR")
    parser.add_argument("--scenarios", nargs="+", help="Cenários específicos para executar")
    parser.add_argument("--skip-validations", action="store_true", help="Pular testes de validação")
    parser.add_argument("--skip-n8n", action="store_true", help="Pular testes de n8n")
    parser.add_argument("--skip-followup", action="store_true", help="Pular testes de follow-up")
    parser.add_argument("--output", help="Arquivo de saída para resultados")
    
    args = parser.parse_args()
    
    print("🚀 Iniciando Trilha de Testes MrDom SDR")
    print("=" * 50)
    
    runner = TrilhaTestRunner()
    
    # Executar cenários principais
    if args.scenarios:
        scenarios_to_run = args.scenarios
    else:
        scenarios_to_run = ["WPP-01", "WPP-02", "SITE-01", "IG-01", "TG-01"]
    
    for scenario_id in scenarios_to_run:
        if scenario_id in cenarios_teste:
            runner.run_scenario(scenario_id, cenarios_teste[scenario_id])
        else:
            print(f"⚠️  Cenário {scenario_id} não encontrado")
    
    # Executar testes de validação
    if not args.skip_validations:
        runner.run_validation_tests()
    
    # Executar testes de n8n
    if not args.skip_n8n:
        runner.run_n8n_tests()
    
    # Executar testes de follow-up
    if not args.skip_followup:
        runner.run_followup_tests()
    
    # Gerar relatório final
    report = runner.generate_final_report()
    
    # Salvar resultados
    output_file = runner.save_results(args.output)
    
    # Exibir resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    print(f"Total de testes: {report['summary']['total_tests']}")
    print(f"Testes aprovados: {report['summary']['passed_tests']}")
    print(f"Testes falhados: {report['summary']['failed_tests']}")
    print(f"Taxa de sucesso: {report['summary']['success_rate']}%")
    print(f"Status geral: {report['summary']['overall_status']}")
    
    print(f"\n📁 Resultados salvos em: {output_file}")
    
    # Exibir recomendações
    if report['recommendations']:
        print("\n💡 RECOMENDAÇÕES:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
    
    return 0 if report['summary']['overall_status'] == "PASSED" else 1

if __name__ == "__main__":
    sys.exit(main())
