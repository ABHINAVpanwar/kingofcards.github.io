from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import db, Player  # Import db and Player from models.py
import os

app = Flask(__name__)
CORS(app, resources={
    r"/scores": {"origins": "https://kingofcards.netlify.app"},
    r"/get_messages": {"origins": "https://kingofcards.netlify.app"},
    r"/send_message": {"origins": "https://kingofcards.netlify.app"},
    r"/get_password": {"origins": "https://kingofcards.netlify.app"}
})

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///scores.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Sample data for initializing the database
def initialize_database():
    with app.app_context():  # Ensure this runs within the application context
        sample_players = [
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
        for player_data in sample_players:
            player = Player.query.filter_by(name=player_data['name']).first()
            if not player:
                new_player = Player(**player_data)
                db.session.add(new_player)
        db.session.commit()

# Create the database tables (if they don't exist)
with app.app_context():
    db.create_all()
    initialize_database()  # Initialize the database with sample data

# API route to provide scores
@app.route('/scores', methods=['GET'])
def get_scores():
    players = Player.query.all()
    filtered_scores = []
    for player in players:
        player.total = (
            player.monopoly1 + player.bluff1 + player.spoon1 + player.uno1 +
            player.monopoly2 + player.bluff2 + player.spoon2 + player.uno2
        )
        if player.total > 0:
            filtered_scores.append({
                "name": player.name,
                "monopoly1": player.monopoly1,
                "bluff1": player.bluff1,
                "spoon1": player.spoon1,
                "uno1": player.uno1,
                "monopoly2": player.monopoly2,
                "bluff2": player.bluff2,
                "spoon2": player.spoon2,
                "uno2": player.uno2,
                "total": player.total
            })
    return jsonify(filtered_scores)

# Management page route
@app.route('/', methods=['GET', 'POST'])
def manage_scores():
    if request.method == 'POST':
        player = Player.query.filter_by(name=request.form['name']).first()
        if player:
            # Update only the fields that are provided in the form and have a value greater than 0
            if 'monopoly1' in request.form and int(request.form['monopoly1']) > 0:
                player.monopoly1 = int(request.form['monopoly1'])
            if 'bluff1' in request.form and int(request.form['bluff1']) > 0:
                player.bluff1 = int(request.form['bluff1'])
            if 'spoon1' in request.form and int(request.form['spoon1']) > 0:
                player.spoon1 = int(request.form['spoon1'])
            if 'uno1' in request.form and int(request.form['uno1']) > 0:
                player.uno1 = int(request.form['uno1'])
            if 'monopoly2' in request.form and int(request.form['monopoly2']) > 0:
                player.monopoly2 = int(request.form['monopoly2'])
            if 'bluff2' in request.form and int(request.form['bluff2']) > 0:
                player.bluff2 = int(request.form['bluff2'])
            if 'spoon2' in request.form and int(request.form['spoon2']) > 0:
                player.spoon2 = int(request.form['spoon2'])
            if 'uno2' in request.form and int(request.form['uno2']) > 0:
                player.uno2 = int(request.form['uno2'])
            # Save updated scores to the database
            db.session.commit()
        return render_template('manage.html', scores=Player.query.all())
    return render_template('manage.html', scores=Player.query.all())

@app.route('/reset', methods=['POST'])
def reset_scores():
    players = Player.query.all()
    for player in players:
        player.monopoly1 = 0
        player.bluff1 = 0
        player.spoon1 = 0
        player.uno1 = 0
        player.monopoly2 = 0
        player.bluff2 = 0
        player.spoon2 = 0
        player.uno2 = 0
        player.total = 0
    db.session.commit()
    return jsonify({"status": "success", "message": "Scores reset to zero."})

messages = []  # Define the messages list globally

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    sender = data.get('sender')
    message = data.get('message')

    if sender and message:
        messages.append({'sender': sender, 'message': message})
        return jsonify({'status': 'Message received', 'message': data})
    
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

PASSWORD = "jhulaagangg"  # Server-stored password

@app.route('/get_password', methods=['GET'])
def get_password():
    return jsonify({"password": PASSWORD})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
