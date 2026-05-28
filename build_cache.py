import pandas as pd
import json
import os

CSV_PATH = "raw/openfoodfacts_export.csv"
OUTPUT_PATH = "cache/filtered_barcodes.csv"

PLASTIC_BOTTLE_TAGS = {
    "en:pet-bottle",
    "en:pet-1-polyethylene-terephthalate",
    "en:mixed-plastic-bottle",
    "en:plastic-bottle",
    "en:hdpe-bottle",
    "en:hdpe-2-high-density-polyethylene",
}

CAN_TAGS = {
    "en:can",
    "en:aluminium",
    "en:aluminium-unknown",
    "en:aluminium-can",
    "en:steel-can",
    "en:metal-can",
}

ACCEPTED_TAGS = PLASTIC_BOTTLE_TAGS | CAN_TAGS

def is_accepted_container(packaging_tags: str) -> bool:
    if not isinstance(packaging_tags, str):
        return False
    tags = {t.strip() for t in packaging_tags.split(",")}
    return bool(tags & ACCEPTED_TAGS)

def build_cache():
    print("Reading CSV...")
    df = pd.read_csv(
        CSV_PATH,
        sep="\t",
        usecols=["code", "product_name_en", "packaging_tags", "categories_tags"],
        dtype=str,
        on_bad_lines="skip"
    )
    print(f"Total rows: {len(df)}")

    # apply mask to packaging tags
    filtered = df[df["packaging_tags"].apply(is_accepted_container)]

    os.makedirs("cache", exist_ok=True)
    filtered.to_csv(OUTPUT_PATH, index=False)

    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"Saved {len(filtered)} products to {OUTPUT_PATH} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    build_cache()