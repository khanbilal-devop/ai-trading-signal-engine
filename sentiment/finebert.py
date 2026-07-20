from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from .base import SentimentModel



class FinBertModel(SentimentModel):
    
    MODEL_NAME = "ProsusAI/finbert"
    
    def __init__(self):
         # 1. Load the TOKENIZER 
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        
        # Load the model
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)
        
        #  Switch to inference mode
        self.model.eval()
        return;
    
    def score(self, articles: list[dict]) -> list[dict]:
    # 1. Pull texts out, preserving order (articles[i] <-> texts[i])
        texts = [article["text"] for article in articles]   
    # 2. TOKENIZE the batch
        inputs = self.tokenizer(
            texts, padding=True, truncation=True, max_length=512, return_tensors="pt",
        )

    # 3. FORWARD PASS -> logits
        with torch.no_grad():
            logits = self.model(**inputs).logits

    # 4. SOFTMAX -> probabilities [N, 3]
        probabilities = torch.softmax(logits, dim=-1)

    # 5. RE-ATTACH ids: distribution + top label per article
        id2label = self.model.config.id2label
        results = []
        for article, row in zip(articles, probabilities):
            scores = {id2label[i]: prob.item() for i, prob in enumerate(row)}
            top_label = max(scores, key=scores.get)
            results.append({
                "id": article["id"],
                "label": top_label,
                "scores": scores,
            })
        return results;
    
    # def score(self, texts: list[str]) -> list[dict[str, float]]:
    #     # TOKENIZE the batch of texts -> tensors
    #     inputs = self.tokenizer(
    #     texts,
    #     padding=True,
    #     truncation=True,
    #     max_length=512,
    #     return_tensors="pt",
    #     )
        
    # #  FORWARD PASS under torch.no_grad() -> logits
    #     with torch.no_grad():
    #         outputs = self.model(**inputs)
    #     logits = outputs.logits
        
    #     # Then apply softmax to get prob districutiuon
    #     probabilities = torch.softmax(logits, dim=-1)
        
    #     # Then return the label that scores the highest
    #     id2label = self.model.config.id2label
    #     distributions = [];
    #     for row in probabilities:
    #         distribution= {
    #             id2label[i] : probability.item()
    #             for i,probability in enumerate(row)
    #         }
    #         distribution.append(distribution)
        
    #     return distributions; 
    
      