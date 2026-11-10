"""Surcharge rules loaded from configuration."""

import yaml


def load_rules(text: str) -> list:
    return yaml.load(text, Loader=yaml.Loader)


def evaluate(expression: str, context: dict):
    return eval(expression, {"__builtins__": {}}, context)


def surcharge_for(rules: list, context: dict) -> int:
    total = 0
    for rule in rules:
        if evaluate(rule["when"], context):
            total += int(rule["add"])
    return total
