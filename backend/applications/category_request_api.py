from flask import request,current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from .models import Users,db,Orders,Cart,Product,Category,CategoryRequest
from .api import cache


class CategoryRequestAPI(Resource):

    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        current_user = get_jwt_identity()
        claims = get_jwt()

        if claims.get("role") == "customer":
           return {"message": "access denied"}, 403
        if claims.get("role") == "manager":
           category_request = CategoryRequest.query.filter_by(manager_id=current_user).all()
        if claims.get("role") == "admin":
           category_request = CategoryRequest.query.all()
        category_request_json = []
        for category_request in category_request:
            category_request_json.append(category_request.convert_to_json())
        return {"category_request": category_request_json}, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get("role") != "manager":
            return {"message": "access denied"}, 403
        data = request.get_json()

        if not data.get("action") or data.get("action").strip() not in ["CREATE","DELETE","UPDATE"]:
            return {"message": "Invalid action"}, 400
        
        if data.get("action").strip() == "CREATE":
            if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
                return {"message": "Name must be between 2 and 100 characters"}, 400
            category_request = CategoryRequest(name=data.get("name").strip(), action="CREATE", manager_id=current_user)
            db.session.add(category_request)
            db.session.commit()
            return {"message": "Category request created successfully"}, 200

        if data.get("action").strip() == "UPDATE":
            category = Category.query.get(data.get("category_id"))

            if not category:
                return {"message": "Category not found"}, 404

            if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 2:
                return {"message": "Name must be between 2 and 100 characters"}, 400

            category_request = CategoryRequest(name=data.get("name").strip(), category_id=data.get("category_id"), action="UPDATE", manager_id=current_user)
            db.session.add(category_request)
            db.session.commit()
            return {"message": "Category request updated successfully"}, 200

        if data.get("action").strip() == "DELETE":
            category = Category.query.get(data.get("category_id"))

            if not category:
                return {"message": "Category not found"}, 404

            category_request = CategoryRequest(category_id=data.get("category_id"), action="DELETE", manager_id=current_user)
            db.session.add(category_request)
            db.session.commit()
            return {"message": "Category request deleted successfully"}, 200

        return {"message": "Invalid action"}, 400
    

class CategoryApprovial(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get("role") == "customer":
            return {"message": "access denied"}, 403
        data = request.get_json()
        if not data.get("action") or data.get("action").strip() not in ["APPROVE","REJECT"]:
            return {"message": "Invalid action"}, 400

        if data.get("action").strip() == "REJECT":
            CategoryRequest.query.filter_by(id=data.get("request_id")).delete()
            db.session.commit()
            return {"message": "Category request rejected successfully"}, 200

        if data.get("action").strip() == "APPROVE":
            category_request = CategoryRequest.query.filter_by(id=data.get("request_id")).first()
            if not category_request:
                return {"message": "Category request not found"}, 404
            if category_request.action == "CREATE":
                category = Category(name=category_request.name)
                db.session.add(category)
                db.session.commit()
                return {"message": "Category created successfully"}, 200
            if category_request.action == "UPDATE":
                category = Category.query.get(category_request.category_id)
                if not category:
                    return {"message": "Category not found"}, 404
                category.name = category_request.name
                db.session.commit()
                return {"message": "Category updated successfully"}, 200
            if category_request.action == "DELETE":
               Category.query.filter_by(id=category_request.category_id).delete()
               db.session.commit()
               return {"message": "Category deleted successfully"}, 200

        return {"message": "Invalid action"}, 400
