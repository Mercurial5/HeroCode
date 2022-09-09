from __future__ import annotations

from HeroCode.models import db


class Enemies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enemy_problems_id = db.Column(db.Integer, db.ForeignKey('enemy_problems.id'))
    name = db.Column(db.String(255))
    hp = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get(**kwargs) -> Enemies:
        return Enemies.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'enemy_problems_id': self.enemy_problems_id,
            'name': self.name,
            'hp': self.hp
        }
