"""
Opportunity Routes - Module 1, 2, 3, 4
Real-time opportunities, classification, personalization, auto-application
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.opportunity import Opportunity, Application
from app.services.scraper import OpportunityScraper
from app.services.classifier import DomainClassifier
from datetime import datetime
from typing import Optional

bp = Blueprint('opportunities', __name__, url_prefix='/opportunities')


@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing personalized opportunities."""
    # Get opportunities matching user's domain
    opportunities = Opportunity.query.filter_by(
        domain=current_user.domain,
        is_active=True
    ).order_by(Opportunity.extracted_at.desc()).all()
    
    return render_template('dashboard.html', opportunities=opportunities)


@bp.route('/all')
@login_required
def all_opportunities():
    """View all opportunities."""
    opportunities = Opportunity.query.filter_by(is_active=True)\
        .order_by(Opportunity.extracted_at.desc()).all()
    return render_template('opportunities.html', opportunities=opportunities)


@bp.route('/scrape')
@login_required
def scrape_opportunities():
    """Trigger web scraping to get new opportunities."""
    scraper = OpportunityScraper()
    classifier = DomainClassifier()
    
    # Scrape all universities
    scraped_data = scraper.scrape_all_universities()
    
    new_count = 0
    for data in scraped_data:
        # Check if opportunity already exists
        existing = Opportunity.query.filter_by(title=data['title']).first()
        if not existing:
            # Classify the opportunity
            domain = classifier.classify_opportunity(data['title'], data['description'])
            category = classifier.categorize_type(data['title'], data['description'])
            
            # Create new opportunity
            opportunity = Opportunity(
                title=data['title'],
                description=data['description'],
                university=data['university'],
                url=data['url'],
                domain=domain,
                category=category
            )
            db.session.add(opportunity)
            new_count += 1
    
    db.session.commit()
    flash(f'Successfully scraped {new_count} new opportunities!', 'success')
    return redirect(url_for('opportunities.all_opportunities'))


@bp.route('/<int:id>')
@login_required
def view_opportunity(id):
    """View single opportunity details."""
    opportunity = Opportunity.query.get_or_404(id)
    
    # Check if user already applied
    application = Application.query.filter_by(
        student_id=current_user.id,
        opportunity_id=id
    ).first()
    
    return render_template('opportunity_detail.html', 
                          opportunity=opportunity,
                          application=application)


@bp.route('/<int:id>/apply', methods=['POST'])
@login_required
def apply_opportunity(id):
    """Auto-apply to an opportunity (Module 4)."""
    opportunity = Opportunity.query.get_or_404(id)
    
    # Check if already applied
    existing = Application.query.filter_by(
        student_id=current_user.id,
        opportunity_id=id
    ).first()
    
    if existing:
        flash('You have already applied to this opportunity', 'warning')
        return redirect(url_for('opportunities.view_opportunity', id=id))
    
    # Create application
    application = Application(
        student_id=current_user.id,
        opportunity_id=id,
        status='submitted'
    )
    
    db.session.add(application)
    db.session.commit()
    
    flash(f'Successfully applied to {opportunity.title}!', 'success')
    return redirect(url_for('opportunities.my_applications'))


