from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, default=True)

# Initialize the database
with app.app_context():
    db.create_all()

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    user = User(
        username=data['username'],
        password=data['password'],
        active=data.get('active', True)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user': {'id': user.id, 'username': user.username, 'active': user.active}}), 201

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': u.id, 'username': u.username, 'active': u.active} for u in users]
    return jsonify(user_list), 200

# Read a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username, 'active': user.active}), 200

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.active = data.get('active', user.active)
    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': {'id': user.id, 'username': user.username, 'active': user.active}}), 200

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
