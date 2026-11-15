# ledgerly

Invoicing, tax and aging helpers for small billing back offices. ledgerly is a plain
Python library (3.11 or 3.12) with a tiny command line front end. It has no web framework
and no database server: invoices live in memory, in JSON files or in SQLite.

## What is in the box

| Module | Purpose |
| --- | --- |
| `ledgerly.money` | Decimal helpers: rounding to cents, percentages, formatting |
| `ledgerly.models` | `Customer`, `LineItem`, `Invoice`, `Payment` data classes |
| `ledgerly.pricing` | Member and volume discounts, customer tiers |
| `ledgerly.tax` | Sales tax and VAT by region, tax exempt SKUs |
| `ledgerly.invoices` | Invoice numbers, payment terms, totals, payments |
| `ledgerly.customers` | In-memory customer registry |
| `ledgerly.validators` | Email, phone and postal code checks |
| `ledgerly.policies` | Credit eligibility, shipping class, late fee waivers |
| `ledgerly.risk` | Customer risk tiers and payment scores |
| `ledgerly.reports` | Aging buckets and region matrices |
| `ledgerly.repository`, `ledgerly.db` | JSON file store and SQLite lookups |
| `ledgerly.exporters`, `ledgerly.importers` | CSV export, CSV and XML import |
| `ledgerly.notifications` | Payment reminder text and batch delivery |
| `ledgerly.gateway` | Client for the card processor status API (legacy v1) |
| `ledgerly.cache`, `ledgerly.rules`, `ledgerly.shell_tools` | Batch job helpers |
| `ledgerly.cli` | `python -m ledgerly.cli demo` and `aging` commands |

## Setup

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

Dependencies are pinned exactly in `requirements.txt` (runtime) and `requirements-dev.txt`
(test tools). `pyproject.toml` declares the same runtime pins.

## Tests

```bash
python -m pytest
python -m pytest --cov=ledgerly --cov-branch
```

The suite needs no network, no environment variables and writes only under pytest's
temporary directories. It runs in a couple of seconds.

## Command line

```bash
python -m ledgerly.cli demo
python -m ledgerly.cli aging --today 2026-06-01
```

## Docker

`Dockerfile` builds a small image that runs the demo command.

## Notes

`ledgerly.gateway` talks to the legacy v1 endpoint and still uses its old checksum scheme;
the v2 client is planned. Credentials in `ledgerly.settings` are the placeholder values
from the AWS documentation and must be replaced through the environment in real use.
