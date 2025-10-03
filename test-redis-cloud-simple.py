#!/usr/bin/env python3
"""
Teste simples de conexão Redis Cloud
"""
import redis
import json

def test_redis_cloud():
    """Testa conexão com Redis Cloud"""
    
    print("Teste de Conexao Redis Cloud")
    print("=" * 40)
    
    # Dados de conexão
    host = "redis-16295.c308.sa-east-1-1.ec2.redns.redis-cloud.com"
    port = 16295
    password = "MHglAh2B2STJ2LYeKYJ1x0cfBfQlc3x1"
    database = 0
    
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {database}")
    
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
        
        # Testar ping
        print("\nTestando ping...")
        response = r.ping()
        
        if response:
            print("OK: Ping funcionando!")
            
            # Testar operações básicas
            print("\nTestando operacoes basicas...")
            
            # SET/GET
            r.set("mrdom:test", "MrDom SDR Test", ex=60)
            value = r.get("mrdom:test")
            
            if value == "MrDom SDR Test":
                print("OK: SET/GET funcionando!")
                r.delete("mrdom:test")
            else:
                print("ERRO: SET/GET falhou")
            
            # Hash
            hash_data = {
                "nome": "Ana Silva",
                "email": "ana@teste.com",
                "telefone": "+5511988887777"
            }
            
            r.hset("mrdom:test:hash", mapping=hash_data)
            retrieved_hash = r.hgetall("mrdom:test:hash")
            
            if retrieved_hash == hash_data:
                print("OK: Hash funcionando!")
                r.delete("mrdom:test:hash")
            else:
                print("ERRO: Hash falhou")
            
            # List
            list_data = ["opening", "qualification", "pitch", "cta", "confirmation"]
            r.lpush("mrdom:test:list", *list_data)
            retrieved_list = r.lrange("mrdom:test:list", 0, -1)
            
            if retrieved_list == list_data:
                print("OK: List funcionando!")
                r.delete("mrdom:test:list")
            else:
                print("ERRO: List falhou")
            
            print("\nSUCESSO: Redis Cloud configurado e funcionando!")
            
        else:
            print("ERRO: Ping falhou")
            
    except redis.ConnectionError as e:
        print(f"ERRO: Erro de conexao: {e}")
        
    except Exception as e:
        print(f"ERRO: Erro inesperado: {e}")

if __name__ == "__main__":
    test_redis_cloud()


