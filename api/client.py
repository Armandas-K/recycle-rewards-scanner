import requests

BASE_URL = "http://localhost:3000"
BIN_ID = "0"
# API_KEY = "secret"

def get_user(uid: str) -> dict:
    # GET user info by NFC UID
    # returns: { found: bool, name: str, language: str, points: int }
    # skeleton - endpoint not implemented on website yet
    # maybe add auth header using api keys?
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/user/{uid}",
            # api key could go here
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[API] get_user failed: {e}")
        return {"found": False, "name": "User", "language": "en", "points": 0}

def checkout(uid: str, bottles: int, cans: int, points: int) -> dict:
    # POST checkout - awards points directly to user account
    # returns: { success: bool }
    # skeleton - endpoint not yet implemented on website
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/checkout",
            # api key could go here
            json={
                "user_uuid": uid,
                "bottle_count": bottles,
                "can_count": cans,
                "points": points,
                "bin_id": BIN_ID,
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[API] Checkout failed: {e}")
        return {"success": False}