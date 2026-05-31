import pandas as pd
import os

CSV_PATH = "raw/openfoodfacts_export.csv"
OUTPUT_PATH = "cache/filtered_barcodes.csv"

PLASTIC_BOTTLE_SUFFIXES = {
    "pet-bottle",
    "pet-1-polyethylene-terephthalate",
    "mixed-plastic-bottle",
    "plastic-bottle",
    "bottle-plastic",
    "hdpe-bottle",
    "hdpe-2-high-density-polyethylene",
    "pp-bottle",
    "pet-transparent",
}

CAN_SUFFIXES = {
    "can", # maybe too broad
    "aluminium", # to catch fr:canette-aluminium
    "aluminium-can",
    "aluminium-tin",
    "metal-can",
    "canned",
    "drink-can",
}

ACCEPTED_SUFFIXES = PLASTIC_BOTTLE_SUFFIXES | CAN_SUFFIXES

def is_accepted_container(packaging_tags: str) -> bool:
    if not isinstance(packaging_tags, str):
        return False
    tags = [t.strip() for t in packaging_tags.split(",")]
    return any(
        tag.endswith(suffix)
        for tag in tags
        for suffix in ACCEPTED_SUFFIXES
    )

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