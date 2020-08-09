from datetime import datetime

import pytest

from workout.models import User, Workout, ExerciseLogEntry, WorkoutSection, Exercise, \
        Variation, Equipment, Category


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
    def test_basic(self, test_datetime):
        new_workout = Workout().import_data({
            'date': test_datetime,
            'user_id': 1,
        })
        
        assert new_workout.date == test_datetime
        assert new_workout.user_id == 1
        workout_data = new_workout.export_data()
        assert workout_data == {
            'date': test_datetime,
            'user_id': 1,
            'exercises': []
        }        