from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from applications.models import db, Users
from applications.api import WelcomeAPI
from applications.auth_api import SignupAPI,AuthAPI
from applications.category_api import CategoryAPI
from applications.product_api import ProductAPI
from applications.cart_api import CartAPI
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.db")
app.config["SECRET_KEY"] = "super-secret"
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = 12)


db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
app.app_context().push()




def add_admin():
    admin = Users.query.filter_by(role="admin").first()
    if not admin:
        admin = Users(name="admin", email="admin@gmail.com", password="1", role="admin")
        db.session.add(admin)
        db.session.commit()
        return "admin added successfully"



api.add_resource(WelcomeAPI,"/api/welcome")
api.add_resource(SignupAPI,"/api/signup")
api.add_resource(AuthAPI,"/api/login","/api/manager","/api/manager/<int:manager_id>")
api.add_resource(CategoryAPI,"/api/category","/api/category/<int:category_id>")
api.add_resource(ProductAPI,"/api/product","/api/product/<int:product_id>")
api.add_resource(CartAPI,"/api/cart","/api/cart/<int:cart_id>")

if __name__ == '__main__':
    db.create_all()
    add_admin()
    app.run(debug=True)