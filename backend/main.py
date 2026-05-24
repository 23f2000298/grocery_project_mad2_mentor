from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from applications.models import db, Users
from applications.api import WelcomeAPI,cache
from applications.auth_api import SignupAPI,AuthAPI
from applications.category_api import CategoryAPI
from applications.product_api import ProductAPI,ExportDataAPI
from applications.cart_api import CartAPI
from applications.purchase_api import PurchaseAPI
from applications.category_request_api import CategoryRequestAPI,CategoryApprovial
from applications.worker import celery
from applications.task import *
import time
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.db")
app.config["SECRET_KEY"] = "super-secret"
app.config["JWT_SECRET_KEY"] = "my-super-secret-key-that-is-long-enough-123"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = 12)

app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    timezone = "Asia/Kolkata"
)


db.init_app(app)
cache.init_app(app)
api = Api(app)
jwt = JWTManager(app)
# celery.init_app(app)
app.app_context().push()




def add_admin():
    admin = Users.query.filter_by(role="admin").first()
    if not admin:
        admin = Users(name="admin", email="admin@gmail.com", password="1", role="admin")
        db.session.add(admin)
        db.session.commit()
        return "admin added successfully"


@app.route("/test_cache")
@cache.cached(timeout=10)
def test_cache():
    time.sleep(10)
    return f"test is working fine {time.localtime()}"


api.add_resource(WelcomeAPI,"/api/welcome")
api.add_resource(SignupAPI,"/api/signup")
api.add_resource(AuthAPI,"/api/login","/api/manager","/api/manager/<int:manager_id>")
api.add_resource(CategoryAPI,"/api/category","/api/category/<int:category_id>")
api.add_resource(ProductAPI,"/api/product","/api/product/<int:product_id>")
api.add_resource(CartAPI,"/api/cart","/api/cart/<int:cart_id>")
api.add_resource(PurchaseAPI,"/api/order")
api.add_resource(CategoryRequestAPI,"/api/category/request")
api.add_resource(CategoryApprovial,"/api/category/request/action")
api.add_resource(ExportDataAPI,"/api/product/export")
    


if __name__ == "__main__":    
    db.create_all()
    add_admin()
    app.run(debug=True)