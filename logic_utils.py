def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard was 1-50 (easier than Normal). Claude Code spotted it in review; widened to 1-200 in agent mode.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    # FIX: whitespace-only input used to slip through. Claude Code added strip(); I requested the fix.
    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    # FIX: "3.7" was silently truncated to 3. Claude Code now rejects non-integers instead.
    try:
        value = int(raw)
    except ValueError:
        return False, None, "Enter a whole number."

    # FIX: no range validation before. Claude Code added bounds checks, refactored here from app.py.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: hints were inverted and a str-fallback hid a type bug. Claude Code diagnosed both;
    # now a plain int comparison with correct hints (done together in agent mode).
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number (attempt_number is 1-based)."""
    if outcome == "Win":
        # FIX: formula used (attempt_number + 1), an off-by-one. Claude Code corrected it at my request.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: "Too High" gave +5 on even attempts (rewarding wrong guesses). Claude Code made both -5.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
