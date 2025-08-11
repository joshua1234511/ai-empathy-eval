from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if user.role != 'admin':
        return jsonify({'msg': 'Admins only'}), 403
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': 'User already exists'}), 400
    new_user = User(username=data['username'], role=data.get('role', 'beta'))
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User created'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token, role=user.role)
    return jsonify({'msg': 'Bad credentials'}), 401
