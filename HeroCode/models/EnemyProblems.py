from __future__ import annotations

from HeroCode.models import db


class Problems(db.Model):
    __tablename__ = 'enemy_problems'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))

    @staticmethod
    def get(**kwargs) -> Problems:
        return Problems.query.filter_by(**kwargs).first()

    def serialize(self):
        return {
            'id': self.id,
            'problem_id': self.name
        }
