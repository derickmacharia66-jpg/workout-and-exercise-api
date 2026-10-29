from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import (
    db, Workout, Exercise, WorkoutExercise,
    workouts_schema, workout_schema,
    exercises_schema, exercise_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Workout Tracker API!"})

# --- WORKOUT ENDPOINTS ---

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.jsonify(workouts), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(workout_schema.jsonify(workout), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        new_workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.jsonify(new_workout), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted successfully"}), 200)


# --- EXERCISE ENDPOINTS ---

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.jsonify(exercises), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(exercise_schema.jsonify(exercise), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.jsonify(new_exercise), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted successfully"}), 200)


# --- WORKOUT-EXERCISE RELATIONSHIP ENDPOINT ---

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response(jsonify({"error": "Workout or Exercise not found"}), 404)

    data = request.get_json() or {}
    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(workout_schema.jsonify(workout), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)