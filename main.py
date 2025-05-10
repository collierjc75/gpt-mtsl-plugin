from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid

app = FastAPI(title="GPT-to-GPT Messaging Relay Plugin")

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

        return {
            "status": "success",
            "message_id": message_id,
            "timestamp": timestamp
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})