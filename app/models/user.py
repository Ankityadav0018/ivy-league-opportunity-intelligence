"""
User Model - Student Profile & Authentication
"""
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for student profiles."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100))
    
    # Student Profile Information
    domain = db.Column(db.String(50))  # AI, Law, Engineering, etc.
    skills = db.Column(db.Text)  # Comma-separated skills
    interests = db.Column(db.Text)  # Student interests
    academic_background = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    
    # InCoScore Parameters
    hackathons_count = db.Column(db.Integer, default=0)
    internships_count = db.Column(db.Integer, default=0)
    research_papers_count = db.Column(db.Integer, default=0)
    coding_score = db.Column(db.Float, default=0.0)
    competition_wins = db.Column(db.Integer, default=0)
    incoscore = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password: str) -> None:
        """Hash and set the user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def calculate_incoscore(self) -> float:
        """
        Calculate InCoScore based on student achievements.
        
        Formula: Weighted sum of various parameters
        """
        score = (
            self.hackathons_count * 10 +
            self.internships_count * 15 +
            self.research_papers_count * 20 +
            self.coding_score * 0.5 +
            self.competition_wins * 12
        )
        self.incoscore = round(score, 2)
        return self.incoscore
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'
