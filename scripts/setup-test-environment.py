#!/usr/bin/env python3
"""
Script para configurar ambiente de teste da trilha MrDom SDR
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class TestEnvironmentSetup:
    """Configurador do ambiente de teste"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_data_dir = self.project_root / "api" / "tests" / "test_data"
        self.results_dir = self.project_root / "test_results"
        
    def setup_directories(self):
        """Cria diretórios necessários"""
        print("📁 Criando diretórios de teste...")
        
        directories = [
            self.test_data_dir,
            self.results_dir,
            self.results_dir / "logs",
            self.results_dir / "screenshots",
            self.results_dir / "exports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory}")
    
    def setup_test_data(self):
        """Configura dados de teste"""
        print("\n📊 Configurando dados de teste...")
        
        # Criar arquivo de configuração de teste
        test_config = {
            "environment": "test",
            "created_at": datetime.now().isoformat(),
            "settings": {
                "redis_host": "localhost",
                "redis_port": 6379,
                "redis_db": 0,
                "test_timeout": 30,
                "retry_attempts": 3,
                "parallel_tests": False
            },
            "test_users": [
                {
                    "id": "test_user_001",
                    "name": "Ana Silva",
                    "email": "ana.silva@teste.com",
                    "phone": "+5511988887777",
                    "company": "ACME Teste",
                    "origin": "WhatsApp"
                },
                {
                    "id": "test_user_002", 
                    "name": "Carlos Santos",
                    "email": "carlos@teste.com",
                    "phone": "+5521999998888",
                    "company": "TechStart Teste",
                    "origin": "Site"
                }
            ],
            "test_scenarios": [
                "WPP-01",
                "WPP-02", 
                "SITE-01",
                "IG-01",
                "TG-01"
            ]
        }
        
        config_file = self.test_data_dir / "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Configuração salva em: {config_file}")
    
    def setup_redis_test_data(self):
        """Configura dados de teste no Redis"""
        print("\n🔴 Configurando dados de teste no Redis...")
        
        try:
            import redis
            
            # Conectar ao Redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            
            # Testar conexão
            r.ping()
            print("  ✓ Conexão com Redis estabelecida")
            
            # Limpar dados de teste anteriores
            keys_to_clear = [
                "test:*",
                "mrdom:test:*",
                "n8n:test:*"
            ]
            
            for pattern in keys_to_clear:
                keys = r.keys(pattern)
                if keys:
                    r.delete(*keys)
                    print(f"  ✓ Limpos {len(keys)} chaves com padrão: {pattern}")
            
            # Configurar dados de teste
            test_data = {
                "test:user:001": json.dumps({
                    "name": "Ana Silva",
                    "email": "ana.silva@teste.com",
                    "phone": "+5511988887777",
                    "status": "active"
                }),
                "test:user:002": json.dumps({
                    "name": "Carlos Santos", 
                    "email": "carlos@teste.com",
                    "phone": "+5521999998888",
                    "status": "active"
                }),
                "test:scenario:WPP-01": json.dumps({
                    "name": "WhatsApp Journey",
                    "status": "ready",
                    "steps": ["opening", "qualification", "pitch", "cta", "confirmation"]
                })
            }
            
            for key, value in test_data.items():
                r.set(key, value)
            
            print(f"  ✓ Configurados {len(test_data)} dados de teste")
            
            # Configurar TTL para dados de teste (1 hora)
            for key in test_data.keys():
                r.expire(key, 3600)
            
            print("  ✓ TTL configurado para 1 hora")
            
        except ImportError:
            print("  ⚠️  Redis não instalado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "redis"], check=True)
            self.setup_redis_test_data()
            
        except redis.ConnectionError:
            print("  ❌ Erro: Redis não está rodando")
            print("     Execute: redis-server")
            return False
            
        except Exception as e:
            print(f"  ❌ Erro ao configurar Redis: {e}")
            return False
        
        return True
    
    def setup_n8n_test_workflows(self):
        """Configura workflows de teste para n8n"""
        print("\n🔗 Configurando workflows de teste n8n...")
        
        # Workflow de teste para criação de lead
        create_lead_workflow = {
            "name": "Test - Create Lead",
            "nodes": [
                {
                    "id": "webhook",
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "parameters": {
                        "path": "test/create-lead",
                        "httpMethod": "POST"
                    }
                },
                {
                    "id": "validate",
                    "name": "Validate Data",
                    "type": "n8n-nodes-base.function",
                    "parameters": {
                        "functionCode": """
                        const data = $input.first().json;
                        
                        // Validar campos obrigatórios
                        const required = ['nome', 'sobrenome', 'email', 'telefone'];
                        const missing = required.filter(field => !data[field]);
                        
                        if (missing.length > 0) {
                            return [{
                                json: {
                                    status: 'error',
                                    message: `Campos obrigatórios faltando: ${missing.join(', ')}`,
                                    code: 'MISSING_FIELDS'
                                }
                            }];
                        }
                        
                        // Validar email
                        const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
                        if (!emailRegex.test(data.email)) {
                            return [{
                                json: {
                                    status: 'error',
                                    message: 'Email inválido',
                                    code: 'INVALID_EMAIL'
                                }
                            }];
                        }
                        
                        // Normalizar telefone
                        const phone = data.telefone.replace(/\\D/g, '');
                        let normalizedPhone = '';
                        
                        if (phone.length === 11 && phone.startsWith('11')) {
                            normalizedPhone = `+55${phone}`;
                        } else if (phone.length === 10) {
                            normalizedPhone = `+5511${phone}`;
                        } else if (phone.length === 13 && phone.startsWith('55')) {
                            normalizedPhone = `+${phone}`;
                        }
                        
                        if (!normalizedPhone) {
                            return [{
                                json: {
                                    status: 'error',
                                    message: 'Telefone inválido',
                                    code: 'INVALID_PHONE'
                                }
                            }];
                        }
                        
                        return [{
                            json: {
                                ...data,
                                telefone: normalizedPhone,
                                status: 'ok',
                                message: 'lead recebido',
                                lead_id: `lead_${Date.now()}`
                            }
                        }];
                        """
                    }
                },
                {
                    "id": "response",
                    "name": "Response",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "parameters": {}
                }
            ],
            "connections": {
                "webhook": {"main": [["validate"]]},
                "validate": {"main": [["response"]]}
            }
        }
        
        # Salvar workflow
        workflow_file = self.test_data_dir / "n8n_test_workflows.json"
        with open(workflow_file, 'w', encoding='utf-8') as f:
            json.dump([create_lead_workflow], f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Workflow de teste salvo em: {workflow_file}")
        print("  💡 Importe este workflow no n8n para testes")
    
    def setup_test_scripts(self):
        """Cria scripts de teste"""
        print("\n📜 Criando scripts de teste...")
        
        scripts_dir = self.project_root / "scripts"
        
        # Script para executar testes
        run_tests_script = """#!/bin/bash
# Script para executar trilha de testes

echo "🚀 Executando Trilha de Testes MrDom SDR"
echo "========================================"

# Verificar se Redis está rodando
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis não está rodando. Iniciando..."
    redis-server --daemonize yes
    sleep 2
fi

# Executar testes
python scripts/run-trilha-tests.py "$@"

echo "✅ Testes concluídos!"
"""
        
        run_tests_file = scripts_dir / "run-tests.sh"
        with open(run_tests_file, 'w') as f:
            f.write(run_tests_script)
        
        # Tornar executável
        os.chmod(run_tests_file, 0o755)
        
        print(f"  ✓ Script de execução criado: {run_tests_file}")
        
        # Script para limpeza
        cleanup_script = """#!/bin/bash
# Script para limpeza do ambiente de teste

echo "🧹 Limpando ambiente de teste..."

# Limpar Redis
redis-cli FLUSHDB

# Limpar arquivos de resultado antigos
find test_results -name "*.json" -mtime +7 -delete
find test_results -name "*.csv" -mtime +7 -delete

echo "✅ Limpeza concluída!"
"""
        
        cleanup_file = scripts_dir / "cleanup-tests.sh"
        with open(cleanup_file, 'w') as f:
            f.write(cleanup_script)
        
        os.chmod(cleanup_file, 0o755)
        
        print(f"  ✓ Script de limpeza criado: {cleanup_file}")
    
    def setup_docker_test_environment(self):
        """Configura ambiente Docker para testes"""
        print("\n🐳 Configurando ambiente Docker para testes...")
        
        # Docker Compose para testes
        docker_compose_test = """version: '3.8'

services:
  redis-test:
    image: redis:7-alpine
    container_name: mrdom-redis-test
    ports:
      - "6380:6379"
    volumes:
      - redis_test_data:/data
    command: redis-server --appendonly yes
    networks:
      - mrdom-test-network

  n8n-test:
    image: n8nio/n8n:latest
    container_name: mrdom-n8n-test
    ports:
      - "5680:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=test123
      - N8N_HOST=localhost
      - N8N_PORT=5680
      - N8N_PROTOCOL=http
    volumes:
      - n8n_test_data:/home/node/.n8n
    networks:
      - mrdom-test-network

volumes:
  redis_test_data:
  n8n_test_data:

networks:
  mrdom-test-network:
    driver: bridge
"""
        
        docker_file = self.project_root / "docker-compose.test.yml"
        with open(docker_file, 'w') as f:
            f.write(docker_compose_test)
        
        print(f"  ✓ Docker Compose de teste criado: {docker_file}")
        print("  💡 Execute: docker-compose -f docker-compose.test.yml up -d")
    
    def verify_environment(self):
        """Verifica se o ambiente está configurado corretamente"""
        print("\n🔍 Verificando ambiente...")
        
        checks = [
            ("Diretórios de teste", self.test_data_dir.exists()),
            ("Diretório de resultados", self.results_dir.exists()),
            ("Arquivo de configuração", (self.test_data_dir / "test_config.json").exists()),
            ("Workflows n8n", (self.test_data_dir / "n8n_test_workflows.json").exists()),
            ("Docker Compose", (self.project_root / "docker-compose.test.yml").exists())
        ]
        
        all_ok = True
        for check_name, check_result in checks:
            status = "✓" if check_result else "❌"
            print(f"  {status} {check_name}")
            if not check_result:
                all_ok = False
        
        # Verificar Redis
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            print("  ✓ Redis conectado")
        except:
            print("  ❌ Redis não conectado")
            all_ok = False
        
        return all_ok
    
    def run_setup(self):
        """Executa configuração completa"""
        print("🚀 Configurando Ambiente de Teste MrDom SDR")
        print("=" * 50)
        
        try:
            self.setup_directories()
            self.setup_test_data()
            
            redis_ok = self.setup_redis_test_data()
            if not redis_ok:
                print("\n⚠️  Redis não configurado. Continue manualmente.")
            
            self.setup_n8n_test_workflows()
            self.setup_test_scripts()
            self.setup_docker_test_environment()
            
            print("\n" + "=" * 50)
            print("✅ CONFIGURAÇÃO CONCLUÍDA!")
            print("=" * 50)
            
            # Verificar ambiente
            if self.verify_environment():
                print("\n🎉 Ambiente de teste configurado com sucesso!")
                print("\n📋 PRÓXIMOS PASSOS:")
                print("1. Inicie o Redis: redis-server")
                print("2. Execute os testes: python scripts/run-trilha-tests.py")
                print("3. Para ambiente Docker: docker-compose -f docker-compose.test.yml up -d")
            else:
                print("\n⚠️  Alguns componentes não foram configurados corretamente.")
                print("   Verifique os erros acima e execute novamente.")
            
        except Exception as e:
            print(f"\n❌ Erro durante configuração: {e}")
            return False
        
        return True

def main():
    """Função principal"""
    setup = TestEnvironmentSetup()
    success = setup.run_setup()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
