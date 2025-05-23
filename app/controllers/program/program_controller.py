# question 1 task 2 part a

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORISED
import validators
from app.Models.Program import Program


# registering Program blueprint
program_bp = Blueprint('program', __name__, url_prefix='/api/v1/programs')

# Create a new program
# this function creates a new program in the database
@program_bp.route('/', methods=['POST'])
def create_program():

    # Validate input data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), HTTP_400_BAD_REQUEST

    # Validate required fields
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

# Validate input types
    if not name or not description or not start_date or not end_date:
        return jsonify({"error": "Missing required fields"}), HTTP_400_BAD_REQUEST
 
    if not isinstance(name, str) or not isinstance(description, str):
        return jsonify({"error": "Invalid input type"}), HTTP_400_BAD_REQUEST
# Validate date format
    if not validators.date(start_date) or not validators.date(end_date):
        return jsonify({"error": "Invalid date format"}), HTTP_400_BAD_REQUEST
# Validate program ID
    # Check if the program already exists
    existing_program = Program.query.filter_by(name=name).first()
    if existing_program:
        return jsonify({"error": "Program already exists"}), HTTP_409_CONFLICT
    
    # Create a new program
    try:
        new_program = Program(name=name, description=description, start_date=start_date, end_date=end_date)
        db.session.add(new_program)
        db.session.commit()
        return jsonify({"message": "Program created successfully", "program_id": new_program.id}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    


    #  question 1 task 2 part f

    # update a program
@program_bp.route('/programs/<int:program_id>', methods=['PUT'])
def update_program(program):
     

     try:
          logged_in_program = request.headers.get('logged_in_program')
          current_program = request.headers.get('current_program')

          #get program by id
          program = Program.query.filter_by(id=id).first()
          if not program:
                 return jsonify({
                        "message": "Author not found"
                 }), HTTP_400_BAD_REQUEST
          
          elif logged_in_program != 'admin' and program.id != current_program:
                    return jsonify({
                            "message": "You are not authorized to update this author details"
                    }), HTTP_401_UNAUTHORISED
          
          else:
               # store request data

               name = request.get_json.get('name', program.name)
               description = request.get_json.get('email', program.decription)
               start_date = request.get_json.get('start_date', program.start_date)
               end_date = request.get_json.get('end_date', program.end_date)
                
              
               if not name or not description or not start_date:
                    return jsonify({
                        "error": "Missing required fields"
                    }), HTTP_400_BAD_REQUEST
               
               program.name = name
               program.description = description
               program.start_date = start_date
               program.end_date = end_date

          db.session.commit()

        
          return jsonify({
                    "message": f"{name} has been updated successfully",
                    "author": {
                        "id": program.id,
                        "name": program.name,
                        "description": program.description,
                        "start_date": program.start_date,
                        "end_date": program.end_date
                    }
                })
     except Exception as e:
          return jsonify({
                "error": str(e)
          }), HTTP_500_INTERNAL_SERVER_ERROR
     


