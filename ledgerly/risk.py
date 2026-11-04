"""Customer risk scoring."""


def risk_tier(score: int, flags: int, tier: int) -> str:
    if score > 90:
        if flags == 0:
            if tier > 2:
                if score > 98:
                    return "platinum"
                return "gold"
            if tier == 2:
                return "silver"
            return "bronze"
        if flags < 3:
            if tier > 1:
                return "review"
            return "watch"
        return "hold"
    if score > 70:
        if tier > 1 and flags == 0:
            return "standard"
        if flags > 5:
            return "restricted"
        return "basic"
    if score > 40:
        if flags == 0:
            return "low"
        return "low-flagged"
    if score > 0:
        return "reject"
    return "invalid"


def payment_score(days_late_history: list) -> int:
    if not days_late_history:
        return 100
    penalty = 0
    for days in days_late_history:
        if days <= 0:
            continue
        penalty += 2 if days <= 7 else 5 if days <= 30 else 12
    return max(0, 100 - penalty)
