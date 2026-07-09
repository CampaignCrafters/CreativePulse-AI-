"""Creative Agent — generates new ad variants exploiting the top messaging gap,
using the Groq LLM API grounded with competitor intelligence (RAG-style)."""
import json
from groq import Groq
from config import GROQ_API_KEY
from utils.prompts import CREATIVE_PROMPT
from utils.logger import get_logger

log = get_logger("creative")
MODEL = "llama-3.3-70b-versatile"

# Your brand context (configuration for the MVP)
BRAND, PRODUCT = "StrideRight", "running shoes"

def _get_client():
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY missing. Add it to your .env file. "
            "Get a free key at https://console.groq.com"
        )
    return Groq(api_key=GROQ_API_KEY)

def run(brief: dict) -> list:
    if not brief.get("gaps"):
        log.info("Creative: no gaps found, nothing to generate")
        return []

    angle = brief["gaps"][0]["angle"]  # top gap = highest-longevity unused angle
    client = _get_client()
    prompt = CREATIVE_PROMPT.format(angle=angle, brand=BRAND, product=PRODUCT)

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        variants = data.get("variants", [])
    except Exception as e:
        log.error("Creative generation failed: %s", e)
        return []

    for v in variants:
        v["angle"] = angle
    log.info("Creative: %d variant(s) generated for angle '%s'", len(variants), angle)
    return variants