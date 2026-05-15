from flask import request,current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from .models import Users,db,Orders,Cart,Product,Category,CategoryRequest



    
class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data.get("email") and not data.get("password"):
            return {"message": "Missing required fields"},400
        user = Users.query.filter_by(email=data.get('email')).first()
        if not user:
            return {"message": "User not found"},404
        if user.password != data.get('password'):
            return {"message": "Invalid password"},401
        
        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        ) 
        return {"message": "Login successful",
                "token":token,
                "user_name":user.name,
                "user_role":user.role},200
                
        
        

class SignupAPI(Resource):
    def post(self):
        data = request.get_json()
        if data.get("name") and data.get("email") and data.get("password") and data.get("role"):
            if len(data.get("name").strip()) > 30 or len(data.get("name").strip()) < 2:
                return {"message": "Name must be between 2 and 30 characters"},400
            if len(data.get("email").strip()) > 30 or len(data.get("email").strip()) < 2 or "@" not in data.get("email"):
                return {"message": "Email must be between 2 and 30 characters and contain @"},400
            if len(data.get("password").strip()) > 30 or len(data.get("password").strip()) < 1:
                return {"message": "Password must be between 1 and 30 characters"},400
            if data.get("role") not in ["admin","customer"]:
                return {"message": "Invalid role"},400
            user = Users.query.filter_by(email=data.get('email')).first()
            if user:
                return {"message": "User already exists"},400
            new_user = Users(name=data.get('name'),email=data.get('email'),password=data.get('password'),role = data.get('role'))
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Signup successful"},200
        return {"message": "Missing required fields"},400
                

class CategoryAPI(Resource):

    @jwt_required()
    def get(self):
        categories = Category.query.all()
        category_json = []
        for category in categories:
            category_json.append(category.convert_to_json())
        return category_json,200

        

    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "admin":
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
    def put(self,category_id):

        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "admin":
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

        db.session.add(category)
        db.session.commit()

        return {"message": "Category updated successfully"}, 200
    
    @jwt_required()
    def delete(self,category_id):

        current_user = get_jwt_identity()

        claims = get_jwt()

        if claims.get("role") != "admin":
            return {"message": "access denied"}, 403

        category = Category.query.get(category_id)

        if not category:
            return {"message": "Category not found"}, 404

        db.session.delete(category)
        db.session.commit()

        return {"message": "Category deleted successfully"}, 200




class WelcomeAPI(Resource):
    @jwt_required()
    def get(self):
        return {"message": "Welcome to the Groccery Store"}, 200

    def post(self):
        msg = f"Hello! {request.get_json().get('name')}"
        return {"message": msg}, 200