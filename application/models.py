from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    monopoly1 = db.Column(db.Integer, default=0)
    bluff1 = db.Column(db.Integer, default=0)
    spoon1 = db.Column(db.Integer, default=0)
    uno1 = db.Column(db.Integer, default=0)
    monopoly2 = db.Column(db.Integer, default=0)
    bluff2 = db.Column(db.Integer, default=0)
    spoon2 = db.Column(db.Integer, default=0)
    uno2 = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)