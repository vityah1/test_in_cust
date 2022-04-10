from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from flasgger import swag_from
from utils import do_sql_cmd, do_sql_sel

# from func import cfg
# from models import Item

api_crud_bp = Blueprint(
    "api_crud_bp",
    __name__,
)


@api_crud_bp.route("/api/items", methods=["POST"])
@cross_origin()
@jwt_required()
@swag_from('item_insert.yml')
def new_cost():
    """
    insert a new item
    """
    req = request.get_json()
    data = {
        "article": req.get("article", ""),
        "name": req.get("name", ""),
        "item_image": req.get("item_image", ""),
        "id_user": get_jwt_identity(),
        "price": req.get("price", 0,type=int),
        "currency": req.get("currency", 0,type=int),
    }
    res = do_sql_cmd(
        """insert into `items` (article,name,item_image,id_user,price,currency) 
        values (:article,:name,:item_image,:id_user,:price,:currency)""",
        data,
    )
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "data": res["data"]})

    return jsonify({"status": "ok", "data": res["data"], "id": res["rowcount"]})


@api_crud_bp.route("/api/items/", methods=["GET"])
# @cross_origin(supports_credentials=True)
@cross_origin()
@jwt_required()
@swag_from('list_items.yml')
def list_items():
    """
    list items
    q - search by name
    article - search by article        
    """
    
    data = {
        "q": request.args.get("q", ""),
        "article": request.args.get("article", ""),
        "sort": request.args.get("sort", ""),
        "id_user": get_jwt_identity(),
        "page": request.args.get("page",1,type=int)
    }

    if not data["sort"]:
        sort = "name"
    elif sort == "article":
        sort = "article"
    elif sort == "name":
        sort = "name"
    else:
        sort = "name"

    if data["q"]:
        search_query = " and name like '%:q%' "
    elif data["article"]:
        search_query = " and article = ':article' "        
    else:
        search_query = ""

    offset = 10*data['page']-10

    sql = f"""
select id,article,name,item_image,price,currency
from `items`
where 1=1 
{search_query}
and id_user=:id_user
order by {sort}
limit by 10 offset {offset}
"""

    res = {"status": "ok", "data": [dict(row) for row in do_sql_sel(sql, data)]}
    if res[0].get("rowcount") is not None and res[0].get("rowcount") < 0:
        return jsonify(
            {
                "status": "error",
                "data": [{"article": "error", "name": "Error excecute sql command"}],
            }
        )
    return jsonify(res)


@api_crud_bp.route("/api/items/<int:id>", methods=["GET"])
@cross_origin()
@jwt_required()
@swag_from('list_item.yml')
def ret_cost(id):
    """
    get info about item

    """
    sql = f"select id,article,name,item_image,price,currency from `items` where id=:id and id_user=:id_user"
    data = {"id": id, "id_user": get_jwt_identity()}
    res = do_sql_sel(sql, data)
    return jsonify({"status": "ok", "data": [dict(row) for row in res]})


@api_crud_bp.route("/api/items/<int:id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
@swag_from('item_delete.yml')
def del_cost(id):
    """
    mark item deleted
"""

    res = do_sql_cmd(
        "update `items` set deleted=1 where id=:id and id_user=:id_user",
        {"id": id, "id_user": get_jwt_identity()},
    )
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "data": res["data"]})

    return jsonify({"status": "ok", "data": res["data"]})


@api_crud_bp.route("/api/items/<id>", methods=["PUT"])
@cross_origin()
@jwt_required()
@swag_from('item_update.yml')
def upd_cost(id):
    """
    update a item
    """
    req = request.get_json()
    sql = f"""update items set article=:article,name=:name,item_image=:item_image,price:=price,currency=:currency
        where id=:id and id_user=:id_user"""
    data = {
        "article": req.get("article", ""),
        "name": req.get("name", ""),
        "item_image": req.get("item_image", ""),
        "id_user": get_jwt_identity(),
        "price": req.get("price", 0,type=int),
        "currency": req.get("currency", 0,type=int),
        "id": id,
    }
    res = do_sql_cmd(sql, data)
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "data": res["data"]})

    return jsonify({"status": "ok", "data": res["data"]})
