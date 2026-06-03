import time
import pytest
from unittest.mock import patch, MagicMock
from core.scanner import BarcodeScanner

VALID_BARCODE_A = "5000193034559"
VALID_BARCODE_B = "5449000276018"
INVALID_BARCODE_A = "1234567" # wrong length
INVALID_BARCODE_B = "5000193034550" # bad checksum

def make_mock_barcode(barcode_string: str):
    mock = MagicMock()
    mock.data = barcode_string.encode()
    return mock

# Frame Detection

def test_real_barcode_frame_triggers_callback(barcode_frame):
    # photo of a barcode should trigger on_scan once
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    scanner.process_frame(barcode_frame)
    assert len(scanned) == 1

def test_blank_frame_does_not_trigger_callback(blank_frame):
    # frame with no barcode should never call on_scan
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    scanner.process_frame(blank_frame)
    assert len(scanned) == 0

# Validation

def test_valid_barcode_data_passed_correctly(blank_frame):
    # on_scan receives the exact decoded barcode string
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_A)]
        scanner.process_frame(blank_frame)
    assert scanned == [VALID_BARCODE_A]

def test_invalid_length_barcode_ignored(blank_frame):
    # barcode failing length check should never reach on_scan
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(INVALID_BARCODE_A)]
        scanner.process_frame(blank_frame)
    assert len(scanned) == 0

def test_invalid_checksum_barcode_ignored(blank_frame):
    # barcode failing checksum should never reach on_scan
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(INVALID_BARCODE_B)]
        scanner.process_frame(blank_frame)
    assert len(scanned) == 0

def test_multiple_barcodes_in_frame_only_first_triggers(blank_frame):
    # if two barcodes are in one frame, global cooldown blocks the second
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [
            make_mock_barcode(VALID_BARCODE_A),
            make_mock_barcode(VALID_BARCODE_B),
        ]
        scanner.process_frame(blank_frame)
    assert len(scanned) == 1
    assert scanned[0] == VALID_BARCODE_A

# Same Barcode Cooldown

def test_same_barcode_within_cooldown_fires_once(blank_frame):
    # same barcode scanned twice rapidly should only trigger on_scan once
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_A)]
        scanner.process_frame(blank_frame)
        scanner.process_frame(blank_frame)
    assert len(scanned) == 1

def test_same_barcode_after_cooldown_fires_again(blank_frame):
    # same barcode should trigger again once both cooldowns have expired
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_A)]
        scanner.process_frame(blank_frame)

        scanner.last_scan    = (VALID_BARCODE_A, time.time() - scanner.cooldown_same - 1)
        scanner.last_any_scan = time.time() - scanner.cooldown_any - 1

        scanner.process_frame(blank_frame)
    assert len(scanned) == 2

# Global Cooldown

def test_global_cooldown_blocks_different_barcode(blank_frame):
    # different barcode within global cooldown window should be blocked
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_A)]
        scanner.process_frame(blank_frame)

        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_B)]
        scanner.process_frame(blank_frame)

    assert len(scanned) == 1
    assert scanned[0] == VALID_BARCODE_A

def test_global_cooldown_expired_allows_different_barcode(blank_frame):
    # different barcode should trigger once global cooldown has expired
    scanned = []
    scanner = BarcodeScanner(on_scan=lambda b: scanned.append(b))
    with patch("core.scanner.decode") as mock_decode:
        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_A)]
        scanner.process_frame(blank_frame)

        scanner.last_any_scan = time.time() - scanner.cooldown_any - 1

        mock_decode.return_value = [make_mock_barcode(VALID_BARCODE_B)]
        scanner.process_frame(blank_frame)

    assert len(scanned) == 2
    assert scanned[1] == VALID_BARCODE_B