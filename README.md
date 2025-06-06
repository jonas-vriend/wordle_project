# Wordle Engine

This program is a Wordle engine that takes a guess and its feedback as inputs and
recommends optimal guesses using Shannon Entropy. 

---

## How to Use
- Type a 5-letter word in the first row. Note that the optimal first guess
'TARSE' is already displayed in the box to the right of the board.
- Click on tiles to toggle between feedback colors (gray, yellow, green).
- When ready, click **Submit**. The box to the right will display the optimal next guess.

---

## Methodology
- After a guess and its feedback are submitted, the program iterates through all
14855 valid guesses. 
- For a given guess, it iterates through a bank of remaining possible answers.
- Each (guess, answer) pair is scored and saved in a dictionary.
- Once the scoring is complete, the probability of each score is computed as
the frequency of the score over the number of remaining answers.
- These probabilities are computed into the Shannon Entropy formula:
 `H = -∑ p(x) log₂ p(x)`
- The word with the highest entropy is selected as the next guess.
- Sometimes entropy calculations yield ties. The algorithm has a preference for
words in the list of possible remaining answers. 
- If multiple words that are potential answers are tied for maximum entropy, a
word is selected at random.

---

## Getting Started

This app is not currently hosted online. To use it, you'll need to run it
locally.

### 1. Clone the repository
```bash
git clone https://github.com/jonas-vriend/wordle_project.git
```
### 2. Install required Python package
```bash
pip install Flask
```
### 3. Run the application
```bash
python wordle_app.py
```
### 4. Access the app
Once up and running, the app should print a link in the terminal (ie Running on http://127.0.0.1:5000). Paste it into your web browser. 

---

## Project Structure
```t
wordle_project/
├── wordle_app.py         # Flask app and backend logic
├── wordle_lists.py       # Valid guesses and possible answers taken from Wordle source
├── templates/
│   └── index.html        # Frontend HTML
├── README.md             # Project documentation
```
---

## Disclaimers

### 1. Perishability of Data
- The NYT has changed the valid guess list and possible answers before. This
program uses lists taken from Worlde source code that are accurate as of **6/6/25**.
- In the event these lists are changed, the lists in `wordle_lists.py`
and the optimal first guess (hard-coded for computational efficiency) in `wordle_app.py`
will need to be updated.

### 2. Entropy Calculations are Computationally Expensive
- Given 14,855 valid words and 2309 candidate answers, millions of calculations may be done for each guess. Make sure the platform you are running the program on can handle it!

### 3. What is Meant by "Optimal"
- Some of the program's recommendations - including the first word 'TARSE' - will
never be the solution to a puzzle. The goal of this program is not to get lucky. Instead, the goal is to minimize the average number of guesses to get to a solution in the **long run**.
---

## Author
```t
Jonas Vriend
BA, Economics, University of Chicago
Github: @jonas-vriend
```