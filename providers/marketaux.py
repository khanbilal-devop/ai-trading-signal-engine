from datetime import datetime

from http_client import HttpClient, HttpClientError, MarketauxEndPoints

from .base import NewsProvider
from .helper import make_id, to_iso_z

RELEVANCE_THRESHOLD = 70  # Marketaux match_score is 0–100


class MarketauxProvider(NewsProvider):
    def __init__(self, api_key):
        self._api_key = api_key
        self._client = HttpClient(base_url=MarketauxEndPoints.BASE_URL)

    def fetch(self, ticker):
        if not self._api_key:
            raise RuntimeError("MARKETAUX_API_KEY is not set. Add it to your .env file.")

        params = {
            "symbols": ticker,
            "api_token": self._api_key,
        }

        try:
            response = self._client.get(MarketauxEndPoints.NEWS_ALL, params=params)
            articles = response.json().get("data", [])
        except HttpClientError as error:
            print(f"⚠️  Failed to fetch Marketaux news: {error}")
            articles = []

        normalize = [self._normalize(article, ticker) for article in articles ]
        return [ article for article in normalize if article is not None]


    def _normalize(self, article, ticker):
        published_at = datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))

        matched_entity = next(
            (
                entity
                for entity in article.get("entities", [])
                if entity.get("symbol", "").upper() == ticker.upper()
                and entity.get("match_score","") is not None
                and entity.get("match_score","") >= RELEVANCE_THRESHOLD
            ),
            None,
        )
        
        
        
        tickers = []
        if matched_entity:
            tickers.append({
                "symbol": matched_entity.get("symbol"),
                "relevance": matched_entity.get("match_score"),
                "provider_sentiment": matched_entity.get("sentiment_score"),
            })
        else:
            return None    

        return {
            "id": make_id(article.get("url"), existing_id=article.get("uuid")),
            "title": article.get("title"),
            "summary": article.get("description"),
            "url": article.get("url"),
            "source": article.get("source"),
            "published_at": to_iso_z(published_at),
            "provider": "marketaux",
            "tickers": tickers,
            "image_url": article.get("image_url"),
            "raw": article,
        }
