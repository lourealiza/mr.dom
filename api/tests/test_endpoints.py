"""
Endpoints de teste para webhooks n8n
"""
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
import uuid

class TestWebhookEndpoints:
    """Endpoints simulados para teste de webhooks n8n"""
    
    def __init__(self):
        self.leads_criados = []
        self.agendamentos_criados = []
        self.eventos_logados = []
        self.followups_enviados = []
    
    def create_lead(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simula criação de lead no CRM"""
        try:
            # Validar campos obrigatórios
            campos_obrigatorios = ["nome", "sobrenome", "email", "telefone"]
            campos_faltando = [campo for campo in campos_obrigatorios if not payload.get(campo)]
            
            if campos_faltando:
                return {
                    "status": "error",
                    "message": f"Campos obrigatórios faltando: {', '.join(campos_faltando)}",
                    "code": "MISSING_FIELDS"
                }
            
            # Validar email
            if not self._validar_email(payload["email"]):
                return {
                    "status": "error", 
                    "message": "Email inválido",
                    "code": "INVALID_EMAIL"
                }
            
            # Validar telefone
            telefone_normalizado = self._normalizar_telefone(payload["telefone"])
            if not telefone_normalizado:
                return {
                    "status": "error",
                    "message": "Telefone inválido",
                    "code": "INVALID_PHONE"
                }
            
            # Criar lead
            lead_id = str(uuid.uuid4())
            lead = {
                "id": lead_id,
                "nome": payload["nome"],
                "sobrenome": payload["sobrenome"],
                "empresa": payload.get("empresa", ""),
                "cargo": payload.get("cargo", ""),
                "email": payload["email"],
                "telefone": telefone_normalizado,
                "segmento": payload.get("segmento", ""),
                "tamanho_time": payload.get("tamanho_time", 0),
                "ferramentas_crm": payload.get("ferramentas_crm", ""),
                "ferramentas_marketing": payload.get("ferramentas_marketing", ""),
                "canais_mensageria": payload.get("canais_mensageria", ""),
                "principal_dor": payload.get("principal_dor", ""),
                "origem": payload.get("origem", ""),
                "fuso": payload.get("fuso", "America/Sao_Paulo"),
                "created_at": datetime.now().isoformat(),
                "status": "new"
            }
            
            self.leads_criados.append(lead)
            
            # Log do evento
            self._log_event("lead_created", {
                "lead_id": lead_id,
                "origem": payload.get("origem", ""),
                "empresa": payload.get("empresa", "")
            })
            
            return {
                "status": "ok",
                "message": "lead recebido",
                "lead_id": lead_id,
                "data": lead
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro interno: {str(e)}",
                "code": "INTERNAL_ERROR"
            }
    
    def schedule_meeting(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simula agendamento de reunião"""
        try:
            # Validar campos obrigatórios
            campos_obrigatorios = ["email", "telefone", "titulo", "opcao_horario"]
            campos_faltando = [campo for campo in campos_obrigatorios if not payload.get(campo)]
            
            if campos_faltando:
                return {
                    "status": "error",
                    "message": f"Campos obrigatórios faltando: {', '.join(campos_faltando)}",
                    "code": "MISSING_FIELDS"
                }
            
            # Simular criação de evento no calendário
            event_id = str(uuid.uuid4())
            evento = {
                "id": event_id,
                "email": payload["email"],
                "telefone": payload["telefone"],
                "titulo": payload["titulo"],
                "duracao_min": payload.get("duracao_min", 30),
                "opcao_horario": payload["opcao_horario"],
                "fuso": payload.get("fuso", "America/Sao_Paulo"),
                "observacoes": payload.get("observacoes", ""),
                "created_at": datetime.now().isoformat(),
                "status": "scheduled"
            }
            
            self.agendamentos_criados.append(evento)
            
            # Gerar links
            link_meet = f"https://meet.google.com/mrdom-{event_id}"
            link_ics = f"https://calendar.google.com/event?eid=mrdom-{event_id}.ics"
            
            # Log do evento
            self._log_event("meeting_scheduled", {
                "event_id": event_id,
                "email": payload["email"],
                "horario": payload["opcao_horario"]
            })
            
            return {
                "status": "ok",
                "message": "agendamento recebido",
                "event_id": event_id,
                "link_meet": link_meet,
                "link_ics": link_ics,
                "data": evento
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro interno: {str(e)}",
                "code": "INTERNAL_ERROR"
            }
    
    def send_followup(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simula envio de follow-up"""
        try:
            # Validar campos obrigatórios
            campos_obrigatorios = ["canal", "template_id", "destinatario"]
            campos_faltando = [campo for campo in campos_obrigatorios if not payload.get(campo)]
            
            if campos_faltando:
                return {
                    "status": "error",
                    "message": f"Campos obrigatórios faltando: {', '.join(campos_faltando)}",
                    "code": "MISSING_FIELDS"
                }
            
            # Simular envio
            followup_id = str(uuid.uuid4())
            followup = {
                "id": followup_id,
                "canal": payload["canal"],
                "template_id": payload["template_id"],
                "destinatario": payload["destinatario"],
                "placeholders": payload.get("placeholders", {}),
                "sent_at": datetime.now().isoformat(),
                "status": "sent"
            }
            
            self.followups_enviados.append(followup)
            
            # Log do evento
            self._log_event("followup_sent", {
                "followup_id": followup_id,
                "canal": payload["canal"],
                "template_id": payload["template_id"],
                "destinatario": payload["destinatario"]
            })
            
            return {
                "status": "ok",
                "message": "followup enviado",
                "followup_id": followup_id,
                "data": followup
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro interno: {str(e)}",
                "code": "INTERNAL_ERROR"
            }
    
    def log_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simula log de evento"""
        try:
            evento = {
                "id": str(uuid.uuid4()),
                "nome_evento": payload.get("nome_evento", ""),
                "properties": payload.get("properties", {}),
                "timestamp": datetime.now().isoformat(),
                "source": payload.get("source", "n8n")
            }
            
            self.eventos_logados.append(evento)
            
            return {
                "status": "ok",
                "message": "evento logado",
                "event_id": evento["id"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro interno: {str(e)}",
                "code": "INTERNAL_ERROR"
            }
    
    def _validar_email(self, email: str) -> bool:
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _normalizar_telefone(self, telefone: str) -> str:
        """Normaliza telefone para formato E.164"""
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, telefone))
        
        # Se não tem código do país, adiciona +55
        if len(numeros) == 11 and numeros.startswith('11'):
            return f"+55{numeros}"
        elif len(numeros) == 10:
            return f"+5511{numeros}"
        elif len(numeros) == 13 and numeros.startswith('55'):
            return f"+{numeros}"
        
        return ""
    
    def _log_event(self, nome_evento: str, properties: Dict[str, Any]):
        """Log interno de eventos"""
        evento = {
            "id": str(uuid.uuid4()),
            "nome_evento": nome_evento,
            "properties": properties,
            "timestamp": datetime.now().isoformat(),
            "source": "internal"
        }
        self.eventos_logados.append(evento)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos testes"""
        return {
            "leads_criados": len(self.leads_criados),
            "agendamentos_criados": len(self.agendamentos_criados),
            "eventos_logados": len(self.eventos_logados),
            "followups_enviados": len(self.followups_enviados),
            "taxa_sucesso": self._calcular_taxa_sucesso()
        }
    
    def _calcular_taxa_sucesso(self) -> float:
        """Calcula taxa de sucesso dos testes"""
        total_operacoes = len(self.leads_criados) + len(self.agendamentos_criados) + len(self.followups_enviados)
        if total_operacoes == 0:
            return 0.0
        
        # Considera sucesso se não há erros nos logs
        eventos_erro = [e for e in self.eventos_logados if "error" in e.get("nome_evento", "").lower()]
        operacoes_com_sucesso = total_operacoes - len(eventos_erro)
        
        return (operacoes_com_sucesso / total_operacoes) * 100
    
    def reset(self):
        """Reseta dados de teste"""
        self.leads_criados = []
        self.agendamentos_criados = []
        self.eventos_logados = []
        self.followups_enviados = []

# Instância global para uso nos testes
test_endpoints = TestWebhookEndpoints()
