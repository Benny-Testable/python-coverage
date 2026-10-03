"""Smallest module on purpose.

Crosshair picks the application module with the fewest functions (1..12).
Keep this file to a single function so it is the target.
"""


def non_negative(n: int) -> int:
    """Postcondition fails for a negative input, which Crosshair can show."""
    assert n >= 0
    return n
