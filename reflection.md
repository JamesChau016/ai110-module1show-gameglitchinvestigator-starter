# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

**Answers:**
- Higher/ Lower hints were backwards
- New game option not working
- Range and number of guesses don't correspond with the difficulty
- Game ends before number of attempts displayed run out
- Submit guess button doesn't submit your answer right away
- The history in the developer info doesn't update right away
- Point system is wrong
- Submit button now clears answer and still doesn't work right away


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

**Answers:**
- Github Copilot
- Example: fixing the hint: Problem: In the check_guess function's except TypeError block
  (lines 42-44), the emoji messages for string comparison were swapped.
- Example: Fix: Added resets for score = 0, history = [], and status = "playing". Also fixed
  using hardcoded. The AI added lines of code that actually already existed


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**Answers:**
- Using the game logic tests and playing the game myself
- I ran test_winning_guess with pytest, it showed me whether the hint works or not
- AI helped me write the tests

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

**Answers:**
- The secret number is generated using random.randint(low, high) everytime the app reruns or reload low/high depend on the difficulty
- Streamlit rerun reruns the entire app upon any user interaction, the session states keep the wanted data between reruns
- By changeing the range of low and high to match the difficulty

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**Answers:**
- Always double check the AI's solution, use git to return to previous version if the solution doesn't work or breaks the app
- Always give the AI the needed context, in this case, the code base before every prompt
- Very convenient, but they tend to hallucinate or change code that they aren't suppose to change

- Claude gave way more efficient fixes compare to CoPilot, this is probably due to the models' capabilities and their access to the entire code base (both of which Claude did better)