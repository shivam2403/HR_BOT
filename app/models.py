# models.py
import uuid
from flask_sqlalchemy import SQLAlchemy
from .extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, default=str(uuid.uuid4()))
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100))
    applied_job_role = db.Column(db.String(100))  
    user_type = db.Column(db.String(50))  # 'Candidate' or 'HR'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, default=str(uuid.uuid4()))  # Use email as UUID
    name = db.Column(db.String(100))
    responses = db.relationship('CandidateResponse', backref='candidate', lazy=True)

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def __repr__(self):
        return f"<Candidate {self.name} - {self.email}>"
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)

class HRInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.String(500), nullable=False)
    key_skills = db.Column(db.String(350), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    required_experience = db.Column(db.String(100), nullable=False)

class CandidateResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    question = db.relationship('Question', backref='responses')

    def __repr__(self):
        return f"<CandidateResponse {self.candidate.name} - {self.question.content}>"