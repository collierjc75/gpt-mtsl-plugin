from fastapi import FastAPI, Request
from concord_session_engine import ConcordSessionEngine
from datetime import datetime

app = FastAPI(title="GPT MTSL Dispatch Plugin", version="1.1")

engine = ConcordSessionEngine()

@app.get("/health")
def health():
    return {"status": "OK", "timestamp": datetime.utcnow().isoformat() + "Z"}

@app.post("/dispatch")
async def dispatch(request: Request):
    try:
        capsule = await request.json()
        required = {"type", "timestamp", "from", "to", "intent", "payload", "ttl"}
        if not required.issubset(capsule):
            return {"status": "error", "reason": "Missing required MTSL fields", "timestamp": datetime.utcnow().isoformat() + "Z"}

        result = engine.relay(capsule)
        return {
            "status": "ok",
            "dispatch_result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
