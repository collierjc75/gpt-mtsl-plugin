import requests
from datetime import datetime

# Agent routing map
AGENT_MAP = {
    "Continuum": "https://podrelay-api.onrender.com/api/mesh/send",
    "Kai-continuum.01": "https://kai-continuum.onrender.com/api/mesh/send",
    "Aletheia": "https://aletheia-gpt.onrender.com/api/mesh/send"
}

class ConcordSessionEngine:
    def __init__(self):
        pass

    def relay(self, capsule):
        to_field = capsule.get("to")
        if not to_field:
            return {"status": "error", "reason": "Missing 'to' field"}

        # Handle single recipient or list
        targets = [to_field] if isinstance(to_field, str) else to_field
        results = []

        for target in targets:
            url = AGENT_MAP.get(target, target)
            try:
                response = requests.post(url, json=capsule, timeout=15)
                response.raise_for_status()
                results.append({
                    "target": target,
                    "resolved_url": url,
                    "status": "success",
                    "response": response.json()
                })
            except Exception as e:
                results.append({
                    "target": target,
                    "resolved_url": url,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "status": "relay_complete",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "results": results
        }
