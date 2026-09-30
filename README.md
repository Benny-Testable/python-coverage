# Python metric coverage

# dummy commit 
Customer-style Python repo for a Testable whitebox run. Point a project at this git repo. The worker detects `pyproject.toml`, plans the Python tools, and each tool has a file that gives it a real signal.

The suite is green on purpose. Cosmic Ray skips mutation scoring when the unmutated tests fail.

## What each tool hits

| Tool | What this repo gives it |
| --- | --- |
| pylint, flake8 | `src/metric_app/style_issues.py` — unused import, unused name, line over 120 characters |
| radon, lizard, cognitive-ast, complexipy | `src/metric_app/complexity.py` |
| jscpd-py | The same `normalize_invoice_lines` body in `duplicate_a.py` and `duplicate_b.py` |
| bandit, semgrep | `src/metric_app/security_sinks.py` — the patterns in `tools/whitebox/python/semgrep-ruleset.yml` |
| pip-audit, safety | `pyproject.toml` pins `jinja2==3.1.3` and `urllib3==1.26.18`. There is no `requirements.txt`, so the worker installs this project from `pyproject.toml` |
| git-churn, pydriller | This git history. `billing.py` is edited across commits |
| coverage-py, testmon | `tests/test_metric_app.py` via pytest |
| py-coverage-delta | `.wb/baseline_coverage.json` plus the coverage-py report from the same run |
| crosshair | `src/metric_app/contracts.py` — the only module with a single function, which is the module Crosshair selects |
| cosmic-ray | `src/` plus a passing pytest suite |
| pymcdc | Compound conditions in `src/metric_app/decisions.py` |
| py-all-defs-uses | `dropped` in `src/metric_app/defs_uses.py` is assigned and never read |
| python-perf-dependency | Unused imports in `style_issues.py`, and the import cycle between `cycle_left.py` and `cycle_right.py` |
| semgrep-perf-static | `src/metric_app/perf_hotspots.py` — N+1 call, triple loop, append in a nested loop, thread start in a loop |
| gitleaks, detect-secrets | `src/metric_app/secrets_fixture.py` — the public AWS documentation sample key, not a live credential |
| presidio, semgrep-pii | `src/metric_app/pii_logging.py` — synthetic email, phone, sample SSN, and Visa test number |

## Not triggered by repo contents

`cert-delay` and `cert-retry` are certification fixtures inside the worker. They do not read this tree.

`github_branch_protection` and `github-access-control` need a GitHub repository, not only a local `.git` directory.

## Run the tests

```bash
python -m pytest
```
