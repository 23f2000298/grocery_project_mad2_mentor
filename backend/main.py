from flask import Flask
from flask_restful import Api
from applications.models import db, Users
from applications.api import WelcomeAPI,SignupAPI,LoginAPI
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.db")


db.init_app(app)
api = Api(app)
app.app_context().push()




def add_admin():
    admin = Users.query.filter_by(role="admin").first()
    if not admin:
        admin = Users(name="admin", email="admin", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()
        return "admin added successfully"



api.add_resource(WelcomeAPI,"/api/welcome")
api.add_resource(SignupAPI,"/api/signup")
api.add_resource(LoginAPI,"/api/login")

if __name__ == '__main__':
    db.create_all()
    add_admin()
    app.run(debug=True)