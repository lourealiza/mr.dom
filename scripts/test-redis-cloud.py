#!/usr/bin/env python3
"""
Script para testar conexão com Redis Cloud
"""
import json
import time
from pathlib import Path

def test_redis_cloud_connection():
    """Testa conexão com Redis Cloud"""
    
    print("🧪 Teste de Conexão Redis Cloud")
    print("=" * 40)
    
    # Carregar configuração
    config_file = Path("api/tests/test_data/redis_cloud_config.json")
    
    if not config_file.exists():
        print("❌ Arquivo de configuração não encontrado!")
        print("   Execute primeiro: python scripts/configure-redis-cloud.py")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        redis_config = config["redis_cloud"]
        
        print(f"📡 Conectando a: {redis_config['host']}:{redis_config['port']}")
        
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return False
    
    # Testar conexão
    try:
        import redis
        
        r = redis.Redis(
            host=redis_config["host"],
            port=redis_config["port"],
            password=redis_config["password"],
            db=redis_config["db"],
            decode_responses=True,
            socket_timeout=30,
            socket_connect_timeout=30
        )
        
        # Teste 1: Ping
        print("\n1️⃣ Testando Ping...")
        start_time = time.time()
        response = r.ping()
        ping_time = (time.time() - start_time) * 1000
        
        if response:
            print(f"✅ Ping OK ({ping_time:.2f}ms)")
        else:
            print("❌ Ping falhou")
            return False
        
        # Teste 2: Operações básicas
        print("\n2️⃣ Testando operações básicas...")
        
        # SET/GET
        test_key = "mrdom:test:basic"
        test_value = f"Teste MrDom SDR - {int(time.time())}"
        
        r.set(test_key, test_value, ex=60)
        retrieved_value = r.get(test_key)
        
        if retrieved_value == test_value:
            print("✅ SET/GET funcionando")
        else:
            print("❌ SET/GET falhou")
            return False
        
        # Teste 3: Estruturas de dados
        print("\n3️⃣ Testando estruturas de dados...")
        
        # Hash
        hash_key = "mrdom:test:hash"
        hash_data = {
            "nome": "Ana Silva",
            "email": "ana@teste.com",
            "telefone": "+5511988887777",
            "origem": "WhatsApp"
        }
        
        r.hset(hash_key, mapping=hash_data)
        retrieved_hash = r.hgetall(hash_key)
        
        if retrieved_hash == hash_data:
            print("✅ Hash funcionando")
        else:
            print("❌ Hash falhou")
            return False
        
        # List
        list_key = "mrdom:test:list"
        list_data = ["opening", "qualification", "pitch", "cta", "confirmation"]
        
        r.delete(list_key)  # Limpar
        r.lpush(list_key, *list_data)
        retrieved_list = r.lrange(list_key, 0, -1)
        
        if retrieved_list == list_data:
            print("✅ List funcionando")
        else:
            print("❌ List falhou")
            return False
        
        # Set
        set_key = "mrdom:test:set"
        set_data = {"WhatsApp", "Site", "Instagram", "Telegram"}
        
        r.delete(set_key)  # Limpar
        r.sadd(set_key, *set_data)
        retrieved_set = r.smembers(set_key)
        
        if retrieved_set == set_data:
            print("✅ Set funcionando")
        else:
            print("❌ Set falhou")
            return False
        
        # Teste 4: Performance
        print("\n4️⃣ Testando performance...")
        
        # Teste de escrita em lote
        start_time = time.time()
        pipe = r.pipeline()
        
        for i in range(100):
            pipe.set(f"mrdom:test:perf:{i}", f"value_{i}", ex=60)
        
        pipe.execute()
        write_time = time.time() - start_time
        
        print(f"✅ 100 escritas em {write_time:.3f}s ({100/write_time:.0f} ops/s)")
        
        # Teste de leitura em lote
        start_time = time.time()
        pipe = r.pipeline()
        
        for i in range(100):
            pipe.get(f"mrdom:test:perf:{i}")
        
        results = pipe.execute()
        read_time = time.time() - start_time
        
        print(f"✅ 100 leituras em {read_time:.3f}s ({100/read_time:.0f} ops/s)")
        
        # Teste 5: Dados específicos da trilha
        print("\n5️⃣ Configurando dados da trilha de testes...")
        
        # Dados de teste da trilha
        trilha_data = {
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
        
        for key, value in trilha_data.items():
            r.set(key, value, ex=3600)  # 1 hora
        
        print("✅ Dados da trilha configurados")
        
        # Teste 6: Limpeza
        print("\n6️⃣ Limpando dados de teste...")
        
        test_keys = [
            test_key,
            hash_key,
            list_key,
            set_key
        ]
        
        # Adicionar chaves de performance
        for i in range(100):
            test_keys.append(f"mrdom:test:perf:{i}")
        
        deleted_count = r.delete(*test_keys)
        print(f"✅ {deleted_count} chaves de teste removidas")
        
        # Manter dados da trilha
        print("✅ Dados da trilha mantidos")
        
        print("\n🎉 Todos os testes passaram!")
        print("\n📊 Resumo da conexão:")
        print(f"   Host: {redis_config['host']}")
        print(f"   Port: {redis_config['port']}")
        print(f"   Database: {redis_config['db']}")
        print(f"   Ping: {ping_time:.2f}ms")
        print(f"   Write Performance: {100/write_time:.0f} ops/s")
        print(f"   Read Performance: {100/read_time:.0f} ops/s")
        
        return True
        
    except ImportError:
        print("❌ Redis não instalado!")
        print("   Execute: pip install redis")
        return False
        
    except redis.ConnectionError as e:
        print(f"❌ Erro de conexão: {e}")
        print("\n🔍 Verifique:")
        print("- Host e port estão corretos")
        print("- Password está correto")
        print("- Database existe")
        print("- Firewall permite conexão")
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    test_redis_cloud_connection()
