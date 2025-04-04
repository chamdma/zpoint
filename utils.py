from jose import jwt

from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "chandana2003"  

oauth2_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")  
        return {"user_id": user_id} if user_id else {"user_id": None}
    except jwt.ExpiredSignatureError:
        return {"user_id": None}  
    except jwt.InvalidTokenError:
        return {"user_id": None}  
