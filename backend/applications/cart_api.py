from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .models import Users, db, Orders, Cart, Product, Category, CategoryRequest


class CartAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart = Cart.query.filter_by(customer_id=current_user).all()
        cart_json = []
        for item in cart:
            cart_json.append(item.convert_to_json())
        return cart_json, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") != "customer":
            return {"message": "access denied"}, 403

        data = request.get_json()

        if not data:
            return {"message": "Invalid or missing JSON body"}, 400

        if not (data.get("product_id") and data.get("quantity")):
            return {"message": "Missing required fields"}, 400

        if data.get("quantity") < 1:
            return {"message": "Quantity must be greater than 0"}, 400

        product = Product.query.get(data.get("product_id"))
        if not product:
            return {"message": "Product not found"}, 404

        new_cart = Cart(
            product_id=data.get("product_id"),
            quantity=data.get("quantity"),
            customer_id=current_user
        )

        db.session.add(new_cart)
        db.session.commit()

        return {"message": "Product added to cart successfully"}, 200

    @jwt_required()
    def patch(self, cart_id):
        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart_product = Cart.query.filter_by(id=cart_id, customer_id=current_user).first()  # fixed

        if not cart_product:
            return {"message": "Product not found"}, 404

        data = request.get_json()

        if not data:
            return {"message": "Invalid or missing JSON body"}, 400

        if not data.get("quantity"):
            return {"message": "Missing required fields"}, 400

        if data.get("quantity") < 1:
            return {"message": "Quantity must be greater than 0"}, 400

        cart_product.quantity = data.get("quantity")
        db.session.commit()

        return {"message": "Quantity updated successfully"}, 200

    @jwt_required()
    def delete(self, cart_id):
        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart_product = Cart.query.filter_by(id=cart_id, customer_id=current_user).first()  # fixed

        if not cart_product:
            return {"message": "Product not found"}, 404

        db.session.delete(cart_product)
        db.session.commit()

        return {"message": "Product deleted successfully"}, 200