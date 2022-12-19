from __future__ import annotations

from datetime import datetime

from HeroCode.models import db


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)

    @staticmethod
    def get(**kwargs) -> Action:
        return Action.query.filter_by(**kwargs).first()

    @staticmethod
    def get_all(**kwargs) -> [Action]:
        return Action.query.filter_by(**kwargs).all()

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'text': self.text,
            'time': self.time,
            'user_id': self.user_id
        }
