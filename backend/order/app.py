from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from module import db, Order
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
jwt = JWTManager(app)

@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
  user_id = get_jwt_identity()
  data = request.get_json()
  product_id = data['product_id']
  quantity = data['quantity']

  response = requests.get(f'http://product/product/{product_id}')
  product = response.json()

  order = Order(user_id=user_id, product_id=product_id, quantity=quantity, product_name=product['name'], product_price=product['price'])
  db.session.add(order)
  db.session.commit()

  return jsonify({'message': 'Order created'}), 201

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
  user_id = get_jwt_identity()
  orders = Order.query.filter_by(user_id=user_id).all()

  return jsonify([order.to_dict() for order in orders])

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
  user_id = get_jwt_identity()
  order = Order.query.get_or_404(order_id)

  if order.user_id != user_id:
    return jsonify({'message': 'Access denied'}), 401

  return jsonify(order.to_dict())

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
  user_id = get_jwt_identity()
  data = request.get_json()
  quantity = data['quantity']

  order = Order.query.get_or_404(order_id)

  if order.user_id != user_id:
    return jsonify({'message': 'Access denied'}), 401

  order.quantity = quantity
  db.session.commit()

  return jsonify({'message': 'Order updated'})

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
  user_id = get_jwt_identity()
  order = Order.query.get_or_404(order_id)

  if order.user_id != user_id:
    return jsonify({'message': 'Access denied'}), 401

  db.session.delete(order)
  db.session.commit()

  return jsonify({'message': 'Order deleted'})

def order_to_dict(order):
  return {
    'id': order.id,
    'user_id': order.user_id,
    'product_id': order.product_id,
    'quantity': order.quantity,
    'product_name': order.product_name,
    'product_price': order.product_price
  }

Order.to_dict = order_to_dict