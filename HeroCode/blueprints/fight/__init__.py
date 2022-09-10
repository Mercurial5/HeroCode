from flask import Blueprint

fight = Blueprint('fight', __name__)

from HeroCode.blueprints.fight import routes
