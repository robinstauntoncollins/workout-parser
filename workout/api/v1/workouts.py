from flask_restful import Resource, reqparse, fields, marshal
from workout import models


workout_fields = {
    'id': fields.Integer,
    'date': fields.DateTime(dt_format='iso8601'),
    'user_id': fields.Integer,
    'self_url': fields.Url('api.workout')
}


class WorkoutListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, required=True, location="json")
        super(WorkoutListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        workouts = models.Workout.query.filter_by(user_id=args['user_id']).all()
        return {
            'workouts': [
                marshal(workout, workout_fields)
                for workout in workouts
                if workout.user.id == args['user_id']
            ]
        }

    def post(self):
        args = self.reqparse.parse_args()
        workout = models.Workout.query.get_or_404(args['workout_id'])
        workout = models.Workout().import_data(args)
        models.db.session.add(workout)
        models.db.session.commit()
        return {'workout': marshal(workout, workout_fields)}, 201


class WorkoutAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('workout_id', type=float, required=False, location="json")
        super(WorkoutAPI, self).__init__()

    def get(self, id):
        workout = models.Workout.query.get_or_404(id)
        return {'workout': marshal(workout, workout_fields)}

    def put(self, id):
        workout = models.Workout.query.get_or_404(id)
        args = self.reqparse.parse_args()
        workout.balance = args['balance']
        models.db.session.add(workout)
        models.db.session.commit()
        return {'workout': marshal(workout, workout_fields)}

    def delete(self, id):
        workout = models.Workout.query.get_or_404(id)
        models.db.session.delete(workout)
        models.db.session.commit()
        return {'result': True}
