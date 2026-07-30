
#  Competitive Creative Intelligence Engine

A multi-agent dashboard that researches competitor ads in real time and helps you respond with your own — powered by SerpAPI, ScrapingBee, Groq (Llama), and free AI image generation.



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
├── requirements.txt            # Python dependencies
├── .env                        # template — copy to .env for local runs, or use HF Spaces "Secrets" in production
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

## Notes on data sources

- **Facebook Ad Library**: Meta's official API only returns commercial ads for the UK/EU (elsewhere it's political/social-issue ads only) — demo data is used by default outside that scope. See `agents/scout.py`
-  for details.
- **Google Custom Search**: evaluated but not used — requires a billing-linked Google Cloud project and overlaps with SerpAPI's coverage.
- **Product/ad images**: sourced live from Google Images via SerpAPI (real images, not verified "currently running" ad screenshots unless coming from a real Facebook Ad Library snapshot).

  ## Output
<img width="1088" height="646" alt="image" src="https://github.com/user-attachments/assets/2bda88ea-429f-4e2b-a79e-b57f39e8224d" />
                                   FIGURE 1: SCOUT AGENT
<img width="1117" height="570" alt="image" src="https://github.com/user-attachments/assets/3d764525-2bcb-44e0-82ee-183158f1bc9f" />
                                  FIGURE 2: Analyst agent 
<img width="1157" height="685" alt="image" src="https://github.com/user-attachments/assets/4b8f3ad3-cf52-4543-b347-a2f6c93092a8" />
                                  FIGURE 3: Strategist Agent
<img width="1167" height="667" alt="image" src="https://github.com/user-attachments/assets/ed868f4c-dad7-4951-a411-f55eee6a02cd" />
                                  FIGURE 4: Fatigue Agent
<img width="1147" height="591" alt="image" src="https://github.com/user-attachments/assets/3cd94097-2524-4837-beed-05f991b3876a" />
                                FIGURE 5 : Creative Agent
<img width="1113" height="626" alt="image" src="https://github.com/user-attachments/assets/331b84a7-2342-4f21-b7b6-8ed6f60d4a6d" />
                               FIGURE 6 : Creative Agent Output Result
                                
                            
                                  
                                  
                                  
                                  
- **Google Custom Search**: evaluated but not used — requires a billing-linked Google Cloud project and overlaps with SerpAPI's coverage.
- **Product/ad images**: sourced live from Google Images via SerpAPI (real images, not verified "currently running" ad screenshots unless coming from a real Facebook Ad Library snapshot).
