"""
Ivy League Opportunity Intelligence System
Main Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ivy_league_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from app.routes import auth, opportunities, community, ranking
    app.register_blueprint(auth.bp)
    app.register_blueprint(opportunities.bp)
    app.register_blueprint(community.bp)
    app.register_blueprint(ranking.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
