


def aggregate_signals(results: list[dict]) -> dict:
    SIGNAL_THRESHOLD = 0.15  # τ — the dead-band edge

    if not results:
        return {"signal": "hold", "overall": 0.0, "article_count": 0}

    article_count = 0
    sum_of_net_effect = 0.0

    for result in results:
        if result["label"] == "neutral":
            continue

        scores = result["scores"]
        net_effect = scores["positive"] - scores["negative"]
        sum_of_net_effect += net_effect
        article_count += 1

    # every article was neutral → nothing directional to average
    if article_count == 0:
        return {"signal": "hold", "overall": 0.0, "article_count": 0}

    final_effect = sum_of_net_effect / article_count

    if final_effect >= SIGNAL_THRESHOLD:
        signal = "bullish"
    elif final_effect <= -SIGNAL_THRESHOLD:
        signal = "bearish"
    else:
        signal = "hold"

    return {
        "signal": signal,
        "article_count": article_count,
    }




