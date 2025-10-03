#!/usr/bin/env python3
"""
Script para configuração manual do Redis Cloud
"""
import json
import os
from pathlib import Path

def setup_redis_cloud_manual():
    """Configuração manual do Redis Cloud"""
    
    print("Configuracao Manual Redis Cloud - MrDom SDR")
    print("=" * 50)
    
    print("\nSe voce nao consegue fazer login no Redis Cloud com GitHub,")
    print("voce pode configurar manualmente usando os dados abaixo:")
    
    print("\n" + "="*50)
    print("DADOS DE CONEXAO REDIS CLOUD")
    print("="*50)
    
    # Dados de exemplo (você deve substituir pelos seus dados reais)
    redis_data = {
        "host": "redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com",
        "port": 12345,
        "password": "sua_senha_aqui",
        "database": 0,
        "url": "redis://:sua_senha_aqui@redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com:12345/0"
    }
    
    print(f"Host: {redis_data['host']}")
    print(f"Port: {redis_data['port']}")
    print(f"Password: {redis_data['password']}")
    print(f"Database: {redis_data['database']}")
    print(f"URL: {redis_data['url']}")
    
    print("\n" + "="*50)
    print("COMO OBTER SEUS DADOS REAIS")
    print("="*50)
    
    print("\n1. Acesse: https://cloud.redis.io/")
    print("2. Tente fazer login com GitHub")
    print("3. Se nao funcionar, tente criar conta com email")
    print("4. No dashboard, va para 'Databases'")
    print("5. Clique em 'New Database' ou selecione uma existente")
    print("6. Copie os dados de conexao")
    
    print("\n" + "="*50)
    print("CONFIGURACAO AUTOMATICA")
    print("="*50)
    
    # Solicitar dados do usuário
    print("\nInsira seus dados de conexao Redis Cloud:")
    
    host = input("Host/Endpoint: ").strip()
    port = input("Port: ").strip()
    password = input("Password: ").strip()
    database = input("Database (padrao 0): ").strip() or "0"
    
    if not all([host, port, password]):
        print("ERRO: Todos os campos sao obrigatorios!")
        return False
    
    # Configurar arquivo de ambiente
    config_file = Path("config.env")
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar configurações Redis Cloud
        redis_cloud_section = f"""
# ====== Configuracoes Redis Cloud ======
REDIS_CLOUD_HOST={host}
REDIS_CLOUD_PORT={port}
REDIS_CLOUD_PASSWORD={password}
REDIS_CLOUD_DB={database}
REDIS_CLOUD_URL=redis://:{password}@{host}:{port}/{database}
"""
        
        # Verificar se já existe configuração Redis Cloud
        if "REDIS_CLOUD_HOST" in content:
            print("AVISO: Configuracao Redis Cloud ja existe. Atualizando...")
            # Remover configuração anterior
            lines = content.split('\n')
            new_lines = []
            skip_redis_cloud = False
            
            for line in lines:
                if line.startswith("# ====== Configuracoes Redis Cloud ======"):
                    skip_redis_cloud = True
                    continue
                elif skip_redis_cloud and line.startswith("# ======"):
                    skip_redis_cloud = False
                    new_lines.append(redis_cloud_section.strip())
                    new_lines.append(line)
                elif not skip_redis_cloud:
                    new_lines.append(line)
            
            if not skip_redis_cloud:
                new_lines.append(redis_cloud_section.strip())
            
            content = '\n'.join(new_lines)
        else:
            content += redis_cloud_section
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"OK: Configuracoes salvas em: {config_file}")
    
    # Criar arquivo de configuração para testes
    test_config = {
        "redis_cloud": {
            "host": host,
            "port": int(port),
            "password": password,
            "db": int(database),
            "url": f"redis://:{password}@{host}:{port}/{database}"
        },
        "test_settings": {
            "timeout": 30,
            "retry_attempts": 3,
            "connection_pool_size": 10
        }
    }
    
    test_config_file = Path("api/tests/test_data/redis_cloud_config.json")
    test_config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(test_config_file, 'w', encoding='utf-8') as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)
    
    print(f"OK: Configuracao de teste salva em: {test_config_file}")
    
    # Testar conexão
    print("\nTestando conexao...")
    
    try:
        import redis
        
        r = redis.Redis(
            host=host,
            port=int(port),
            password=password,
            db=int(database),
            decode_responses=True,
            socket_timeout=30,
            socket_connect_timeout=30
        )
        
        # Testar ping
        response = r.ping()
        if response:
            print("OK: Conexao com Redis Cloud estabelecida!")
            
            # Testar operações básicas
            r.set("mrdom:test:connection", "MrDom SDR Test", ex=60)
            value = r.get("mrdom:test:connection")
            
            if value == "MrDom SDR Test":
                print("OK: Operacoes de leitura/escrita funcionando!")
                r.delete("mrdom:test:connection")
            else:
                print("AVISO: Problema nas operacoes de leitura/escrita")
            
            # Configurar dados de teste da trilha
            test_data = {
                "mrdom:trilha:status": "active",
                "mrdom:trilha:version": "1.0.0",
                "mrdom:trilha:scenarios": json.dumps([
                    "WPP-01", "WPP-02", "SITE-01", "IG-01", "TG-01"
                ])
            }
            
            for key, value in test_data.items():
                r.set(key, value, ex=3600)  # 1 hora
            
            print("OK: Dados da trilha configurados")
            
        else:
            print("ERRO: Falha no ping do Redis Cloud")
            return False
            
    except ImportError:
        print("AVISO: Redis nao instalado. Instalando...")
        import subprocess
        subprocess.run(["pip", "install", "redis"], check=True)
        print("OK: Redis instalado. Execute o script novamente.")
        return False
        
    except redis.ConnectionError as e:
        print(f"ERRO: Erro de conexao: {e}")
        print("\nVerifique:")
        print("- Host e port estao corretos")
        print("- Password esta correto")
        print("- Database existe")
        print("- Firewall permite conexao")
        return False
        
    except Exception as e:
        print(f"ERRO: Erro inesperado: {e}")
        return False
    
    print("\nSUCESSO: Configuracao Redis Cloud concluida!")
    print("\nProximos passos:")
    print("1. Execute os testes: python scripts/run-trilha-tests.py")
    print("2. Configure n8n com os dados Redis Cloud")
    print("3. Verifique a documentacao: docs/redis-cloud-setup.md")
    
    return True

if __name__ == "__main__":
    setup_redis_cloud_manual()
