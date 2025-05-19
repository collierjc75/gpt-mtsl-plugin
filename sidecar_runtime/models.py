from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Text, Enum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sidecar_runtime.database import Base

class Phase(Base):
    __tablename__ = "phases"
    phase_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    validator_id = Column(String, nullable=False)
    stream_epoch = Column(String, nullable=False)
    phase_state = Column(Enum("init", "active", "committing", "finalizing", name="phase_states"), nullable=False)
    trigger_event = Column(String)
    transition_reason = Column(Text)
    transition_time = Column(TIMESTAMP)
    sequence_number = Column(Integer)
    phase_metadata = Column(JSON)
    schema_version = Column(String, default="v0.1")

class MemoryAnchor(Base):
    __tablename__ = "memory_anchors"
    anchor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    validator_id = Column(String, nullable=False)
    capsule_id = Column(String, nullable=False)
    anchor_type = Column(Enum("checkpoint", "rehydration", "pacing_reset", name="anchor_types"))
    anchor_scope = Column(String)
    anchor_payload = Column(JSON)
    checkpoint_time = Column(TIMESTAMP)
    ttl = Column(String)
    schema_version = Column(String, default="v0.1")
    created_at = Column(TIMESTAMP)

class TokenPacingLog(Base):
    __tablename__ = "token_pacing_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    validator_id = Column(String, nullable=False)
    phase_id = Column(UUID(as_uuid=True), ForeignKey("phases.phase_id"))
    max_tokens = Column(Integer)
    tokens_generated = Column(Integer)
    pacing_scope = Column(Enum("agent", "relay", "global", name="pacing_scope"))
    decay_model = Column(String)
    backoff_flag = Column(Boolean, default=False)
    pacing_context = Column(Enum("manual", "automated", "relay", name="pacing_context"))
    token_balance = Column(Integer)
    last_decay_time = Column(TIMESTAMP)
    pacing_notes = Column(JSON)
    schema_version = Column(String, default="v0.1")
    created_at = Column(TIMESTAMP)
