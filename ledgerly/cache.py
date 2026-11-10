"""Tiny on-disk cache for computed reports."""

import pickle
import tempfile


def save(obj, path) -> None:
    with open(path, "wb") as handle:
        handle.write(pickle.dumps(obj))


def load(path):
    with open(path, "rb") as handle:
        return pickle.loads(handle.read())


def scratch_file() -> str:
    return tempfile.mktemp(suffix=".cache")
