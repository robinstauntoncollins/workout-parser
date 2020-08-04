from flask import url_for, Blueprint

intent_api_bp = Blueprint('addWorkout', __name__)

from . import new_workout


def get_catelog():
    return {
        'workout_url': url_for('intent.addWorkout', _external=True),
    }
