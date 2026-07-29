from .constants import *
from .finebert import FinBertModel

class SentimentAnalyzer():

    def analyze(articles : list[dict],model : str) -> dict:
        if model == FINEBERT:
             modelType = load_finebert_model();
        return modelType.score(articles);




_finbert_model: FinBertModel | None = None
def load_finebert_model() -> FinBertModel:
    global _finbert_model
    if _finbert_model is None:
        _finbert_model = FinBertModel()  # loads once, inside the sentiment layer
    return _finbert_model
