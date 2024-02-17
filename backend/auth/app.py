from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from module import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)

@app.route('/auth/check-auth/<jwt_token>', methods=['GET'])
def check_auth(jwt_token):
  user_id = jwt.decode(jwt_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256']).get('sub')
  user = User.query.get(user_id)
  if not user:
    return jsonify({'message': 'Invalid user'}), 401

  return jsonify({'message': 'Authorized'}), 200

def create_access_token(data):
  import jwt
  jwt_payload = data
  jwt_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
  access_token = jwt.encode(jwt_payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
  return access_token

@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  password = generate_password_hash(data['password'])
  new_user = User(username=data['username'], password=password)
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  user = User.query.filter_by(username=data['username']).first()
  if user and check_password_hash(user.password, data['password']):
    access_token = create_access_token({'id': user.id, 'username': user.username})
    return jsonify({'access_token': access_token}), 200
  else:
    return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
  app.run(port=5001)