import pandas as pd
import json
import os

CSV_PATH = "raw/openfoodfacts_export.csv"
OUTPUT_PATH = "cache/barcodes.json"
VALID_LENGTHS = {8, 12, 13}


def is_valid_checksum(barcode: str) -> bool:
    if len(barcode) != 13:
        return True  # skip checksum for EAN-8 and UPC-A
    total = sum(
        int(d) * (1 if i % 2 == 0 else 3)
        for i, d in enumerate(barcode[:12])
    )
    return (10 - (total % 10)) % 10 == int(barcode[-1])


def build_cache():
    print("Reading CSV...")
    # only load the code column
    df = pd.read_csv(
        CSV_PATH,
        sep="\t",
        usecols=["code"],
        dtype={"code": str},
        on_bad_lines="skip"
    )

    print(f"Total rows: {len(df)}")

    barcodes = set()
    skipped = 0

    for code in df["code"].dropna():
        code = code.strip().zfill(13) if len(code.strip()) == 12 else code.strip()

        if len(code) not in VALID_LENGTHS:
            skipped += 1
            continue
        if not code.isdigit():
            skipped += 1
            continue
        if not is_valid_checksum(code):
            skipped += 1
            continue

        barcodes.add(code)

    print(f"Valid barcodes: {len(barcodes)}")
    print(f"Skipped: {skipped}")

    os.makedirs("cache", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump({"barcodes": list(barcodes)}, f)

    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"Saved to {OUTPUT_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    build_cache()