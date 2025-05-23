# qtn 1 task 1 part a

from app.extensions import db
from datetime import datetime

class Program(db.Model):
    
    _tablename_ = 'Programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, description, start_date, end_date):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
    def __repr__(self):
        return f'<Program {self.name}>'
    def __str__(self):
        return f'Program: {self.name}, Description: {self.description}, Start Date: {self.start_date}, End Date: {self.end_date}'




