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
            raise ValueError()
        return self

    def export_data(self):
        return {}


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sections = db.relationship('Section', backref='workout', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Workout {self.date.date()} of user: {self.user_id} with sections: {self.sections.all()}"

    def import_data(self, data):
        try:
            self.date = data['date']
            self.user = data['user']
        except KeyError as e:
            raise ValueError()
        return self

    def export_data(self):
        return {}


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True)
    rest = db.Column(db.Integer, default=90)
    exercises = db.relationship('ExerciseLogEntry', backref='section', lazy='dynamic')
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))

    def __repr__(self):
        return f"<Section {self.name} rest: {self.rest if self.rest is not None else 0}s>"

    def import_data(self, data):
        try:
            self.name = data['name']
            self.rest = data.get('rest')
            self.workout = data['workout']
        except KeyError as e:
            raise ValueError()
        return self

    def export_data(self):
        return {}


class ExerciseLogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    set_number = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

    def __repr__(self):
        return f"<LogEntry Exercise: {self.exercise} Set: {self.set_number} reps: {self.reps} weight: {self.weight}>"

    def import_data(self, data):
        try:
            self.set_number = data['set_number']
            self.reps = data['reps']
            self.weight = data.get('weight')
            self.section = data['section']
        except KeyError as e:
            raise ValueError()
        return self

    def export_data(self):
        return {}



class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    logs = db.relationship('ExerciseLogEntry', backref='exercise', lazy='dynamic')

    def __repr__(self):
        return f"<Exercise {self.name} {self.variation} on {self.equipment}>"

    def import_data(self, data):
        try:
            self.name = data['name']
            self.description = data.get('description')
            self.variation = data.get('variation')
            self.equipment = data.get('equipment')
            self.category = data.get('category')
        except KeyError as e:
            raise ValueError()
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
            raise ValueError()
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
            raise ValueError()
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
            raise ValueError()
        return self

    def export_data(self):
        return {}
