from flask import request  # , current_app
# from flask_restful import marshal

# from workout.errors import make_error
# from workout.models import Workout
# from workout.utils import create_account

from . import intent_api_bp
# from .common import account_fields


@intent_api_bp.route('/addWorkout', methods=['POST'])
def new_workout():
    data = request.get_json()
    print(data)
