import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- check_guess: outcomes (starter tests fixed to unpack the (outcome, message) tuple) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug: hints were inverted ---

def test_too_high_tells_player_to_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_too_low_tells_player_to_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


# --- Bug: secret became a str on even attempts, giving lexicographic comparison ---

def test_comparison_is_numeric_not_lexicographic():
    # As strings, "9" > "50" would be True; numerically 9 is too low.
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


def test_string_secret_is_not_silently_accepted():
    # The old TypeError fallback masked the bug; a str secret should now fail loudly.
    with pytest.raises(TypeError):
        check_guess(9, "50")


# --- Bug: Hard range (1-50) was easier than Normal (1-100) ---

def test_hard_range_is_larger_than_normal():
    n_low, n_high = get_range_for_difficulty("Normal")
    h_low, h_high = get_range_for_difficulty("Hard")
    assert (h_high - h_low) > (n_high - n_low)


def test_easy_is_smallest_range():
    e_low, e_high = get_range_for_difficulty("Easy")
    n_low, n_high = get_range_for_difficulty("Normal")
    assert (e_high - e_low) < (n_high - n_low)


# --- Bugs: parse_guess truncated decimals, ignored whitespace, had no range check ---

def test_parse_valid_integer():
    assert parse_guess("7", 1, 20) == (True, 7, None)


def test_parse_strips_whitespace():
    ok, value, _ = parse_guess("  7  ", 1, 20)
    assert ok and value == 7


@pytest.mark.parametrize("raw", ["", "   ", None])
def test_parse_rejects_empty(raw):
    ok, value, err = parse_guess(raw, 1, 20)
    assert not ok and value is None and err


def test_parse_rejects_decimal_instead_of_truncating():
    ok, value, _ = parse_guess("3.7", 1, 20)
    assert not ok and value is None


@pytest.mark.parametrize("raw", ["abc", "nan", "inf", "1e3"])
def test_parse_rejects_non_numbers(raw):
    ok, _, err = parse_guess(raw, 1, 20)
    assert not ok and err


@pytest.mark.parametrize("raw", ["0", "21", "-5", "1000"])
def test_parse_rejects_out_of_range(raw):
    ok, value, err = parse_guess(raw, 1, 20)
    assert not ok and value is None and "between 1 and 20" in err


@pytest.mark.parametrize("raw", ["1", "20"])
def test_parse_accepts_range_boundaries(raw):
    ok, _, _ = parse_guess(raw, 1, 20)
    assert ok


# --- Bugs: win formula off by one; "Too High" rewarded wrong guesses on even attempts ---

def test_win_on_first_attempt_scores_90():
    # Old formula used (attempt + 1) and gave 80.
    assert update_score(0, "Win", 1) == 90


def test_win_score_has_floor_of_10():
    assert update_score(0, "Win", 50) == 10


@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_too_high_always_penalised_regardless_of_attempt_parity(attempt):
    assert update_score(20, "Too High", attempt) == 15


@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_too_low_always_penalised(attempt):
    assert update_score(20, "Too Low", attempt) == 15


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(20, "???", 1) == 20
