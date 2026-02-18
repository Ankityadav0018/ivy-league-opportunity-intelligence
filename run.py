"""
Main entry point for the Ivy League Opportunity Intelligence System
Run this file to start the Flask application
"""
from app import create_app, db
from app.models.user import User
from app.models.opportunity import Opportunity, Application
from app.models.community import Post, Comment, Like, Group

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    return {
        'db': db,
        'User': User,
        'Opportunity': Opportunity,
        'Application': Application,
        'Post': Post,
        'Comment': Comment,
        'Like': Like,
        'Group': Group
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        print("Starting Flask application...")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
