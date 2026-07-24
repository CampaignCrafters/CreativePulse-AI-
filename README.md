
#  Competitive Creative Intelligence Engine

A multi-agent dashboard that researches competitor ads in real time and helps you respond with your own — powered by SerpAPI, ScrapingBee, Groq (Llama), and free AI image generation.

## Team Description

Sanjay - 8208E23ASR047
Seljilin Brijo - 8208E23ASR048
Shahana - 8208E23ASR049
Shinas Begum - 8208E23ASR050
Sinega - 8208E23ASR51

## What it does

| Agent | Function |
|---|---|
| 01 — Scout | Collects real competitor ads (SerpAPI search, Google Images, Facebook Ad Library) plus a LinkedIn company snapshot |
| 02 — Analyst | Extracts angle, hook, offer, and CTA from every collected ad, plus an aggregate summary |
| 03 — Strategist | Clusters messaging with TF-IDF, ranks the top 5 ads with plain-English reasoning, and finds gaps in your own messaging |
| 04 — Fatigue Monitor | Checks your own brand's CTR history for performance decay and sends a real email alert if it's dropping |
| 05 — Creative | Generates a professional, unique ad (copy via Groq/Llama + a real generated image via Pollinations.ai) from your own product inputs |

## Folder structure

```
project/
├── Dockerfile                  # Hugging Face Spaces container definition
├── README.md                   # this file (also the Space's landing page)
├── requirements.txt            # Python dependencies
├── .dockerignore
├── .env.example                # template — copy to .env for local runs, or use HF Spaces "Secrets" in production
│
├── server.py                   # Flask app — serves the dashboard + all /api/* endpoints
├── main.py                     # CLI entry point for the original batch pipeline (python main.py)
├── config.py                   # loads all API keys / thresholds from .env
│
├── agents/
│   ├── __init__.py
│   ├── scout.py                 # Agent 01 — SerpAPI, Google Images, Facebook Ad Library, LinkedIn
│   ├── analyst.py                # Agent 02 — rule-based angle/hook/offer/cta extraction
│   ├── strategist.py             # Agent 03 — TF-IDF clustering, longevity ranking, top-5 ranking
│   ├── fatigue_monitor.py        # Agent 04 — CTR decay detection
│   └── creative.py               # Agent 05 — Groq-generated copy + Pollinations.ai image
│
├── orchestrator/
│   ├── __init__.py
│   └── pipeline.py               # sequences Scout -> Analyst -> Strategist -> Fatigue -> Creative (batch mode)
│
├── database/
│   ├── __init__.py
│   └── store.py                  # persists known ad IDs + saved reports between runs
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                 # shared logging setup
│   └── emailer.py                # Gmail SMTP alert sender (Agent 04)
│
├── dashboard/
│   └── index.html                # the live dashboard UI (served by server.py at "/")
│
└── data/
    └── ctr_history.csv           # your own brand's CTR history (used by Agent 04)
```

## Environment variables (set as HF Spaces "Secrets", not committed to the repo)

```
SERPAPI_KEY=              # required — Agent 01 search + Google Ads/Images
SCRAPINGBEE_API_KEY=      # required — Agent 01 LinkedIn snapshot
FACEBOOK_ACCESS_TOKEN=    # optional — leave blank to use Facebook demo data
USE_FACEBOOK_DEMO_DATA=True

GROQ_API_KEY=             # optional — Agent 05 AI copywriting (falls back to templates if unset)
GROQ_MODEL=llama-3.3-70b-versatile

EMAIL_ADDRESS=            # optional — Agent 04 alert sender (Gmail address)
EMAIL_APP_PASSWORD=       # optional — Gmail App Password, not your normal password
ALERT_RECIPIENT=shahanakarthikeyan0@gmail.com

BRAND_NAME=YourBrand
BRAND_PRODUCT=your product
CTR_CSV_PATH=data/ctr_history.csv

COMPETITORS=              # optional — comma-separated, only used by the batch CLI (main.py)
```

## Running locally

```bash
pip install -r requirements.txt
python server.py
```
Open `http://localhost:7860` (or the port shown in your terminal).

## Deploying to Hugging Face Spaces

1. Create a new Space → SDK: **Docker**
2. Push this repo's contents (including `Dockerfile` and this `README.md`) to the Space's git remote
3. Go to **Settings → Repository secrets** and add each environment variable above — never commit `.env` itself
4. The Space builds automatically and becomes available at `https://<your-username>-<space-name>.hf.space`

## Notes on data sources

- **Facebook Ad Library**: Meta's official API only returns commercial ads for the UK/EU (elsewhere it's political/social-issue ads only) — demo data is used by default outside that scope. See `agents/scout.py` for details.
- **Google Custom Search**: evaluated but not used — requires a billing-linked Google Cloud project and overlaps with SerpAPI's coverage.
- **Product/ad images**: sourced live from Google Images via SerpAPI (real images, not verified "currently running" ad screenshots unless coming from a real Facebook Ad Library snapshot).
