from fastapi import FastAPI
from pydantic import BaseModel


class Response(BaseModel):
    ticker:str

app = FastAPI()

@app.get("/check")
def check(ticker) -> Response:
    return Response(ticker=ticker)