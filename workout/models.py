from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username} e: {self.email or 'none'}>"

    def import_data(self, data):
        try:
            self.username = data['username']
            self.email = data.get('email')
        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercises = db.relationship('ExerciseLogEntry', backref='workout', lazy='dynamic')

    def __repr__(self):
        return f"<Workout {self.date.date()} of user: {self.user.name}"

    def import_data(self, data):
        try:
            self.date = data['date']
            self.user = data['user']
        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}


class ExerciseLogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    set_number = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    hold = db.Column(db.Integer)
    rest = db.Column(db.Integer, default=90)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    workout_section_id = db.Column(db.Integer, db.ForeignKey('workout_section.id'))

    def __repr__(self):
        return f"<LogEntry Workout: {self.workout.date} Section: {self.workout_section.name} Exercise: {self.exercise} Set: {self.set_number} reps: {self.reps} weight: {self.weight}>"

    def import_data(self, data):
        try:
            self.set_number = data['set_number']
            self.reps = data['reps']
            self.weight = data.get('weight')
            self.section = data.get('section')
            self.hold = data.get('hold')
            self.workout = data['workout']
            self.exercise = data['exercise']
            self.workout_section = data['workout_section']

        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}


class WorkoutSection(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True)
    exercises = db.relationship('ExerciseLogEntry', backref='workout_section', lazy='dynamic')

    def __repr__(self):
        return f"<Section: {self.name}"

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValueError(f"Missing 'name': {str(e)}")
        return self


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    logs = db.relationship('ExerciseLogEntry', backref='exercise', lazy='dynamic')

    def __repr__(self):
        return (f"<Exercise "
                f"{' ' + self.variation.name if self.variation is not None else ''}"
                f"{' ' + self.equipment.name if self.equipment is not None else ''}"
                f"{' ' + self.name}>")

    def import_data(self, data):
        try:
            self.name = data['name']
            self.description = data.get('description')
            self.variation = data.get('variation')
            self.equipment = data.get('equipment')
            self.category = data.get('category')
        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}


class Variation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    difficulty = db.Column(db.Integer, index=True)
    exercises = db.relationship('Exercise', backref='variation', lazy='dynamic')

    def __repr__(self):
        return f"<Variation {self.name}>"

    def import_data(self, data):
        try:
            self.name = data['name']
            self.difficulty = data['difficulty']
            self.description = data.get('description')
        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    exercises = db.relationship('Exercise', backref='equipment', lazy='dynamic')

    def __repr__(self):
        return f"<Equipment {self.name}>"

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    exercises = db.relationship('Exercise', backref='category', lazy='dynamic')

    def __repr__(self):
        return f"<Category {self.name}>"

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValueError(f"Missing parameter: {str(e)}")
        return self

    def export_data(self):
        return {}
