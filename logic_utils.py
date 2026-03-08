def get_range_for_difficulty(difficulty: str):
    """
    Retrieve the valid number range for a given game difficulty level.
    
    This function maps difficulty levels to their corresponding number ranges.
    Unknown difficulty levels default to the Hard range to ensure reasonable gameplay.
    
    Args:
        difficulty (str): The difficulty level as a string. Supported values are:
            - "Easy": Range 1-20 (narrower range, easier to guess)
            - "Normal": Range 1-50 (medium range, balanced difficulty)
            - "Hard": Range 1-100 (wide range, challenging difficulty)
            - Any other value defaults to Hard range
    
    Returns:
        tuple: A pair of integers (low, high) representing the inclusive range.
            - low (int): The minimum possible secret number (always 1)
            - high (int): The maximum possible secret number (20, 50, or 100)
    
    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Normal")
        (1, 50)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
        >>> get_range_for_difficulty("Impossible")  # Unknown difficulty
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse and validate user input into an integer guess.
    
    Converts raw user input (string) into an integer value. Handles various input
    formats including integers, floats (truncated to int), and numbers with whitespace.
    Returns validation status and error messages for invalid input.
    
    Args:
        raw (str or None): The raw user input to parse. Accepts:
            - Integer strings: "42", "-25", "+10"
            - Float strings: "3.14" (converts to int: 3)
            - Whitespace: Leading/trailing spaces are handled by float()
            - None: Treated as empty/no input
    
    Returns:
        tuple: A three-element tuple (ok, guess_int, error_message)
            - ok (bool): True if parsing succeeded, False otherwise
            - guess_int (int or None): The parsed integer value if ok is True,
              None if parsing failed
            - error_message (str or None): Descriptive error message if ok is False,
              None if parsing succeeded. Possible messages:
              - "Enter a guess." - Input was None or empty string
              - "That is not a number." - Input could not be converted to a number
    
    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.14")
        (True, 3, None)
        >>> parse_guess("")
        (False, None, "Enter a guess.")
        >>> parse_guess("abc")
        (False, None, "That is not a number.")
        >>> parse_guess("-25")
        (True, -25, None)
    
    Notes:
        - Float values are truncated (not rounded) to integers using int()
        - Negative numbers are supported and returned as-is
        - Very large numbers are supported by Python's integer type
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare a player's guess against the secret number and return the outcome.
    
    Determines the relationship between the guess and secret number, providing
    immediate feedback to the player. Used for each guess in the game loop.
    
    Args:
        guess (int or float): The player's guess value. Can be any numeric value
            including negative numbers and floats.
        secret (int or float): The target secret number to match. Can be any numeric
            value as defined by the game difficulty range.
    
    Returns:
        str: One of three outcome strings:
            - "Win": The guess exactly matches the secret number
            - "Too High": The guess is greater than the secret number
            - "Too Low": The guess is less than the secret number
    
    Examples:
        >>> check_guess(50, 50)
        "Win"
        >>> check_guess(60, 50)
        "Too High"
        >>> check_guess(40, 50)
        "Too Low"
        >>> check_guess(100, 1)
        "Too High"
        >>> check_guess(-5, 50)
        "Too Low"
    
    Notes:
        - Uses simple numeric comparison (==, >, <) for determining outcomes
        - No side effects; pure function for game logic
        - Works with any numeric types (int, float)
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    else:
        return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate the updated player score based on game outcome and attempt count.
    
    Applies the game's scoring rules to award or deduct points based on the player's
    guess outcome and how many attempts it took. Incentivizes winning quickly while
    penalizing incorrect guesses.
    
    Scoring Rules:
        - Win: Award max(100 - 10*(attempt_number + 1), 10) points
          * First attempt: +90 points
          * Second attempt: +80 points
          * ... decreasing by 10 for each attempt
          * Minimum: 10 points (added to player's score regardless of attempt count)
        
        - Too High (empty on even attempts): +5 points
        - Too High (on odd attempts): -5 points
        
        - Too Low: Always -5 points (regardless of attempt number)
        
        - Unknown outcome: No change to score
    
    Args:
        current_score (int): The player's current score before this update.
            Can be negative or any integer value.
        outcome (str): The result of the most recent guess. Supported values:
            - "Win": Player guessed correctly
            - "Too High": Player's guess exceeded the secret number
            - "Too Low": Player's guess was below the secret number
            - Any other value: Score remains unchanged
        attempt_number (int): Zero-indexed attempt count (0 for first attempt,
            1 for second, etc.). Used to determine point values.
    
    Returns:
        int: The updated score after applying the outcome and attempt penalties/bonuses.
            Formula: current_score + points_adjustment
    
    Examples:
        >>> update_score(0, "Win", 0)  # First attempt win
        90
        >>> update_score(0, "Win", 1)  # Second attempt win
        80
        >>> update_score(100, "Too High", 0)  # Even attempt (no penalty)
        105
        >>> update_score(100, "Too High", 1)  # Odd attempt (penalty)
        95
        >>> update_score(100, "Too Low", 0)  # Always -5
        95
        >>> update_score(100, "Unknown", 5)  # Unknown outcome
        100
    
    Notes:
        - Win outcomes have a minimum floor of 10 points even after deductions
        - Too High alternates between +5 and -5 based on attempt parity
        - Score can go negative; no minimum floor on final score
        - This function is pure and has no side effects
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
