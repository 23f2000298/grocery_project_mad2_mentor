from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
import json

from .models import Users, db, Orders, Cart, Product, Category, CategoryRequest
from .api import cache


class PurchaseAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())

        if current_user.get("role") != "customer":
            return {"message": "access denied"}, 403

        orders = Orders.query.filter_by(customer_id=current_user["id"]).all()
        return {"orders": [order.convert_to_json() for order in orders]}, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())

        if current_user.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart_products = Cart.query.filter_by(customer_id=current_user["id"]).all()

        if not cart_products:
            return {"message": "Cart is empty"}, 400

        for product in cart_products:
            new_order = Orders(
                product_id=product.product_id,
                quantity=product.quantity,
                customer_id=current_user["id"]  # ✅
            )
            db.session.add(new_order)
            product.products.sold += product.quantity
            db.session.delete(product)

        db.session.commit()
        return {"message": "Thank you for your purchase"}, 200