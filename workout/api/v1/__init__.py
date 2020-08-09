from flask import Blueprint
from flask_restful import Api


API_VERSION_V1 = 1


api_v1_bp = Blueprint('api', __name__)
api = Api(api_v1_bp)

from . import workouts
api.add_resource(workouts.WorkoutListAPI, '/workouts', '/workouts/', endpoint='workouts')
api.add_resource(workouts.WorkoutAPI, '/workouts/<int:id>', '/workouts/<int:id>/', endpoint='workout')


def get_catelog():
    return {
        'workouts_url': api.url_for(workouts.WorkoutListAPI, _external=True),
    }
