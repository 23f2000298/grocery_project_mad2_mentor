from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Product, Category, Users
from .api import cache
from .task import data_export
import json  # ✅ added


class ProductAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())  # ✅ fixed
        manager_id = current_user.get("id")
        role = current_user.get("role")

        if role == "manager":
            products = Product.query.filter_by(manager_id=manager_id).all()  # ✅ fixed
        else:
            products = Product.query.all()

        products_json = [product.convert_to_json() for product in products]
        return {"products": products_json}, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())  # ✅ fixed
        manager_id = current_user.get("id")

        if current_user.get("role") != "manager":       # ✅ fixed
            return {"message": "access denied"}, 403

        data = request.get_json()

        if not data.get("name") or not data.get("price") or not data.get("category_id") or not data.get("unit") or not data.get("stock"):
            return {"message": "Missing required fields"}, 400  # ✅ fixed 'and' to 'or'

        if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
            return {"message": "Name must be between 2 and 100 characters"}, 400

        category = Category.query.get(data.get("category_id"))
        if not category:
            return {"message": "Category not found"}, 404

        new_product = Product(
            name=data.get("name").strip(),
            price=data.get("price"),
            description=data.get("description", "").strip(),
            category_id=data.get("category_id"),
            unit=data.get("unit"),
            stock=data.get("stock"),
            sold=0,
            manager_id=manager_id  # ✅ fixed
        )
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Product added successfully"}, 200

    @jwt_required()
    def put(self, product_id):
        current_user = json.loads(get_jwt_identity())  # ✅ fixed
        manager_id = current_user.get("id")

        if current_user.get("role") != "manager":       # ✅ fixed
            return {"message": "access denied"}, 403

        data = request.get_json()

        product = Product.query.filter_by(id=product_id, manager_id=manager_id).first()  # ✅ fixed
        if not product:
            return {"message": "Product not found"}, 404

        product.name = data.get("name", product.name).strip()
        product.price = data.get("price", product.price)
        product.description = data.get("description", product.description)
        product.category_id = data.get("category_id", product.category_id)
        product.unit = data.get("unit", product.unit)
        product.stock = data.get("stock", product.stock)

        db.session.commit()
        return {"message": "Product updated successfully"}, 200

    @jwt_required()
    def delete(self, product_id):                        # ✅ renamed param from category_id to product_id
        current_user = json.loads(get_jwt_identity())  # ✅ fixed
        manager_id = current_user.get("id")

        if current_user.get("role") != "manager":       # ✅ fixed
            return {"message": "access denied"}, 403

        product = Product.query.filter_by(id=product_id, manager_id=manager_id).first()  # ✅ fixed
        if not product:
            return {"message": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200


class ExportDataAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())  # ✅ fixed
        manager_id = current_user.get("id")

        if current_user.get("role") != "manager":       # ✅ fixed
            return {"message": "access denied"}, 403

        products = Product.query.filter_by(manager_id=manager_id).all()  # ✅ fixed
        manager = Users.query.filter_by(id=manager_id).first()           # ✅ fixed

        if manager:
            product_details = [{
                "product_id": p.id,
                "quantity": p.stock,
                "name": p.name,
                "price": p.price,
                "unit": p.unit
            } for p in products]
            data_export(product_details, manager.email)
            return {"message": "Data exported successfully, please check your email"}, 200