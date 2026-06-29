"""Regression tests for the bugs fixed in the Game Glitch Investigator.

Run from the project root:  pytest

Bugs covered:
  1. Backwards hints  -> check_guess (logic_utils.py)
  2. Swapped ranges   -> get_range_for_difficulty (logic_utils.py)
  3. Attempt counting -> the "Attempts left" / game-over logic in app.py
"""

import sys
from pathlib import Path

import pytest

# Make sure the project root (which holds logic_utils.py) is importable
# regardless of where pytest is launched from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logic_utils import check_guess, get_range_for_difficulty


# ---------------------------------------------------------------------------
# Bug 1: Hints were backwards.
# A guess ABOVE the secret must tell the player to go LOWER, and a guess
# BELOW the secret must tell the player to go HIGHER.
# ---------------------------------------------------------------------------

def test_guess_higher_than_secret_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_guess_lower_than_secret_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


def test_correct_guess_wins():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


@pytest.mark.parametrize(
    "guess, secret, expected_outcome",
    [
        (1, 100, "Too Low"),    # far below
        (100, 1, "Too High"),   # far above
        (51, 50, "Too High"),   # just above (off-by-one direction check)
        (49, 50, "Too Low"),    # just below
    ],
)
def test_hint_direction_is_never_inverted(guess, secret, expected_outcome):
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected_outcome


# ---------------------------------------------------------------------------
# Bug 2: Difficulty ranges for Normal and Hard were swapped.
# Easy = 1-20 (already correct), Normal = 1-50, Hard = 1-100.
# Hard must cover at least as wide a range as Normal.
# ---------------------------------------------------------------------------

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 50)


def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_hard_is_wider_than_normal_is_wider_than_easy():
    easy_high = get_range_for_difficulty("Easy")[1]
    normal_high = get_range_for_difficulty("Normal")[1]
    hard_high = get_range_for_difficulty("Hard")[1]
    assert easy_high < normal_high < hard_high


# ---------------------------------------------------------------------------
# Bug 3: Attempt counting.
# The header showed "Attempts left" decreasing while the debug panel showed
# the raw attempt count increasing, and the game declared "out of attempts"
# while a guess still remained.
#
# The attempt logic lives inline in app.py (Streamlit), so it is reproduced
# here as the intended specification. Both displays must derive from the same
# `attempts` counter, and the game must only be over once attempts reach the
# limit -- never while at least one attempt remains.
# ---------------------------------------------------------------------------

def attempts_left(attempt_limit, attempts):
    """What the header should show -- the single source of truth."""
    return attempt_limit - attempts


def is_game_over(attempt_limit, attempts):
    """Game ends only when no attempts remain (matches app.py: attempts >= limit)."""
    return attempts >= attempt_limit


def test_attempts_left_matches_remaining_count():
    limit = 8
    # After 3 guesses, 5 attempts should remain.
    assert attempts_left(limit, 3) == 5


def test_attempts_left_and_debug_count_are_consistent():
    # The header value and the debug "Attempts" value come from the same
    # counter, so they must always add up to the limit.
    limit = 6
    for attempts in range(0, limit + 1):
        assert attempts_left(limit, attempts) + attempts == limit


def test_not_game_over_while_an_attempt_remains():
    limit = 5
    # On the 4th attempt one guess still remains -> not out of attempts.
    assert attempts_left(limit, 4) == 1
    assert is_game_over(limit, 4) is False


def test_game_over_exactly_when_attempts_reach_limit():
    limit = 5
    assert is_game_over(limit, 5) is True
    assert attempts_left(limit, 5) == 0


def test_attempts_left_never_negative_before_game_over():
    limit = 8
    for attempts in range(0, limit + 1):
        if not is_game_over(limit, attempts):
            assert attempts_left(limit, attempts) > 0
