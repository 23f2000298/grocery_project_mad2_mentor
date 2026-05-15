from flask import request,current_app as app
from flask_restful import Resource
from .models import Users,db,Orders,Cart,Product,Category,CategoryRequest

class WelcomeAPI(Resource):
    def get(self):
        return {"message": "Welcome to the API"},200
    def post(self):
        data = request.get_json()
        print(request)
        print(data)
        msg = f"Welcome {data['name']}"
        return {"message": msg},200
    
class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        user = Users.query.filter_by(email=data.get('email')).first()
        if user:
            if user.password == data.get('password'):
                return {"message": "Login successful"},200
            else:
                return {"message": "Invalid password"},401
        else:
            return {"message": "User not found"},404
        

class SignupAPI(Resource):
    def post(self):
        data = request.get_json()
        user = Users.query.filter_by(email=data.get('email')).first()
        if user:
            return {"message": "User already exists"},400
        else:
            new_user = Users(name=data.get('name'),email=data.get('email'),password=data.get('password'),role = data.get('role'))
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Signup successful"},200