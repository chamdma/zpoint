from fastapi import FastAPI
from routes import routes
from database import *




app=FastAPI()


app.include_router(routes.router)




@app.get("/")
def home():
    return {"API is running"}
