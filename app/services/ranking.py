"""
Module 6: InCoScore Ranking Engine
Intelligent Competency Score calculation and ranking system
"""
from typing import List, Dict
from app.models.user import User


class InCoScoreEngine:
    """Intelligent ranking system for student competency."""
    
    # Weights for different parameters
    WEIGHTS = {
        'hackathons': 10,
        'internships': 15,
        'research_papers': 20,
        'coding_score': 0.5,
        'competition_wins': 12
    }
    
    @staticmethod
    def calculate_score(user: User) -> float:
        """
        Calculate InCoScore for a student.
        
        Args:
            user: User object
            
        Returns:
            Calculated InCoScore
        """
        score = (
            user.hackathons_count * InCoScoreEngine.WEIGHTS['hackathons'] +
            user.internships_count * InCoScoreEngine.WEIGHTS['internships'] +
            user.research_papers_count * InCoScoreEngine.WEIGHTS['research_papers'] +
            user.coding_score * InCoScoreEngine.WEIGHTS['coding_score'] +
            user.competition_wins * InCoScoreEngine.WEIGHTS['competition_wins']
        )
        return round(score, 2)
    
    @staticmethod
    def get_leaderboard(domain: str = None, limit: int = 10) -> List[Dict]:
        """
        Get top students based on InCoScore.
        
        Args:
            domain: Filter by specific domain (optional)
            limit: Number of top students to return
            
        Returns:
            List of top students with their scores
        """
        query = User.query
        
        if domain:
            query = query.filter_by(domain=domain)
        
        top_students = query.order_by(User.incoscore.desc()).limit(limit).all()
        
        leaderboard = []
        for rank, student in enumerate(top_students, 1):
            leaderboard.append({
                'rank': rank,
                'name': student.full_name,
                'username': student.username,
                'domain': student.domain,
                'incoscore': student.incoscore,
                'hackathons': student.hackathons_count,
                'internships': student.internships_count,
                'research_papers': student.research_papers_count
            })
        
        return leaderboard
    
    @staticmethod
    def recommend_students_for_opportunity(opportunity_domain: str, limit: int = 5) -> List[User]:
        """
        Recommend top students for a specific opportunity based on domain match and InCoScore.
        
        Args:
            opportunity_domain: Domain of the opportunity
            limit: Number of students to recommend
            
        Returns:
            List of recommended students
        """
        students = User.query.filter_by(domain=opportunity_domain)\
                            .order_by(User.incoscore.desc())\
                            .limit(limit)\
                            .all()
        
        return students
