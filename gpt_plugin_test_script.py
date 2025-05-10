
import requests
import datetime

# Your plugin API endpoint
url = "https://api.podrelay.com/v1/message/send"

# Secure API key you've set in your FastAPI backend
headers = {
    "X-API-Key": "GPT-Relay-7a8d3f2b9c5e4a6d9e1f",
    "Content-Type": "application/json"
}

# Example MTSL message payload
data = {
    "from_agent": "Pulse",
    "to_agent": "Continuum",
    "payload": {
        "intent": "test_message",
        "context": {
            "message": "Hello from Pulse via external script!",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    }
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("✅ Success! Response:")
    print(response.json())
else:
    print(f"❌ Failed with status code {response.status_code}:")
    print(response.text)
