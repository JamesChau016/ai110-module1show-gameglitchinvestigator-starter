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
