"""Nested branches for radon, lizard, cognitive-ast, and complexipy."""


def label_prefix() -> str:
    return "tier"


def classify(score: int, flags: int, tier: int) -> str:
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
