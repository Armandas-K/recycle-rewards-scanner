import urllib.request
import json

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
TIMEOUT = 3

def lookup(barcode: str) -> dict:
    # returns dict with keys:
    # found bool
    # name str
    # category str
    # flagged bool - true if not found with api, needs manual review

    url = f"{BASE_URL}/{barcode}.json"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            data = json.loads(response.read())

        if data.get("status") == 1:
            product = data["product"]
            return {
                "found":    True,
                "name":     product.get("product_name", "Unknown"),
                "category": product.get("categories", "Unknown"),
                "flagged":  False
            }

    except Exception as e:
        print(f"[LOOKUP] API error for {barcode}: {e}")

    # valid barcode structure but not in Open Food Facts
    return {
        "found":    False,
        "name":     "Unknown",
        "category": "Unknown",
        "flagged":  True
    }