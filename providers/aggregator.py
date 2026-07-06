class NewsAggregator:
    def __init__(self, providers):
        self._providers = providers

    def get_articles(self, ticker):
        articles = []
        for provider in self._providers:
            articles += provider.fetch(ticker)
        return articles


