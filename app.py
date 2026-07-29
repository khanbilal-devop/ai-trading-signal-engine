from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sentiment import load_finebert_model
from service import SignalService, get_signal_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_finebert_model()   # warm the model before the server accepts requests
    yield                 # (cleanup after yield, if ever needed)



class SentimentResponse(BaseModel):
    sentiment:str
    article_count: int

app = FastAPI(lifespan=lifespan)

@app.get("/sentiment-analysis")
def check(ticker:str,service:SentimentResponse =Depends(get_signal_service)) -> SentimentResponse:
    result =  service.get_signal(ticker)
    return   SentimentResponse(**result)