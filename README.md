# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Purpose.** A Streamlit number-guessing game. You pick a difficulty (Easy 1–20, Normal 1–100, Hard 1–200), guess the secret number within a limited number of attempts, and get a "Go HIGHER" / "Go LOWER" hint after each guess. Your score goes up for winning quickly and down for wrong guesses.

**Bugs found.**
- The hints were inverted ("Go HIGHER" when the guess was too high).
- On every even attempt the secret was converted to a string, so numbers were compared as text (`"9" > "50"`).
- New Game did not reset score, status or history, ignored the difficulty range, and left you stuck on "Game over" after a win or loss.
- Hard (1–50) was easier than Normal (1–100).
- The attempt counter started at 1, so the first guess used up two attempts' worth of the limit, and the "Attempts left" text lagged one guess behind.
- Invalid input (like `abc`) used up an attempt, and decimals like `3.7` were silently truncated to `3`.
- Changing difficulty kept the old secret, so it could fall outside the new range.
- Scoring was off by one on a win, and a wrong "Too High" guess gave +5 points on even attempts.

**Fixes applied.**
- The game logic now lives in `logic_utils.py`, and `app.py` imports it instead of keeping duplicate copies.
- Hints are correct, and guesses are always compared as integers.
- `parse_guess` trims whitespace and rejects empty input, non-integers and out-of-range numbers without costing an attempt.
- A single `reset_game()` helper resets the secret, attempts, score, status and history, and runs on New Game and on difficulty changes.
- The attempt counter starts at 0, and the info line uses the real range and a correct "Attempts left" count.
- The score formula is fixed: a win scores `100 - 10 × attempt` (minimum 10), and every wrong guess costs 5.
- Each fix has a `# FIX:` comment in the code, and `tests/test_game_logic.py` has regression tests for the logic fixes.

## 📸 Demo Walkthrough

A sample game on **Normal** (range 1–100) where the secret number is **55**:

1. The sidebar shows "Range: 1 to 100" and "Attempts allowed: 8". The info line says "Attempts left: 8".
2. The user enters `abc`. The game shows "Enter a whole number." and no attempt is used.
3. The user enters `150`. The game shows "Guess must be between 1 and 100." and no attempt is used.
4. The user enters `40`. The game shows "📈 Go HIGHER!" (outcome "Too Low"). The score is **-5** and "Attempts left" is 7.
5. The user enters `70`. The game shows "📉 Go LOWER!" (outcome "Too High"). The score is **-10** and "Attempts left" is 6.
6. The user enters `55`. The game shows "🎉 Correct!" with balloons, and the status becomes "won". The win scores 100 - 10 × 3 = 70, so the final score is **60**.
7. Any further guess shows "You already won. Start a new game to play again."
8. The user clicks **New Game**. A new secret is drawn from the current difficulty range, the score goes back to 0, the history is cleared and the attempts counter resets.

The scores and messages above come from running `parse_guess`, `check_guess` and `update_score` on that exact sequence of inputs. I haven't recorded a screenshot.

## 🧪 Test Results

```
$ python3 -m pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/parvbhardwaj/Desktop/AI110/p1/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.10.0
collected 36 items

tests/test_game_logic.py ....................................            [100%]

============================== 36 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
