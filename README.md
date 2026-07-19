# AI Trading Signal Engine

Turns the flood of financial news on a watchlist into simple, explainable
signals — **bullish / bearish / hold** — for US stocks and crypto, validated
against actual price movements.

The problem: a retail trader can't read every headline about every asset they
follow, and often finds out about market-moving news too late. This project
automates news-based sentiment analysis and turns it into an at-a-glance signal.

> ⚠️ **Not financial advice.** This is an educational / portfolio project.

## Status
🚧 Actively in development — **Version 1** (off-the-shelf sentiment model + dashboard).

## Planned stack
Python · Hugging Face (FinBERT) · FastAPI · Streamlit · Docker

## Roadmap
- **v1** — Off-the-shelf sentiment model, news pipeline, dashboard, live deployment.
- **v2** — Fine-tuned model, retrieval-augmented rationales, agentic workflow.
- **v3** — Model built from scratch + benchmarked against v1/v2, full MLOps, polished product.

## Why FinBERT?

For this project I needed a model that does one thing well: score the sentiment
of financial news text (positive / negative / neutral). I chose **FinBERT**
(`ProsusAI/finbert`) for the following reasons:

- **It's a purpose-built classifier, not a text generator.** FinBERT is an
  encoder (BERT-based) model designed for classification. You feed it text and it
  directly outputs sentiment class scores — no prompting, no parsing a generated
  response. This is a more direct and reliable fit for sentiment scoring than a
  general-purpose generative LLM, which would require prompting it to answer in a
  specific format and then parsing that output.
- **It's fine-tuned specifically on financial text.** General sentiment models
  miss domain nuance — in finance, phrases like "beat estimates" or "shares fell
  on dilution" carry sentiment that everyday-language models don't capture well.
  FinBERT was fine-tuned on financial data, so it understands this context out of
  the box.
- **It's small enough to run locally.** FinBERT (~400 MB) downloads and runs
  comfortably on my laptop's CPU. A generative LLM capable of the same task would
  be far larger and a real bottleneck to load and run locally. Keeping the model
  small was a deliberate constraint.
- **It's a good learning vehicle.** This project's goal is to learn AI
  engineering fundamentals hands-on — not to ship a market-ready product. A small,
  well-understood model that I can download, run manually, inspect layer-by-layer,
  and later fine-tune myself lets me work at a small, transparent scale and
  understand the full pipeline end to end.

In short: FinBERT gives me a domain-specialized, directly-usable sentiment
classifier that's lightweight enough to run and experiment with locally — the
right tool for learning the fundamentals rather than over-engineering a solution.