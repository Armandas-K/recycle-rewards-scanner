VALID_LENGTHS = {8, 12, 13} # EAN-8 (8), UPC-A (12), EAN-13 (13)

def is_valid_length(barcode: str) -> bool:
    return len(barcode) in VALID_LENGTHS

def is_valid_checksum(barcode: str) -> bool:
    # EAN-13 checksum validation, returns true for EAN-8/UPC-A without full check
    if not barcode.isdigit():
        return False
    if len(barcode) != 13:
        return True  # skip checksum for EAN-8 and UPC-A

    total = sum(
        int(d) * (1 if i % 2 == 0 else 3)
        for i, d in enumerate(barcode[:12])
    )
    return (10 - (total % 10)) % 10 == int(barcode[-1])

def is_valid_barcode(barcode: str) -> tuple[bool, str]:
    # returns (is_valid, reason) tuple
    # reason empty if valid

    if not is_valid_length(barcode):
        return False, f"invalid length ({len(barcode)})"
    if not is_valid_checksum(barcode):
        return False, "failed checksum"

    return True, ""