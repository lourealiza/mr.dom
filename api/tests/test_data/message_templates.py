"""
Templates de mensagens para a trilha de testes
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class MessageTemplates:
    """Classe para gerenciar templates de mensagens"""
    
    def __init__(self):
        self.templates = {
            "opening": "Olá {{nome}}! 👋 Sou o assistente virtual da MrDom. Posso fazer 3 perguntas rápidas para entender melhor suas necessidades?",
            
            "qualificacao_perguntas": [
                "Qual é o tamanho da sua empresa?",
                "Qual ferramenta de CRM vocês usam atualmente?", 
                "Qual é o principal desafio na gestão de leads?"
            ],
            
            "pitch_geral": "Baseado nas suas respostas, a MrDom pode ajudar com {{principal_dor}}. Temos uma solução específica para empresas do seu segmento.",
            
            "pitch_tecnologia": "Para empresas de tecnologia como a {{empresa}}, temos automações específicas que podem resolver {{principal_dor}}.",
            
            "pitch_startup": "Startups como a {{empresa}} precisam de soluções escaláveis. Podemos ajudar com {{principal_dor}} de forma eficiente.",
            
            "cta_agenda": "Que tal agendarmos uma conversa de 30 minutos para eu apresentar como podemos resolver isso? Tenho disponível: {{horario1}} ou {{horario2}}.",
            
            "confirmacao_agendada": "Perfeito {{nome}}! Seu agendamento está confirmado para {{data}} às {{horario}}. Aqui estão os links: {{link_meet}} | {{link_ics}}",
            
            "lembrete_24h": "Olá {{nome}}! Lembrete: nossa conversa é amanhã às {{horario}}. Link: {{link_meet}}",
            
            "lembrete_2h": "{{nome}}, nossa conversa é em 2 horas! Link: {{link_meet}}",
            
            "pos_nao_venda_D0": "Oi {{nome}}! Entendo que você precisa pensar. Que tal tentarmos novamente? Tenho disponível: {{horario1}} ou {{horario2}}.",
            
            "pos_nao_venda_D2": "{{nome}}, como está? Ainda temos disponível: {{horario1}} ou {{horario2}}. Vale a pena uma conversa rápida!",
            
            "pos_nao_venda_D7": "{{nome}}, tudo bem? Não desista da oportunidade! Temos: {{horario1}} ou {{horario2}}.",
            
            "pos_nao_venda_D14": "Última tentativa, {{nome}}! Últimos horários: {{horario1}} ou {{horario2}}. Não perca essa oportunidade!",
            
            "erro_email_invalido": "Ops! O email {{email}} parece estar incorreto. Pode verificar e enviar novamente?",
            
            "erro_telefone_invalido": "Ops! O telefone {{telefone}} precisa ter DDD. Pode enviar no formato (11) 99999-9999?",
            
            "erro_campos_obrigatorios": "Para agendar, preciso do seu nome completo, email e telefone. Pode preencher esses dados?",
            
            "erro_calendario": "Ops! Houve um problema ao criar o agendamento. Vou tentar novamente em alguns minutos.",
            
            "erro_crm": "Ops! Houve um problema ao salvar seus dados. Vou tentar novamente.",
            
            "nutricao_time_pequeno": "Entendo! Para empresas com menos de 3 pessoas, temos um programa especial de nutrição. Posso enviar informações por email?",
            
            "objeccao_tempo": "Entendo a falta de tempo! Por isso mesmo nossa conversa é só 30 minutos. Vale muito a pena!",
            
            "objeccao_custo": "Entendo a preocupação com investimento! Por isso fazemos um diagnóstico gratuito primeiro. Sem compromisso!"
        }
    
    def render_template(self, template_name: str, placeholders: Dict[str, Any]) -> str:
        """Renderiza um template com placeholders"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' não encontrado")
        
        template = self.templates[template_name]
        
        # Se for uma lista de perguntas, renderiza cada uma
        if isinstance(template, list):
            return [self._replace_placeholders(str(item), placeholders) for item in template]
        
        return self._replace_placeholders(template, placeholders)
    
    def _replace_placeholders(self, text: str, placeholders: Dict[str, Any]) -> str:
        """Substitui placeholders no texto"""
        for key, value in placeholders.items():
            placeholder = f"{{{{{key}}}}}"
            text = text.replace(placeholder, str(value))
        return text
    
    def get_available_horarios(self, data: str = None) -> List[str]:
        """Retorna horários disponíveis para agendamento"""
        if not data:
            # Usar amanhã como padrão
            tomorrow = datetime.now() + timedelta(days=1)
            data = tomorrow.strftime("%Y-%m-%d")
        
        # Horários padrão para teste
        return ["10:00", "14:00"]
    
    def generate_confirmation_data(self, usuario: Dict[str, Any], horario: str) -> Dict[str, Any]:
        """Gera dados para confirmação de agendamento"""
        data_agendamento = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        return {
            "nome": usuario.get("nome", ""),
            "data": data_agendamento,
            "horario": horario,
            "link_meet": f"https://meet.google.com/mrdom-{usuario.get('id', 'test')}",
            "link_ics": f"https://calendar.google.com/event?eid=mrdom-{usuario.get('id', 'test')}.ics"
        }
    
    def generate_followup_data(self, usuario: Dict[str, Any], dias: int) -> Dict[str, Any]:
        """Gera dados para follow-up"""
        data_futura = datetime.now() + timedelta(days=dias)
        horarios = self.get_available_horarios(data_futura.strftime("%Y-%m-%d"))
        
        return {
            "nome": usuario.get("nome", ""),
            "horario1": f"{data_futura.strftime('%Y-%m-%d')} {horarios[0]}",
            "horario2": f"{data_futura.strftime('%Y-%m-%d')} {horarios[1]}"
        }

