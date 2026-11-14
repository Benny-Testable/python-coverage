"""Small helpers."""

import re


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def chunked(values: list, size: int) -> list:
    return [values[i : i + size] for i in range(0, len(values), size)]


def legacy_round(value: float) -> int:
    return int(value + 0.5)


class DeprecatedFormatter:
    prefix = ">>"

    def render(self, text: str) -> str:
        return self.prefix + text


UNUSED_LIMIT = 250
