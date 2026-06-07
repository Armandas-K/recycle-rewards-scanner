from utils.validator import is_valid_length, is_valid_checksum, is_valid_barcode

# known valid barcodes
VALID_EAN13_A = "5000193034559"
VALID_EAN13_B = "5054267007123"
VALID_EAN8  = "12345670"
VALID_UPCA  = "012345678905"

# wrong check digit on valid barcodes
INVALID_EAN13_CHECKSUM = "5000193034550"
INVALID_EAN8_CHECKSUM  = "12345671"
INVALID_UPCA_CHECKSUM  = "012345678900"

# is_valid_length

def test_ean13_length_valid():
    assert is_valid_length(VALID_EAN13_A) is True

def test_ean8_length_valid():
    assert is_valid_length(VALID_EAN8) is True

def test_upc_a_length_valid():
    assert is_valid_length(VALID_UPCA) is True

def test_length_too_short():
    assert is_valid_length("123456") is False

def test_length_too_long():
    assert is_valid_length("12345678901234") is False

def test_length_nine_digits():
    assert is_valid_length("123456789") is False

def test_length_eleven_digits():
    assert is_valid_length("12345678901") is False

def test_length_empty():
    assert is_valid_length("") is False

# is_valid_checksum

def test_ean13_valid_checksum():
    assert is_valid_checksum(VALID_EAN13_A) is True

def test_ean13_second_valid_checksum():
    assert is_valid_checksum(VALID_EAN13_B) is True

def test_ean13_invalid_checksum():
    assert is_valid_checksum(INVALID_EAN13_CHECKSUM) is False

def test_ean8_valid_checksum():
    assert is_valid_checksum(VALID_EAN8) is True

def test_ean8_invalid_checksum():
    assert is_valid_checksum(INVALID_EAN8_CHECKSUM) is False

def test_upc_a_valid_checksum():
    assert is_valid_checksum(VALID_UPCA) is True

def test_upc_a_invalid_checksum():
    assert is_valid_checksum(INVALID_UPCA_CHECKSUM) is False

def test_checksum_non_digit_returns_false():
    assert is_valid_checksum("500019303455X") is False

def test_checksum_all_non_digit_returns_false():
    assert is_valid_checksum("ABCDEFGHIJKLM") is False

def test_checksum_all_zeros_ean13():
    # sum of all zero digits is 0, check digit is 0 - valid structure
    assert is_valid_checksum("0000000000000") is True

# is_valid_barcode

def test_valid_ean13_passes():
    valid, reason = is_valid_barcode(VALID_EAN13_A)
    assert valid is True
    assert reason == ""

def test_valid_ean8_passes():
    valid, reason = is_valid_barcode(VALID_EAN8)
    assert valid is True
    assert reason == ""

def test_valid_upc_a_passes():
    valid, reason = is_valid_barcode(VALID_UPCA)
    assert valid is True
    assert reason == ""

def test_invalid_length_short_fails():
    valid, reason = is_valid_barcode("123456")
    assert valid is False
    assert "length" in reason

def test_invalid_length_long_fails():
    valid, reason = is_valid_barcode("12345678901234")
    assert valid is False
    assert "length" in reason

def test_invalid_length_reason_contains_digit_count():
    valid, reason = is_valid_barcode("123456")
    assert "6" in reason

def test_invalid_checksum_fails():
    valid, reason = is_valid_barcode(INVALID_EAN13_CHECKSUM)
    assert valid is False
    assert "checksum" in reason

def test_non_digit_barcode_fails():
    valid, reason = is_valid_barcode("500019303455X")
    assert valid is False
    assert "checksum" in reason

def test_empty_string_fails():
    valid, reason = is_valid_barcode("")
    assert valid is False
    assert "length" in reason

def test_valid_barcode_empty_reason():
    valid, reason = is_valid_barcode(VALID_EAN13_A)
    assert reason == ""

def test_invalid_barcode_non_empty_reason():
    valid, reason = is_valid_barcode("123456")
    assert reason != ""