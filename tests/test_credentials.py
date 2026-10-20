"""Tests credentials selection, without calling the Google Analytics API."""

from __future__ import annotations

import json

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from google.oauth2 import service_account

from tap_google_analytics.tap import SCOPES, TapGoogleAnalytics

BASE_CONFIG = {
    "property_id": "312647579",
    "start_date": "2024-01-01T00:00:00Z",
}


@pytest.fixture(scope="module")
def service_account_key():
    """Service account JSON key signed by a throwaway private key."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return {
        "type": "service_account",
        "project_id": "my-project",
        "private_key_id": "key-id",
        "private_key": private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode(),
        "client_email": "tap-ga4@my-project.iam.gserviceaccount.com",
        "token_uri": "https://oauth2.googleapis.com/token",
    }


def initialize_credentials(config: dict):
    """Build the tap's credentials from the given config."""
    tap = TapGoogleAnalytics(config={**BASE_CONFIG, **config}, setup_mapper=False)
    return tap._initialize_credentials()  # noqa: SLF001


@pytest.mark.parametrize("as_json_string", [False, True])
def test_service_account_key(service_account_key, as_json_string):
    """Accept the key as an object or as a JSON-encoded string."""
    key = json.dumps(service_account_key) if as_json_string else service_account_key

    credentials = initialize_credentials({"service_account_key": key})

    assert isinstance(credentials, service_account.Credentials)
    assert credentials.service_account_email == service_account_key["client_email"]
    assert credentials.scopes == SCOPES


def test_service_account_key_takes_precedence_over_oauth(service_account_key):
    """Use the service account even when OAuth keys are injected alongside it."""
    credentials = initialize_credentials(
        {
            "service_account_key": json.dumps(service_account_key),
            "client_id": "client_id",
            "client_secret": "client_secret",
            "refresh_token": "refresh_token",
        }
    )

    assert isinstance(credentials, service_account.Credentials)
