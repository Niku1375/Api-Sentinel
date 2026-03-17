from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.routers import health, auth, projects, endpoints, monitoring, alerts, ws_monitor
from app.routers import api_keys                          # ← added
from app.workers.scheduler import start_scheduler

app = FastAPI(
    title="API Sentinel",
    description="API Monitoring Platform",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(endpoints.router)
app.include_router(monitoring.router)
app.include_router(alerts.router)
app.include_router(ws_monitor.router)
app.include_router(api_keys.router)                       # ← added

@app.get("/")
def root():
    return {"message": "API Sentinel Running"}

@app.on_event("startup")
async def startup_event():
    start_scheduler()