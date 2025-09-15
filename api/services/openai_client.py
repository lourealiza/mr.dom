from openai import AsyncOpenAI
import os
import logging
from typing import Dict, Any, Optional, List
import json

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY é obrigatório")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    async def analyze_message_intent(self, message: str) -> Dict[str, Any]:
        """Analisar intenção de uma mensagem"""
        try:
            prompt = f"""
            Analise a seguinte mensagem de um cliente e determine:
            1. Intenção principal (interesse, objeção, pergunta, etc.)
            2. Nível de interesse (alto, médio, baixo)
            3. Tipo de objeção (se houver)
            4. Próximos passos recomendados
            5. Urgência (alta, média, baixa)
            
            Mensagem: "{message}"
            
            Responda em formato JSON:
            {{
                "intent": "string",
                "interest_level": "string",
                "objection_type": "string ou null",
                "next_steps": "string",
                "urgency": "string",
                "confidence": "float entre 0 e 1"
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de vendas e atendimento ao cliente."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Análise de intenção concluída: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao analisar intenção: {str(e)}")
            raise

    async def generate_response(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Gerar resposta personalizada para o cliente"""
        try:
            context_str = ""
            if context:
                context_str = f"Contexto: {json.dumps(context, ensure_ascii=False)}\n"
            
            prompt = f"""
            {context_str}
            
            Cliente disse: "{message}"
            
            Gere uma resposta profissional, amigável e persuasiva que:
            1. Reconheça a mensagem do cliente
            2. Forneça valor ou informação útil
            3. Faça uma pergunta para engajar
            4. Mantenha tom conversacional e não muito comercial
            
            Resposta:
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente de vendas experiente e amigável."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"Resposta gerada: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            raise

    async def handle_objection(self, objection: str, product_context: str) -> str:
        """Lidar com objeções específicas"""
        try:
            prompt = f"""
            Cliente apresentou a seguinte objeção: "{objection}"
            
            Contexto do produto/serviço: {product_context}
            
            Gere uma resposta que:
            1. Valide a preocupação do cliente
            2. Forneça uma solução ou benefício
            3. Use prova social ou dados quando possível
            4. Faça uma pergunta para continuar a conversa
            
            Resposta:
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em lidar com objeções de vendas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"Objeção tratada: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao lidar com objeção: {str(e)}")
            raise

    async def qualify_lead(
        self, 
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Qualificar lead baseado no histórico da conversa"""
        try:
            history_str = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in conversation_history
            ])
            
            prompt = f"""
            Baseado no histórico da conversa abaixo, qualifique o lead:
            
            {history_str}
            
            Analise e retorne em formato JSON:
            {{
                "qualification_score": "float entre 0 e 100",
                "budget_indication": "string",
                "authority_level": "string",
                "need_level": "string",
                "timeline": "string",
                "next_best_action": "string",
                "risk_factors": ["array de strings"],
                "opportunity_size": "string"
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em qualificação de leads BANT (Budget, Authority, Need, Timeline)."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Lead qualificado: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao qualificar lead: {str(e)}")
            raise

    async def generate_follow_up_message(
        self, 
        lead_info: Dict[str, Any],
        follow_up_type: str
    ) -> str:
        """Gerar mensagem de follow-up personalizada"""
        try:
            prompt = f"""
            Gere uma mensagem de follow-up do tipo "{follow_up_type}" para o seguinte lead:
            
            Informações do lead: {json.dumps(lead_info, ensure_ascii=False)}
            
            A mensagem deve:
            1. Ser personalizada baseada nas informações do lead
            2. Fornecer valor adicional
            3. Incluir uma call-to-action clara
            4. Manter tom profissional mas amigável
            5. Ser concisa (máximo 200 palavras)
            
            Mensagem:
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em follow-up de vendas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"Mensagem de follow-up gerada: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao gerar follow-up: {str(e)}")
            raise

    async def extract_contact_info(self, message: str) -> Dict[str, Any]:
        """Extrair informações de contato de uma mensagem"""
        try:
            prompt = f"""
            Extraia informações de contato da seguinte mensagem:
            
            "{message}"
            
            Retorne em formato JSON:
            {{
                "name": "string ou null",
                "email": "string ou null",
                "phone": "string ou null",
                "company": "string ou null",
                "position": "string ou null",
                "website": "string ou null"
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em extração de informações de contato."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Informações extraídas: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações: {str(e)}")
            raise
