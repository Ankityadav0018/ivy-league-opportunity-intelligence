# 🎓 Ivy League Opportunity Intelligence System

**LPU Project 3 - Python & Full Stack Development**

A platform that helps students discover opportunities from Ivy League universities. Features include automated web scraping, domain classification, application tracking, and a student ranking system based on achievements.

---

## About

This project solves a common problem - students miss out on great opportunities from top universities because there's no centralized place to find them. This system:

- Scrapes Ivy League university websites for opportunities
- Categorizes them by field (AI, Engineering, Law, etc.)
- Lets students apply with one click
- Ranks students based on achievements (InCoScore)
- Provides a social platform for academic networking

---

## Features

**For Students:**
- Personalized dashboard with relevant opportunities
- One-click applications using your profile
- Track all your applications in one place
- Share achievements and connect with peers
- See where you rank among other students

**System Capabilities:**
- Monitors 8 Ivy League universities automatically
- Smart classification using keywords and text analysis
- Community features (posts, comments, likes)
- Achievement-based ranking algorithm

---

## Tech Stack

- **Backend:** Flask, SQLAlchemy, SQLite
- **Scraping:** BeautifulSoup4, Requests
- **Classification:** NLTK, scikit-learn, TF-IDF
- **Frontend:** Jinja2 templates, custom CSS
- **Auth:** Flask-Login

---

## Installation

```bash
# Clone the repo
cd project3

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

Visit `http://localhost:5000` to get started.

---

## Quick Start

1. Register an account and pick your domain
2. Update your profile with skills and achievements
3. Click "Scrape New Opportunities" to fetch latest postings
4. Browse and apply to opportunities
5. Join the community and create posts
6. Check the leaderboard to see your ranking

---

## Project Structure

```
app/
├── models/          # Database models (User, Opportunity, Post, etc.)
├── routes/          # URL routes and views
├── services/        # Scraper, classifier, ranking logic
├── templates/       # HTML templates
└── static/          # CSS and JavaScript

data/                # Storage for scraped data
instance/            # SQLite database
```

---

## How It Works

**Web Scraping:**
The scraper checks university websites for new events, workshops, hackathons, and research opportunities. It extracts titles, descriptions, and URLs.

**Classification:**
Uses keyword matching to categorize opportunities into domains like AI, Engineering, Medicine, etc. Also identifies the type (workshop, hackathon, scholarship, etc.).

**InCoScore Algorithm:**
```
InCoScore = (Hackathons × 10) + (Internships × 15) + (Research Papers × 20) + 
            (Coding Score × 0.5) + (Competition Wins × 12)
```

This score helps rank students based on their achievements. Research papers get the highest weight since they show deep expertise.

**Auto-Application:**
Instead of filling forms repeatedly, students can apply with one click using their saved profile information.

---

## Main Routes

- `/` - Home page
- `/register` - Sign up
- `/login` - Login
- `/opportunities/dashboard` - Your personalized dashboard
- `/opportunities/all` - Browse all opportunities
- `/community/` - Social feed
- `/ranking/leaderboard` - Student rankings
- `/profile` - View and edit your profile

---

## Database Models

**User:** Student accounts with domain, skills, and achievement metrics  
**Opportunity:** Scraped opportunities with classification  
**Application:** Tracks which students applied to what  
**Post/Comment/Like:** Community features  

All relationships are properly set up using SQLAlchemy ORM.

---

## Future Ideas

- Email notifications for new opportunities
- Resume parsing and auto-fill
- Real-time chat between students
- Mobile app version
- Integration with LinkedIn
- Better ML models for classification

---

## Development

This was built as part of LPU's Python & Full Stack Development course. The goal was to create a practical system that combines web scraping, database design, AI classification, and social networking.

Key learning areas:
- Flask application architecture
- Database design and relationships
- Web scraping techniques
- Text classification
- User authentication
- Building social features

---

## Notes

- The scraper respects rate limits and has timeouts
- Passwords are hashed, never stored in plain text
- SQLAlchemy prevents SQL injection
- The app runs in debug mode for development

---

## Author

Ankit Yadav  
Lovely Professional University

---

**Last Updated:** February 2026  
**Status:** Working and tested
