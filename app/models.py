from datetime import datetime
from sqlalchemy import ARRAY, Column, Integer, String
from init import db
from sqlalchemy.ext.hybrid import hybrid_property


class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    properties = db.Column(ARRAY(String), nullable=False)