from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Table Constraints (Fulfills Table Constraints requirement)
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    # Model Validations (Fulfills Model Validations requirement)
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return duration

    @validates('date')
    def validate_date(self, key, date):
        if not date or not date.strip():
            raise ValueError("Workout date cannot be empty.")
        return date

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Table Constraints
    __table_args__ = (
        CheckConstraint("length(name) > 0", name='check_exercise_name_not_empty'),
    )

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    # Model Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty.")
        return name

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Strength', 'Cardio', 'Flexibility', 'Endurance', 'Balance']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {valid_categories}")
        return category

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Table Constraints
    __table_args__ = (
        CheckConstraint('sets IS NULL OR sets > 0', name='check_sets_positive'),
    )

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps < 0:
            raise ValueError("Reps cannot be negative.")
        return reps


# Marshmallow Schemas (Fulfills Serialization & Schema Validation requirement)
class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        include_fk = True
        load_instance = True

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True

class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True

    workout_exercises = ma.Nested(WorkoutExerciseSchema, many=True)
    exercises = ma.Nested(ExerciseSchema, many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()