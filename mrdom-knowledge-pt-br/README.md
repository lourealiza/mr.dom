# Mr. DOM — Pacote de Vector Store

Este pacote contém:
- `files/` — arquivos originais (PDF/DOCX/JSON)
- `mrdom_knowledge_chunks.jsonl` — chunks de conhecimento com metadados (pronto para ingestão)
- `mrdom_tfidf.joblib` e `mrdom_index_mapping.json` — índice TF‑IDF local para testes (opcional)
- `upload_openai.py` — script de exemplo para criar **Vector Store** na OpenAI e subir os arquivos
- `query_local_tfidf.py` — exemplo de busca local (sem dependência de modelos)
- `README.md` — este guia

## Uso — OpenAI (Assistants / File Search / Vector Store)

1. Defina suas variáveis de ambiente:
   ```bash
   export OPENAI_API_KEY="sk-..."
   export OPENAI_ORG_ID="org_..."
   export OPENAI_PROJECT_ID="proj_..."    # se aplicável
   export ASSISTANT_ID=""                 # opcional; se vazio, o script só cria o vector store
   ```

2. Instale dependências mínimas:
   ```bash
   pip install --upgrade openai python-dotenv
   ```

3. Execute o upload:
   ```bash
   python upload_openai.py --name "mrdom-knowledge-pt-br" --path ./files
   ```

O script cria um **Vector Store** e envia todos os arquivos da pasta `files/`. Se você fornecer `--assistant-id`, ele **anexa** o vector store ao Assistant.

> Observação: a OpenAI realiza a chunkificação e embeddings. Você não precisa subir o JSONL para a OpenAI; ele serve para auditoria/portabilidade.

## Uso — Busca local (debug)

Instale dependências (opcional):
```bash
pip install scikit-learn joblib
```

Rode o exemplo:
```bash
python query_local_tfidf.py "automação de follow-up no CRM"
```

O retorno lista os chunks mais similares via TF‑IDF para debug rápido.

---

Gerado em: 2025-09-17T02:03:47
