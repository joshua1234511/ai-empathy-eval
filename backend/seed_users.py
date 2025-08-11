from app import app
from models import db, User

def seed():
    with app.app_context():
        db.create_all()
        users = [
            {'username': 'admin', 'password': 'adminpass', 'role': 'admin'},
            {'username': 'beta1', 'password': 'betapass1', 'role': 'beta'},
            {'username': 'beta2', 'password': 'betapass2', 'role': 'beta'},
            {'username': 'beta3', 'password': 'betapass3', 'role': 'beta'},
        ]
        for u in users:
            if not User.query.filter_by(username=u['username']).first():
                user = User(username=u['username'], role=u['role'])
                user.set_password(u['password'])
                db.session.add(user)
        db.session.commit()
        print("Seeded users:")
        for u in users:
            print(f"{u['username']} ({u['role']})")

if __name__ == '__main__':
    seed()
