from datetime import datetime

import pytest

from workout.models import db, User, Workout, ExerciseLogEntry


class TestUserModel():

    def test_basic(self):
        new_user = User().import_data({
            'username': 'Robin',
            'email': '123fake@gmail.com',
            'password_hash': '18hfiaheh923hqohhfskan0f3',
        })

        assert new_user.username == 'Robin'
        assert new_user.email == '123fake@gmail.com'
        assert new_user.password_hash == '18hfiaheh923hqohhfskan0f3'
        user_data = new_user.export_data()
        assert user_data == {
            'username': 'Robin',
            'email': '123fake@gmail.com',
            'password_hash': '18hfiaheh923hqohhfskan0f3',
        }


class TestWorkoutModel():
    def test_basic_workout(self, test_datetime):
        new_workout = Workout(
            date=test_datetime,
            user_id=1
        )
        assert new_workout.date == test_datetime
        assert new_workout.user_id == 1

    def test_import_workout(self, test_datetime):
        new_workout = Workout().import_data({
            'date': test_datetime,
            'user_id': 1,
        })

        assert new_workout.date == test_datetime
        assert new_workout.user_id == 1

    def test_import_workout_without_date(self, test_client):
        new_workout = Workout().import_data(
            {
                'user_id': 1
            }
        )
        db.session.add(new_workout)
        db.session.commit()
        now = datetime.utcnow()
        workout = Workout.query.first()
        assert workout.user_id == 1
        assert type(workout.date) == datetime
        assert pytest.approx(workout.date.timestamp(), now.timestamp())

    def test_export_workout(self, new_workout, test_datetime):
        workout_data = new_workout.export_data()
        assert workout_data == {
            'date': test_datetime,
            'user_id': 1,
            'exercises': []
        }


class TestExerciseLogEntryModel():

    def test_basic_log_entry(self):
        log_entry = ExerciseLogEntry(
            set_number=1,
            reps=5,
            weight=0,
            hold=0,
            workout_id=1,
            exercise_id=5,
            workout_section_id=3,
        )
        assert log_entry.set_number == 1
        assert log_entry.reps == 5
        assert log_entry.weight == 0
        assert log_entry.hold == 0
        assert log_entry.workout_id == 1
        assert log_entry.exercise_id == 5
        assert log_entry.workout_section_id == 3

    def test_import_log_entry(self):
        log_entry = ExerciseLogEntry().import_data({
            'set_number': 1,
            'reps': 5,
            'weight': 0,
            'hold': 0,
            'workout_id': 1,
            'exercise_id': 6,
            'workout_section_id': 3
        })
        assert log_entry.set_number == 1
        assert log_entry.reps == 5
        assert log_entry.weight == 0
        assert log_entry.hold == 0
        assert log_entry.workout_id == 1
        assert log_entry.exercise_id == 6
        assert log_entry.workout_section_id == 3

    def test_export_log_entry(self, exercise_log_entries):
        log_entry_data = exercise_log_entries[0].export_data()
        assert log_entry_data == {
            'set_number': 1,
            'reps': 5,
            'weight': 0,
            'hold': 0,
            'workout_id': 1,
            'exercise_id': 6,
            'workout_section_id': 3
        }
