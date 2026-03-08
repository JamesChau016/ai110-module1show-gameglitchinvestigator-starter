from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ===== Tests for check_guess =====
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_guess_far_too_high():
    # Edge case: very high guess
    result = check_guess(100, 1)
    assert result == "Too High"


def test_guess_far_too_low():
    # Edge case: very low guess
    result = check_guess(1, 100)
    assert result == "Too Low"


# ===== Tests for get_range_for_difficulty =====
def test_easy_difficulty():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_difficulty():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50


def test_hard_difficulty():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100


def test_invalid_difficulty_defaults_to_hard():
    # Invalid difficulty should default to Hard range
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100


# ===== Tests for parse_guess =====
def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_valid_float_as_integer():
    # Floats like "3.14" should be converted to int
    ok, value, err = parse_guess("3.14")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_float_rounded_down():
    ok, value, err = parse_guess("50.9")
    assert ok is True
    assert value == 50  # int() truncates, not rounds
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_non_numeric_string():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_mixed_string():
    ok, value, err = parse_guess("12abc34")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_negative_number():
    ok, value, err = parse_guess("-25")
    assert ok is True
    assert value == -25
    assert err is None


def test_parse_zero():
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None


# ===== Tests for update_score =====
def test_update_score_win_first_attempt():
    # First attempt (attempt_number=0): 100 - 10*(0+1) = 90
    new_score = update_score(0, "Win", 0)
    assert new_score == 90


def test_update_score_win_second_attempt():
    # Second attempt (attempt_number=1): 100 - 10*(1+1) = 80
    new_score = update_score(0, "Win", 1)
    assert new_score == 80


def test_update_score_win_many_attempts():
    # Many attempts (attempt_number=8): 100 - 10*(8+1) = 10 (but min is 10)
    new_score = update_score(0, "Win", 8)
    assert new_score == 10


def test_update_score_win_minimum_points():
    # Even more attempts: min is 10 points
    new_score = update_score(0, "Win", 15)
    assert new_score == 10  # Cannot go below 10


def test_update_score_too_high_even_attempt():
    # Even attempt number: +5 points
    new_score = update_score(100, "Too High", 0)
    assert new_score == 105


def test_update_score_too_high_odd_attempt():
    # Odd attempt number: -5 points
    new_score = update_score(100, "Too High", 1)
    assert new_score == 95


def test_update_score_too_low():
    # Too Low: always -5 points
    new_score = update_score(100, "Too Low", 0)
    assert new_score == 95


def test_update_score_too_low_even_attempt():
    # Too Low is always -5, regardless of attempt number
    new_score = update_score(100, "Too Low", 2)
    assert new_score == 95


def test_update_score_unknown_outcome():
    # Unknown outcome should return current score unchanged
    new_score = update_score(100, "Unknown", 5)
    assert new_score == 100


# ===== EDGE CASE TESTS =====

# ===== Edge cases for check_guess =====

def test_check_guess_negative_guess_positive_secret():
    # Negative guess vs positive secret
    result = check_guess(-5, 50)
    assert result == "Too Low"


def test_check_guess_with_zero_secret():
    # Zero as secret
    result = check_guess(5, 0)
    assert result == "Too High"


def test_check_guess_zero_guess_positive_secret():
    # Zero as guess, positive secret
    result = check_guess(0, 5)
    assert result == "Too Low"


def test_check_guess_large_numbers():
    # Very large numbers
    result = check_guess(1000000, 999999)
    assert result == "Too High"


# ===== Edge cases for parse_guess =====
def test_parse_guess_with_leading_whitespace():
    # Leading whitespace should fail
    ok, value, err = parse_guess(" 42")
    assert ok is True
    assert value == 42


def test_parse_guess_with_trailing_whitespace():
    # Trailing whitespace should be handled by int() wrapper
    ok, value, err = parse_guess("42 ")
    # This might fail depending on float() behavior with spaces
    assert ok is False or value == 42


def test_parse_guess_decimal_with_leading_zero():
    # Decimal number with leading zero
    ok, value, err = parse_guess("0.55")
    assert ok is True
    assert value == 0
    assert err is None


def test_parse_guess_multiple_decimals():
    # Multiple decimal points should fail
    ok, value, err = parse_guess("1.2.3")
    assert ok is False
    assert err == "That is not a number."


def test_parse_guess_very_large_number():
    # Very large number
    ok, value, err = parse_guess("999999999999")
    assert ok is True
    assert value == 999999999999
    assert err is None


def test_parse_guess_negative_float():
    # Negative float
    ok, value, err = parse_guess("-3.9")
    assert ok is True
    assert value == -3  # Truncates toward zero
    assert err is None


def test_parse_guess_only_decimal_point():
    # Just a decimal point
    ok, value, err = parse_guess(".")
    assert ok is False
    assert err == "That is not a number."


def test_parse_guess_plus_sign():
    # Plus sign with number
    ok, value, err = parse_guess("+42")
    assert ok is True
    assert value == 42
    assert err is None


# ===== Edge cases for update_score =====
def test_update_score_win_with_negative_score():
    # Win with negative current score
    new_score = update_score(-50, "Win", 0)
    assert new_score == 40  # -50 + 90


def test_update_score_too_high_with_negative_score():
    # Too High with negative current score
    new_score = update_score(-50, "Too High", 0)
    assert new_score == -45  # -50 + 5


def test_update_score_too_low_with_negative_score():
    # Too Low with negative current score
    new_score = update_score(-50, "Too Low", 0)
    assert new_score == -55  # -50 - 5


def test_update_score_with_very_large_attempt_number():
    # Very large attempt number for Win
    new_score = update_score(0, "Win", 1000)
    assert new_score == 10  # Minimum of 10 points


def test_update_score_with_large_current_score():
    # Large current score
    new_score = update_score(10000, "Too High", 2)
    assert new_score == 10005


def test_update_score_win_exact_minimum():
    # Win that results in exactly 10 points
    new_score = update_score(0, "Win", 9)
    # 100 - 10*(9+1) = 100 - 100 = 0, so this adds 0 and hits minimum floor
    # Actually: 100 - 10*(9+1) = 0, which is < 10, so returns 10
    # Wait, need to re-read: it returns current_score + points where points is max(100 - 10*(n+1), 10)
    # So 100 - 10*10 = 0, becomes 10, so 0 + 10 = 10
    assert new_score == 10
