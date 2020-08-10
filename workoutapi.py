#!/usr/bin/env python3
import os
import click
from workout import create_app, db, models

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': models.User,
        'Workout': models.Workout,
        'WorkoutSection': models.WorkoutSection,
        'ExerciseLogEntry': models.ExerciseLogEntry,
        'Exercise': models.Exercise,
        'Variation': models.Variation,
        'Equipment': models.Equipment,
        'Category': models.Category
    }


@app.cli.command('createdb')
@click.option('--test-data', type=bool, default=True, help="Initializes database with pre-loaded data")
def createdb(test_data):
    db.drop_all()
    db.create_all()
    if test_data:
        users = [
            {'username': "Robin", 'email': "robyo12121@gmail.com"},
        ]
        categories = [
            {'name': 'Push'},
            {'name': 'Pull'},
            {'name': 'Legs'},
        ]

        equipment = [
            {'name': 'Rings'},
            {'name': 'Bar'},
            {'name': 'Ab-wheel'},
            {'name': 'Band'},
            {'name': 'Barbell'},
        ]

        variations = [
            {'name': 'Unmodified', 'difficulty': 2},
            {'name': 'Beginner', 'difficulty': 1},
            {'name': 'Intermediate', 'difficulty': 2},
            {'name': 'Advanced', 'difficulty': 3},
            {'name': 'Assisted', 'difficulty': 1},
        ]

        exercises = [
            {'name': 'Pullups'},
            {'name': 'Dips'},
            {'name': 'Pushups'},
            {'name': 'Nordic Curl'},
            {'name': 'Deadlift'},
            {'name': 'Squat'},
            {'name': 'Support Holds'},
            {'name': 'Shrimp Squat'},
            {'name': 'Row'},
            {'name': 'Rollouts'},
            {'name': 'Arch Hangs'},
        ]

        workout_sections = [
            {'name': 'Warmup'},
            {'name': 'Strength'},
            {'name': 'Core'},
        ]

        users = [models.User().import_data(u) for u in users]
        db.session.add_all(users)

        categories = [models.Category().import_data(c) for c in categories]
        db.session.add_all(categories)

        equipment = [models.Equipment().import_data(e) for e in equipment]
        db.session.add_all(equipment)

        variations = [models.Variation().import_data(v) for v in variations]
        db.session.add_all(variations)

        exercises = [models.Exercise().import_data(e) for e in exercises]
        db.session.add_all(exercises)

        workout_sections = [models.WorkoutSection().import_data(ws) for ws in workout_sections]
        db.session.add_all(workout_sections)

        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
