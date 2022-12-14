from __future__ import annotations

from HeroCode.models import db


class Problems(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemies.id'))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    solution = db.Column(db.Text)

    @staticmethod
    def get(**kwargs) -> Problems:
        return Problems.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'enemy_id': self.enemy_id,
            'name': self.name,
            'description': self.description,
            'solution': self.solution
        }
