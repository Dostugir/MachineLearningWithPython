from flask import Flask, render_template, request, jsonify, session
import random
import os

# Initialize Flask app with the correct template folder
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'your-secret-key'

# Game state stored in a dictionary to handle multiple games
games = {}

@app.route('/')
def home():
    return render_template('game.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game_id = str(random.randint(100000, 999999))
    games[game_id] = {
        'secret_number': random.randint(1, 100),
        'game_status': 'playing'
    }
    return jsonify({'game_id': game_id})

@app.route('/make_guess', methods=['POST'])
def make_guess():
    data = request.get_json()
    game_id = data.get('game_id')
    guess = data.get('guess')
    
    if game_id not in games:
        return jsonify({'error': 'Invalid game'}), 400
    
    game = games[game_id]
    
    if game['game_status'] != 'playing':
        return jsonify({'error': 'Game is over'}), 400
    
    if guess == game['secret_number']:
        game['game_status'] = 'won'
        result = 'correct'
    elif guess < game['secret_number']:
        result = 'low'
    else:
        result = 'high'
    
    response = {
        'result': result,
        'game_status': game['game_status']
    }
    
    if game['game_status'] == 'won':
        response['secret_number'] = game['secret_number']
    
    return jsonify(response)

if __name__ == '__main__':
    # Print the template directory path for debugging
    print(f"Template directory: {template_dir}")
    app.run(debug=True, host='0.0.0.0', port=5000)
