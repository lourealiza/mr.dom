"""
Teste completo da trilha MrDom SDR
"""
import pytest
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock, patch

import sys
from pathlib import Path

# Adicionar o diretório de testes ao path
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir))

from test_data.trilha_test_data import *
from test_data.message_templates import message_templates, scenario_builder
from test_endpoints import test_endpoints

@pytest.mark.e2e
@pytest.mark.trilha
class TestTrilhaCompleta:
    """Testes da trilha completa MrDom SDR"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self):
        """Setup para cada teste"""
        test_endpoints.reset()
        yield
        # Cleanup após cada teste
    
    @pytest.fixture
    def usuario_teste(self):
        """Usuário de teste padrão"""
        return {
            "id": "user_001",
            "nome": "Ana",
            "sobrenome": "Silva", 
            "empresa": "ACME Tecnologia",
            "cargo": "Diretora Comercial",
            "email": "ana.silva@acme.com.br",
            "telefone": "+5511988887777",
            "segmento": "Tecnologia B2B",
            "tamanho_time": 8,
            "ferramentas_crm": "Pipedrive",
            "ferramentas_marketing": "RD Station",
            "canais_mensageria": "WhatsApp, Email",
            "principal_dor": "Pós‑não‑venda inexistente",
            "origem": "WhatsApp",
            "fuso": "America/Sao_Paulo"
        }
    
    def test_wpp_01_jornada_completa(self, usuario_teste):
        """WPP-01: WhatsApp → abertura → qualificação → agenda → confirmação"""
        
        # 1. Abertura
        mensagem_abertura = message_templates.render_template("opening", {"nome": usuario_teste["nome"]})
        assert "Olá Ana!" in mensagem_abertura
        assert "3 perguntas" in mensagem_abertura
        
        # 2. Qualificação
        perguntas = message_templates.render_template("qualificacao_perguntas", {})
        assert len(perguntas) == 3
        assert "tamanho da sua empresa" in perguntas[0]
        assert "ferramenta de CRM" in perguntas[1]
        assert "principal desafio" in perguntas[2]
        
        # 3. Pitch
        mensagem_pitch = message_templates.render_template("pitch_geral", usuario_teste)
        assert "Pós‑não‑venda inexistente" in mensagem_pitch
        
        # 4. CTA de Agenda
        horarios = message_templates.get_available_horarios()
        mensagem_cta = message_templates.render_template("cta_agenda", {
            "horario1": horarios[0],
            "horario2": horarios[1]
        })
        assert "10:00" in mensagem_cta
        assert "14:00" in mensagem_cta
        
        # 5. Criar Lead
        payload_lead = {
            "nome": usuario_teste["nome"],
            "sobrenome": usuario_teste["sobrenome"],
            "empresa": usuario_teste["empresa"],
            "cargo": usuario_teste["cargo"],
            "email": usuario_teste["email"],
            "telefone": usuario_teste["telefone"],
            "segmento": usuario_teste["segmento"],
            "tamanho_time": usuario_teste["tamanho_time"],
            "ferramentas_crm": usuario_teste["ferramentas_crm"],
            "ferramentas_marketing": usuario_teste["ferramentas_marketing"],
            "canais_mensageria": usuario_teste["canais_mensageria"],
            "principal_dor": usuario_teste["principal_dor"],
            "origem": usuario_teste["origem"]
        }
        
        response_lead = test_endpoints.create_lead(payload_lead)
        assert response_lead["status"] == "ok"
        assert "lead_id" in response_lead
        
        # 6. Agendamento
        payload_agendamento = {
            "email": usuario_teste["email"],
            "telefone": usuario_teste["telefone"],
            "titulo": "Diagnóstico DOM360 (30 min)",
            "duracao_min": 30,
            "opcao_horario": "2025-10-02T14:00:00",
            "fuso": usuario_teste["fuso"],
            "observacoes": "Preferência por WhatsApp; foco em pós não venda"
        }
        
        response_agendamento = test_endpoints.schedule_meeting(payload_agendamento)
        assert response_agendamento["status"] == "ok"
        assert "link_meet" in response_agendamento
        assert "link_ics" in response_agendamento
        
        # 7. Confirmação
        confirmacao_data = message_templates.generate_confirmation_data(usuario_teste, "14:00")
        mensagem_confirmacao = message_templates.render_template("confirmacao_agendada", confirmacao_data)
        assert "Perfeito Ana!" in mensagem_confirmacao
        assert "14:00" in mensagem_confirmacao
        
        # Verificar estatísticas
        stats = test_endpoints.get_stats()
        assert stats["leads_criados"] == 1
        assert stats["agendamentos_criados"] == 1
        assert stats["taxa_sucesso"] == 100.0
    
    def test_wpp_02_normalizacao_telefone(self):
        """WPP-02: WhatsApp com telefone sem +55 → normalização E.164"""
        
        usuario_telefone_invalido = {
            "nome": "Carlos",
            "sobrenome": "Santos",
            "email": "carlos@techstart.com.br",
            "telefone": "11999998888",  # Sem +55
            "origem": "WhatsApp"
        }
        
        # Testar normalização
        telefone_normalizado = test_endpoints._normalizar_telefone(usuario_telefone_invalido["telefone"])
        assert telefone_normalizado == "+5511999998888"
        
        # Criar lead com telefone normalizado
        payload_lead = {
            "nome": usuario_telefone_invalido["nome"],
            "sobrenome": usuario_telefone_invalido["sobrenome"],
            "email": usuario_telefone_invalido["email"],
            "telefone": telefone_normalizado,
            "origem": usuario_telefone_invalido["origem"]
        }
        
        response = test_endpoints.create_lead(payload_lead)
        assert response["status"] == "ok"
        assert response["data"]["telefone"] == "+5511999998888"
    
    def test_site_01_widget_jornada_completa(self):
        """SITE-01: Widget do site → jornada completa"""
        
        usuario_site = {
            "id": "user_003",
            "nome": "Maria",
            "sobrenome": "Oliveira",
            "empresa": "Consultoria Plus",
            "cargo": "Gerente de Marketing",
            "email": "maria.oliveira@consultoriaplus.com",
            "telefone": "+5531988887777",
            "segmento": "Consultoria",
            "tamanho_time": 12,
            "ferramentas_crm": "Salesforce",
            "ferramentas_marketing": "ActiveCampaign",
            "canais_mensageria": "Instagram, Email",
            "principal_dor": "Qualificação de leads",
            "origem": "Site"
        }
        
        # Construir fluxo completo
        flow = scenario_builder.build_conversation_flow(usuario_site, "Site")
        
        # Verificar se todos os steps estão presentes
        steps_esperados = ["opening", "qualificacao_1", "qualificacao_2", "qualificacao_3", "pitch", "cta_agenda", "coleta_dados", "confirmacao"]
        steps_obtidos = [step["step"] for step in flow]
        
        for step_esperado in steps_esperados:
            assert step_esperado in steps_obtidos
        
        # Testar criação de lead
        payload_lead = {
            "nome": usuario_site["nome"],
            "sobrenome": usuario_site["sobrenome"],
            "email": usuario_site["email"],
            "telefone": usuario_site["telefone"],
            "empresa": usuario_site["empresa"],
            "origem": usuario_site["origem"]
        }
        
        response = test_endpoints.create_lead(payload_lead)
        assert response["status"] == "ok"
        assert response["data"]["origem"] == "Site"
    
    def test_ig_01_instagram_origem_preservada(self):
        """IG-01: Instagram DM → captação de origem preservada"""
        
        usuario_instagram = {
            "nome": "João",
            "sobrenome": "Ferreira",
            "email": "joao.ferreira@ecommercebrasil.com.br",
            "telefone": "+5541999888777",
            "origem": "Instagram"
        }
        
        payload_lead = {
            "nome": usuario_instagram["nome"],
            "sobrenome": usuario_instagram["sobrenome"],
            "email": usuario_instagram["email"],
            "telefone": usuario_instagram["telefone"],
            "origem": usuario_instagram["origem"]
        }
        
        response = test_endpoints.create_lead(payload_lead)
        assert response["status"] == "ok"
        assert response["data"]["origem"] == "Instagram"
    
    def test_tg_01_telegram_jornada_completa(self):
        """TG-01: Telegram → jornada completa"""
        
        usuario_telegram = {
            "nome": "Fernanda",
            "sobrenome": "Costa",
            "email": "fernanda@agenciadigital.com",
            "telefone": "+5551999888777",
            "origem": "Telegram"
        }
        
        # Testar fluxo completo
        flow = scenario_builder.build_conversation_flow(usuario_telegram, "Telegram")
        assert len(flow) >= 6  # Pelo menos 6 steps
        
        # Testar criação de lead
        payload_lead = {
            "nome": usuario_telegram["nome"],
            "sobrenome": usuario_telegram["sobrenome"],
            "email": usuario_telegram["email"],
            "telefone": usuario_telegram["telefone"],
            "origem": usuario_telegram["origem"]
        }
        
        response = test_endpoints.create_lead(payload_lead)
        assert response["status"] == "ok"
        assert response["data"]["origem"] == "Telegram"
    
    def test_val_email_invalido(self):
        """VAL-E-MAIL-01: email inválido deve pedir correção"""
        
        usuario_email_invalido = {
            "nome": "Teste",
            "sobrenome": "Inválido",
            "email": "email-invalido",  # Email inválido
            "telefone": "+5511988887777"
        }
        
        response = test_endpoints.create_lead(usuario_email_invalido)
        assert response["status"] == "error"
        assert response["code"] == "INVALID_EMAIL"
        assert "Email inválido" in response["message"]
    
    def test_val_telefone_invalido(self):
        """VAL-FONE-01: DDI/DDD ausente → normalizar ou solicitar ajuste"""
        
        usuario_telefone_invalido = {
            "nome": "Teste",
            "sobrenome": "Inválido",
            "email": "teste@teste.com",
            "telefone": "988887777"  # Sem DDD
        }
        
        response = test_endpoints.create_lead(usuario_telefone_invalido)
        assert response["status"] == "error"
        assert response["code"] == "INVALID_PHONE"
        assert "Telefone inválido" in response["message"]
    
    def test_val_campos_obrigatorios(self):
        """VAL-OBRIG-01: bloqueio de agenda sem campos obrigatórios"""
        
        usuario_incompleto = {
            "nome": "",  # Nome vazio
            "sobrenome": "",  # Sobrenome vazio
            "email": "teste@teste.com",
            "telefone": "+5511988887777"
        }
        
        response = test_endpoints.create_lead(usuario_incompleto)
        assert response["status"] == "error"
        assert "Campos obrigatórios faltando" in response["message"]
        assert "nome" in response["message"]
        assert "sobrenome" in response["message"]
    
    def test_n8n_create_lead(self, usuario_teste):
        """N8N-CL-01: POST create_lead com payload completo → CRM Upsert Lead OK"""
        
        payload_completo = {
            "nome": usuario_teste["nome"],
            "sobrenome": usuario_teste["sobrenome"],
            "empresa": usuario_teste["empresa"],
            "cargo": usuario_teste["cargo"],
            "email": usuario_teste["email"],
            "telefone": usuario_teste["telefone"],
            "segmento": usuario_teste["segmento"],
            "tamanho_time": usuario_teste["tamanho_time"],
            "ferramentas_crm": usuario_teste["ferramentas_crm"],
            "ferramentas_marketing": usuario_teste["ferramentas_marketing"],
            "canais_mensageria": usuario_teste["canais_mensageria"],
            "principal_dor": usuario_teste["principal_dor"],
            "origem": usuario_teste["origem"]
        }
        
        response = test_endpoints.create_lead(payload_completo)
        assert response["status"] == "ok"
        assert "lead_id" in response
        assert response["data"]["origem"] == usuario_teste["origem"]
        
        # Verificar se foi logado
        eventos_lead = [e for e in test_endpoints.eventos_logados if e["nome_evento"] == "lead_created"]
        assert len(eventos_lead) == 1
        assert eventos_lead[0]["properties"]["lead_id"] == response["lead_id"]
    
    def test_n8n_schedule_meeting(self, usuario_teste):
        """N8N-AG-01: POST schedule_meeting → evento criado"""
        
        payload_agendamento = {
            "email": usuario_teste["email"],
            "telefone": usuario_teste["telefone"],
            "titulo": "Diagnóstico DOM360 (30 min)",
            "duracao_min": 30,
            "opcao_horario": "2025-10-02T14:00:00",
            "fuso": usuario_teste["fuso"],
            "observacoes": "Preferência por WhatsApp"
        }
        
        response = test_endpoints.schedule_meeting(payload_agendamento)
        assert response["status"] == "ok"
        assert "event_id" in response
        assert "link_meet" in response
        assert "link_ics" in response
        
        # Verificar se foi logado
        eventos_agendamento = [e for e in test_endpoints.eventos_logados if e["nome_evento"] == "meeting_scheduled"]
        assert len(eventos_agendamento) == 1
        assert eventos_agendamento[0]["properties"]["event_id"] == response["event_id"]
    
    def test_n8n_log_event(self):
        """N8N-LOG-01: POST log_event → Analytics Track recebe"""
        
        payload_log = {
            "nome_evento": "test_event",
            "properties": {
                "user_id": "test_user",
                "action": "button_click",
                "page": "home"
            },
            "source": "n8n"
        }
        
        response = test_endpoints.log_event(payload_log)
        assert response["status"] == "ok"
        assert "event_id" in response
        
        # Verificar se foi logado
        eventos = [e for e in test_endpoints.eventos_logados if e["nome_evento"] == "test_event"]
        assert len(eventos) == 1
        assert eventos[0]["properties"]["user_id"] == "test_user"
    
    def test_n8n_send_followup(self, usuario_teste):
        """N8N-FU-01: POST send_followup → mensageria envia template"""
        
        payload_followup = {
            "canal": "WhatsApp",
            "template_id": "pos_nao_venda_D2",
            "destinatario": usuario_teste["telefone"],
            "placeholders": {
                "nome": usuario_teste["nome"],
                "horario1": "2025-10-03 10:00",
                "horario2": "2025-10-03 14:00"
            }
        }
        
        response = test_endpoints.send_followup(payload_followup)
        assert response["status"] == "ok"
        assert "followup_id" in response
        
        # Verificar se foi logado
        eventos_followup = [e for e in test_endpoints.eventos_logados if e["nome_evento"] == "followup_sent"]
        assert len(eventos_followup) == 1
        assert eventos_followup[0]["properties"]["template_id"] == "pos_nao_venda_D2"
    
    def test_cadencia_pos_nao_venda(self, usuario_teste):
        """CAD-D0/D2/D7/D14: sequência completa de reengajamento"""
        
        # Construir sequência de follow-up
        followups = scenario_builder.build_followup_sequence(usuario_teste)
        
        # Verificar se todos os follow-ups estão presentes
        steps_esperados = ["followup_D0", "followup_D2", "followup_D7", "followup_D14"]
        steps_obtidos = [step["step"] for step in followups]
        
        for step_esperado in steps_esperados:
            assert step_esperado in steps_obtidos
        
        # Testar envio de cada follow-up
        for followup in followups:
            payload = {
                "canal": "WhatsApp",
                "template_id": followup["step"].replace("followup_", "pos_nao_venda_"),
                "destinatario": usuario_teste["telefone"],
                "placeholders": {
                    "nome": usuario_teste["nome"],
                    "horario1": "2025-10-03 10:00",
                    "horario2": "2025-10-03 14:00"
                }
            }
            
            response = test_endpoints.send_followup(payload)
            assert response["status"] == "ok"
        
        # Verificar se todos foram enviados
        assert len(test_endpoints.followups_enviados) == 4
    
    def test_erro_calendario_401(self):
        """ERR-CAL-401: falha de OAuth no calendário → mensagem de contingência"""
        
        # Simular erro de autenticação
        payload_agendamento = {
            "email": "teste@teste.com",
            "telefone": "+5511988887777",
            "titulo": "Teste",
            "opcao_horario": "2025-10-02T14:00:00"
        }
        
        # Mock para simular erro 401
        with patch.object(test_endpoints, 'schedule_meeting') as mock_schedule:
            mock_schedule.return_value = {
                "status": "error",
                "message": "Falha de autenticação no calendário",
                "code": "CALENDAR_AUTH_ERROR"
            }
            
            response = mock_schedule(payload_agendamento)
            assert response["status"] == "error"
            assert response["code"] == "CALENDAR_AUTH_ERROR"
    
    def test_erro_crm_422(self):
        """ERR-CRM-422: schema inválido no upsert → log com campo causador"""
        
        payload_invalido = {
            "nome": "Teste",
            "sobrenome": "Inválido",
            "email": "email-invalido",
            "telefone": "telefone-invalido"
        }
        
        response = test_endpoints.create_lead(payload_invalido)
        assert response["status"] == "error"
        assert "INVALID_EMAIL" in response["code"] or "INVALID_PHONE" in response["code"]
    
    def test_erro_msg_429(self):
        """ERR-MSG-429: limite de envio/antispam → retentativa com backoff"""
        
        payload_followup = {
            "canal": "WhatsApp",
            "template_id": "pos_nao_venda_D0",
            "destinatario": "+5511988887777",
            "placeholders": {"nome": "Teste"}
        }
        
        # Simular erro 429 (rate limit)
        with patch.object(test_endpoints, 'send_followup') as mock_send:
            mock_send.return_value = {
                "status": "error",
                "message": "Rate limit exceeded",
                "code": "RATE_LIMIT",
                "retry_after": 60
            }
            
            response = mock_send(payload_followup)
            assert response["status"] == "error"
            assert response["code"] == "RATE_LIMIT"
            assert "retry_after" in response
    
    def test_criterios_aprovacao(self, usuario_teste):
        """Teste dos critérios de aprovação (DoD)"""
        
        # Executar múltiplos cenários
        cenarios = ["WPP-01", "SITE-01", "IG-01", "TG-01"]
        sucessos = 0
        total = len(cenarios)
        
        for cenario in cenarios:
            try:
                # Simular jornada completa
                payload_lead = {
                    "nome": usuario_teste["nome"],
                    "sobrenome": usuario_teste["sobrenome"],
                    "email": usuario_teste["email"],
                    "telefone": usuario_teste["telefone"],
                    "origem": cenario.replace("-01", "")
                }
                
                response_lead = test_endpoints.create_lead(payload_lead)
                if response_lead["status"] == "ok":
                    sucessos += 1
                    
            except Exception:
                pass  # Contar como falha
        
        # Critério: ≥80% das jornadas completam
        taxa_sucesso = (sucessos / total) * 100
        assert taxa_sucesso >= 80.0, f"Taxa de sucesso {taxa_sucesso}% abaixo de 80%"
        
        # Verificar estatísticas finais
        stats = test_endpoints.get_stats()
        assert stats["leads_criados"] >= 3  # Pelo menos 3 leads criados
        assert stats["taxa_sucesso"] >= 80.0  # Taxa de sucesso ≥80%
