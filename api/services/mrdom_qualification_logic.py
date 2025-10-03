"""
Lógica de Qualificação MrDom - Integração com AgentOS
Implementa o script específico de qualificação do MrDom SDR.
"""

import os
import json
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass

class QualificationStage(Enum):
    """Estágios da qualificação MrDom."""
    GREETING = "greeting"
    POST_SALE = "post_sale"
    MKT_SALES_INTEGRATION = "mkt_sales_integration"
    CURRENT_TOOLS = "current_tools"
    PITCH_ADAPTATION = "pitch_adaptation"
    SCHEDULING = "scheduling"
    CONFIRMATION = "confirmation"
    FOLLOW_UP = "follow_up"

@dataclass
class QualificationData:
    """Dados coletados durante a qualificação."""
    post_sale: Optional[str] = None
    mkt_sales: Optional[str] = None
    tools: Optional[str] = None
    tools_satisfaction: Optional[str] = None
    scheduling_response: Optional[str] = None
    lead_data: Dict[str, str] = None
    
    def __post_init__(self):
        if self.lead_data is None:
            self.lead_data = {}

class MrDomQualificationLogic:
    """Lógica de qualificação específica do MrDom."""
    
    def __init__(self):
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
    
    def analyze_response(self, user_input: str, stage: QualificationStage) -> str:
        """Analisa resposta do usuário baseado no estágio atual."""
        input_lower = user_input.lower()
        
        if stage == QualificationStage.POST_SALE:
            if any(word in input_lower for word in ["sim", "sim,", "retomamos", "sim retomamos"]):
                return "sim"
            elif any(word in input_lower for word in ["não", "nao", "não retomamos", "nao retomamos"]):
                return "não"
            else:
                return "mais_ou_menos"
        
        elif stage == QualificationStage.MKT_SALES_INTEGRATION:
            if any(word in input_lower for word in ["bem", "muito bem", "conectado", "integração"]):
                return "muito_bem"
            elif any(word in input_lower for word in ["não", "nao", "separado", "cada um"]):
                return "nao_conecta"
            else:
                return "nao_sei"
        
        elif stage == QualificationStage.CURRENT_TOOLS:
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
        
        elif stage == QualificationStage.SCHEDULING:
            if any(word in input_lower for word in ["10h", "14h", "amanhã", "amanha", "sim"]):
                return "aceitou"
            elif any(word in input_lower for word in ["outro", "quarta", "quinta", "segunda"]):
                return "outro_horario"
            else:
                return "depois"
        
        return "default"
    
    def adapt_pitch(self, qualification_data: QualificationData) -> str:
        """Adapta pitch baseado nas respostas coletadas."""
        pitches = []
        
        # Analisa dor principal
        if qualification_data.post_sale == "não":
            pitches.append("Foco em cadências automatizadas para pós não venda")
        elif qualification_data.mkt_sales == "nao_conecta":
            pitches.append("Foco em marketing + vendas conectados")
        elif qualification_data.tools in ["sem_crm", "limitado"]:
            pitches.append("Foco em ecossistema completo (CRM + Marketing + Mensageria + BI)")
        
        if pitches:
            return f"Baseado no que conversamos, nossa proposta é: {', '.join(pitches)}. O DOM360 transforma sua operação comercial em uma máquina previsível de vendas."
        else:
            return "O DOM360 oferece uma solução completa: Tecnologia + Processos + Pessoas para transformar sua operação comercial."
    
    def get_next_message(self, stage: QualificationStage, user_input: str, qualification_data: QualificationData) -> tuple[str, QualificationStage]:
        """Retorna próxima mensagem e estágio baseado no script MrDom."""
        script = self.scripts.get(stage, {})
        
        if stage == QualificationStage.PITCH_ADAPTATION:
            response = self.adapt_pitch(qualification_data)
            return response, QualificationStage.SCHEDULING
        
        elif "responses" in script:
            response_category = self.analyze_response(user_input, stage)
            
            if response_category in script["responses"]:
                response = script["responses"][response_category]["response"]
                next_stage = script["responses"][response_category].get("next_stage", script.get("next_stage", stage))
                return response, next_stage
        
        # Mensagem padrão do estágio
        response = script.get("message", "Como posso te ajudar?")
        next_stage = script.get("next_stage", stage)
        
        return response, next_stage
    
    def update_qualification_data(self, stage: QualificationStage, user_input: str, qualification_data: QualificationData):
        """Atualiza dados de qualificação baseado na resposta."""
        response_category = self.analyze_response(user_input, stage)
        
        if stage == QualificationStage.POST_SALE:
            qualification_data.post_sale = response_category
        elif stage == QualificationStage.MKT_SALES_INTEGRATION:
            qualification_data.mkt_sales = response_category
        elif stage == QualificationStage.CURRENT_TOOLS:
            qualification_data.tools = response_category
        elif stage == QualificationStage.SCHEDULING:
            qualification_data.scheduling_response = response_category
    
    def get_qualification_summary(self, qualification_data: QualificationData) -> Dict[str, Any]:
        """Retorna resumo da qualificação."""
        return {
            "post_sale": qualification_data.post_sale,
            "mkt_sales": qualification_data.mkt_sales,
            "tools": qualification_data.tools,
            "tools_satisfaction": qualification_data.tools_satisfaction,
            "scheduling_response": qualification_data.scheduling_response,
            "lead_data": qualification_data.lead_data,
            "qualification_complete": all([
                qualification_data.post_sale,
                qualification_data.mkt_sales,
                qualification_data.tools
            ])
        }

# Instância global para uso nos agentes
mrdom_qualification = MrDomQualificationLogic()
