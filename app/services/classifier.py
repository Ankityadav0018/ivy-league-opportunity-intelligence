"""
Module 2: Domain Classification System
Classifies opportunities into relevant domains using keyword matching and NLP techniques.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os
import re
from typing import Dict, List


class DomainClassifier:
    """Classifier for categorizing opportunities by domain and type."""
    
    DOMAINS = [
        'Artificial Intelligence',
        'Law',
        'Engineering',
        'Biomedical',
        'Economics',
        'Computer Science',
        'Physics',
        'Chemistry',
        'Mathematics',
        'Other'
    ]
    
    # Keywords for domain identification
    DOMAIN_KEYWORDS = {
        'Artificial Intelligence': ['ai', 'machine learning', 'deep learning', 'neural network', 'nlp', 'computer vision'],
        'Law': ['law', 'legal', 'justice', 'court', 'attorney', 'legislation'],
        'Engineering': ['engineering', 'mechanical', 'civil', 'electrical', 'design'],
        'Biomedical': ['biomedical', 'medicine', 'biology', 'health', 'clinical', 'medical'],
        'Economics': ['economics', 'finance', 'business', 'market', 'trade'],
        'Computer Science': ['programming', 'software', 'coding', 'algorithm', 'data structure'],
        'Physics': ['physics', 'quantum', 'mechanics', 'thermodynamics'],
        'Chemistry': ['chemistry', 'chemical', 'molecular', 'organic'],
        'Mathematics': ['mathematics', 'calculus', 'statistics', 'algebra'],
    }
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.classifier = MultinomialNB()
        self.is_trained = False
    
    def classify_by_keywords(self, text: str) -> str:
        """
        Classify text using keyword matching.
        
        Args:
            text: Opportunity title and description
            
        Returns:
            Predicted domain
        """
        text_lower = text.lower()
        scores = {}
        
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[domain] = score
        
        # Return domain with highest score, or 'Other' if no match
        max_domain = max(scores, key=scores.get)
        return max_domain if scores[max_domain] > 0 else 'Other'
    
    def classify_opportunity(self, title: str, description: str) -> str:
        """
        Classify an opportunity into a domain.
        
        Args:
            title: Opportunity title
            description: Opportunity description
            
        Returns:
            Classified domain
        """
        text = f"{title} {description}"
        return self.classify_by_keywords(text)
    
    def categorize_type(self, title: str, description: str) -> str:
        """
        Categorize opportunity type (Workshop, Hackathon, etc.).
        
        Args:
            title: Opportunity title
            description: Opportunity description
            
        Returns:
            Opportunity category
        """
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['workshop', 'seminar', 'training']):
            return 'Workshop'
        elif any(word in text for word in ['hackathon', 'hack', 'coding competition']):
            return 'Hackathon'
        elif any(word in text for word in ['research', 'internship', 'lab']):
            return 'Research'
        elif any(word in text for word in ['scholarship', 'grant', 'funding']):
            return 'Scholarship'
        elif any(word in text for word in ['conference', 'symposium', 'summit']):
            return 'Conference'
        else:
            return 'Other'
