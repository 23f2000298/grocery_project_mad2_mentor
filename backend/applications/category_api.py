from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .models import Users, db, Orders, Cart, Product, Category, CategoryRequest
from .api import cache
import json


class CategoryAPI(Resource):

    @jwt_required()
    # @cache.cached(timeout=120)
    def get(self):
        categories = Category.query.all()
        category_json = [category.convert_to_json() for category in categories]
        return category_json, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())  # role is here

        if current_user.get("role") != "admin":        # check identity, not claims
            return {"message": "access denied"}, 403

        data = request.get_json()

        if not data.get("name"):
            return {"message": "Missing required fields"}, 400

        if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
            return {"message": "Name must be between 2 and 100 characters"}, 400

        new_category = Category(name=data.get("name").strip())
        db.session.add(new_category)
        db.session.commit()

        return {"message": "Category added successfully"}, 200

    @jwt_required()
    def put(self, category_id):
        current_user = json.loads(get_jwt_identity())

        if current_user.get("role") != "admin":
            return {"message": "access denied"}, 403

        data = request.get_json()

        if not data.get("name"):
            return {"message": "Missing required fields"}, 400

        if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
            return {"message": "Name must be between 2 and 100 characters"}, 400

        category = Category.query.get(category_id)

        if not category:
            return {"message": "Category not found"}, 404

        category.name = data.get("name").strip()
        db.session.commit()

        return {"message": "Category updated successfully"}, 200

    @jwt_required()
    def delete(self, category_id):
        current_user = json.loads(get_jwt_identity())

        if current_user.get("role") != "admin":
            return {"message": "access denied"}, 403

        category = Category.query.get(category_id)

        if not category:
            return {"message": "Category not found"}, 404

        db.session.delete(category)
        db.session.commit()

        return {"message": "Category deleted successfully"}, 200