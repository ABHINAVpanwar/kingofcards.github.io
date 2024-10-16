from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data for players' scores with games played twice
scores = [
    {"name": "ABHINAV", "monopoly1": 1, "bluff1": 2, "spoon1": 0, "uno1": 0, "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
    {"name": "ABHISHEK", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0, "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
    {"name": "SAHIL", "monopoly1": 0, "bluff1": 1, "spoon1": 2, "uno1": 2, "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
    {"name": "SHRUTI", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0, "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
    {"name": "UTKARSH", "monopoly1": 0, "bluff1": 0, "spoon1": 0, "uno1": 0, "monopoly2": 0, "bluff2": 0, "spoon2": 0, "uno2": 0, "total": 0},
]

# API route to provide scores
@app.route('/scores', methods=['GET'])
def get_scores():
    for player in scores:
        # Calculate total score for each player
        player['total'] = (
            player['monopoly1'] + player['bluff1'] + player['spoon1'] + player['uno1'] +
            player['monopoly2'] + player['bluff2'] + player['spoon2'] + player['uno2']
        )
    return jsonify(scores)

if __name__ == '__main__':
    app.run(debug=True)