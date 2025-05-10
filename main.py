from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import uuid

app = FastAPI(title="GPT-to-GPT Messaging Relay Plugin")

# Agent-specific in-memory MTSL logs
agent_logs = {}

@app.post("/message/send")
async def send_message(request: Request):
    try:
        data = await request.json()
        from_agent = data.get("from_agent")
        to_agent = data.get("to_agent")
        payload = data.get("payload")

        if not from_agent or not to_agent or not payload:
            return JSONResponse(status_code=400, content={"error": "Missing required fields."})

        message_id = f"msg_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Build full MTSL message
        mtsl_message = {
            "type": "MTSL",
            "from": from_agent,
            "to": to_agent,
            "timestamp": timestamp,
            "payload": payload
        }

        # Store in logs for both sender and receiver
        for agent in [from_agent, to_agent]:
            if agent not in agent_logs:
                agent_logs[agent] = []
            agent_logs[agent].append(mtsl_message)

        return {
            "status": "success",
            "message_id": message_id,
            "timestamp": timestamp
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/registry/history/{agent}")
async def get_agent_history(agent: str):
    log = agent_logs.get(agent, [])[-50:]  # Last 50 entries
    return JSONResponse(content={"log": log})

@app.post("/registry/history/{agent}")
async def add_agent_history(agent: str, request: Request):
    try:
        data = await request.json()
        if agent not in agent_logs:
            agent_logs[agent] = []
        agent_logs[agent].append(data)
        return {"status": "added", "entries": len(agent_logs[agent])}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/openapi.yaml")
async def get_openapi():
    return FileResponse("openapi.yaml", media_type="text/yaml")

@app.get("/.well-known/ai-plugin.json")
async def get_plugin_manifest():
    return FileResponse("ai-plugin.json", media_type="application/json")
