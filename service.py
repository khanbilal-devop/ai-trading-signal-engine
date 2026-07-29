from error import NoArticlesError
from providers import create_default_aggregator
from sentiment import SentimentAnalyzer, FINEBERT


class SignalService:

    def get_signal(self, ticker: str) -> dict:
        aggregator = create_default_aggregator()
        articles = aggregator.get_articles(ticker)

        if not articles:
            raise NoArticlesError("No articles fetched for ticker.")

        # --- build the {id, text} input the sentiment layer expects ---
        # (temporary inline text-prep; the real preprocessing module comes later)
        model_inputs = [
            {
                "id": a["id"],
                "text": ". ".join(p for p in (a.get("title"), a.get("summary")) if p),
            }
            for a in articles
        ]

        results = SentimentAnalyzer.analyze(model_inputs, FINEBERT)
        return results


def get_signal_service() -> SignalService:
    return SignalService()