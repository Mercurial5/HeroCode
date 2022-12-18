from flask import request

from HeroCode import db
from HeroCode.blueprints.analytics import analytics
from HeroCode.models import Action


@analytics.route('/action', methods=['POST'])
def action():
    body = request.json
    type = body.get('type', None)
    text = body.get('text', None)
    username = body.get('username', None)

    if None in [type, text, username]:
        return (dict(status=False))

    action = Action(type=type, text=text, username=username)
    db.session.add(action)
    db.session.commit()

    return (dict(status=True))