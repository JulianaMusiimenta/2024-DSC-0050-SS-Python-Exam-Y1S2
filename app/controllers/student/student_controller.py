from flask import Blueprint, request, jsonify
from app.extensions import db
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_401_UNAUTHORIZED
import validators
from app.Models.Student import Student


# registering Student blueprint
student_bp = Blueprint('student', __name__, url_prefix='/api/v1/students')


# Create a new student
@student_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), HTTP_400_BAD_REQUEST
 
    # Validate input data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    date_of_birth = data.get('date_of_birth')
    address = data.get('address')

    # Validate required fields
    # this function checks if the required fields are present in the input data
    if not first_name or not last_name or not email or not phone or not date_of_birth or not address:
        return jsonify({"error": "Missing required fields"}), HTTP_400_BAD_REQUEST

    # Validate input types
    # this function checks if the input data is of the correct type
    if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(email, str) or not isinstance(phone, str) or not isinstance(address, str):
        return jsonify({"error": "Invalid input type"}), HTTP_400_BAD_REQUEST

    # Validate date format
    # this function checks if the date of birth is in the correct format
    if not validators.email(email):
        return jsonify({"error": "Invalid email format"}), HTTP_400_BAD_REQUEST


    try:
        new_student = Student(first_name=first_name, last_name=last_name, email=email, phone=phone, date_of_birth=date_of_birth, address=address)
        db.session.add(new_student)
        db.session.commit()

        # Check if the student was created successfully
        return jsonify({"message": "Student created successfully", "student_id": new_student.id}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

 # question 1 task 2 part d

# fetch all students
# this function fetches all students from the database and returns them in JSON format
@student_bp.route('/', methods=['GET'])
def get_all_students():
    # this function fetches all students from the database and returns them in JSON format
    # this function checks if the user is logged in and if they are an admin
    try:
        students = Student.query.all()
        student_list = []
        for student in students:
            student_list.append({
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'phone': student.phone,
                'date_of_birth': student.date_of_birth,
                'address': student.address
            })
        # return the list of students
        return jsonify(student_list), HTTP_200_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


        # question 1 task 2 part e
        # delete a student
        # this function deletes a student from the database based on the student ID provided in the URL
@student_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_author(id):

    try:
        logged_in_student = Student.query.filter_by(id=id).first() # get logged in student


        #get student by id
        author = Student.query.filter_by(id=id).first()
        if not author:
            return jsonify({
                "message": "Student not found"
            }), HTTP_400_BAD_REQUEST
        
        # check if the logged in student is an admin
        elif logged_in_student != 'admin':
            return jsonify({
                "message": "You are not authorized to delete this student"
            }), HTTP_401_UNAUTHORIZED
        
        else:
            # delete associated students
            # this is done by iterating through the students and deleting them one by one
            for student in student.students:
                db.session.delete(student)
            
            # delete the student
            # this deletes the student from the database
            db.session.delete(student)
            db.session.commit()

          
            # return success message
            return jsonify({
                "message": f"{student.first_name} has been deleted successfully"
            }), HTTP_200_OK
    # this function handles any exceptions that occur during the deletion process
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
