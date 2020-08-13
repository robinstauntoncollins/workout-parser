from flask import url_for, Blueprint

intent_api_bp = Blueprint('intent', __name__)


def get_catelog():
    return {
        'workout_url': url_for('intent.new_workout', _external=True),
    }
