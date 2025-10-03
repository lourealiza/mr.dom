#!/usr/bin/env python3
"""
Script para configurar conexão com Redis Cloud
"""
import os
import json
from pathlib import Path

def configure_redis_cloud():
    """Configura conexão com Redis Cloud"""
    
    print("Configuracao Redis Cloud - MrDom SDR")
    print("=" * 50)
    
    print("\nPara obter os dados de conexao:")
    print("1. Acesse: https://cloud.redis.io/")
    print("2. Faca login com sua conta GitHub")
    print("3. Va para o dashboard da sua conta")
    print("4. Clique em 'Databases' ou 'My Databases'")
    print("5. Selecione sua database")
    print("6. Copie os dados de conexao")
    
    print("\nDados necessarios:")
    print("- Host/Endpoint (ex: redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com)")
    print("- Port (ex: 12345)")
    print("- Password (senha gerada automaticamente)")
    print("- Database (geralmente 0)")
    
    # Solicitar dados do usuário
    print("\nInsira os dados de conexao:")
    
    host = input("Host/Endpoint: ").strip()
    port = input("Port: ").strip()
    password = input("Password: ").strip()
    database = input("Database (padrão 0): ").strip() or "0"
    
    if not all([host, port, password]):
        print("ERRO: Todos os campos sao obrigatorios!")
        return False
    
    # Configurar variáveis de ambiente
    env_vars = {
        "REDIS_CLOUD_HOST": host,
        "REDIS_CLOUD_PORT": port,
        "REDIS_CLOUD_PASSWORD": password,
        "REDIS_CLOUD_DB": database,
        "REDIS_CLOUD_URL": f"redis://:{password}@{host}:{port}/{database}"
    }
    
    # Atualizar config.env
    config_file = Path("config.env")
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar ou atualizar configurações Redis Cloud
        redis_section = """
# ====== Configurações Redis Cloud ======
REDIS_CLOUD_HOST={host}
REDIS_CLOUD_PORT={port}
REDIS_CLOUD_PASSWORD={password}
REDIS_CLOUD_DB={database}
REDIS_CLOUD_URL={redis_url}
""".format(
            host=host,
            port=port,
            password=password,
            database=database,
            redis_url=env_vars["REDIS_CLOUD_URL"]
        )
        
        # Remover seção anterior se existir
        lines = content.split('\n')
        new_lines = []
        skip_redis_cloud = False
        
        for line in lines:
            if line.startswith("# ====== Configurações Redis Cloud ======"):
                skip_redis_cloud = True
                continue
            elif skip_redis_cloud and line.startswith("# ======"):
                skip_redis_cloud = False
                new_lines.append(redis_section.strip())
                new_lines.append(line)
            elif not skip_redis_cloud:
                new_lines.append(line)
        
        if not skip_redis_cloud:
            new_lines.append(redis_section.strip())
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"OK: Configuracoes salvas em: {config_file}")
    
    # Criar arquivo de configuração específico para testes
    test_config = {
        "redis_cloud": {
            "host": host,
            "port": int(port),
            "password": password,
            "db": int(database),
            "url": env_vars["REDIS_CLOUD_URL"]
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
        
        # Conectar ao Redis Cloud
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
            r.set("test:connection", "MrDom SDR Test", ex=60)
            value = r.get("test:connection")
            
            if value == "MrDom SDR Test":
                print("OK: Operacoes de leitura/escrita funcionando!")
                r.delete("test:connection")
            else:
                print("AVISO: Problema nas operacoes de leitura/escrita")
            
            # Configurar dados de teste
            test_data = {
                "mrdom:test:setup": "Redis Cloud configurado",
                "mrdom:test:timestamp": str(int(time.time())),
                "mrdom:test:version": "1.0.0"
            }
            
            for key, value in test_data.items():
                r.set(key, value, ex=3600)  # 1 hora
            
            print("OK: Dados de teste configurados")
            
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
    print("3. Verifique a documentacao: docs/trilha-testes.md")
    
    return True

if __name__ == "__main__":
    import time
    configure_redis_cloud()
