from api.session import ScanSession

BARCODE_A = "5000193034559"
BARCODE_B = "5054267007123"
BARCODE_C = "5010251484851"

TEST_UID  = "04:3a:78:9b:dd:2a:81"
TEST_USER = {"found": True, "name": "Test User", "language": "en", "points": 0}

# start

def test_start_sets_uid():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    assert session.uid == TEST_UID

def test_start_sets_user():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    assert session.user == TEST_USER

def test_start_makes_session_active():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    assert session.active is True

def test_start_clears_previous_items():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    session.add(BARCODE_A, "bottle")
    session.start("new-uid", TEST_USER)
    assert session.count == 0

# active

def test_not_active_on_init():
    assert ScanSession().active is False

def test_active_after_start():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    assert session.active is True

def test_not_active_after_clear():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    session.clear()
    assert session.active is False

# add

def test_add_bottle_increases_bottle_count():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    assert session.bottle_count == 1

def test_add_can_increases_can_count():
    session = ScanSession()
    session.add(BARCODE_A, "can")
    assert session.can_count == 1

def test_add_bottle_does_not_affect_can_count():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    assert session.can_count == 0

def test_add_can_does_not_affect_bottle_count():
    session = ScanSession()
    session.add(BARCODE_A, "can")
    assert session.bottle_count == 0

def test_add_multiple_bottles():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.add(BARCODE_B, "bottle")
    session.add(BARCODE_C, "bottle")
    assert session.bottle_count == 3

def test_add_multiple_cans():
    session = ScanSession()
    session.add(BARCODE_A, "can")
    session.add(BARCODE_B, "can")
    assert session.can_count == 2

def test_add_mixed_containers():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.add(BARCODE_B, "can")
    assert session.bottle_count == 1
    assert session.can_count == 1

# count

def test_count_zero_on_init():
    assert ScanSession().count == 0

def test_count_is_total_of_bottles_and_cans():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.add(BARCODE_B, "bottle")
    session.add(BARCODE_C, "can")
    assert session.count == 3

# checkout

def test_checkout_returns_tuple():
    result = ScanSession().checkout()
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_checkout_empty_returns_empty_lists():
    bottles, cans = ScanSession().checkout()
    assert bottles == []
    assert cans == []

def test_checkout_returns_correct_bottles():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.add(BARCODE_B, "bottle")
    bottles, cans = session.checkout()
    assert BARCODE_A in bottles
    assert BARCODE_B in bottles

def test_checkout_returns_correct_cans():
    session = ScanSession()
    session.add(BARCODE_A, "can")
    bottles, cans = session.checkout()
    assert BARCODE_A in cans

def test_checkout_separates_bottles_and_cans():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.add(BARCODE_B, "can")
    bottles, cans = session.checkout()
    assert BARCODE_A in bottles and BARCODE_A not in cans
    assert BARCODE_B in cans and BARCODE_B not in bottles

def test_checkout_clears_bottles():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.checkout()
    assert session.bottle_count == 0

def test_checkout_clears_cans():
    session = ScanSession()
    session.add(BARCODE_A, "can")
    session.checkout()
    assert session.can_count == 0

# clear

def test_clear_resets_uid():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    session.clear()
    assert session.uid is None

def test_clear_resets_user():
    session = ScanSession()
    session.start(TEST_UID, TEST_USER)
    session.clear()
    assert session.user == {}

def test_clear_resets_bottle_count():
    session = ScanSession()
    session.add(BARCODE_A, "bottle")
    session.clear()
    assert session.bottle_count == 0

def test_clear_resets_can_count():
    session = ScanSession()
    session.add(BARCODE_A, "can")
    session.clear()
    assert session.can_count == 0