@bp.route('/my-applications')
@login_required
def my_applications():
    """View user's applications."""
    applications = Application.query.filter_by(student_id=current_user.id)\
        .order_by(Application.submitted_at.desc()).all()
    return render_template('my_applications.html', applications=applications)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_opportunity():
    """
    Allow users to create their own opportunities (hackathons, internships, jobs).
    
    Returns:
        Rendered template for GET request or redirect for POST request.
    """
    if request.method == 'POST':
        # Get form data with validation
        title: str = request.form.get('title', '').strip()
        description: str = request.form.get('description', '').strip()
        university: str = request.form.get('university', '').strip()
        domain: str = request.form.get('domain', '').strip()
        category: str = request.form.get('category', '').strip()
        url: str = request.form.get('url', '').strip()
        location: str = request.form.get('location', '').strip()
        requirements: str = request.form.get('requirements', '').strip()
        deadline_str: str = request.form.get('deadline', '')
        
        # Validate required fields
        if not title or not description or not domain or not category:
            flash('Title, description, domain, and category are required!', 'error')
            return redirect(url_for('opportunities.create_opportunity'))
        
        # Parse deadline if provided
        deadline: Optional[datetime] = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid deadline format. Use YYYY-MM-DD', 'error')
                return redirect(url_for('opportunities.create_opportunity'))
        
        # Create new opportunity
        opportunity = Opportunity(
            title=title,
            description=description,
            university=university or 'User Generated',
            domain=domain,
            category=category,
            url=url,
            location=location,
            requirements=requirements,
            deadline=deadline,
            is_active=True,
            created_by=current_user.id  # Track who created it
        )
        
        try:
            db.session.add(opportunity)
            db.session.commit()
            flash(f'Opportunity "{title}" created successfully! 🎉', 'success')
            return redirect(url_for('opportunities.my_opportunities'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create opportunity: {str(e)}', 'error')
            return redirect(url_for('opportunities.create_opportunity'))
    
    return render_template('create_opportunity.html')


@bp.route('/my-opportunities')
@login_required
def my_opportunities():
    """
    View opportunities created by the current user.
    
    Returns:
        Rendered template with user's created opportunities.
    """
    opportunities = Opportunity.query.filter_by(created_by=current_user.id)\
        .order_by(Opportunity.extracted_at.desc()).all()
    return render_template('my_opportunities.html', opportunities=opportunities)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_opportunity(id: int):
    """
    Edit an opportunity created by the current user.
    
    Args:
        id: The opportunity ID to edit.
        
    Returns:
        Rendered template for GET or redirect for POST.
    """
    opportunity = Opportunity.query.get_or_404(id)
    
    # Check if user is the creator
    if opportunity.created_by != current_user.id:
        flash('You can only edit opportunities you created!', 'error')
        return redirect(url_for('opportunities.all_opportunities'))
    
    if request.method == 'POST':
        # Update opportunity fields
        opportunity.title = request.form.get('title', '').strip()
        opportunity.description = request.form.get('description', '').strip()
        opportunity.university = request.form.get('university', '').strip()
        opportunity.domain = request.form.get('domain', '').strip()
        opportunity.category = request.form.get('category', '').strip()
        opportunity.url = request.form.get('url', '').strip()
        opportunity.location = request.form.get('location', '').strip()
        opportunity.requirements = request.form.get('requirements', '').strip()
        
        deadline_str: str = request.form.get('deadline', '')
        if deadline_str:
            try:
                opportunity.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid deadline format', 'error')
                return redirect(url_for('opportunities.edit_opportunity', id=id))
        
        # Validate required fields
        if not opportunity.title or not opportunity.description:
            flash('Title and description are required!', 'error')
            return redirect(url_for('opportunities.edit_opportunity', id=id))
        
        try:
            db.session.commit()
            flash('Opportunity updated successfully!', 'success')
            return redirect(url_for('opportunities.my_opportunities'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update opportunity: {str(e)}', 'error')
    
    return render_template('edit_opportunity.html', opportunity=opportunity)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_opportunity(id: int):
    """
    Delete an opportunity created by the current user.
    
    Args:
        id: The opportunity ID to delete.
        
    Returns:
        Redirect to my opportunities page.
    """
    opportunity = Opportunity.query.get_or_404(id)
    
    # Check if user is the creator
    if opportunity.created_by != current_user.id:
        flash('You can only delete opportunities you created!', 'error')
        return redirect(url_for('opportunities.all_opportunities'))
    
    try:
        db.session.delete(opportunity)
        db.session.commit()
        flash('Opportunity deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete opportunity: {str(e)}', 'error')
    
    return redirect(url_for('opportunities.my_opportunities'))


@bp.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
def toggle_opportunity_status(id: int):
    """
    Toggle opportunity active/inactive status.
    
    Args:
        id: The opportunity ID to toggle.
        
    Returns:
        Redirect to my opportunities page.
    """
    opportunity = Opportunity.query.get_or_404(id)
    
    # Check if user is the creator
    if opportunity.created_by != current_user.id:
        flash('You can only modify opportunities you created!', 'error')
        return redirect(url_for('opportunities.all_opportunities'))
    
    opportunity.is_active = not opportunity.is_active
    db.session.commit()
    
    status: str = 'active' if opportunity.is_active else 'inactive'
    flash(f'Opportunity marked as {status}!', 'success')
    return redirect(url_for('opportunities.my_opportunities'))
