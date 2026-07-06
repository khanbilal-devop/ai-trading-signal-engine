from abc import ABC, abstractmethod


class NewsProvider(ABC):
    @abstractmethod
    def fetch(self, ticker: str) -> list[dict]:
        """Return a list of normalized article dicts for the given ticker."""
