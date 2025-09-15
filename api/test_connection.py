import os
from dotenv import load_dotenv
import httpx
import asyncio

# Carregar variáveis de ambiente
load_dotenv('../config.env')

async def test_chatwoot():
    base_url = os.getenv('CHATWOOT_BASE_URL')
    token = os.getenv('CHATWOOT_ACCESS_TOKEN')
    account_id = os.getenv('CHATWOOT_ACCOUNT_ID')
    
    print(f'Base URL: {base_url}')
    print(f'Account ID: {account_id}')
    print(f'Token: {token[:10] if token else "None"}...')
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'{base_url}/api/v1/accounts/{account_id}',
                headers=headers
            )
            print(f'Status: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                print(f'Account Name: {data.get("name", "N/A")}')
                print('✅ Conexão com Chatwoot OK!')
            else:
                print(f'❌ Erro: {response.text}')
        except Exception as e:
            print(f'❌ Erro de conexão: {e}')

async def test_n8n():
    base_url = os.getenv('N8N_BASE_URL')
    api_key = os.getenv('N8N_API_KEY')
    
    print(f'\nN8N Base URL: {base_url}')
    print(f'N8N API Key: {api_key[:20] if api_key else "None"}...')
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    if api_key:
        headers['X-N8N-API-KEY'] = api_key
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'{base_url}/api/v1/workflows',
                headers=headers
            )
            print(f'N8N Status: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                print(f'Workflows encontrados: {len(data.get("data", []))}')
                print('✅ Conexão com N8N OK!')
            else:
                print(f'❌ Erro N8N: {response.text}')
        except Exception as e:
            print(f'❌ Erro de conexão N8N: {e}')

if __name__ == "__main__":
    asyncio.run(test_chatwoot())
    asyncio.run(test_n8n())
