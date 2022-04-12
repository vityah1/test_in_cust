from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from flasgger import swag_from
from utils import do_sql_cmd, do_sql_sel
from models import *
from mydb import db


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
    new_item = Item(
        article=req.get("article", ""),
        name=req.get("name", ""),
        item_image=req.get("item_image", ""),
        id_user=get_jwt_identity(),
    )
    db.session.add(new_item)
    db.session.flush()
    # db.session.refresh(new_item)

    item_id = new_item.id
    # rowcount = len(db.session.new)

    new_item_price = Price(
        item_id=item_id, price=req.get("price", 0), currency=req.get("currency", 0)
    )
    db.session.add(new_item_price)

    db.session.commit()

    return jsonify({"status": "ok", "id": item_id})


@api_crud_bp.route("/api/items/<int:id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
@swag_from("item_delete.yml")
def del_item(id):
    """
    mark item deleted
    """
    # item_for_del = Item.query.get_or_404(id)
    item_for_del = Item.query.filter_by(id=id, id_user=get_jwt_identity()).first()
    item_for_del.deleted = 1
    db.session.add(item_for_del)

    price_for_del = Price.query.filter_by(item_id=id).first_or_404()
    db.session.delete(price_for_del)

    db.session.commit()

    return jsonify({"status": "ok", "id": id})


@api_crud_bp.route("/api/items/<id>", methods=["PUT"])
@cross_origin()
@jwt_required()
@swag_from("item_update.yml")
def upd_item(id):
    """
    update a item and price item
    """

    req = request.get_json()

    # item_for_upd = Item.query.get_or_404(id)
    item_for_upd = Item.query.filter_by(
        id=id, id_user=get_jwt_identity()
    ).first_or_404()

    item_for_upd.article = req.get("article", "")
    item_for_upd.name = req.get("name", "")
    item_for_upd.item_image = req.get("item_image", "")
    item_for_upd.id_user = get_jwt_identity()

    db.session.add(item_for_upd)

    price_for_upd = Price.query.filter_by(item_id=id).first_or_404()

    price_for_upd.price = req.get("price", 0)
    price_for_upd.currency = req.get("currency", 0)

    db.session.add(price_for_upd)

    db.session.commit()

    return jsonify({"status": "ok", "id": id})


@api_crud_bp.route("/api/items/<int:id>", methods=["GET"])
@cross_origin()
@jwt_required()
@swag_from("list_item.yml")
def show_item(id):
    """
    get info about item
    """

    item = Item.query.filter_by(
        id=id, id_user=get_jwt_identity(), deleted=0
    ).first_or_404()
    result = dict(item.__dict__)
    result.pop("_sa_instance_state", None)
    return jsonify({"status": "ok", "data": [result]})


@api_crud_bp.route("/api/items", methods=["GET"])
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
from `items` a left join `prices` b on a.id=b.item_id
where 1=1 
{search_query}
and id_user=:id_user
and deleted != 1
order by :sort
limit 10 offset :offset
"""
    res = do_sql_sel(sql, sql_data_conditions)
    result = [dict(row) for row in res]

    return jsonify({"status": "ok", "data": result})
