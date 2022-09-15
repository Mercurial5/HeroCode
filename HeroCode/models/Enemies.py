from __future__ import annotations

from HeroCode.models import db


class Enemies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hp = db.Column(db.Integer, nullable=False)
    damage = db.Column(db.Integer)

    @staticmethod
    def get(**kwargs) -> Enemies:
        return Enemies.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'hp': self.hp
        }
