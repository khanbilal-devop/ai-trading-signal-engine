from datetime import datetime, timedelta, timezone

from http_client import HttpClient, HttpClientError, AlphaVantageEndPoints

from .base import NewsProvider
from .normalize import make_id, to_iso_z


class AlphaVantageProvider(NewsProvider):
    def __init__(self, api_key):
        self._api_key = api_key
        self._client = HttpClient()  # no base_url — Alpha Vantage uses one fixed URL per call

    def fetch(self, ticker):
        if not self._api_key:
            raise RuntimeError("ALPHAVANTAGE_API_KEY is not set. Add it to your .env file.")

        time_from, time_to = self._date_range()

        params = {
            "function": AlphaVantageEndPoints.NEWS_SENTIMENT,
            "tickers": ticker,
            "sort": "LATEST",
            "time_from": time_from,
            "time_to": time_to,
            "limit": 1000,
            "apikey": self._api_key,
        }

        try:
            response = self._client.get(AlphaVantageEndPoints.BASE_URL, params=params)
            articles = response.json().get("feed", [])
        except HttpClientError as error:
            print(f"⚠️  Failed to fetch Alpha Vantage news: {error}")
            articles = []

        return [self._normalize(article, ticker) for article in articles]

    def _date_range(self):
        now = datetime.now(timezone.utc)
        time_from = (now - timedelta(days=2)).strftime("%Y%m%dT%H%M")
        time_to = now.strftime("%Y%m%dT%H%M")
        return time_from, time_to

    def _normalize(self, article, ticker):
        # Alpha Vantage's docs don't state time_published's timezone — assuming UTC.
        published_at = datetime.strptime(article["time_published"], "%Y%m%dT%H%M%S").replace(
            tzinfo=timezone.utc
        )

        tickers = [
            {
                "symbol": t.get("ticker"),
                "relevance": float(t["relevance_score"]) if t.get("relevance_score") is not None else None,
                "provider_sentiment": (
                    float(t["ticker_sentiment_score"])
                    if t.get("ticker_sentiment_score") is not None
                    else None
                ),
            }
            for t in article.get("ticker_sentiment", [])
            if t.get("ticker", "").upper() == ticker.upper()
        ]

        return {
            "id": make_id(article.get("url")),
            "title": article.get("title"),
            "summary": article.get("summary"),
            "url": article.get("url"),
            "source": article.get("source"),
            "published_at": to_iso_z(published_at),
            "provider": "alphavantage",
            "tickers": tickers,
            "image_url": article.get("banner_image"),
            "raw": article,
        }
