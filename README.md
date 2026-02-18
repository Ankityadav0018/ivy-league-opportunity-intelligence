# 🎓 Real-Time Ivy League Opportunity Intelligence & Student Competency Network

**LPU Project 3: Python and Full Stack Development**

A comprehensive AI-driven platform that monitors Ivy League universities for opportunities (workshops, hackathons, research internships, scholarships, conferences), classifies them by domain, enables auto-application, and provides an academic social network with intelligent student ranking (InCoScore).

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [System Modules](#system-modules)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Screenshots & Usage](#screenshots--usage)
- [InCoScore Algorithm](#incoscore-algorithm)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Problem Statement

Students often miss high-quality opportunities from top universities due to:
1. No centralized real-time platform for Ivy League opportunities
2. Manual searching consumes time
3. Students receive irrelevant information
4. No smart ranking of student competency
5. No auto-application assistance
6. Limited academic networking platforms

---

## 🏗️ System Modules

### Module 1: Real-Time Opportunity Extraction
- **Function**: Monitors Ivy League university websites and detects updates automatically
- **Techniques**: Web scraping, API monitoring, change detection
- **Implementation**: `app/services/scraper.py`

### Module 2: AI-Based Domain Classification
- **Function**: Analyzes opportunity text and categorizes into domains (AI, Law, Engineering, etc.)
- **Techniques**: NLP, Machine Learning classifiers, keyword matching
- **Implementation**: `app/services/classifier.py`

### Module 3: Student Profile & Personalization
- **Function**: Stores skills, interests, academic background, and resume
- **Outcome**: Personalized opportunity feed matching student's domain
- **Implementation**: `app/models/user.py`

### Module 4: Auto-Application System
- **Features**: Form detection, resume upload, auto-fill, submission confirmation
- **Implementation**: `app/routes/opportunities.py`

### Module 5: Academic Community Platform
- **Includes**: Posts, comments, likes, domain-based groups, chat system
- **Implementation**: `app/routes/community.py`, `app/models/community.py`

### Module 6: InCoScore Ranking Engine
- **Parameters**: Hackathons, internships, research papers, coding performance, competition results
- **Output**: Student leaderboard and smart shortlisting
- **Implementation**: `app/services/ranking.py`

---

## ✨ Features

### For Students
- ✅ **Personalized Dashboard** - View opportunities matching your domain
- ✅ **Real-time Updates** - Get latest opportunities from Ivy League universities
- ✅ **One-Click Applications** - Auto-apply using your profile information
- ✅ **Social Network** - Share achievements, interact with peers
- ✅ **InCoScore Tracking** - Monitor your competency ranking
- ✅ **Domain Filtering** - Filter opportunities and posts by field of interest

### For the Platform
- ✅ **Automated Scraping** - Continuous monitoring of university websites
- ✅ **Smart Classification** - AI categorizes opportunities automatically
- ✅ **Application Tracking** - Monitor all submitted applications
- ✅ **Leaderboard System** - Rank students based on achievements
- ✅ **Community Engagement** - Likes, comments, and interaction tracking

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy (SQLite)
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

### AI & Machine Learning
- **NLP**: NLTK, scikit-learn
- **Classification**: TF-IDF Vectorizer, Naive Bayes
- **Data Processing**: Pandas, NumPy

### Web Scraping
- **Libraries**: BeautifulSoup4, Requests
- **Monitoring**: Change detection algorithms

### Frontend
- **Templates**: Jinja2
- **Styling**: Custom CSS (embedded in base.html)
- **Responsive Design**: Mobile-friendly layout

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/ankityadav/lpu/project3
   ```

2. **Create a virtual environment (if not already created)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize the database**
   ```bash
   python run.py
   ```
   This will automatically create the database tables.

---

## 🚀 Running the Application

### Start the Flask Server
```bash
python run.py
```

The application will be available at: **http://localhost:5000**

### Default Access
- **Home Page**: http://localhost:5000/
- **Register**: http://localhost:5000/register
- **Login**: http://localhost:5000/login

### First-Time Setup
1. Register a new student account
2. Complete your profile with domain and skills
3. Add achievements to calculate your InCoScore
4. Click "Scrape New Opportunities" to fetch opportunities
5. Browse personalized opportunities and apply
6. Join the community and create posts

---

## 📁 Project Structure

```
project3/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── user.py              # User/Student model with InCoScore
│   │   ├── opportunity.py       # Opportunity and Application models
│   │   └── community.py         # Post, Comment, Like, Group models
│   ├── routes/
│   │   ├── auth.py              # Authentication routes
│   │   ├── opportunities.py     # Opportunity viewing and application
│   │   ├── community.py         # Social network features
│   │   └── ranking.py           # Leaderboard and ranking
│   ├── services/
│   │   ├── scraper.py           # Web scraping module
│   │   ├── classifier.py        # AI domain classification
│   │   └── ranking.py           # InCoScore calculation engine
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── opportunities.html
│   │   ├── opportunity_detail.html
│   │   ├── my_applications.html
│   │   ├── profile.html
│   │   ├── community.html
│   │   ├── create_post.html
│   │   ├── post_detail.html
│   │   └── leaderboard.html
│   └── static/
│       ├── css/
│       └── js/
├── data/                        # Data storage directories
│   ├── opportunities/
│   └── students/
├── run.py                       # Main application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .env.example                 # Environment configuration example
└── LPU_Project_3.pdf           # Project requirements document
```

---

## 🔍 How It Works

### 1. Web Scraping & Opportunity Extraction
```python
from app.services.scraper import OpportunityScraper

scraper = OpportunityScraper()
opportunities = scraper.scrape_all_universities()
```
- Monitors 8 Ivy League universities
- Extracts title, description, URL, and metadata
- Detects new opportunities using change detection

### 2. AI-Based Classification
```python
from app.services.classifier import DomainClassifier

classifier = DomainClassifier()
domain = classifier.classify_opportunity(title, description)
category = classifier.categorize_type(title, description)
```
- Uses keyword matching and NLP
- Classifies into 10+ domains
- Categorizes as Workshop, Hackathon, Research, etc.

### 3. InCoScore Calculation
```python
InCoScore = (Hackathons × 10) + 
            (Internships × 15) + 
            (Research Papers × 20) + 
            (Coding Score × 0.5) + 
            (Competition Wins × 12)
```
- Weighted formula based on achievements
- Automatically recalculated on profile update
- Used for leaderboard ranking

### 4. Auto-Application System
- One-click application submission
- Uses stored profile data
- Tracks application status (pending, submitted, accepted, rejected)

### 5. Community Features
- Create posts about achievements
- Comment on others' posts
- Like/unlike posts
- Domain-based filtering

---

## 📸 Screenshots & Usage

### Registration & Profile Setup
1. Navigate to http://localhost:5000/register
2. Fill in your details and select your domain
3. After login, go to Profile and add achievements
4. Your InCoScore will be calculated automatically

### Finding Opportunities
1. Click "Scrape New Opportunities" on dashboard
2. Browse personalized opportunities matching your domain
3. Click on any opportunity to view details
4. Click "Apply Now" for one-click submission

### Community Engagement
1. Navigate to Community section
2. Create posts about your achievements
3. Like and comment on others' posts
4. View domain-specific posts

### Checking Rankings
1. Go to Leaderboard
2. Filter by domain
3. View top students and their InCoScores
4. Compare your ranking

---

## 🏆 InCoScore Algorithm

The **Intelligent Competency Score (InCoScore)** is calculated using a weighted formula:

### Parameters and Weights
| Parameter | Weight | Description |
|-----------|--------|-------------|
| Hackathons | 10 | Number of hackathons participated |
| Internships | 15 | Number of internships completed |
| Research Papers | 20 | Number of research papers published |
| Coding Score | 0.5 | Coding proficiency (0-1000) |
| Competition Wins | 12 | Number of competitions won |

### Example Calculation
```
Student Profile:
- Hackathons: 5
- Internships: 2
- Research Papers: 1
- Coding Score: 800
- Competition Wins: 3

InCoScore = (5 × 10) + (2 × 15) + (1 × 20) + (800 × 0.5) + (3 × 12)
          = 50 + 30 + 20 + 400 + 36
          = 536
```

---

## 🔌 API Endpoints

### Authentication
- `GET /` - Home page
- `GET /register` - Registration form
- `POST /register` - Create new account
- `GET /login` - Login form
- `POST /login` - Authenticate user
- `GET /logout` - Logout user

### Opportunities
- `GET /opportunities/dashboard` - Personalized dashboard
- `GET /opportunities/all` - All opportunities
- `GET /opportunities/scrape` - Trigger scraping
- `GET /opportunities/<id>` - View opportunity details
- `POST /opportunities/<id>/apply` - Apply to opportunity
- `GET /opportunities/my-applications` - View applications

### Community
- `GET /community/` - Community feed
- `GET /community/post/create` - Create post form
- `POST /community/post/create` - Submit new post
- `GET /community/post/<id>` - View post details
- `POST /community/post/<id>/comment` - Add comment
- `POST /community/post/<id>/like` - Like/unlike post

### Ranking
- `GET /ranking/leaderboard` - View leaderboard
- `GET /ranking/api/top-students/<domain>` - API for top students
- `GET /ranking/calculate-score` - Recalculate all scores

### Profile
- `GET /profile` - View profile
- `POST /profile/update` - Update profile and achievements

---

## 🧪 Testing the Application

### Manual Testing Steps
1. **User Registration**: Create multiple test accounts with different domains
2. **Scraping Test**: Click scrape button and verify opportunities are fetched
3. **Classification Test**: Check if opportunities are correctly categorized
4. **Application Test**: Apply to opportunities and verify tracking
5. **Community Test**: Create posts, add comments, like posts
6. **Ranking Test**: Update achievements and verify InCoScore calculation
7. **Leaderboard Test**: Check ranking order and domain filtering

---

## 🐛 Debugging in VS Code

### Setup Debug Configuration
1. Open Run and Debug panel (Ctrl+Shift+D / Cmd+Shift+D)
2. Click "create a launch.json file"
3. Select "Python" → "Flask"
4. Update the configuration if needed
5. Press F5 to start debugging

### Quick Debug
```bash
python run.py
```
The application runs in debug mode by default with auto-reload enabled.

---

## �� Code Quality

This project follows Python best practices:
- ✅ **PEP 8** style guidelines
- ✅ **Type hints** for function parameters
- ✅ **Docstrings** for all functions and classes
- ✅ **Clear variable names** and code structure
- ✅ **Error handling** patterns
- ✅ **Modular architecture** (MVC pattern)
- ✅ **Database relationships** properly defined
- ✅ **Security** - Password hashing, SQL injection prevention

---

## 🎓 Learning Outcomes

By completing this project, you will have learned:
1. Full-stack web development with Flask
2. Database design and ORM (SQLAlchemy)
3. Web scraping techniques
4. AI/ML classification using scikit-learn
5. User authentication and authorization
6. RESTful API design
7. Social network features implementation
8. Algorithm design (InCoScore)
9. Project structure and organization
10. Version control with Git

---

## 📚 Future Enhancements

Potential improvements for the system:
- [ ] Email notifications for new opportunities
- [ ] Real-time chat system using WebSockets
- [ ] Advanced ML models for better classification
- [ ] Resume parsing and auto-fill
- [ ] Mobile app (React Native/Flutter)
- [ ] Integration with LinkedIn
- [ ] Recommendation engine for students
- [ ] Analytics dashboard
- [ ] Export opportunities to calendar
- [ ] Multi-language support

---

## 🤝 Contributing

This is an academic project. For any improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is created for **LPU Project 3** academic purposes.

---

## 👨‍💻 Author

**Ankit Yadav**  
Lovely Professional University  
Course: Python and Full Stack Development  
Project: Real-Time Ivy League Opportunity Intelligence System

---

## 📞 Contact & Support

For queries or guidance:
- Refer to the project documentation
- Check the code comments
- Review the PDF requirements (LPU_Project_3.pdf)

---

## 🎉 Acknowledgments

- Flask Framework Documentation
- SQLAlchemy Documentation
- BeautifulSoup4 Documentation
- scikit-learn Documentation
- Lovely Professional University

---

**Last Updated**: February 17, 2026  
**Version**: 1.0.0  
**Status**: ✅ Fully Functional

---

*This project demonstrates the integration of web scraping, AI classification, social networking, and intelligent ranking systems in a comprehensive full-stack Python application.*
