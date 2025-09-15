import sys
sys.path.append('.')

try:
    from main import app
    print('✅ Aplicação importada com sucesso!')
    print('Configurações carregadas:')
    import os
    print(f'  CHATWOOT_BASE_URL: {os.getenv("CHATWOOT_BASE_URL", "Não configurado")}')
    print(f'  N8N_BASE_URL: {os.getenv("N8N_BASE_URL", "Não configurado")}')
    print(f'  OPENAI_API_KEY: {"Configurado" if os.getenv("OPENAI_API_KEY") else "Não configurado"}')
    
    print('\nEndpoints disponíveis:')
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f'  {route.methods} {route.path}')
            
except Exception as e:
    print(f'❌ Erro ao importar aplicação: {e}')
    import traceback
    traceback.print_exc()