class TestScenarioBuilder:
    """Construtor de cenários de teste"""
    
    def __init__(self):
        self.templates = MessageTemplates()
    
    def build_conversation_flow(self, usuario: Dict[str, Any], canal: str) -> List[Dict[str, Any]]:
        """Constrói um fluxo completo de conversa"""
        flow = []
        
        # 1. Abertura
        flow.append({
            "step": "opening",
            "message": self.templates.render_template("opening", {"nome": usuario["nome"]}),
            "expected_response": "sim|ok|pode|claro"
        })
        
        # 2. Qualificação
        perguntas = self.templates.render_template("qualificacao_perguntas", {})
        for i, pergunta in enumerate(perguntas):
            flow.append({
                "step": f"qualificacao_{i+1}",
                "message": pergunta,
                "expected_response": "qualquer_texto"
            })
        
        # 3. Pitch
        pitch_template = "pitch_geral"
        if usuario.get("segmento") == "Tecnologia":
            pitch_template = "pitch_tecnologia"
        elif usuario.get("segmento") == "Startup":
            pitch_template = "pitch_startup"
        
        flow.append({
            "step": "pitch",
            "message": self.templates.render_template(pitch_template, usuario),
            "expected_response": "interesse|agendar|ok"
        })
        
        # 4. CTA de Agenda
        horarios = self.templates.get_available_horarios()
        flow.append({
            "step": "cta_agenda",
            "message": self.templates.render_template("cta_agenda", {
                "horario1": horarios[0],
                "horario2": horarios[1]
            }),
            "expected_response": "agendar|sim|ok"
        })
        
        # 5. Coleta de dados
        flow.append({
            "step": "coleta_dados",
            "message": "Para confirmar o agendamento, preciso dos seus dados:",
            "expected_data": ["nome", "sobrenome", "email", "telefone"]
        })
        
        # 6. Confirmação
        confirmacao_data = self.templates.generate_confirmation_data(usuario, horarios[0])
        flow.append({
            "step": "confirmacao",
            "message": self.templates.render_template("confirmacao_agendada", confirmacao_data),
            "expected_response": "confirmado"
        })
        
        return flow
    
    def build_followup_sequence(self, usuario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Constrói sequência de follow-up"""
        followups = []
        
        # D0 - Imediato
        followups.append({
            "step": "followup_D0",
            "delay": 0,
            "message": self.templates.render_template("pos_nao_venda_D0", 
                self.templates.generate_followup_data(usuario, 1))
        })
        
        # D2
        followups.append({
            "step": "followup_D2", 
            "delay": 2,
            "message": self.templates.render_template("pos_nao_venda_D2",
                self.templates.generate_followup_data(usuario, 3))
        })
        
        # D7
        followups.append({
            "step": "followup_D7",
            "delay": 7, 
            "message": self.templates.render_template("pos_nao_venda_D7",
                self.templates.generate_followup_data(usuario, 8))
        })
        
        # D14
        followups.append({
            "step": "followup_D14",
            "delay": 14,
            "message": self.templates.render_template("pos_nao_venda_D14",
                self.templates.generate_followup_data(usuario, 15))
        })
        
        return followups

# Instância global para uso nos testes
message_templates = MessageTemplates()
scenario_builder = TestScenarioBuilder()
