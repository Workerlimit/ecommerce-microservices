from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, nullable=False)
  product_id = db.Column(db.Integer, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f'<Order {self.id}>'