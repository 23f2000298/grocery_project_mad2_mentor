from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Cart, Product
import json

class CartAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart = Cart.query.filter_by(customer_id=current_user["id"]).all()
        cart_json = [item.convert_to_json() for item in cart]
        total = sum(float(item.get("product_price", 0)) * int(item.get("quantity", 0)) for item in cart_json)
        return {"cart": cart_json, "total": total}, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get("role") != "customer":
            return {"message": "access denied"}, 403

        data = request.get_json()
        if not data:
            return {"message": "Invalid or missing JSON body"}, 400
        if not (data.get("product_id") and data.get("quantity")):
            return {"message": "Missing required fields"}, 400

        cart_product = Cart.query.filter_by(
            customer_id=current_user["id"],
            product_id=data.get("product_id")
        ).first()

        if not cart_product:
            product = Product.query.get(data.get("product_id"))
            if not product:
                return {"message": "Product not found"}, 404
            new_cart = Cart(
                product_id=data.get("product_id"),
                quantity=data.get("quantity", 1),
                customer_id=current_user["id"]
            )
            db.session.add(new_cart)
            db.session.commit()
            return {"message": "Product added to cart successfully"}, 200

        cart_product.quantity += data.get("quantity", 1)
        db.session.commit()
        return {"message": "Product quantity updated successfully"}, 200

    @jwt_required()
    def patch(self, cart_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart_product = Cart.query.filter_by(
            id=cart_id,
            customer_id=current_user["id"]
        ).first()
        if not cart_product:
            return {"message": "Product not found"}, 404

        data = request.get_json()
        if not data or data.get("quantity") is None:
            return {"message": "Missing required fields"}, 400

        cart_product.quantity += int(data.get("quantity"))
        if cart_product.quantity < 1:
            db.session.delete(cart_product)  # auto-remove if quantity hits 0
        db.session.commit()
        return {"message": "Quantity updated successfully"}, 200

    @jwt_required()
    def delete(self, cart_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart_product = Cart.query.filter_by(
            id=cart_id,
            customer_id=current_user["id"]
        ).first()
        if not cart_product:
            return {"message": "Product not found"}, 404

        db.session.delete(cart_product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200