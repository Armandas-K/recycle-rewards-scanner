import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:3000")

def checkout(barcodes: list[str]) -> dict:
    # POST scanned barcodes to backend
    # returns: { token: str, redeem_url: str }
    # skeleton - endpoint not implemented on website yet
    # maybe add auth header using api keys?
    try:
        response = requests.post(
            f"{BASE_URL}/api/checkout",
            json={"barcodes": barcodes},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[API] Checkout failed: {e}")
        return {}


def get_transaction_status(token: str) -> str:
    # GET status of a pending transaction.
    # returns: 'pending'/'redeemed'/'expired'
    # skeleton - endpoint not implemented on website yet
    try:
        response = requests.get(
            f"{BASE_URL}/api/transactions/{token}/status",
            timeout=5
        )
        response.raise_for_status()
        return response.json().get("status", "pending")
    except requests.RequestException as e:
        print(f"[API] Status check failed: {e}")
        return "pending"