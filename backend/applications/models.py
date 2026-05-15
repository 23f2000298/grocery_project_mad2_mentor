from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False,default="customer")
    status = db.Column(db.String(120), nullable=False,default="active")
    carts = db.relationship('Cart', backref='users',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted
    category_requests = db.relationship('CategoryRequest', backref='users',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    products = db.relationship('Product', backref='category',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(80),nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    Cart = db.relationship('Cart', backref='products',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_of_purchase = db.Column(db.DateTime, nullable=False, default=datetime.now())


class CategoryRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    action = db.Column(db.String(80),nullable=False)
    manager_id = db.Column(db.Integer,ForeignKey('users.id'), nullable=False)