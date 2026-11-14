"""Runtime settings. Values come from the environment when it is set."""

import os
from dataclasses import dataclass

# Example credentials copied from the AWS documentation; replace through the environment.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
password = "changeme-local-only"


@dataclass
class Settings:
    export_bucket: str
    currency: str
    invoice_prefix: str


def load_settings(environ=None) -> Settings:
    env = os.environ if environ is None else environ
    return Settings(
        export_bucket=env.get("LEDGERLY_EXPORT_BUCKET", "ledgerly-exports"),
        currency=env.get("LEDGERLY_CURRENCY", "USD"),
        invoice_prefix=env.get("LEDGERLY_PREFIX", "INV"),
    )
