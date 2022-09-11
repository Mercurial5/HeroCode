from __future__ import annotations

from HeroCode.models import db


class Tests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    input = db.Column(db.Text)
    output = db.Column(db.Text)

    @staticmethod
    def get(**kwargs) -> list[Tests]:
        return Tests.query.filter_by(**kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'input': self.input,
            'output': self.output
        }
