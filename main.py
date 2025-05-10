from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import uuid

app = FastAPI(title="GPT-to-GPT Messaging Relay Plugin")

message_log = []  # In-memory log store

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

        # Log the message
        message_log.append({
            "timestamp": timestamp,
            "from": from_agent,
            "to": to_agent,
            "intent": payload.get("intent", "unspecified"),
            "summary": payload.get("context", {}).get("message", "") or payload.get("message", "")
        })

        return {
            "status": "success",
            "message_id": message_id,
            "timestamp": timestamp
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/registry/history")
async def get_history():
    return JSONResponse(content={"log": message_log[-50:]})

@app.post("/registry/history")
async def add_history(request: Request):
    try:
        data = await request.json()
        message_log.append(data)
        return {"status": "added", "entries": len(message_log)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/openapi.yaml")
async def get_openapi():
    return FileResponse("openapi.yaml", media_type="text/yaml")

@app.get("/.well-known/ai-plugin.json")
async def get_plugin_manifest():
    return FileResponse("ai-plugin.json", media_type="application/json")
