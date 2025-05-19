from fastapi import FastAPI
from routes import router

app = FastAPI(title="Chronos Runtime", version="1.1")
app.include_router(router)
