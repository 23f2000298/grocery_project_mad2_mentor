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
    products = db.relationship('Product', backref='users',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted
    category_requests = db.relationship('CategoryRequest', backref='users',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted

    def convert_to_json(self):
        return {"id":self.id,
                "name":self.name,
                "email":self.email,
                "role":self.role,
                "status":self.status}

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    products = db.relationship('Product', backref='category',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted

    def convert_to_json(self):
        return {"id":self.id,"name":self.name}

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer,nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    carts = db.relationship('Cart', backref='products',cascade = "all, delete-orphan",lazy=True) #when parent is deleted, child is deleted

    def convert_to_json(self):
        return {"id":self.id,
                "name":self.name,
                "description":self.description,
                "price":self.price,
                "unit":self.unit,
                "stock":self.stock,
                "sold":self.sold,
                "category_id":self.category_id}

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def convert_to_json(self):
        return {"id":self.id,
                "quantity":self.quantity,
                "product_id":self.product_id,
                "product_name":self.products.name,
                "product_price":self.products.price,
                "product_unit":self.products.unit,
                "product_description":self.products.description}
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