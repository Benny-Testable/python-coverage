"""Style findings for pylint and flake8. Not imported by the tests."""

import os
import sys


def style_tag() -> str:
    return "style"


def badly_styled_report(customer_name: str) -> str:
    unused_local = customer_name
    return "This sentence is intentionally longer than one hundred and twenty characters so flake8 E501 and pylint line-too-long both emit a finding for this metric fixture sample."
