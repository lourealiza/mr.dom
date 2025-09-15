
from fastapi import APIRouter, Request, HTTPException
import os
import hmac
import hashlib
from ..services.chatwoot_client import chatwoot_client
from ..services.n8n_client import trigger as n8n_trigger
from ..domain.models import State
from ..domain.bot_logic import step_transition

router = APIRouter()

HMAC_SECRET = os.getenv("HMAC_SECRET", "changeme")
ACCOUNT_ID = os.getenv("ACCOUNT_ID", "changeme")

async def verify_request(req: Request) -> bool:
	body = await req.body()
	sig = req.headers.get("X-Chatwoot-Signature", "")
	mac = hmac.new(HMAC_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
	return hmac.compare_digest(sig, mac.hexdigest())

@router.post("/agentbot")
async def agentbot(req: Request):
	if not await verify_request(req):
		raise HTTPException(status_code=401, detail="invalid signature")

	payload = await req.json()

	# Extrai IDs
	account_id = payload.get("account", {}).get("id", ACCOUNT_ID)
	conv = payload.get("conversation", {})
	conversation_id = conv.get("id")

	# Eventos aceitos
	event = payload.get("event")
	if event not in {"message_created", "message_updated", "widget_triggered"}:
		return {"ignored": True}

	# Ignora mensagens que já são do tipo "outgoing"
	message = payload.get("message", {})
	if message.get("message_type") == "outgoing":
		return {"ignored": True}

	user_text = (message.get("content") or "").strip()

	# Carrega estado atual da conversa
	conv_data = await chatwoot_client.get_conversation(account_id, conversation_id)
	attrs = conv_data.get("custom_attributes") or {}
	state = State(**attrs) if attrs else State()

	# Lógica de passo → próxima mensagem e ação
	state, reply_text, action = step_transition(state, user_text)

	# Persiste novo estado
	await chatwoot_client.set_attributes(account_id, conversation_id, **state.model_dump())

	# Ações integradas
	if action == "handoff":
		await chatwoot_client.set_status(account_id, conversation_id, "open")
	elif action == "create_lead":
		await n8n_trigger("create_lead", state.model_dump())
	elif action == "schedule":
		res = await n8n_trigger("schedule_meeting", {
			"nome": state.nome,
			"email": state.email,
			"celular": state.celular,
			"horario1": state.horario1,
			"horario2": state.horario2,
			"observacoes": f"empresa={state.empresa}; ferramentas={state.ferramentas}; dor={state.dor_principal}",
		})
		if isinstance(res, dict):
			meet = res.get("link_meet")
			if meet:
				reply_text += f"\n\nLink da reunião: {meet}"

	# Responde para o usuário
	if reply_text:
		await chatwoot_client.reply(account_id, conversation_id, reply_text)

	return {"ok": True}

				payload = await req.json()

				# Extrai IDs
				account_id = payload.get("account", {}).get("id", ACCOUNT_ID)
				conv = payload.get("conversation", {})
				conversation_id = conv.get("id")

				# Eventos aceitos
				event = payload.get("event")
				if event not in {"message_created", "message_updated", "widget_triggered"}:
					return {"ignored": True}

				# Ignora mensagens que já são do tipo "outgoing"
				message = payload.get("message", {})
				if message.get("message_type") == "outgoing":
					return {"ignored": True}

				user_text = (message.get("content") or "").strip()

				# Carrega estado atual da conversa
				conv_data = await chatwoot_client.get_conversation(account_id, conversation_id)
				attrs = conv_data.get("custom_attributes") or {}
				state = State(**attrs) if attrs else State()

				# Lógica de passo → próxima mensagem e ação
				state, reply_text, action = step_transition(state, user_text)

				# Persiste novo estado
				await chatwoot_client.set_attributes(account_id, conversation_id, **state.model_dump())

				# Ações integradas
				if action == "handoff":
					await chatwoot_client.set_status(account_id, conversation_id, "open")
				elif action == "create_lead":
					await n8n_trigger("create_lead", state.model_dump())
				elif action == "schedule":
					res = await n8n_trigger("schedule_meeting", {
						"nome": state.nome,
						"email": state.email,
						"celular": state.celular,
						"horario1": state.horario1,
						"horario2": state.horario2,
						"observacoes": f"empresa={state.empresa}; ferramentas={state.ferramentas}; dor={state.dor_principal}",
					})
					if isinstance(res, dict):
						meet = res.get("link_meet")
						if meet:
							reply_text += f"\n\nLink da reunião: {meet}"

				# Responde para o usuário
				if reply_text:
					await chatwoot_client.reply(account_id, conversation_id, reply_text)

				return {"ok": True}