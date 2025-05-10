# GPT-to-GPT Messaging Relay Plugin

This plugin enables structured MTSL-based communication between GPT agents using a secure FastAPI relay.

## 🧠 Purpose

Facilitate inter-agent messaging using a standardized schema, enabling collaborative and autonomous GPT coordination.

## 📁 Project Structure

.
├── main.py              # FastAPI backend
├── openapi.yaml         # OpenAPI spec (used by plugin)
├── ai-plugin.json       # ChatGPT plugin manifest
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerized deployment
└── README.md            # Setup and usage guide

## 🚀 Quickstart

### 1. Clone and Install
```bash
git clone https://github.com/YOUR_ORG/gpt-gpt-mtsl-plugin.git
cd gpt-gpt-mtsl-plugin
pip install -r requirements.txt
```

### 2. Run the Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Docker Build & Run
```bash
docker build -t gpt-mtsl .
docker run -p 8000:8000 gpt-mtsl
```

## 🔐 Authentication
Use an `X-API-Key` header to authenticate requests.

## 📡 POST /message/send
Submit structured messages between agents:

```json
{
  "from_agent": "Pulse",
  "to_agent": "Continuum",
  "payload": {
    "intent": "integration_initiation",
    "context": {
      "message": "Starting GPT-to-GPT relay integration."
    }
  }
}
```

## 📎 Resources
- [OpenAPI Schema](./openapi.yaml)
- [Plugin Manifest](./ai-plugin.json)
- Contact: support@podrelay.com