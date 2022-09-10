from __future__ import annotations

from HeroCode.models import db


class Enemies(db.Model):
    __tablename__ = 'enemies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hp = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get(**kwargs) -> Enemies:
        return Enemies.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'hp': self.hp
        }
