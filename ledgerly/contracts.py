"""Cent-exact allocation with machine-checkable contracts."""


def split_cents(total_cents: int, parts: int) -> list:
    """Split ``total_cents`` into ``parts`` shares that differ by at most one cent.

    pre: total_cents >= 0
    pre: 1 <= parts <= 8
    post: sum(__return__) == total_cents
    post: len(__return__) == parts
    """
    base, extra = divmod(total_cents, parts)
    return [base + 1 if index < extra else base for index in range(parts)]
