"""Central configuration for the Competitive Creative Intelligence Engine."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "data" / "cci.db"

# --- API keys (loaded from .env file) ---
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Mock mode: True only if keys are missing
MOCK_MODE = not (META_ACCESS_TOKEN and GROQ_API_KEY)

# --- Competitors to track (real brand names for Ad Library search) ---
COMPETITORS = ["Nike", "Adidas", "Puma"]

# --- Fatigue detection thresholds (industry-standard heuristics) ---
FATIGUE_CTR_DROP_PCT = 0.20      # 20% drop vs rolling baseline
FATIGUE_BASELINE_DAYS = 7        # rolling baseline window
FATIGUE_RECENT_DAYS = 3          # recent window compared to baseline
FATIGUE_FREQUENCY_LIMIT = 3.0    # avg impressions per user

# --- Strategist ---
N_CLUSTERS = 4                   # messaging-angle clusters
LONGEVITY_SUCCESS_DAYS = 14      # ad running >= this = proven performer

# --- Scheduler ---
RUN_INTERVAL_HOURS = 24