from datetime import datetime, timedelta, timezone

from http_client import HttpClient, HttpClientError, FinnhubEndPoints

from .base import NewsProvider
from .helper import make_id, to_iso_z


class FinnhubProvider(NewsProvider):
    def __init__(self, api_key):
        self._api_key = api_key
        self._client = HttpClient(base_url=FinnhubEndPoints.BASE_URL)

    def fetch(self, ticker):
        if not self._api_key:
            raise RuntimeError("FINNHUB_API_KEY is not set. Add it to your .env file.")

        date_from, date_to = self._date_range()

        params = {
            "symbol": ticker,
            "from": date_from,
            "to": date_to,
            "token": self._api_key,
        }

        try:
            response = self._client.get(FinnhubEndPoints.COMPANY_NEWS, params=params)
            articles = response.json()
        except HttpClientError as error:
            print(f"⚠️  Failed to fetch Finnhub news: {error}")
            articles = []

        return [self._normalize(article, ticker) for article in articles]

    def _date_range(self):
        today = datetime.now(timezone.utc).date()
        date_from = (today - timedelta(days=2)).isoformat()
        date_to = today.isoformat()
        return date_from, date_to

    def _normalize(self, article, ticker):
        published_at = datetime.fromtimestamp(article["datetime"], tz=timezone.utc)

        tickers = [
            {"symbol": symbol.strip(), "relevance": None, "provider_sentiment": None}
            for symbol in article.get("related", "").split(",")
            if symbol.strip().upper() == ticker.upper()
        ]

        return {
            "id": make_id(article.get("url"), existing_id=article.get("id")),
            "title": article.get("headline"),
            "summary": article.get("summary"),
            "url": article.get("url"),
            "source": article.get("source"),
            "published_at": to_iso_z(published_at),
            "provider": "finnhub",
            "tickers": tickers,
            "image_url": article.get("image"),
            "raw": article,
        }
