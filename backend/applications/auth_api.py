from flask import request,current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from .models import Users,db,Orders,Cart,Product,Category,CategoryRequest
import json


    
class AuthAPI(Resource):


    @jwt_required() 
    def get(self):
        current_user =json.loads(get_jwt_identity())

        claims = get_jwt()

        if current_user.get("role") != "admin":
            return {"message": "access denied"},403
        manager = Users.query.filter_by(role = "manager").all()
        manager_json = []
        for manager in manager:
            manager_json.append(manager.convert_to_json())
        return manager_json,200
        
    def post(self):
        data = request.get_json()
        if not (data.get("email") and data.get("password")):
            return {"message": "Missing required fields"},400
        user = Users.query.filter_by(email=data.get('email')).first()
        if not user:
            return {"message": "User not found"},404
        if user.password != data.get('password'):
            return {"message": "Invalid password"},401
        
        if user.role == "manager" and user.status == "pending":
            return {"message": "Your account is pending"},401        
        identity = {"role":user.role,"id":user.id}
        token = create_access_token(
            identity=json.dumps(identity)
        ) 
        return {"message": "Login successful",
                "token":token,
                "user_name":user.name,
                "user_role":user.role},200
                

    @jwt_required() 
    def patch(self,manager_id):
        current_user =json.loads(get_jwt_identity())

        claims = get_jwt()

        if current_user.get("role") != "admin":
            return {"message": "access denied"},403
        manager = Users.query.filter_by(id=manager_id).first()
        if not manager:
            return {"message": "Manager not found"},404
        manager.status = "active"
        db.session.commit()
        return {"message": "Manager approved successfully"},200
        

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
            if data.get("role") not in ["admin","customer","manager"]:
                return {"message": "Invalid role"},400
            user = Users.query.filter_by(email=data.get('email')).first()
            if user:
                return {"message": "User already exists"},400
            new_user = Users(name=data.get('name'),email=data.get('email'),password=data.get('password'),role = data.get('role'),status = "pending" if data.get('role').strip() == "manager" else "active")
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Signup successful"},200
        return {"message": "Missing required fields"},400
                
