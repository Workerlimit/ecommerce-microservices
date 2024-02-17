from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.String(255))

  def __repr__(self):
    return '<Product %r>' % self.name