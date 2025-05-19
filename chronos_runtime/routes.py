from fastapi import APIRouter
from models import CapsuleLog
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

router = APIRouter()
capsule_store = []
drift_log = []

# TTL buckets defined in seconds
TTL_BUCKETS = {
    "30s": timedelta(seconds=30),
    "60s": timedelta(seconds=60),
    "300s": timedelta(seconds=300),
}

@router.post("/log_capsule")
def log_capsule(data: CapsuleLog):
    # Trust capsule timestamp as canonical time
    parsed_time = parse(str(data.timestamp)).astimezone(timezone.utc)
    now = parsed_time  # Now = capsule's timestamp

    expiry_time = parsed_time + TTL_BUCKETS[data.ttl_bucket]
    drift = 0.0  # Since we're trusting the incoming time, drift is 0

    capsule_store.append(data)
    drift_log.append({
        "capsule_id": data.capsule_id,
        "sequence_number": data.sequence_number,
        "ttl_bucket": data.ttl_bucket,
        "drift_ms": drift,
        "logged_at": now.isoformat()
    })

    return {
        "status": "stored",
        "drift_ms": drift,
        "logged_at": now.isoformat(),
        "expires_at": expiry_time.isoformat()
    }

@router.get("/drift_score")
def get_drift_score():
    return {"recent_drifts": drift_log[-5:]}

@router.get("/ttl_bucket_origin")
def get_ttl_buckets():
    return {"ttl_buckets": list(TTL_BUCKETS.keys())}
