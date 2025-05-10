import logging
from enum import Enum
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ConcordSessionEngine")

class Agent(str, Enum):
    CONTINUUM = "Continuum"
    PULSE = "Pulse"
    NOVA = "Nova"
    ALETHEIA = "Aletheia"
    KAI = "Kai"

class MTSLMessage:
    def __init__(self, message: Dict[str, Any]):
        self.session_id = message.get("session_id")
        self.sender = message.get("sender")
        self.target = message.get("target")
        self.type = message.get("type")
        self.intent = message.get("intent")
        self.payload = message.get("payload")

    def __repr__(self):
        return f"<MTSLMessage from {self.sender} to {self.target} ({self.type})>"

class ConcordSessionEngine:
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}

    def handle_message(self, raw_message: Dict[str, Any]) -> Dict[str, Any]:
        msg = MTSLMessage(raw_message)
        logger.info(f"Received message: {msg}")

        if msg.session_id not in self.active_sessions:
            self.active_sessions[msg.session_id] = {
                "log": [],
                "agents": set(),
            }

        self.active_sessions[msg.session_id]["log"].append(msg)
        self.active_sessions[msg.session_id]["agents"].add(msg.sender)

        return self.route(msg)

    def route(self, msg: MTSLMessage) -> Dict[str, Any]:
        if msg.target == Agent.PULSE:
            return self.invoke_pulse(msg)
        elif msg.target == Agent.NOVA:
            return self.invoke_nova(msg)
        elif msg.target == Agent.CONTINUUM:
            return self.reflect_continuum(msg)
        elif msg.target == Agent.ALETHEIA:
            return self.invoke_aletheia(msg)
        elif msg.target == Agent.KAI:
            return self.invoke_kai(msg)
        else:
            logger.warning(f"Unknown target agent: {msg.target}")
            return {"status": "error", "reason": "Unknown target"}

    def invoke_pulse(self, msg: MTSLMessage) -> Dict[str, Any]:
        logger.info(f"Routing to Pulse: intent={msg.intent}, payload={msg.payload}")
        return {
            "status": "queued",
            "to": Agent.PULSE,
            "intent": msg.intent,
            "payload": msg.payload,
            "routed": True
        }

    def invoke_nova(self, msg: MTSLMessage) -> Dict[str, Any]:
        logger.info(f"Routing to Nova: intent={msg.intent}, payload={msg.payload}")
        return {
            "status": "queued",
            "to": Agent.NOVA,
            "intent": msg.intent,
            "payload": msg.payload,
            "routed": True
        }

    def reflect_continuum(self, msg: MTSLMessage) -> Dict[str, Any]:
        logger.info("Continuum handling its own message")
        return {
            "status": "ok",
            "message": "Handled internally by Continuum",
            "payload": msg.payload
        }

    def invoke_aletheia(self, msg: MTSLMessage) -> Dict[str, Any]:
        logger.info(f"Routing to Aletheia: intent={msg.intent}, payload={msg.payload}")
        return {
            "status": "queued",
            "to": Agent.ALETHEIA,
            "intent": msg.intent,
            "payload": msg.payload,
            "routed": True
        }

    def invoke_kai(self, msg: MTSLMessage) -> Dict[str, Any]:
        logger.info(f"Routing to Kai: intent={msg.intent}, payload={msg.payload}")
        return {
            "status": "queued",
            "to": Agent.KAI,
            "intent": msg.intent,
            "payload": msg.payload,
            "routed": True
        }
