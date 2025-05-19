from pydantic import BaseModel, Field
from datetime import datetime

class CapsuleLog(BaseModel):
    capsule_id: str
    validator_id: str
    sequence_number: int
    timestamp: datetime = Field(..., example="2025-05-11T13:55:00Z")
    ttl_bucket: str
