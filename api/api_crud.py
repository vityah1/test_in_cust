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
@swag_from("item_insert.yml")
def create_item():
    """
    insert a new item
    """
    req = request.get_json()
    data = {
        "article": req.get("article", ""),
        "name": req.get("name", ""),
        "item_image": req.get("item_image", ""),
        "id_user": get_jwt_identity(),
    }
    res = do_sql_cmd(
        """insert into `items` (article,name,item_image,id_user) 
        values (:article,:name,:item_image,:id_user)""",
        data,
    )
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "data": res["data"]})

    id_item = res["lastrowid"]
    rowcount = res["rowcount"]
    res = do_sql_cmd(
        """insert into `prices` (id_item,price,currency) 
        values (:id_item,:price,:currency)""",
        {
            "id_item": id_item,
            "price": req.get("price", 0),
            "currency": req.get("currency", 0),
        },
    )

    return jsonify(
        {"status": "ok", "data": rowcount, "lastrowid": id_item, "id": rowcount}
    )


@api_crud_bp.route("/api/items", methods=["GET"])
# @cross_origin(supports_credentials=True)
@cross_origin()
@jwt_required()
@swag_from("list_items.yml")
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
        "page": request.args.get("page", 1),
    }
    sql_data_conditions = {}
    if not data["sort"]:
        sql_data_conditions["sort"] = "name"
    elif data["sort"] == "article":
        sql_data_conditions["sort"] = "article"
    elif data["sort"] == "name":
        sql_data_conditions["sort"] = "name"
    else:
        sql_data_conditions["sort"] = "name"

    if data["q"]:
        search_query = " and name like :q "
        sql_data_conditions["q"] = data["q"]
    elif data["article"]:
        search_query = " and article = :article "
        sql_data_conditions["article"] = data["article"]
    else:
        search_query = ""

    offset = 10 * data["page"] - 10

    sql_data_conditions["offset"] = offset
    sql_data_conditions["id_user"] = data["id_user"]

    sql = f"""
select a.id,article,name,item_image,price,currency
from `items` a left join `prices` b on a.id=b.id_item
where 1=1 
{search_query}
and id_user=:id_user
and deleted != 1
order by :sort
limit 10 offset :offset
"""
    res = do_sql_sel(sql, sql_data_conditions)
    result = [dict(row) for row in res]

    # if res[0].get("rowcount") is not None and res[0].get("rowcount") < 0:
    #     return jsonify(
    #         {
    #             "status": "error",
    #             "data": [{"article": "error", "name": "Error excecute sql command"}],
    #         }
    #     )
    return jsonify({"status": "ok", "data": result})


@api_crud_bp.route("/api/items/<int:id>", methods=["GET"])
@cross_origin()
@jwt_required()
@swag_from("list_item.yml")
def ret_cost(id):
    """
    get info about item

    """
    sql = f"""select id,article,name,item_image,price,currency 
    from `items` 
    where id=:id and id_user=:id_user and deleted != 1
    """
    data = {"id": id, "id_user": get_jwt_identity()}
    res = do_sql_sel(sql, data)
    return jsonify({"status": "ok", "data": [dict(row) for row in res]})


@api_crud_bp.route("/api/items/<int:id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
@swag_from("item_delete.yml")
def del_cost(id):
    """
    mark item deleted"""

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
@swag_from("item_update.yml")
def upd_item(id):
    """
    update a item
    """
    req = request.get_json()
    sql = f"""update items set article=:article,name=:name,item_image=:item_image
    where id=:id and id_user=:id_user"""
    data = {
        "article": req.get("article", ""),
        "name": req.get("name", ""),
        "item_image": req.get("item_image", ""),
        "id_user": get_jwt_identity(),
        "id": id,
    }
    res_item = do_sql_cmd(sql, data)
    if res_item["rowcount"] < 1:
        return jsonify({"status": "error", "data": res_item["data"]})

    sql = f"""update `prices` set 
    price:=price
    where id_item=:id and currency=:currency"""
    data = {
        "price": req.get("price", 0),
        "currency": req.get("currency", 0),
        "id": id,
    }
    res = do_sql_cmd(sql, data)
    if res["rowcount"] < 1:
        return jsonify({"status": "error", "data": res["data"]})

    return jsonify({"status": "ok", "data": res_item["data"]})
