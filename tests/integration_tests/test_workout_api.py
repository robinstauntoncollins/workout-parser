from datetime import datetime

import pytest

from workout.models import db, Workout, User


class TestWorkoutAPI():

    def test_get_workouts(self, test_client):
        u = User(username='Robin', email='123fake@gmail.com')
        w = Workout(date=datetime.utcnow(), user=u)
        db.session.add_all([u, w])
        db.session.commit()

        r = test_client.get(
            '/api/v1/workouts',
            json={
                'user_id': 1
            })
        assert r.get_json() == {
            'workouts': [
                {
                    "email": '123fake@gmail.com',
                    "id": 1,
                    "uri": "/api/v1/workouts/1",
                    "username": 'Robin'
                }
            ]
        }
