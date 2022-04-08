from mydb import db


class User(db.Model):
    """User Model for storing user related details"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    token = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(100), nullable=False)


class Item(db.Model):
    """Item Model for storing item details"""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article = db.Column(db.String(20), unique=True, nullable=False)
    id_user = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    item_image = db.Column(db.String(100))
