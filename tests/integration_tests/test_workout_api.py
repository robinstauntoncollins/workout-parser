from datetime import datetime

import pytest

from workout.models import db, Workout, User, ExerciseLogEntry


class TestWorkoutAPI():

    def test_get_workouts(self, test_client, test_datetime):
        u = User(username='Robin', email='123fake@gmail.com')
        w = Workout(date=test_datetime, user=u)
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
                    "id": 1,
                    "date": test_datetime.isoformat(),
                    "user_id": 1,
                    "self_url": "/api/v1/workouts/1",
                }
            ]
        }
    
    @pytest.mark.skip()
    def test_post_workout(self, new_user, test_client):
        pass

    @pytest.mark.skip()
    def test_get_workout_with_exercises(self, test_client, test_datetime, exercise_log_entries):
        u = User(username='Robin', email='123fake@gmail.com')
        w = Workout(
            date=test_datetime,
            user=u,
            exercises=exercise_log_entries
        )
        db.session.add(w)
        db.session.commit()

        r = test_client.get(
            '/api/v1/workouts',
            json={
                'user_id': 1
            }
        )

        assert r.get_json() == {
            'workouts': [
                {
                    'id': 1,
                    'date': test_datetime.isoformat(),
                    'user_id': 1,
                    'self_url': '/api/v1/workouts/1',
                }
            ]
        }
