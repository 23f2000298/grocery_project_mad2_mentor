from flask import request,current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from .models import Users,db,Orders,Cart,Product,Category,CategoryRequest



class WelcomeAPI(Resource):
    @jwt_required()
    def get(self):
        return {"message": "Welcome to the Groccery Store"}, 200

    def post(self):
        msg = f"Hello! {request.get_json().get('name')}"
        return {"message": msg}, 200