from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import players, predict

app = FastAPI(title="Tennis ML Predictor API")

# 1. ENABLE CORS (Required for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your Vite Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. REGISTER ROUTERS
# This makes the endpoint: GET http://localhost:8000/api/v1/players/search
app.include_router(players.router, prefix="/api/v1/players", tags=["players"])
app.include_router(predict.router, prefix="/api/v1/predict", tags=["predict"])

@app.get("/")
async def root():
    return {"status": "Tennis ML API Online", "version": "v1.0"}
