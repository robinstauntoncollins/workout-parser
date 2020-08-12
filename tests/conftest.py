from datetime import datetime

import pytest

from workout import create_app
from workout.models import db, Workout, ExerciseLogEntry

@pytest.fixture()
def test_client():
    app = create_app('testing')

    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        db.drop_all()
        db.create_all()

        yield client
        db.drop_all()
        ctx.pop()

@pytest.fixture()
def test_datetime():
    return datetime(2020, 8, 9, 19, 54, 00)

@pytest.fixture()
def new_user():
    return User().import_data({'username': 'Robin', 'email': '123fake@gmail.com'})


@pytest.fixture()
def new_workout(test_datetime):
    new_workout = Workout().import_data({
            'date': test_datetime,
            'user_id': 1,
        })
    return new_workout

@pytest.fixture()
def exercise_log_entries():
    log_entry_data = [
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
    return [ExerciseLogEntry().import_data(e) for e in log_entry_data]