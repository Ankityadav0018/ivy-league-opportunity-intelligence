"""
Authentication Routes - User Registration & Login
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        domain = request.form.get('domain', '')
        
        # Validate inputs
        if not username or not email or not password or not full_name or not domain:
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            domain=domain
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Student login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate inputs
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        # Query user from database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password verification
        if user:
            # User exists, now check password
            if user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('opportunities.dashboard'))
            else:
                flash('Invalid password', 'error')
        else:
            flash('Username not found. Please check your username or register.', 'error')
    
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.index'))


@bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('profile.html', user=current_user)


@bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile and achievements."""
    current_user.full_name = request.form.get('full_name', current_user.full_name)
    current_user.domain = request.form.get('domain', current_user.domain)
    current_user.skills = request.form.get('skills', current_user.skills)
    current_user.interests = request.form.get('interests', current_user.interests)
    current_user.academic_background = request.form.get('academic_background', current_user.academic_background)
    
    # Update achievement counts
    current_user.hackathons_count = int(request.form.get('hackathons_count', 0))
    current_user.internships_count = int(request.form.get('internships_count', 0))
    current_user.research_papers_count = int(request.form.get('research_papers_count', 0))
    current_user.coding_score = float(request.form.get('coding_score', 0.0))
    current_user.competition_wins = int(request.form.get('competition_wins', 0))
    
    # Recalculate InCoScore
    current_user.calculate_incoscore()
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('auth.profile'))
