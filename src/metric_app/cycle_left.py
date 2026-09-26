"""Import cycle for python-perf-dependency.

These modules import each other. Tests never import them, so the suite stays green.
The dependency tool reads the AST, so the cycle still counts.
"""

from metric_app.cycle_right import RIGHT_MARK


def left_tag() -> str:
    return "left"


def left_value() -> str:
    return RIGHT_MARK
