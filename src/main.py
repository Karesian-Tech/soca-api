from fastapi import FastAPI
from .api import init_routers


app = FastAPI()

init_routers(app)


@app.get("/ping")
def ping():
    return {"message": "pong"}
