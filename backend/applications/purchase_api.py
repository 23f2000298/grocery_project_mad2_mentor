from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from .models import Users, db, Orders, Cart, Product, Category, CategoryRequest
from .api import cache


class PurchaseAPI(Resource):

    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):

        
        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") != "customer":
            return {"message": "access denied"}, 403

        orders = Orders.query.filter_by(
            customer_id=current_user
        ).all()

        orders_json = []

        for order in orders:
            orders_json.append(order.convert_to_json())

        return {"orders": orders_json}, 200

    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") != "customer":
            return {"message": "access denied"}, 403

        cart_product = Cart.query.filter_by(
            customer_id=current_user
        ).all()

        if len(cart_product) == 0:
            return {"message": "Cart is empty"}, 400

        for product in cart_product:

            new_order = Orders(
                product_id=product.product_id,
                quantity=product.quantity,
                customer_id=current_user
            )

            db.session.add(new_order)
            db.session.delete(product)
            product.products.sold += product.quantity

        db.session.commit()

        return {"message": "Thank you for your purchase"}, 200