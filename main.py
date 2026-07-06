import os

from dotenv import load_dotenv

from providers import MarketauxProvider, AlphaVantageProvider, FinnhubProvider, NewsAggregator

load_dotenv()

aggregator = NewsAggregator([
    MarketauxProvider(api_key=os.getenv("MARKETAUX_API_KEY")),
    AlphaVantageProvider(api_key=os.getenv("ALPHAVANTAGE_API_KEY")),
    FinnhubProvider(api_key=os.getenv("FINNHUB_API_KEY")),
])


if __name__ == "__main__":
    articles = aggregator.get_articles("AAPL")
    print(f"Fetched {len(articles)} articles\n")

    for article in articles:
        print(f"[{article['provider']}] {article['title']}")
        print(f"  {article['published_at']} | {article['source']}")
        print(f"  {article['url']}")
        if article["tickers"]:
            print(f"  tickers: {article['tickers']}")
        print()
