from flask import Flask, request, session, jsonify, render_template
import string
import random
from words import words

app = Flask(__name__)
app.secret_key = 'your_secret_key'

HANGMAN_VISUAL = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

@app.route('/guess', methods=['POST'])
def guess():
    letter = request.form['letter'].upper()
    if 'output' not in session:
        session['output'] = []
    
    if letter in string.ascii_uppercase and letter not in session['used_letters']:
        session['used_letters'].append(letter)
        if letter in session['word_letters']:
            session['word_letters'] = [l for l in session['word_letters'] if l != letter]
            session['output'].append(f">>> {letter}\nCorrect!")
        else:
            session['lives'] -= 1
            session['output'].append(f">>> {letter}\nIncorrect!")
    else:
        session['output'].append(f">>> {letter}\nInvalid input or already used letter.")
    
    session['hangman_visual'] = HANGMAN_VISUAL[7 - session['lives']]
    
    if session['lives'] == 0:
        session['output'].append("Game Over! You've run out of lives.")
        session['game_over'] = True
    elif len(session['word_letters']) == 0:
        session['output'].append("Congratulations! You've guessed the word.")
        session['output'].append("walnutshrimp.aternos.me")
    
    print(len(session['word_letters']))

    game_state = {
        'word': session['word'],
        'word_letters': session['word_letters'],
        'used_letters': session['used_letters'],
        'lives': session['lives'],
        'output': session['output'],
        'hangman_visual': session['hangman_visual'],
        'game_over': session['game_over']
    }
    
    return jsonify(game_state=game_state), 200

@app.route('/game_over')
def game_over():
    return render_template('game_over.html', 
                           word=session['word'], 
                           lives=session['lives'])

@app.route('/')
def index():
    if 'word' not in session:
        session['word'] = random.choice(words).upper()
        session['word_letters'] = list(session['word'])
        session['used_letters'] = []
        session['lives'] = 7
        session['output'] = []
        session['hangman_visual'] = HANGMAN_VISUAL[0]
        session['game_over'] = False
    return render_template('index.html', game_state=session)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    session['word'] = random.choice(words).upper()
    session['word_letters'] = list(session['word'])
    session['used_letters'] = []
    session['lives'] = 6
    session['output'] = []
    session['hangman_visual'] = HANGMAN_VISUAL[0]
    session['game_over'] = False
    return jsonify(message="Game has been reset"), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)  # Ensure this is set correctly