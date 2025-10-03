#!/usr/bin/env python3
"""
Script para configurar automaticamente Redis Cloud com dados fornecidos
"""
import json
import time
from pathlib import Path

def configure_redis_cloud_auto():
    """Configuração automática do Redis Cloud"""
    
    print("Configuracao Automatica Redis Cloud - MrDom SDR")
    print("=" * 50)
    
    # Dados de conexão fornecidos pelo usuário
    redis_data = {
        "host": "redis-16295.c308.sa-east-1-1.ec2.redns.redis-cloud.com",
        "port": 16295,
        "password": "MHglAh2B2STJ2LYeKYJ1x0cfBfQlc3x1",
        "database": 0,
        "url": "redis://default:MHglAh2B2STJ2LYeKYJ1x0cfBfQlc3x1@redis-16295.c308.sa-east-1-1.ec2.redns.redis-cloud.com:16295"
    }
    
    print("Dados de conexao Redis Cloud:")
    print(f"Host: {redis_data['host']}")
    print(f"Port: {redis_data['port']}")
    print(f"Password: {redis_data['password']}")
    print(f"Database: {redis_data['database']}")
    print(f"URL: {redis_data['url']}")
    
    # Configurar arquivo de ambiente
    config_file = Path("config.env")
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar configurações Redis Cloud
        redis_cloud_section = f"""
# ====== Configuracoes Redis Cloud ======
REDIS_CLOUD_HOST={redis_data['host']}
REDIS_CLOUD_PORT={redis_data['port']}
REDIS_CLOUD_PASSWORD={redis_data['password']}
REDIS_CLOUD_DB={redis_data['database']}
REDIS_CLOUD_URL={redis_data['url']}
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
            "host": redis_data["host"],
            "port": redis_data["port"],
            "password": redis_data["password"],
            "db": redis_data["database"],
            "url": redis_data["url"]
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
            host=redis_data["host"],
            port=redis_data["port"],
            password=redis_data["password"],
            db=redis_data["database"],
            decode_responses=True,
            socket_timeout=30,
            socket_connect_timeout=30
        )
        
        # Testar ping
        start_time = time.time()
        response = r.ping()
        ping_time = (time.time() - start_time) * 1000
        
        if response:
            print(f"OK: Conexao com Redis Cloud estabelecida! ({ping_time:.2f}ms)")
            
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
                ]),
                "mrdom:trilha:users": json.dumps([
                    {
                        "id": "user_001",
                        "nome": "Ana Silva",
                        "email": "ana.silva@teste.com",
                        "telefone": "+5511988887777",
                        "origem": "WhatsApp"
                    },
                    {
                        "id": "user_002",
                        "nome": "Carlos Santos",
                        "email": "carlos@teste.com",
                        "telefone": "+5521999998888",
                        "origem": "Site"
                    }
                ])
            }
            
            for key, value in test_data.items():
                r.set(key, value, ex=3600)  # 1 hora
            
            print("OK: Dados da trilha configurados")
            
            # Teste de performance
            print("\nTestando performance...")
            
            # Teste de escrita em lote
            start_time = time.time()
            pipe = r.pipeline()
            
            for i in range(50):
                pipe.set(f"mrdom:test:perf:{i}", f"value_{i}", ex=60)
            
            pipe.execute()
            write_time = time.time() - start_time
            
            print(f"OK: 50 escritas em {write_time:.3f}s ({50/write_time:.0f} ops/s)")
            
            # Teste de leitura em lote
            start_time = time.time()
            pipe = r.pipeline()
            
            for i in range(50):
                pipe.get(f"mrdom:test:perf:{i}")
            
            results = pipe.execute()
            read_time = time.time() - start_time
            
            print(f"OK: 50 leituras em {read_time:.3f}s ({50/read_time:.0f} ops/s)")
            
            # Limpeza
            pipe = r.pipeline()
            for i in range(50):
                pipe.delete(f"mrdom:test:perf:{i}")
            pipe.execute()
            
            print("OK: Dados de teste de performance removidos")
            
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
    print("\nResumo da conexao:")
    print(f"   Host: {redis_data['host']}")
    print(f"   Port: {redis_data['port']}")
    print(f"   Database: {redis_data['database']}")
    print(f"   Ping: {ping_time:.2f}ms")
    print(f"   Write Performance: {50/write_time:.0f} ops/s")
    print(f"   Read Performance: {50/read_time:.0f} ops/s")
    
    print("\nProximos passos:")
    print("1. Execute os testes: python scripts/run-trilha-tests.py")
    print("2. Configure n8n com os dados Redis Cloud")
    print("3. Verifique a documentacao: docs/redis-cloud-setup.md")
    
    return True

if __name__ == "__main__":
    configure_redis_cloud_auto()


