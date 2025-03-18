from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/user_data": {"origins": "https://kingofcards.netlify.app"}})

# Configure the in-memory SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'defaultsecret'  # You can keep this as is

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a User model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local_ips = db.Column(db.String(200))
    time_zone = db.Column(db.String(100))
    network_type = db.Column(db.String(50))
    device_type = db.Column(db.String(50))

    def __repr__(self):
        return f"<User {self.id}>"

# Route to handle user data submission
@app.route('/user_data', methods=['POST'])
def user_data():
    try:
        data = request.get_json()
        
        # Create a new User entry
        new_user = User(
            local_ips=str(data.get('local_ips')),
            time_zone=data.get('time_zone'),
            network_type=data.get('network_type'),
            device_type=data.get('device_type')
        )
        
        # Add to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "Data saved successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to show saved user data in a simple webpage
@app.route('/')
def index():
    users = User.query.all()  # Retrieve all user data from the database

    # HTML template as a string, used directly in render_template_string
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KING OF CARDS</title>
        <link rel="icon" href="static/icon.png" />
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                cursor: default;
                display: flex;
                flex-direction: column;
                min-height: 100vh;  /* Ensures the body takes full height */
            }
            .container {
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 1000px;
                padding: 20px;
                flex: 1;  /* Allows the container to take available space */
                overflow: auto;  /* Scroll the container if content exceeds the height */
            }
            h1 {
                text-align: center;
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                table-layout: auto;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
                word-wrap: break-word;
            }
            th {
                background-color: #333;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            tr:hover {
                background-color: #e0e0e0;
            }
            @media (max-width: 768px) {
                table {
                    font-size: 14px;
                    border: 1px solid #ddd;
                }
                th, td {
                    padding: 8px;
                }
                .container {
                    padding: 10px;
                }
            }
            @media (max-width: 480px) {
                h1 {
                    font-size: 1.5em;
                }
                table {
                    font-size: 12px;
                }
                th, td {
                    padding: 6px;
                }
            }
            /* Responsive table: make table scrollable on smaller screens */
            .table-container {
                overflow-x: auto;
                width: 100%;
            }
            .fetch-button {
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .fetch-button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>LIVE USER TRACKING</h1>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Local IPs</th>
                            <th>Time Zone</th>
                            <th>Network Type</th>
                            <th>Device Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                            <tr>
                                <td>{{ user.id }}</td>
                                <td>{{ user.local_ips }}</td>
                                <td>{{ user.time_zone }}</td>
                                <td>{{ user.network_type }}</td>
                                <td>{{ user.device_type }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <button class="fetch-button" onclick="fetchData()">Fetch</button>
        <script>
            function fetchData() {
                location.reload();  // Reload the page when the "Fetch" button is clicked
            }
        </script>
    </body>
    </html>
    """

    # Render the HTML with the data
    return render_template_string(html, users=users)

# Initialize the database (create tables) at the start
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)