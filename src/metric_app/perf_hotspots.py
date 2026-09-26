"""Static performance shapes from tools/whitebox/shared/semgrep-perf-static.yaml."""

import threading


def chatty(ids: list[int]) -> list[str]:
    import requests

    pages = []
    for item in ids:
        pages.append(requests.get(f"https://example.invalid/{item}").text)
    return pages


def triple(groups: list[int], rows: list[int], cols: list[int]) -> int:
    total = 0
    for group in groups:
        for row in rows:
            for col in cols:
                total += group + row + col
    return total


def alloc(rows: list[int], cols: list[int]) -> list[tuple[int, int]]:
    found = []
    for row in rows:
        for col in cols:
            found.append((row, col))
    return found


def fanout(workers: list[threading.Thread]) -> None:
    for worker in workers:
        worker.start()
