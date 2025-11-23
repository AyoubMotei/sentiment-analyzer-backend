from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

from app.auth import verify_token, login
from app.services.ai_service import analyze_sentiment

app = FastAPI(title="Sentiment Analysis API")

# CORS pour Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class PredictRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Sentiment Analysis API"}

@app.post("/login")
def login_endpoint(request: LoginRequest):
    return login(request.username, request.password)


@app.post("/predict")
def predict_endpoint(request: PredictRequest, token: dict = Depends(verify_token)):
    try:
        result = analyze_sentiment(request.text)
        return {
            "text": request.text,
            "score": result["score"],
            "sentiment": result["sentiment"],
            "user": token["sub"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test-env")
def test_env():
    """Endpoint de test pour vérifier les variables d'environnement"""
    return {
        "hf_key_configured": bool(os.getenv("HF_API_KEY")),
        "jwt_secret_configured": bool(os.getenv("JWT_SECRET")),
        "hf_key_preview": os.getenv("HF_API_KEY", "")[:10] + "..." if os.getenv("HF_API_KEY") else "None"
    }