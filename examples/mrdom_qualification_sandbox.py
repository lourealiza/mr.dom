#!/usr/bin/env python3
"""
Sandbox de Qualificação MrDom - Script Específico
Implementa o fluxo de qualificação detalhado do MrDom SDR.
"""

import os
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

class QualificationStage(Enum):
    """Estágios da qualificação."""
    GREETING = "greeting"
    POST_SALE = "post_sale"
    MKT_SALES_INTEGRATION = "mkt_sales_integration"
    CURRENT_TOOLS = "current_tools"
    PITCH_ADAPTATION = "pitch_adaptation"
    SCHEDULING = "scheduling"
    CONFIRMATION = "confirmation"
    FOLLOW_UP = "follow_up"

class MrDomQualificationSandbox:
    """Sandbox específico para qualificação MrDom."""
    
    def __init__(self):
        self.conversation_history = []
        self.current_stage = QualificationStage.GREETING
        self.qualification_data = {
            "post_sale": None,  # sim, não, mais_ou_menos
            "mkt_sales": None,  # bem_conectado, nao_conecta, nao_sei
            "tools": None,      # sem_crm, limitado, robusto
            "tools_satisfaction": None,  # satisfeito, caro_complexo
            "scheduling_response": None,  # aceitou, outro_horario, depois
            "lead_data": {}  # nome, empresa, email, etc.
        }
        
        # Scripts específicos do MrDom
        self.scripts = {
            QualificationStage.GREETING: {
                "message": "Olá! Sou o Mr. DOM, do DOM360. Para te direcionar melhor, como você se chama e qual é a sua empresa?",
                "next_stage": QualificationStage.POST_SALE
            },
            QualificationStage.POST_SALE: {
                "message": "Depois das propostas, vocês retomam quem não decide?",
                "responses": {
                    "sim": {
                        "response": "Ótimo! Isso mostra maturidade comercial. E como vocês fazem essa retomada hoje? É manual ou já têm alguma automação?",
                        "value": "automação_cadências"
                    },
                    "não": {
                        "response": "Entendo. Muitas empresas perdem oportunidades valiosas por não terem um processo estruturado de pós não venda. Isso pode representar 20-30% de vendas perdidas.",
                        "value": "ganho_pós_não_venda"
                    },
                    "mais_ou_menos": {
                        "response": "Interessante! E se houvesse um processo automático para isso? Que diferença faria no resultado da equipe?",
                        "value": "processo_automático"
                    }
                },
                "next_stage": QualificationStage.MKT_SALES_INTEGRATION
            },
            QualificationStage.MKT_SALES_INTEGRATION: {
                "message": "Como o marketing se conecta com o comercial?",
                "responses": {
                    "muito_bem": {
                        "response": "Excelente! Isso é um diferencial competitivo. Vocês já acompanham métricas integradas? Tem BI para acompanhar o funil completo?",
                        "value": "bi_cadências"
                    },
                    "nao_conecta": {
                        "response": "Essa desconexão é comum e custa caro. Empresas que integram marketing e vendas crescem em média 30% mais rápido. Qual seria o impacto disso no seu negócio?",
                        "value": "integração_crescimento"
                    },
                    "nao_sei": {
                        "response": "Muitas empresas aumentam 30% só integrando marketing e vendas. Isso acontece porque elimina desperdícios e acelera conversões.",
                        "value": "educação_integração"
                    }
                },
                "next_stage": QualificationStage.CURRENT_TOOLS
            },
            QualificationStage.CURRENT_TOOLS: {
                "message": "Quais ferramentas (CRM/automação/mensageria) usam hoje? Estão satisfeitos?",
                "responses": {
                    "sem_crm": {
                        "response": "Entendo. Sem CRM, vocês podem estar perdendo oportunidades por desorganização invisível. O DOM360 organiza e guia por etapas, transformando caos em processo.",
                        "value": "desorganização_invisível"
                    },
                    "limitado": {
                        "response": "Ótimo que já têm CRM! Pipedrive/RDCRM são bons para funil, mas falta integração completa + método estruturado. É aí que o DOM360 faz a diferença.",
                        "value": "integração_método"
                    },
                    "robusto_satisfeito": {
                        "response": "Salesforce/Hubspot são robustos mesmo! O DOM360 complementa com simplicidade e custo-benefício. Vale a pena conhecer nossa abordagem.",
                        "value": "nutrir_sem_forçar"
                    },
                    "robusto_caro": {
                        "response": "Salesforce é poderoso, mas complexo e caro. O DOM360 oferece robustez + intuitividade + acessibilidade. Melhor custo-benefício.",
                        "value": "robusto_acessível"
                    }
                },
                "next_stage": QualificationStage.PITCH_ADAPTATION
            },
            QualificationStage.PITCH_ADAPTATION: {
                "message": "Baseado no que conversamos, vou adaptar nossa proposta:",
                "next_stage": QualificationStage.SCHEDULING
            },
            QualificationStage.SCHEDULING: {
                "message": "Consigo te encaixar amanhã às 10h ou 14h (30 min). Qual funciona melhor?",
                "responses": {
                    "aceitou": {
                        "response": "Perfeito! Vou precisar de alguns dados para confirmar: nome completo, empresa, cargo, e-mail e WhatsApp.",
                        "next_stage": QualificationStage.CONFIRMATION
                    },
                    "outro_horario": {
                        "response": "Claro! Que horários funcionam melhor para você? Tenho disponibilidade na quarta e quinta também.",
                        "next_stage": QualificationStage.SCHEDULING
                    },
                    "depois": {
                        "response": "Entendo. Vou te enviar um resumo do que conversamos e entro em contato em alguns dias.",
                        "next_stage": QualificationStage.FOLLOW_UP
                    }
                }
            }
        }
    
    def get_current_script(self) -> Dict[str, Any]:
        """Retorna script atual baseado no estágio."""
        return self.scripts.get(self.current_stage, {})
    
    def analyze_response(self, user_input: str) -> str:
        """Analisa resposta do usuário e determina categoria."""
        input_lower = user_input.lower()
        
        if self.current_stage == QualificationStage.POST_SALE:
            if any(word in input_lower for word in ["sim", "sim,", "retomamos", "sim retomamos"]):
                return "sim"
            elif any(word in input_lower for word in ["não", "nao", "não retomamos", "nao retomamos"]):
                return "não"
            else:
                return "mais_ou_menos"
        
        elif self.current_stage == QualificationStage.MKT_SALES_INTEGRATION:
            if any(word in input_lower for word in ["bem", "muito bem", "conectado", "integração"]):
                return "muito_bem"
            elif any(word in input_lower for word in ["não", "nao", "separado", "cada um"]):
                return "nao_conecta"
            else:
                return "nao_sei"
        
        elif self.current_stage == QualificationStage.CURRENT_TOOLS:
            if any(word in input_lower for word in ["sem crm", "não temos", "nao temos", "nada"]):
                return "sem_crm"
            elif any(word in input_lower for word in ["pipedrive", "rdcrm", "agendor", "limitado"]):
                return "limitado"
            elif any(word in input_lower for word in ["salesforce", "hubspot", "dynamics", "robusto"]):
                if any(word in input_lower for word in ["caro", "complexo", "difícil", "difícil"]):
                    return "robusto_caro"
                else:
                    return "robusto_satisfeito"
            else:
                return "sem_crm"
        
        elif self.current_stage == QualificationStage.SCHEDULING:
            if any(word in input_lower for word in ["10h", "14h", "amanhã", "amanha", "sim"]):
                return "aceitou"
            elif any(word in input_lower for word in ["outro", "quarta", "quinta", "segunda"]):
                return "outro_horario"
            else:
                return "depois"
        
        return "default"
    
    def adapt_pitch(self) -> str:
        """Adapta pitch baseado nas respostas coletadas."""
        pitches = []
        
        # Analisa dor principal
        if self.qualification_data["post_sale"] == "não":
            pitches.append("Foco em cadências automatizadas para pós não venda")
        elif self.qualification_data["mkt_sales"] == "nao_conecta":
            pitches.append("Foco em marketing + vendas conectados")
        elif self.qualification_data["tools"] in ["sem_crm", "limitado"]:
            pitches.append("Foco em ecossistema completo (CRM + Marketing + Mensageria + BI)")
        
        if pitches:
            return f"Baseado no que conversamos, nossa proposta é: {', '.join(pitches)}. O DOM360 transforma sua operação comercial em uma máquina previsível de vendas."
        else:
            return "O DOM360 oferece uma solução completa: Tecnologia + Processos + Pessoas para transformar sua operação comercial."
    
    async def process_message(self, user_input: str) -> Dict[str, Any]:
        """Processa mensagem seguindo o script MrDom."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Salva entrada do usuário
        self.conversation_history.append({
            "timestamp": timestamp,
            "stage": self.current_stage.value,
            "user_message": user_input,
            "agent_response": None
        })
        
        # Analisa resposta
        response_category = self.analyze_response(user_input)
        
        # Atualiza dados de qualificação
        if self.current_stage == QualificationStage.POST_SALE:
            self.qualification_data["post_sale"] = response_category
        elif self.current_stage == QualificationStage.MKT_SALES_INTEGRATION:
            self.qualification_data["mkt_sales"] = response_category
        elif self.current_stage == QualificationStage.CURRENT_TOOLS:
            self.qualification_data["tools"] = response_category
        elif self.current_stage == QualificationStage.SCHEDULING:
            self.qualification_data["scheduling_response"] = response_category
        
        # Gera resposta do agente
        script = self.get_current_script()
        
        if self.current_stage == QualificationStage.PITCH_ADAPTATION:
            agent_response = self.adapt_pitch()
            self.current_stage = QualificationStage.SCHEDULING
        elif "responses" in script and response_category in script["responses"]:
            agent_response = script["responses"][response_category]["response"]
            if "next_stage" in script["responses"][response_category]:
                self.current_stage = script["responses"][response_category]["next_stage"]
            elif "next_stage" in script:
                self.current_stage = script["next_stage"]
        else:
            agent_response = script.get("message", "Como posso te ajudar?")
            if "next_stage" in script:
                self.current_stage = script["next_stage"]
        
        # Atualiza histórico
        self.conversation_history[-1]["agent_response"] = agent_response
        
        return {
            "success": True,
            "stage": self.current_stage.value,
            "response": agent_response,
            "timestamp": timestamp,
            "qualification_data": self.qualification_data.copy()
        }
    
    def print_status(self):
        """Mostra status da qualificação."""
        print(f"\n📊 STATUS DA QUALIFICAÇÃO:")
        print(f"   Estágio atual: {self.current_stage.value}")
        print(f"   Mensagens: {len(self.conversation_history)}")
        print(f"\n📋 Dados coletados:")
        for key, value in self.qualification_data.items():
            if value:
                print(f"   {key}: {value}")
    
    def export_qualification(self):
        """Exporta dados de qualificação."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qualification_export_{timestamp}.json"
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "conversation": self.conversation_history,
            "qualification_data": self.qualification_data,
            "final_stage": self.current_stage.value
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Qualificação exportada para: {filename}")
    
    async def run(self):
        """Executa o sandbox de qualificação."""
        print("🎯 SANDBOX DE QUALIFICAÇÃO MRDOM")
        print("=" * 40)
        print("Script específico do MrDom SDR")
        print("Seguindo metodologia: Pós Não Venda → MKT-Vendas → Ferramentas → Pitch → Agenda")
        print("\n💡 Comandos:")
        print("   /status - Status da qualificação")
        print("   /export - Exporta dados")
        print("   /quit - Sair")
        print("=" * 40)
        
        # Inicia com saudação
        script = self.get_current_script()
        print(f"\n🤖 Mr. DOM: {script['message']}")
        
        while True:
            try:
                user_input = input("\n👤 Você: ").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiais
                if user_input == "/status":
                    self.print_status()
                    continue
                elif user_input == "/export":
                    self.export_qualification()
                    continue
                elif user_input == "/quit":
                    break
                
                # Processa mensagem
                result = await self.process_message(user_input)
                
                if result["success"]:
                    print(f"\n🤖 Mr. DOM: {result['response']}")
                else:
                    print(f"❌ Erro: {result.get('error', 'Desconhecido')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Saindo do sandbox...")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
        
        # Resumo final
        print(f"\n📊 RESUMO DA QUALIFICAÇÃO:")
        print(f"   Estágio final: {self.current_stage.value}")
        print(f"   Mensagens: {len(self.conversation_history)}")
        print(f"   Dados coletados: {sum(1 for v in self.qualification_data.values() if v)}/6")

async def main():
    """Função principal."""
    print("🚀 Iniciando Sandbox de Qualificação MrDom...")
    
    sandbox = MrDomQualificationSandbox()
    await sandbox.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sandbox interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
