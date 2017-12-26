# coding=utf-8
from photohub.extensions.flasksqlalchemy import db


# 动漫
class Comic(db.Model):
    __tablename__ = 'comics'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    refresh_time = db.Column(db.DateTime, nullable=True)
    author = db.Column(db.String(256), nullable=True)
    classify_id = db.Column(db.Integer, nullable=False)
    front_cover = db.Column(db.String(256), nullable=True)
