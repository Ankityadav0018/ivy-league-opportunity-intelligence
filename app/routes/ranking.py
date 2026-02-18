"""
Ranking Routes - Module 6
InCoScore Leaderboard and Student Recommendations
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.user import User
from app.services.ranking import InCoScoreEngine

bp = Blueprint('ranking', __name__, url_prefix='/ranking')


@bp.route('/leaderboard')
@login_required
def leaderboard():
    """Display student leaderboard based on InCoScore."""
    domain = request.args.get('domain')
    limit = int(request.args.get('limit', 50))
    
    leaderboard_data = InCoScoreEngine.get_leaderboard(domain=domain, limit=limit)
    
    # Get unique domains for filter
    domains = db.session.query(User.domain).distinct().all()
    domains = [d[0] for d in domains if d[0]]
    
    return render_template('leaderboard.html', 
                          leaderboard=leaderboard_data,
                          domains=domains,
                          selected_domain=domain)


@bp.route('/api/top-students/<domain>')
@login_required
def api_top_students(domain):
    """API endpoint to get top students for a domain."""
    limit = int(request.args.get('limit', 5))
    students = InCoScoreEngine.recommend_students_for_opportunity(domain, limit)
    
    result = []
    for student in students:
        result.append({
            'id': student.id,
            'name': student.full_name,
            'username': student.username,
            'incoscore': student.incoscore,
            'domain': student.domain
        })
    
    return jsonify(result)


@bp.route('/calculate-score')
@login_required
def calculate_all_scores():
    """Recalculate InCoScore for all users."""
    users = User.query.all()
    
    for user in users:
        user.incoscore = InCoScoreEngine.calculate_score(user)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Recalculated scores for {len(users)} users'})
