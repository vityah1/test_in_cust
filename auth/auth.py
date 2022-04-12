from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
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
def login_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    data = {"username": username, "password": password}

    sql = "select id,username,password_hash from users where username=:username"
    res = do_sql_cmd(sql, data)
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "message": "Bad username or password"}), 200

    if not check_password_hash(res.get("data")[0][2], password):
        return jsonify({"status": "error", "message": "Bad username or password"}), 200

    # create a new token with the user id inside
    access_token = create_access_token(
        identity=res.get("data")[0][0], expires_delta=timedelta(days=30)
    )
    return jsonify(
        {
            "status": "ok",
            "message": f"Login user {username} Ok",
            "accessToken": access_token,
            "username": username,
        }
    )


@auth_bp.route("/api/auth/signup", methods=["POST"])
@cross_origin()
def create_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    password_hash = generate_password_hash(password)
    sql = "insert into users (username,password_hash) values (:username,:password_hash)"
    data = {"username": username, "password_hash": password_hash}
    res = do_sql_cmd(sql, data)
    if res["rowcount"] < 1:
        return (
            jsonify(
                {"status": "error", "message": f"error create username {res['data']}"}
            ),
            200,
        )

    # create a new token with the user id inside
    access_token = create_access_token(
        identity=res["lastrowid"], expires_delta=timedelta(days=30)
    )

    do_sql_cmd(
        "update `users` set token=:access_token where id=:id",
        {"access_token": access_token, "id": res["lastrowid"]},
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
@cross_origin()
@jwt_required()
def edit_user():
    id = get_jwt_identity()
    username = request.json.get("username", None)
    avatar = request.json.get("avatar", None)
    # Query your database for username and password
    # print(f"username:{username}, password:{password}")
    sql = "update users set username=:username,avatar=:avatar where id=:id"
    data = {"username": username, "avatar": avatar, "id": id}
    if do_sql_cmd(sql=sql, data=data)["rowcount"] < 1:
        return jsonify({"status": "error", "message": "error create username"}), 401

    return jsonify({"status": "ok", "message": f"User {username} edited OK"})
