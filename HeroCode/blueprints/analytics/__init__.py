from flask import Blueprint

analytics = Blueprint('analytics', __name__)

from HeroCode.blueprints.analytics import routes