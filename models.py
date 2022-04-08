from mydb import db
from sqlalchemy import ForeignKey, UniqueConstraint


class User(db.Model):
    """User Model for storing user related details"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    token = db.Column(db.String(100))
    avatar = db.Column(db.String(100))


class Item(db.Model):
    """Item Model for storing item details"""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article = db.Column(db.String(20))
    id_user = db.Column(db.Integer, ForeignKey("users.id"))
    name = db.Column(db.String(100))
    deleted = db.Column(db.Integer)
    item_image = db.Column(db.String(100))
    __table_args__ = (
        UniqueConstraint(
            "article", "id_user", "deleted", name="u_items_article_id_user"
        ),
    )


class Price(db.Model):
    """Item Model for storing item details"""

    __tablename__ = "prices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_item = db.Column(db.Integer, ForeignKey("items.id"))
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.Integer, ForeignKey("currencies.id"))
    __table_args__ = (
        UniqueConstraint(
            "id_item", "price", "currency", name="u_prices_item_price_currency"
        ),
    )


class Currency(db.Model):
    """Item Model for storing item details"""

    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency = db.Column(db.String(3), nullable=False)
