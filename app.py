#!/home/vityah1/kt.if.ua/mypy/gapi/bin/python3.6
# _*_ coding:UTF-8 _*_
# import cgitb
# gitb.enable()
import sys

# added for venv shared hosting
sys.path.insert(0, "/home/vityah1/kt.if.ua/mypy/gapi/lib/python3.6/site-packages")

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_migrate import Migrate

from mydb import db

migrate = Migrate()

app = Flask(__name__)
swagger = Swagger(app)
CORS(app, support_credentials=True)
from config import cfg


@app.before_request
def log_request_info():
    with open("debugger.log", "a", encoding="utf8") as f:
        try:
            f.write(f"Headers: {request.headers}\n")
            f.write(f"Body: {request.get_data()}\n")
        except Exception as e:
            with open("error.log", "a", encoding="utf8") as err:
                err.write(f"{e}\n")


# mysql external database
app.config["SQLALCHEMY_DATABASE_URI"] = cfg["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = cfg["secret_key"]

jwt = JWTManager(app)

db.init_app(app)
from models import *

migrate.init_app(app, db)

# from api.api_crud import api_crud_bp
from api.api_crud_orm import api_crud_bp
from auth.auth import auth_bp

app.register_blueprint(api_crud_bp)
app.register_blueprint(auth_bp)


def __repr__(self):
    return "<Mysession %r" % self.id


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": f"{error}, path: {request.path}"}), 404


@app.route("/")
def index():
    return """This is test Flask app for InCust company with authentication and swagger support<br>
    Swagger UI available on <a href="/apidocs/">this link</a>.
    """


if __name__ == "__main__":
    #    app.run(debug=True)
    #    app.debug=True
    #    app.run(host='0.0.0.0',port=4000)
    # app.run(host="0.0.0.0", debug=False)
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host="0.0.0.0", port=cfg.get("PORT", 5000))
