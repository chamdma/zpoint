import jwt
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends

SECRET_KEY = "chandana2003"
security = HTTPBearer()

def create_access_token(data: dict):

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def jwt_bearer_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return decode_jwt_token(credentials.credentials)

