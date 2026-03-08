import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


def get_hint_message(outcome: str):
    """Get the hint message for a given outcome."""
    if outcome == "Win":
        return "🎉 Correct!"
    elif outcome == "Too High":
        return "📉 Go LOWER!"
    else:  # Too Low
        return "📈 Go HIGHER!"

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 4,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "raw_guess_input" not in st.session_state:
    st.session_state.raw_guess_input = ""

if "_clear_input_next_run" not in st.session_state:
    st.session_state._clear_input_next_run = False

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

# Clear input at the START of the run, before the widget is instantiated
if st.session_state._clear_input_next_run:
    st.session_state.raw_guess_input = ""
    st.session_state._clear_input_next_run = False

st.subheader("Make a guess")

# Placeholder for the info box to update after processing a guess
info_placeholder = st.empty()

st.text_input(
    "Enter your guess:",
    key="raw_guess_input"
)

raw_guess = st.session_state.raw_guess_input

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True, key="show_hint")

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.status = "playing"
    st.session_state.last_hint = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.last_hint = ("error", err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)

        if show_hint:
            message = get_hint_message(outcome)
            st.session_state.last_hint = ("warning", message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    # Clear the input next run so it doesn't appear to lag on the next run.
    st.session_state._clear_input_next_run = True
    st.rerun()

# Update the status display after handling any actions.
info_placeholder.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

if st.session_state.last_hint:
    kind, msg = st.session_state.last_hint
    if kind == "warning":
        st.warning(msg)
    else:
        st.error(msg)

# Display debug info
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
