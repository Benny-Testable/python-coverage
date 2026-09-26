"""Fake credentials so gitleaks and detect-secrets have a hit.

The AWS pair is the public sample from the AWS documentation.
It is not a live access key.
"""

# https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
api_key = "sk_test_fixture_not_a_real_key_000000"
password = "fixture-password-not-used"
