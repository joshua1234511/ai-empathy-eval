from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import Config
from models import db, User, Scenario, ModelOutput, HumanRating
from auth import auth_bp
from ml_models import run_all_models

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)
jwt = JWTManager(app)
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/evaluate', methods=['POST'])
@jwt_required()
def evaluate():
    data = request.json
    user = User.query.filter_by(username=get_jwt_identity()).first()
    scenario = Scenario(text=data['scenario_text'], reference_decision=data.get('reference_decision'), additional_data=str(data.get('additional_data')))
    db.session.add(scenario)
    db.session.commit()
    outputs = run_all_models(data['scenario_text'], data.get('additional_data'))
    for out in outputs:
        mo = ModelOutput(scenario_id=scenario.id, model=out['model'], decision=out['decision'], rationale=out['rationale'], accuracy=out.get('accuracy'), user_id=user.id)
        db.session.add(mo)
    db.session.commit()
    return jsonify({'scenario_id': scenario.id, 'results': outputs})

@app.route('/api/rate', methods=['POST'])
@jwt_required()
def rate():
    data = request.json
    user = User.query.filter_by(username=get_jwt_identity()).first()
    rating = HumanRating(scenario_id=data['scenario_id'], model=data['model'], empathy=data['empathy'], explanation=data['explanation'], user_id=user.id)
    db.session.add(rating)
    db.session.commit()
    return jsonify({'msg': 'Rating saved'})

@app.route('/api/results/<int:scenario_id>', methods=['GET'])
@jwt_required()
def get_results(scenario_id):
    outputs = ModelOutput.query.filter_by(scenario_id=scenario_id).all()
    ratings = HumanRating.query.filter_by(scenario_id=scenario_id).all()
    return jsonify({
        'outputs': [dict(model=o.model, decision=o.decision, rationale=o.rationale, accuracy=o.accuracy) for o in outputs],
        'ratings': [dict(model=r.model, empathy=r.empathy, explanation=r.explanation, user_id=r.user_id) for r in ratings]
    })

if __name__ == '__main__':
    app.run(debug=True)
