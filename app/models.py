from sqlalchemy import ARRAY, String
from init import db


class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    some_url = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    properties = db.Column(ARRAY(String), nullable=False)
