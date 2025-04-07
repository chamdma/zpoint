from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routes import router

app = FastAPI()


security = HTTPBearer()


@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    return {"message": "Access granted", "token": token}


app.include_router(router)

@app.get("/")
def home():
    return {"message": "API is running"}
