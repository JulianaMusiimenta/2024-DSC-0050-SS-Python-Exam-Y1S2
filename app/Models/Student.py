
# qtn 1 task 1 part c
from app.extensions import db
from datetime import datetime

class Student(db.Model):
    
    _tablename_ = 'students'
    id = db.Column(db.Integer, primary_key=True)  
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)



    def __init__(self, first_name, last_name, email, phone, date_of_birth, address):
        super(Student).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.address = address
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
