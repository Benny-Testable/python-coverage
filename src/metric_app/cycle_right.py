"""Other half of the import cycle. See cycle_left."""

from metric_app.cycle_left import left_value


RIGHT_MARK = "right"


def right_tag() -> str:
    return "right"


def right_value() -> str:
    return left_value()
