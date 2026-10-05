# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
 1. 53      Guess lower          Guess higher        n/a
 2. clicked new game | new game starts | nothing happens | n/a
3. toaster messages are faulty
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude (Claude Code in VS Code, agent mode)
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

**Correct suggestion: the hints were inverted, and the string-secret was the real cause of the "random" behaviour.**
Claude pointed out that `check_guess` returned "Go HIGHER!" when the guess was above the secret (and "Go LOWER!" when below). It also found that `app.py` converted the secret to a `str` on every even attempt, which forced `check_guess` into its `except TypeError` fallback and compared the numbers as text (`"9" > "50"` is true). That second finding explained why the hints felt wrong only some of the time, which I hadn't worked out myself. It was correct because the messages contradicted the outcome labels right next to them, and the string comparison is a known pitfall. I verified it by reading the code path, then with pytest: `check_guess(60, 50)` must say "LOWER", `check_guess(40, 50)` must say "HIGHER", `check_guess(9, 50)` must be "Too Low", and a `str` secret now raises `TypeError` instead of being silently compared.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**Changed suggestion: the first "New Game" fix kept `attempts = 1`.**
When I asked Claude to fix New Game not resetting, its first version reset score, status and history and used the difficulty range, but it set `attempts` to 1 to match the initial value in the file. That value was itself part of an off-by-one bug (the first guess counted as attempt 2, so you lost an attempt). Copying a buggy default just to be consistent was a poor fit, so the later pass changed it: `attempts` now counts guesses made and starts at 0, and a single `reset_game()` helper is used for startup, New Game and difficulty changes. I verified it by checking that "Attempts left" starts at the full limit, and with the scoring tests (a first-attempt win scores 90, not 80).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I treated a bug as fixed only when a test failed on the old behaviour and passed on the new one. For each bug in the log I wrote the expectation first (for example, "a guess of 60 against 50 must tell me to go lower"), then checked the code against it. I also moved the logic out of `app.py` into `logic_utils.py` so it could be tested without running Streamlit.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

Running `python3 -m pytest -q` in the project folder gives **36 passed**. Beyond the hint and string-secret tests above, the tests cover:
- `parse_guess` rejecting `3.7`, `nan`, `inf`, `1e3`, whitespace-only input and out-of-range numbers, while accepting the boundaries 1 and 20.
- Hard's range being larger than Normal's.
- `update_score` giving 90 for a first-attempt win and charging 5 points for both "Too High" and "Too Low" on every attempt, odd or even.

One thing a test showed me about the starter code: the three provided tests compared `check_guess(...)` to a bare string, but the function returns an `(outcome, message)` tuple, so they could never pass. I fixed them to unpack the tuple. I also ran `python3 -m py_compile app.py` to confirm the refactored app has no syntax errors.

Not covered by tests: the fixes that live in the Streamlit script itself (New Game resetting state, invalid input not using up an attempt, secret regenerating on difficulty change). Those need a manual playthrough in the browser (`streamlit run app.py`) or Streamlit's `AppTest`.

- Did AI help you design or understand any tests? How?

Yes. Claude wrote the test cases and organised them by the bug each one targets, so a failing test points at the exact regression. It suggested edge cases I wouldn't have thought of, like `"nan"`, `"inf"` and the range boundaries, and it explained why the starter tests were broken. I read each test and checked that it asserts the behaviour I wanted before trusting it.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
