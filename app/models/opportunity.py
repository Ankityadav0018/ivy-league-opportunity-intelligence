"""
Opportunity Model - Stores extracted opportunities from Ivy League universities
"""
from app import db
from datetime import datetime


class Opportunity(db.Model):
    """Model for storing opportunities from Ivy League universities."""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    university = db.Column(db.String(100))  # Harvard, MIT, Yale, etc.
    
    # Classification
    domain = db.Column(db.String(50))  # AI, Law, Engineering, Biomedical, etc.
    category = db.Column(db.String(50))  # Workshop, Hackathon, Research, Scholarship, Conference
    
    # Details
    deadline = db.Column(db.DateTime)
    url = db.Column(db.String(500))
    requirements = db.Column(db.Text)
    location = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    
    # Track who created this opportunity (for user-generated opportunities)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    extracted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='opportunity', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('User', backref='created_opportunities', foreign_keys=[created_by])
    
    def __repr__(self) -> str:
        return f'<Opportunity {self.title}>'


class Application(db.Model):
    """Model for tracking student applications to opportunities."""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    
    status = db.Column(db.String(20), default='pending')  # pending, submitted, accepted, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'<Application {self.id}>'
