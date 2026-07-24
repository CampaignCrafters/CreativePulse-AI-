Agent 2 – Analyst (Developed by Sanjay)
Analyzes collected advertisements to extract the marketing angle, hook, offer, and call-to-action (CTA), and generates key insights.

import re
from utils.logger import get_logger

log = get_logger("analyst")

# Order matters — first matching angle wins, so put more specific signals first.
ANGLE_KEYWORDS = {
    "discount": ["% off", "discount", "deal", "sale", "save"],
    "urgency": ["today only", "limited", "hurry", "last chance", "ends soon", "this week only"],
    "social proof": ["rated", "reviews", "customers", "trusted", "loved by", "5 star", "5-star"],
    "free_shipping": ["free shipping", "free delivery"],
    "convenience": ["easy", "fast delivery", "in 2 days", "next day", "hassle-free"],
    "quality": ["premium", "best", "top rated", "top-rated", "durable", "handcrafted"],
}

CTA_KEYWORDS = {
    "Shop Now": ["shop now", "shop the"],
    "Buy Now": ["buy now", "order now"],
    "Sign Up": ["sign up", "join now"],
    "Get Yours": ["get yours", "claim"],
    "Learn More": ["learn more", "find out"],
}


def _detect_angle(text: str) -> str:
    text = text.lower()
    for angle, keywords in ANGLE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return angle
    return "general"


def _detect_offer(text: str) -> str:
    match = re.search(r"(\d{1,3}\s?%\s?off)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    if "free" in text.lower():
        return "free offer mentioned"
    return "none"


def _detect_cta(text: str) -> str:
    text = text.lower()
    for cta, keywords in CTA_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return cta
    return "Learn More"


def _analyze_one(ad: dict) -> dict:
    text = f"{ad.get('headline', '')} {ad.get('body', '')}"
    return {
        "angle": _detect_angle(text),
        "hook": ad.get("headline") or (ad.get("body") or "")[:60],
        "offer": _detect_offer(text),
        "cta": _detect_cta(text),
    }


def run(ads: list) -> dict:
    insights = {}
    for ad in ads:
        try:
            insights[ad["ad_id"]] = _analyze_one(ad)
        except Exception as e:
            log.warning("Analyst failed on %s: %s", ad.get("ad_id"), e)
            insights[ad["ad_id"]] = {
                "angle": "unknown", "hook": ad.get("headline", ""),
                "offer": "unknown", "cta": "unknown",
            }
    log.info("Analyst: %d ads analyzed (rule-based, no LLM)", len(insights))
    return insights
