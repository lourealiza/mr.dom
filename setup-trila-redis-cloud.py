#!/usr/bin/env python3
"""
Configurar dados da trilha de testes no Redis Cloud
"""
import redis
import json
import time

def setup_trilha_data():
    """Configura dados da trilha no Redis Cloud"""
    
    print("Configurando dados da trilha no Redis Cloud")
    print("=" * 50)
    
    # Dados de conexão
    host = "redis-16295.c308.sa-east-1-1.ec2.redns.redis-cloud.com"
    port = 16295
    password = "MHglAh2B2STJ2LYeKYJ1x0cfBfQlc3x1"
    database = 0
    
    try:
        # Conectar ao Redis Cloud
        r = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=database,
            decode_responses=True,
            socket_timeout=30,
            socket_connect_timeout=30
        )
        
        # Testar conexão
        if not r.ping():
            print("ERRO: Falha na conexao com Redis Cloud")
            return False
        
        print("OK: Conectado ao Redis Cloud")
        
        # Dados da trilha
        trilha_data = {
            "mrdom:trilha:status": "active",
            "mrdom:trilha:version": "1.0.0",
            "mrdom:trilha:created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "mrdom:trilha:scenarios": json.dumps([
                "WPP-01", "WPP-02", "SITE-01", "IG-01", "TG-01"
            ]),
            "mrdom:trilha:validation_tests": json.dumps([
                "VAL-E-MAIL-01", "VAL-FONE-01", "VAL-OBRIG-01"
            ]),
            "mrdom:trilha:n8n_tests": json.dumps([
                "N8N-CL-01", "N8N-AG-01", "N8N-LOG-01", "N8N-FU-01"
            ]),
            "mrdom:trilha:followup_tests": json.dumps([
                "CAD-D0", "CAD-D2", "CAD-D7", "CAD-D14"
            ])
        }
        
        # Usuários de teste
        usuarios_teste = [
            {
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
                "principal_dor": "Pos-nao-venda inexistente",
                "origem": "WhatsApp",
                "fuso": "America/Sao_Paulo"
            },
            {
                "id": "user_002",
                "nome": "Carlos",
                "sobrenome": "Santos",
                "empresa": "TechStart Ltda",
                "cargo": "CEO",
                "email": "carlos@techstart.com.br",
                "telefone": "+5521999998888",
                "segmento": "Startup",
                "tamanho_time": 3,
                "ferramentas_crm": "HubSpot",
                "ferramentas_marketing": "Mailchimp",
                "canais_mensageria": "WhatsApp",
                "principal_dor": "Falta de automacao",
                "origem": "Site",
                "fuso": "America/Sao_Paulo"
            },
            {
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
                "principal_dor": "Qualificacao de leads",
                "origem": "Instagram",
                "fuso": "America/Sao_Paulo"
            }
        ]
        
        # Configurar dados da trilha
        print("\nConfigurando dados da trilha...")
        for key, value in trilha_data.items():
            r.set(key, value, ex=86400)  # 24 horas
            print(f"  OK: {key}")
        
        # Configurar usuários de teste
        print("\nConfigurando usuarios de teste...")
        for usuario in usuarios_teste:
            user_key = f"mrdom:user:{usuario['id']}"
            r.hset(user_key, mapping=usuario)
            r.expire(user_key, 86400)  # 24 horas
            print(f"  OK: {usuario['nome']} {usuario['sobrenome']}")
        
        # Configurar cenários de teste
        print("\nConfigurando cenarios de teste...")
        cenarios = {
            "WPP-01": {
                "descricao": "WhatsApp -> jornada completa",
                "usuario": "user_001",
                "canal": "WhatsApp",
                "fluxo": ["opening", "qualificacao", "pitch", "cta_agenda", "confirmacao"]
            },
            "SITE-01": {
                "descricao": "Widget do site -> jornada completa",
                "usuario": "user_002",
                "canal": "Site",
                "fluxo": ["opening", "qualificacao", "pitch", "cta_agenda", "confirmacao"]
            },
            "IG-01": {
                "descricao": "Instagram DM -> origem preservada",
                "usuario": "user_003",
                "canal": "Instagram",
                "origem_esperada": "Instagram"
            }
        }
        
        for cenario_id, cenario_data in cenarios.items():
            scenario_key = f"mrdom:scenario:{cenario_id}"
            # Converter dados para string se necessário
            for key, value in cenario_data.items():
                if isinstance(value, list):
                    cenario_data[key] = json.dumps(value)
            r.hset(scenario_key, mapping=cenario_data)
            r.expire(scenario_key, 86400)  # 24 horas
            print(f"  OK: {cenario_id}")
        
        # Configurar templates de mensagem
        print("\nConfigurando templates de mensagem...")
        templates = {
            "opening": "Ola {{nome}}! Sou o assistente virtual da MrDom. Posso fazer 3 perguntas rapidas?",
            "qualificacao_perguntas": json.dumps([
                "Qual e o tamanho da sua empresa?",
                "Qual ferramenta de CRM voces usam atualmente?",
                "Qual e o principal desafio na gestao de leads?"
            ]),
            "pitch_geral": "Baseado nas suas respostas, a MrDom pode ajudar com {{principal_dor}}.",
            "cta_agenda": "Que tal agendarmos uma conversa de 30 minutos? Tenho disponivel: {{horario1}} ou {{horario2}}.",
            "confirmacao_agendada": "Perfeito {{nome}}! Seu agendamento esta confirmado para {{data}} as {{horario}}.",
            "pos_nao_venda_D0": "Oi {{nome}}! Entendo que voce precisa pensar. Que tal tentarmos novamente?",
            "pos_nao_venda_D2": "{{nome}}, como esta? Ainda temos disponivel: {{horario1}} ou {{horario2}}.",
            "pos_nao_venda_D7": "{{nome}}, tudo bem? Nao desista da oportunidade!",
            "pos_nao_venda_D14": "Ultima tentativa, {{nome}}! Ultimos horarios: {{horario1}} ou {{horario2}}."
        }
        
        for template_id, template_content in templates.items():
            template_key = f"mrdom:template:{template_id}"
            r.set(template_key, template_content, ex=86400)  # 24 horas
            print(f"  OK: {template_id}")
        
        # Configurar horários disponíveis
        print("\nConfigurando horarios disponiveis...")
        horarios = {
            "2025-10-02": ["10:00", "14:00"],
            "2025-10-03": ["09:00", "11:00", "15:00"],
            "2025-10-04": ["10:00", "14:00", "16:00"]
        }
        
        for data, horarios_list in horarios.items():
            horarios_key = f"mrdom:horarios:{data}"
            r.set(horarios_key, json.dumps(horarios_list), ex=86400)  # 24 horas
            print(f"  OK: {data} - {len(horarios_list)} horarios")
        
        # Estatísticas finais
        print("\n" + "=" * 50)
        print("CONFIGURACAO CONCLUIDA!")
        print("=" * 50)
        
        # Contar dados configurados
        trilha_keys = r.keys("mrdom:trilha:*")
        user_keys = r.keys("mrdom:user:*")
        scenario_keys = r.keys("mrdom:scenario:*")
        template_keys = r.keys("mrdom:template:*")
        horarios_keys = r.keys("mrdom:horarios:*")
        
        print(f"Dados da trilha: {len(trilha_keys)}")
        print(f"Usuarios de teste: {len(user_keys)}")
        print(f"Cenarios de teste: {len(scenario_keys)}")
        print(f"Templates: {len(template_keys)}")
        print(f"Horarios: {len(horarios_keys)}")
        
        print("\nProximos passos:")
        print("1. Execute os testes: python scripts/run-trilha-tests.py")
        print("2. Configure n8n com Redis Cloud")
        print("3. Verifique a documentacao: docs/trilha-testes.md")
        
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    setup_trilha_data()
