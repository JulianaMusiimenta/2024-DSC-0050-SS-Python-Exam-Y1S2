# qtn 1 task 1 part b

from app.extensions import db
from datetime import datetime

class Course(db.Model):
    
    _tablename_ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)



def _init_(self, name, description, start_date, end_date, program_id):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.program_id = program_id





    
