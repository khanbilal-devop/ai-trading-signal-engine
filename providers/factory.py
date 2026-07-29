import os

from dotenv import load_dotenv

from .aggregator import NewsAggregator
from .marketaux import MarketauxProvider
from .alphavantage import AlphaVantageProvider
from .finnhub import FinnhubProvider


load_dotenv()

def create_default_aggregator() -> NewsAggregator:
    return NewsAggregator([
        MarketauxProvider(api_key=os.getenv("MARKETAUX_API_KEY")),
        AlphaVantageProvider(api_key=os.getenv("ALPHAVANTAGE_API_KEY")),
        FinnhubProvider(api_key=os.getenv("FINNHUB_API_KEY")),
    ])