import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

db = SQLAlchemy(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=False)

  def __repr__(self):
    return f'<Product {self.name}>'

def authorize_user():
  jwt_token = request.headers.get('Authorization').split(' ')[1]
  response = requests.get(f'http://auth-microservice:5000/auth/check-auth/{jwt_token}')
  return response.status_code == 401

@app.route('/product', methods=['POST'])
@jwt_required()
def create_product():
  if not authorize_user():
    return jsonify({'message': 'User not authorized'}), 401

  data = request.get_json()
  new_product = Product(name=data['name'], price=data['price'])
  db.session.add(new_product)
  db.session.commit()

  return jsonify({'message': 'Product created'}), 201

@app.route('/product/<id>', methods=['GET'])
@jwt_required()
def get_product(id):
  if not authorize_user():
    return jsonify({'message': 'User not authorized'}), 401

  product = Product.query.get(id)
  if not product:
    return jsonify({'message': 'Product not found'}), 404

  return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 200

if __name__ == '__main__':
    app.run(port=5001)