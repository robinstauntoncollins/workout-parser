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
                    "uri": "/api/v1/workouts/1",
                }
            ]
        }

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
                    'uri': '/api/v1/workouts/1',
                    'exercises': [
                        {
                            'set_number': 1,
                            'reps': 5,
                            'weight': 0,
                            'hold': 0,
                            'workout_id': 1,
                            'exercise_id': 6,
                            'workout_section_id': 3
                        },
                        {
                            'set_number': 2,
                            'reps': 5,
                            'weight': 0,
                            'hold': 0,
                            'workout_id': 1,
                            'exercise_id': 6,
                            'workout_section_id': 3
                        },
                        {
                            'set_number': 3,
                            'reps': 6,
                            'weight': 0,
                            'hold': 0,
                            'workout_id': 1,
                            'exercise_id': 6,
                            'workout_section_id': 3
                        },  
                    ]
                }
            ]
        }
