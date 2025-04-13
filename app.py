from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store student details and attendance
students = {}       
attendance = {}     

@app.route('/')
def home():
    return "Welcome to the Student Attendance System!"

#  Register a new student
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

#  View all students
@app.route('/students', methods=['GET'])
def list_students():
    return jsonify(students)

#  Mark attendance for a student
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

#  Get attendance of a student
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
