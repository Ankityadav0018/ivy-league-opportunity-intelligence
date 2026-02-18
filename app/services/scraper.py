"""
Module 1: Real-Time Opportunity Extraction
Web scraping service for Ivy League universities
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpportunityScraper:
    """Scraper for extracting opportunities from Ivy League universities."""
    
    IVY_LEAGUE_URLS = {
        'Harvard': 'https://www.harvard.edu/events',
        'MIT': 'https://www.mit.edu/events',
        'Yale': 'https://www.yale.edu/events',
        'Princeton': 'https://www.princeton.edu/events',
        'Columbia': 'https://www.columbia.edu/events',
        'Cornell': 'https://www.cornell.edu/events',
        'UPenn': 'https://www.upenn.edu/events',
        'Brown': 'https://www.brown.edu/events',
    }
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_university(self, university: str, url: str) -> List[Dict]:
        """
        Scrape opportunities from a specific university.
        
        Args:
            university: Name of the university
            url: URL to scrape
            
        Returns:
            List of opportunity dictionaries
        """
        opportunities = []
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic scraping logic (adapt based on actual website structure)
            events = soup.find_all(['div', 'article'], class_=['event', 'opportunity', 'item'])
            
            for event in events[:10]:  # Limit to 10 per university
                title = event.find(['h2', 'h3', 'h4'])
                description = event.find(['p', 'div'], class_=['description', 'summary'])
                link = event.find('a')
                
                if title:
                    opportunity = {
                        'title': title.get_text(strip=True),
                        'description': description.get_text(strip=True) if description else 'No description',
                        'university': university,
                        'url': link.get('href') if link else url,
                        'extracted_at': datetime.utcnow()
                    }
                    opportunities.append(opportunity)
            
            logger.info(f"Scraped {len(opportunities)} opportunities from {university}")
            
        except Exception as e:
            logger.error(f"Error scraping {university}: {str(e)}")
        
        return opportunities
    
    def scrape_all_universities(self) -> List[Dict]:
        """
        Scrape opportunities from all Ivy League universities.
        
        Returns:
            Combined list of all opportunities
        """
        all_opportunities = []
        
        for university, url in self.IVY_LEAGUE_URLS.items():
            opportunities = self.scrape_university(university, url)
            all_opportunities.extend(opportunities)
        
        logger.info(f"Total opportunities scraped: {len(all_opportunities)}")
        return all_opportunities
    
    def detect_changes(self, existing_opportunities: List[Dict], new_opportunities: List[Dict]) -> List[Dict]:
        """
        Detect new opportunities by comparing with existing ones.
        
        Args:
            existing_opportunities: List of existing opportunities
            new_opportunities: List of newly scraped opportunities
            
        Returns:
            List of new opportunities
        """
        existing_titles = {opp['title'] for opp in existing_opportunities}
        new_opps = [opp for opp in new_opportunities if opp['title'] not in existing_titles]
        
        logger.info(f"Found {len(new_opps)} new opportunities")
        return new_opps
