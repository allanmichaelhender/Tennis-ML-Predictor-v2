from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import lab, players, manual_predict, upcoming_matches
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.ratelimit import limiter

app = FastAPI(title="Tennis ML API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router, prefix="/api/v1/players", tags=["players"])
app.include_router(manual_predict.router, prefix="/api/v1/predict", tags=["predict"])
app.include_router(upcoming_matches.router, prefix="/api/v1/upcoming", tags=["Live Sync"])
app.include_router(lab.router, prefix="/api/v1/lab", tags=["Lab"])


@app.get("/")
async def root():
    return {"status": "API Online", "version": "v1.0"}
