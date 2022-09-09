from __future__ import annotations

from HeroCode.models import db


class Problems(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)

    @staticmethod
    def get(**kwargs) -> Problems:
        return Problems.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
