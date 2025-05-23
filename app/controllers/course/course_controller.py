from flask import Blueprint, request, jsonify
from app.extensions import db
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORISED
import validators
from app.Models.Course import Course

# registering Course blueprint
course_bp = Blueprint('course', __name__, url_prefix='/api/v1/courses')

# Create a new course
@course_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), HTTP_400_BAD_REQUEST
 
   # Validate input data
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    program_id = data.get('program_id')
    
    # Validate required fields
    if not name or not description or not start_date or not end_date or not program_id:
        return jsonify({"error": "Missing required fields"}), HTTP_400_BAD_REQUEST

# Validate input types
    if not isinstance(name, str) or not isinstance(description, str):
        return jsonify({"error": "Invalid input type"}), HTTP_400_BAD_REQUEST
 
 # Validate date format
    if not validators.date(start_date) or not validators.date(end_date):
        return jsonify({"error": "Invalid date format"}), HTTP_400_BAD_REQUEST
    

# Validate program ID
    try:
        new_course = Course(name=name, description=description, start_date=start_date, end_date=end_date, program_id=program_id)
        db.session.add(new_course)
        db.session.commit()
        
        # Check if the course was created successfully
        return jsonify({"message": "Course created successfully", "course_id": new_course.id}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
