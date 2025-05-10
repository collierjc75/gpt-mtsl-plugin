from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import uuid
import copy
import sqlite3
import json

app = FastAPI(title="GPT-to-GPT Messaging Relay Plugin")

# Initialize SQLite database
conn = sqlite3.connect("mtsl_logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
    message_id TEXT PRIMARY KEY,
    timestamp TEXT,
    from_agent TEXT,
    to_agent TEXT,
    session_id TEXT,
    payload TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS discussions (
    thread_id TEXT,
    agent TEXT,
    timestamp TEXT,
    response_type TEXT,
    content TEXT
)''')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_agent ON logs (from_agent, to_agent)')
conn.commit()

@app.post("/message/send")
async def send_message(request: Request):
    try:
        data = await request.json()
        from_agent = data.get("from_agent")
        to_agent = data.get("to_agent")
        payload = data.get("payload")
        session_id = data.get("session_id", "POD-2302")

        if not from_agent or not to_agent or not payload:
            return JSONResponse(status_code=400, content={"error": "Missing required fields."})

        message_id = f"msg_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().isoformat() + "Z"

        mtsl_message = {
            "type": "MTSL",
            "from": from_agent,
            "to": to_agent,
            "timestamp": timestamp,
            "payload": payload
        }

        cursor.execute('INSERT INTO logs (message_id, timestamp, from_agent, to_agent, session_id, payload) VALUES (?, ?, ?, ?, ?, ?)',
                       (message_id, timestamp, from_agent, to_agent, session_id, json.dumps(payload)))
        conn.commit()

        return {
            "status": "success",
            "message_id": message_id,
            "timestamp": timestamp
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/registry/self")
async def get_self_log(x_agent_id: str = Header(...)):
    try:
        cursor.execute('''SELECT timestamp, from_agent, to_agent, payload FROM logs
                          WHERE from_agent = ? OR to_agent = ? OR to_agent = "All_Agents"
                          ORDER BY timestamp DESC LIMIT 50''', (x_agent_id, x_agent_id))
        rows = cursor.fetchall()
        messages = []
        for row in rows:
            messages.append({
                "type": "MTSL",
                "timestamp": row[0],
                "from": row[1],
                "to": row[2],
                "payload": json.loads(row[3])
            })
        return JSONResponse(content={"log": messages})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/registry/discussions/{thread_id}")
async def post_discussion_entry(thread_id: str, request: Request):
    try:
        data = await request.json()
        agent = data.get("agent")
        response_type = data.get("response_type")
        content = data.get("content")
        timestamp = datetime.utcnow().isoformat() + "Z"

        cursor.execute('''INSERT INTO discussions (thread_id, agent, timestamp, response_type, content)
                          VALUES (?, ?, ?, ?, ?)''', (thread_id, agent, timestamp, response_type, content))
        conn.commit()

        return {"status": "posted", "thread_id": thread_id, "timestamp": timestamp}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/registry/discussions/{thread_id}")
async def get_discussion(thread_id: str):
    try:
        cursor.execute('''SELECT agent, timestamp, response_type, content FROM discussions
                          WHERE thread_id = ? ORDER BY timestamp ASC''', (thread_id,))
        rows = cursor.fetchall()
        responses = []
        for row in rows:
            responses.append({
                "agent": row[0],
                "timestamp": row[1],
                "response_type": row[2],
                "content": row[3]
            })
        return JSONResponse(content={"thread_id": thread_id, "responses": responses})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/openapi.yaml")
async def get_openapi():
    return FileResponse("openapi.yaml", media_type="text/yaml")

@app.get("/.well-known/ai-plugin.json")
async def get_plugin_manifest():
    return FileResponse("ai-plugin.json", media_type="application/json")
