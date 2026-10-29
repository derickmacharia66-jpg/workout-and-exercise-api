#!/usr/bin/env python3

from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    ex1 = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    ex2 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    ex3 = Exercise(name="Bench Press", category="Strength", equipment_needed=True)

    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(date="2026-10-25", duration_minutes=45, notes="Morning upper body routine")
    w2 = Workout(date="2026-10-26", duration_minutes=30, notes="Evening cardio run")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Linking workouts and exercises...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, reps=20, sets=3)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex3.id, reps=10, sets=4)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex2.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded successfully!")