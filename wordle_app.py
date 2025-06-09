import math
import random
from flask import Flask, render_template, request
from wordle_lists import curated_words, possible_words

app = Flask(__name__)


def score_wordle(guess, answer):
    """
    Given a guess and an answer, return score in the format: ['#','#','#','#','#']
    - A score of 1 means the letter is correct and in the right position
    - A score of 2 means the letter is present in the answer but in the wrong position
    - A score of 0 means the letter is not present in the answer word

    Input:
        guess (str): A 5-letter guess the user submits
        answer (str): The 5-letter answer of a given Wordle puzzle
    Output (List[str]): A list representation of a Wordle feedback score with 0,1,2
        representing gray, green, and yellow tiles respectively
    """
    score = ['0'] * 5
    remaining = {}

    for i in range(5):
        if guess[i] == answer[i]:
            score[i] = '1'
        else:
            remaining[answer[i]] = remaining.get(answer[i], 0) + 1

    for i in range(5):
        if score[i] == '0' and guess[i] in remaining and remaining[guess[i]] > 0:
            score[i] = '2'
            remaining[guess[i]] -= 1

    return score


def guess_eliminator(guess, score, possible):
    """
    Given a guess, feedback score, and bank of remaining possible answers, prune
    candidate answers that do not adhere to the feedback score.

    Input:
        guess (str): A 5-letter guess the user submits
        score (List[str]): A list representation of a Wordle feedback score with 0,1,2
            representing gray, green, and yellow tiles respectively
        possible (List[str]): List of candidate answers 
    Output (List[str]): Pruned list of candidate answers
    """
    remaining = []
    required_counts = {}

    for i in range(5):
        if score[i] in ('1', '2'):
            required_counts[guess[i]] = required_counts.get(guess[i], 0) + 1

    for candidate in possible:
        match = True
        for i in range(5):
            g_letter = guess[i]
            c_letter = candidate[i]
            feedback = score[i]
            if feedback == '1':
                if not c_letter == g_letter:
                    match = False
                    break
            elif feedback == '2':
                if g_letter not in candidate or c_letter == g_letter:
                    match = False
                    break
            elif feedback == '0':
                if g_letter in required_counts and candidate.count(g_letter) > required_counts[g_letter]:
                    match = False
                    break
                elif g_letter not in required_counts and g_letter in candidate:
                    match = False
                    break

        if match:
            remaining.append(candidate)

    return remaining


def next_guess(remaining_answers):
    """
    Given a list of remaining answers, find the next optimal guess using
    entropy. If multiple guesses are tied for maximum entropy, guesses in the remaining
    answers list are preferred. If multiple words in the remaining answers list
    are tied, one is chosen at random.
        
    Input:
        remaining_answers (List[str]): A list of remaining answers that have
            been pruned to adhere to the most recent feedback score
    Output (str): Optimal guess with maximum entropy or None if no answers remain
    """
    if not remaining_answers:
        return None

    if len(remaining_answers) == 1:
        return remaining_answers[0]

    max_entropy = 0
    best_guesses = []
    denominator = len(remaining_answers)
    for candidate in possible_words:
        score_dict = {}
        for answer in remaining_answers:
            score = ''.join(score_wordle(candidate, answer))
            score_dict[score] = score_dict.get(score, 0) + 1
        ent = 0
        for count in score_dict.values():
            fraction = count / denominator
            ent -= fraction * math.log2(fraction)
        if ent > max_entropy:
            max_entropy = ent
            best_guesses = [candidate]
        elif ent == max_entropy:
            best_guesses.append(candidate)

    if not best_guesses:
        best_guesses = remaining_answers

    finalists = [w for w in best_guesses if w in remaining_answers] or best_guesses

    return random.choice(finalists)


state = {
    "remaining_words": curated_words.copy()
}

first_guess = 'TARSE'

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the Wordle Engine.

    - On GET: renders the current board state with the suggested guess.
    - On POST: receives a user guess and feedback, validates input, updates the
      list of possible answers, and returns a new suggestion or an error message.

    Output: Rendered HTML page with updated state and recommendation
    """
    message = ""
    suggested_guess = first_guess if state["remaining_words"] == curated_words else ""

    if request.method == "POST":
        guess = request.form.get("guess", "").strip().lower()
        feedback = request.form.get("feedback", "").strip()

        if guess not in possible_words:
            message = "Invalid submission. Guess not in valid word list."
        else:
            score_formatted = list(feedback)
            new_remaining_words = guess_eliminator(guess, score_formatted, state["remaining_words"])

            if not new_remaining_words:
                message = "Invalid submission. Feedback leaves no remaining answers"
            else:
                suggested_guess = next_guess(new_remaining_words)
                message = f"Remaining words: {len(new_remaining_words)}"
                state["remaining_words"] = new_remaining_words

    return render_template(
        "index.html",
        message=message,
        guess=suggested_guess,
        total_count=len(curated_words),
        remaining_words=state["remaining_words"]
    )



@app.route("/reset", methods=["POST"])
def reset():
    """
    Resets the state of the app to the full curated word list.
    Called via POST from the frontend when the user clicks the Reset button.

    Output: Empty 204 response to signal frontend that reset is complete
    """
    state["remaining_words"] = curated_words.copy()
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
