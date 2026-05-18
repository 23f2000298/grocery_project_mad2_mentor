from flask import request,current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from .models import db,Product,Category,Users
from .api import cache
from .task import data_export



class ProductAPI(Resource):

    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):

        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role")  == "manager":
            products = Product.query.filter_by(manager_id=current_user).all()
        else:
            products = Product.query.all()

        products_json = []

        for product in products:
            products_json.append(product.convert_to_json())

        return {"products": products_json}, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "manager":
            return {"message": "access denied"}, 403

        data = request.get_json()

        if not data.get("name") and not data.get("price") and not data.get("description") and not data.get("category_id") and not data.get("unit") and not data.get("stock") and not data.get("sold"):
            return {"message": "Missing required fields"}, 400

        if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
            return {"message": "Name must be between 2 and 100 characters"}, 400
        category = Category.query.get(data.get("category_id"))

        if not category:
            return {"message": "Category not found"}, 404
        new_product = Product(name=data.get("name").strip(),price = data.get("price"),description = data.get("description").strip(),category_id = data.get("category_id"),
                              unit = data.get("unit"),stock = data.get("stock"),sold = 0,manager_id = current_user)

        db.session.add(new_product)
        db.session.commit()

        return {"message": "product added successfully"}, 200

        
    @jwt_required()
    def put(self,product_id):

        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "manager":
            return {"message": "access denied"}, 403

        data = request.get_json()

        if not data.get("name") and not data.get("price") and not data.get("description") and not data.get("category_id") and not data.get("unit") and not data.get("stock") and not data.get("sold"):
            return {"message": "Missing required fields"}, 400

        if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
            return {"message": "Name must be between 2 and 100 characters"}, 400
        category = Category.query.get(data.get("category_id").strip())

        if not category:
            return {"message": "Category not found"}, 404
        product = Product.query.filter_by(id=product_id,manager_id=current_user).first()
        if not product:
            return {"message": "Product not found"}, 404

        product.name = data.get("name").strip() if data.get("name") else product.name
        product.price = data.get("price") if data.get("price") else product.price
        product.description = data.get("description").strip() if data.get("description") else product.description
        product.category_id = data.get("category_id") if data.get("category_id") else product.category_id
        product.unit = data.get("unit") if data.get("unit") else product.unit
        product.stock = data.get("stock") if data.get("stock") else product.stock
        product.sold = data.get("sold") if data.get("sold") else product.sold

        db.session.add(product)
        db.session.commit()

        return {"message": "Product updated successfully"}, 200
    @jwt_required()
    def delete(self,category_id):

        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "manager":
            return {"message": "access denied"}, 403

        product = Product.query.filter_by(id=category_id,manager_id=current_user).first()
        if not product:
            return {"message": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted successfully"}, 200

       
class ExportDataAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "manager":
            return {"message": "access denied"}, 403

        products = Product.query.filter_by(manager_id=current_user).all()
        manager = Users.query.filter_by(id=current_user).first()
        if manager:
            product_details = []
            for product in products:
                product_details.append({"product_id": product.id,"quantity": product.stock,"date_of_purchase": product.date_of_purchase,"name": product.name,"price": product.price,"unit": product.unit})
            data_export(product_details,manager.email)
            return {"message": "Data exported successfully, please check your email"}, 200


        