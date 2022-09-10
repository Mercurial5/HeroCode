from __future__ import annotations

from datetime import datetime

from HeroCode.models import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    registered = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)

    @staticmethod
    def get(**kwargs) -> Users:
        return Users.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'is_active': self.is_active,
            'registered': self.registered
        }
