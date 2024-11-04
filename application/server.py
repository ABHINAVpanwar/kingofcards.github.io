from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/scores": {"origins": "https://kingofcards.netlify.app/views/alert"}})

# Define the path for the scores file
scores_file = 'scores.txt'

# Load scores from file or initialize with default data
def load_scores():
    if os.path.exists(scores_file):
        with open(scores_file, 'r') as f:
            return json.load(f)
    else:
        # Sample data for players' scores
        return [
            {"name": "ABHINAV", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0,
             "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
            {"name": "ABHISHEK", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0,
             "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
            {"name": "AKHIL", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0,
             "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
            {"name": "SAHIL", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0,
             "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
            {"name": "SHRUTI", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0,
             "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
            {"name": "UTKARSH", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0,
             "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
        ]

# Save scores to file
def save_scores():
    with open(scores_file, 'w') as f:
        json.dump(scores, f)

# Load initial scores
scores = load_scores()

# API route to provide scores
@app.route('/scores', methods=['GET'])
def get_scores():
    filtered_scores = []
    for player in scores:
        # Calculate total score for each player
        player['total'] = (
            player['monopoly1'] + player['bluff1'] + player['spoon1'] + player['uno1'] +
            player['monopoly2'] + player['bluff2'] + player['spoon2'] + player['uno2']
        )
        # Add player to the filtered list if their total score is not zero
        if player['total'] > 0:
            filtered_scores.append(player)
    
    return jsonify(filtered_scores)

# Management page route
@app.route('/', methods=['GET', 'POST'])
def manage_scores():
    if request.method == 'POST':
        for player in scores:
            if player['name'] == request.form['name']:
                # Update only the specific scores from the form data if they are greater than zero
                if int(request.form['monopoly1']) > 0:
                    player['monopoly1'] = int(request.form['monopoly1'])
                if int(request.form['bluff1']) > 0:
                    player['bluff1'] = int(request.form['bluff1'])
                if int(request.form['spoon1']) > 0:
                    player['spoon1'] = int(request.form['spoon1'])
                if int(request.form['uno1']) > 0:
                    player['uno1'] = int(request.form['uno1'])
                if int(request.form['monopoly2']) > 0:
                    player['monopoly2'] = int(request.form['monopoly2'])
                if int(request.form['bluff2']) > 0:
                    player['bluff2'] = int(request.form['bluff2'])
                if int(request.form['spoon2']) > 0:
                    player['spoon2'] = int(request.form['spoon2'])
                if int(request.form['uno2']) > 0:
                    player['uno2'] = int(request.form['uno2'])
                
                # Save updated scores to file
                save_scores()
                break

        return render_template('manage.html', scores=scores)

    return render_template('manage.html', scores=scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
