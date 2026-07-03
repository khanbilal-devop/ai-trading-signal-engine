"""API endpoint constants, grouped by service.

Each external service gets its own class holding a ``BASE_URL`` and one
attribute per entity/endpoint (paths relative to ``BASE_URL``). Add a new
class here as the engine starts talking to more services.
"""


class MarketauxEndPoints:
    BASE_URL = "https://api.marketaux.com/v1"

    # entity endpoints (relative to BASE_URL)
    NEWS_ALL = "/news/all"
    # future examples:
    # NEWS_SIMILAR = "/news/similar/{uuid}"
    # ENTITY_STATS = "/entity/stats"
    
