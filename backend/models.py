from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='beta')  # 'admin' or 'beta'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    reference_decision = db.Column(db.String(2))
    additional_data = db.Column(db.Text)

class ModelOutput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    model = db.Column(db.String(50))
    decision = db.Column(db.String(2))
    rationale = db.Column(db.Text)
    accuracy = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class HumanRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    model = db.Column(db.String(50))
    empathy = db.Column(db.Integer)
    explanation = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))