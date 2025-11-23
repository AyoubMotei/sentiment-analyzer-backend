from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os


SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Base de données utilisateurs 
USERS_DB = {
    "admin": "admin123",
    "user": "password"
}

security = HTTPBearer()

def create_access_token(username):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
        "token_type": "bearer",
        "username": username
    }

# def verify_token(token):
#     try:
     
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
        
#         if username is None:
#             raise HTTPException(status_code=401, detail="Token invalide")
        
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token invalide ou expiré")


# def verify_token(authorization: Optional[str] = Header(None)):

#     # Vérifier que le header existe
#     if not authorization:
#         raise HTTPException(
#             status_code=403, 
#             detail="Not authenticated"
#         )
    
#     # Vérifier le format "Bearer <token>"
#     parts = authorization.split()
#     if len(parts) != 2 or parts[0].lower() != "bearer":
#         raise HTTPException(
#             status_code=403,
#             detail="Invalid authentication credentials"
#         )
    
#     token = parts[1]
    
#     try:
#         # Décoder le token
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
        
#         if username is None:
#             raise HTTPException(status_code=401, detail="Token invalide")
        
#         return payload
        
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token invalide ou expiré")



def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Extraire le token depuis les credentials
        token = credentials.credentials
        
        # Décoder le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Token invalide ou expiré: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Erreur d'authentification: {str(e)}"
        )
        