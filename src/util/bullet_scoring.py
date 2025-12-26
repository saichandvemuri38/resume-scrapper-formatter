IMPACT_KEYWORDS = [
    "reduced", "improved", "increased", "optimized",
    "performance", "efficiency", "accuracy", "%"
]

SENIOR_KEYWORDS = [
    "designed", "architected", "owned", "led", "deployed", "built"
]

def score_bullet(bullet, skills):
    score = 0
    text = bullet.lower()

    # Impact metrics
    if any(k in text for k in IMPACT_KEYWORDS):
        score += 3

    # Senior ownership signals
    if any(k in text for k in SENIOR_KEYWORDS):
        score += 2

    # Tech density
    for s in skills:
        if s.lower() in text:
            score += 1

    return score

def reorder_bullets(bullets, skills):
    scored = [(b, score_bullet(b, skills)) for b in bullets]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [b for b, _ in scored]
