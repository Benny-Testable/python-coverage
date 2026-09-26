"""Syntactic sinks that match the bundled Python Semgrep rules and Bandit checks.

Each function is a separate pattern. Nothing here is wired into a request path,
and the tests never call these functions.
"""

import hashlib
import os
import pickle
import subprocess
import tempfile
import xml.etree.ElementTree


def run_expr(user_input: str) -> object:
    return eval(user_input)


def run_shell(cmd: str) -> int:
    return subprocess.call(cmd, shell=True)


def run_os(cmd: str) -> int:
    return os.system(cmd)


def unpack(blob: bytes) -> object:
    return pickle.loads(blob)


def load_blob(blob: str) -> object:
    import yaml

    return yaml.load(blob)


def fetch_insecure(url: str) -> str:
    import requests

    return requests.get(url, verify=False).text


def weak_digest(payload: bytes) -> str:
    return hashlib.md5(payload).hexdigest() + hashlib.sha1(payload).hexdigest()


def render_raw(template_name: str) -> object:
    import jinja2

    env = jinja2.Environment(autoescape=False)
    return env.get_template(template_name)


def lookup(cur: object, user_id: str) -> object:
    return cur.execute(f"SELECT * FROM users WHERE id = {user_id}")


def start_debug(app: object) -> None:
    app.run(debug=True)


def scratch_path() -> str:
    return tempfile.mktemp()


def read_xml(payload: str) -> xml.etree.ElementTree.Element:
    return xml.etree.ElementTree.fromstring(payload)


password = "fixture-password-not-used"
api_key = "fixture-api-key-not-used"
secret = "fixture-secret-not-used"
