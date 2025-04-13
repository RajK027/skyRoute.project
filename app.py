from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store student details and attendance
students = {}       # Format: { "1": "Alice", "2": "Bob" }
attendance = {}     # Format: { "1": ["2024-04-13", "2024-04-14"] c}

@app.route('/')
def home():
    return "Welcome to the Student Attendance System!"

# 1. Register a new student
@app.route('/students', methods=['POST'])
def register_student():
    data = request.get_json()
    student_id = data.get('id')
    name = data.get('name')

    if student_id in students:
        return jsonify({"error": "Student already registered!"}), 400

    students[student_id] = name
    attendance[student_id] = []
    return jsonify({"message": "Student registered!", "id": student_id, "name": name}), 201

# 2. View all students
@app.route('/students', methods=['GET'])
def list_students():
    return jsonify(students)

# 3. Mark attendance for a student
@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    student_id = data.get('id')

    if student_id not in students:
        return jsonify({"error": "Student not found!"}), 404

    today = datetime.now().strftime('%Y-%m-%d')
    if today in attendance[student_id]:
        return jsonify({"message": "Attendance already marked today!"}), 200

    attendance[student_id].append(today)
    return jsonify({"message": f"Attendance marked for {students[student_id]} on {today}"}), 200

# 4. Get attendance of a student
@app.route('/attendance/<student_id>', methods=['GET'])
def get_attendance(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found!"}), 404

    return jsonify({
        "name": students[student_id],
        "attendance": attendance[student_id]
    })

if __name__ == '__main__':
    app.run(debug=True)
