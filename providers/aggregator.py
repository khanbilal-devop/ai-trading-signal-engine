from .helper import dedupe_articles_by_title

class NewsAggregator:
    def __init__(self, providers):
        self._providers = providers

    def get_articles(self, ticker):
        articles = []
        for provider in self._providers:
            articles += provider.fetch(ticker)
        return dedupe_articles_by_title(articles)


