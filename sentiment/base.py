
from abc import ABC, abstractmethod

class SentimentModel(ABC):
    
    @abstractmethod
    def score(self, texts: list[str]) -> list[dict[str, float]]:
        """Return a probability distribution over sentiment classes for `text`,
            e.g. {"positive": 0.87, "negative": 0.05, "neutral": 0.08}."""