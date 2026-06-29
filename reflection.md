# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  It looked like a typical guessing game. You would enter a number you are guessing and it would give you hints of whether to go higher or lower. You can choose different levels of difficulties which means the range of numbers would either decrease/increase thus changing how hard/easy it may be to guess the correct number.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  - The hints were a little skewed (backwards). If your guess is higher than the secret number, it would still say "go higher" on the hint
  - The range of numbers for different difficulties. e.g. easy being range 1-20 is correct but normal range of 1-100 and hard range of 1-50 need to be switched.
  - The "Attempts left:" number that it shows on top of the screen keeps reducing count whereas under the developer debug info, the attemps count keeps increasing. It would also say I am out of attempts when I may have an attempt still left.



**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|guess of 34 |it should say go lower (secret number is 12) |Hint says go higher | none|
|guess of 101 |give error out of bounds since out of range 1 to 100|hint: Go HIGHER! |none |
|guess of 10|hint should be: Go higher |Hint: go lower |none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
The AI's suggestions on fixing the bugs it was asked to were correct. It was mostly correct because I would tell it exactly which lines/functions the bug may be in. I verified it by checking for that bug fixed in the app each time before proceeding to the next fix.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
One of the bugs the AI didn't correctly help fix was the hints correction. It didn't understand my prompt initially which may have caused it to be incorrect. A correction and more detailed prompt helped fix this eventually.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Refreshed the app after each bug fix, either visually or through the use of some test cases, verified if the bug was now working correctly as compared to incorrect ones before
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"
  this test checked if the hints shown each time a guess was entered were correct to help a player make better decisions
- Did AI help you design or understand any tests? How?
The AI did design the pytest cases but it was quite easy to follow along and understand them on my own

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
