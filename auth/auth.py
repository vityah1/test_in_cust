from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin
from utils import do_sql_cmd
from models import User

auth_bp = Blueprint(
    "auth_bp",
    __name__,
)

# Create a route to authenticate your users and return JWT Token. The
# create_access_token() function is used to actually generate the JWT.
@auth_bp.route("/api/auth/signin", methods=["POST"])
@cross_origin()
# @app.route("/token", methods=["POST"])
def check_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    data = {username: username, password: password}
    # Query your database for username and password
    # print(f"username:{username}, password:{password}")
    sql = "select token from users where username=:username and password=:password"
    res = do_sql_cmd(sql, data)
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "message": "Bad username or password"}), 401

    # create a new token with the user id inside
    access_token = create_access_token(
        identity=res["lastrowid"], username=username, expires_delta=timedelta(days=30)
    )
    return jsonify(
        {
            "status": "ok",
            "message": f"check user {username} Ok",
            "accessToken": access_token,
            "username": username,
        }
    )


@auth_bp.route("/api/auth/signup", methods=["POST"])
# @cross_origin()
# @app.route("/token", methods=["POST"])
def create_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    # print(f"username:{username}, password:{password}")
    sql = "insert into users (username,password) values (:username,:password) "
    data = {username: username, password: password}

    if do_sql_cmd(sql, data)["rowcount"] < 1:
        return jsonify({"status": "error", "message": "error create username"}), 401

    # create a new token with the user id inside
    access_token = create_access_token(
        identity=username, expires_delta=timedelta(days=30)
    )
    return jsonify(
        {
            "status": "ok",
            "message": f"create user {username} Ok",
            "accessToken": access_token,
            "username": username,
        }
    )


@auth_bp.route("/api/auth/edit", methods=["PUT"])
# @cross_origin()
# @app.route("/token", methods=["POST"])
def edit_user():
    id = request.json.get("id", None)
    username = request.json.get("username", None)
    avatar = request.json.get("avatar", None)
    # Query your database for username and password
    # print(f"username:{username}, password:{password}")
    sql = "update users set username=:username,avatar=:avatar where id=:id"
    data = {username: username, avatar: avatar, id: id}
    if do_sql_cmd(sql=sql, data=data)["rowcount"] < 1:
        return jsonify({"status": "error", "message": "error create username"}), 401

    return jsonify({"status": "ok", "message": f"User {username} edited OK"})
