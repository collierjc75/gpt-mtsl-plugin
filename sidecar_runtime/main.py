from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from sidecar_runtime.database import SessionLocal, engine
from sidecar_runtime import models, schemas

app = FastAPI()

# Initialize DB tables
models.Base.metadata.create_all(bind=engine)

# Dependency for DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "Sidecar runtime ready", "schema": "v0.1"}

@app.post("/phases/")
def create_phase(phase: schemas.PhaseCreate, db: Session = Depends(get_db)):
    new_phase = models.Phase(
        phase_id=uuid4(),
        validator_id=phase.validator_id,
        stream_epoch=phase.stream_epoch,
        phase_state=phase.phase_state,
        trigger_event=phase.trigger_event,
        transition_reason=phase.transition_reason,
        transition_time=phase.transition_time,
        sequence_number=phase.sequence_number,
        phase_metadata=phase.phase_metadata
    )
    db.add(new_phase)
    db.commit()
    db.refresh(new_phase)
    return {"status": "stored", "phase_id": str(new_phase.phase_id)}
