from .constants import *
from .finebert import FinBertModel

class SentimentAnalyzer():

    def analyze(articles : list[dict],model : str) -> dict:
        if model == FINEBERT:
             modelType = FinBertModel();
        return modelType.score(articles);