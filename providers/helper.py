import hashlib
import re
from datetime import timezone

# Marketaux and Alpha Vantage carry richer data (sentiment, relevance) than
# Finnhub, so when the same story is duplicated across vendors, Finnhub's
# copy is the one discarded. Between Marketaux and Alpha Vantage, either is
# fine to keep, so they share the same (higher) priority.
_PROVIDER_PRIORITY = {"marketaux": 1, "alphavantage": 1, "finnhub": 0}


def make_id(url, existing_id=None):
    if existing_id is not None:
        return str(existing_id)
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def to_iso_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonicalize_title(title):
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())


def dedupe_articles_by_title(articles):
    best_by_key = {}

    for article in articles:
        canonical_title = _canonicalize_title(article.get("title"))
        key = canonical_title or article["id"]
        priority = _PROVIDER_PRIORITY.get(article["provider"], 0)

        current_best = best_by_key.get(key)
        current_priority = _PROVIDER_PRIORITY.get(current_best["provider"], 0) if current_best else -1

        if priority > current_priority:
            best_by_key[key] = article

    return list(best_by_key.values())
