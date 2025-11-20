from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Base de données utilisateurs 
USERS_DB = {
    "admin": "admin123",
    "user": "password"
}

def create_access_token(username):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def login(username, password):
    if username not in USERS_DB or USERS_DB[username] != password:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    
    token = create_access_token(username)
    return {
        "access_token": token,
        "username": username
    }

def verify_token(token):
    try:
     
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")