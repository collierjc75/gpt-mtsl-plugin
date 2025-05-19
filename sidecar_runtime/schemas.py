from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class PhaseCreate(BaseModel):
    validator_id: str
    stream_epoch: str
    phase_state: str
    trigger_event: Optional[str] = None
    transition_reason: Optional[str] = None
    transition_time: datetime
    sequence_number: Optional[int] = None
    phase_metadata: Optional[dict] = None
