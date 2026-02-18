# 🚀 Quick Start Guide

## Start the Application (3 Simple Steps)

### Method 1: Using the startup script
```bash
./start.sh
```

### Method 2: Manual start
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the application
python run.py
```

### Method 3: Direct Python command
```bash
/Users/ankityadav/lpu/project3/.venv/bin/python run.py
```

## Access the Application

Open your browser and go to: **http://localhost:5000**

## First Steps

1. **Register** a new account at http://localhost:5000/register
   - Choose your domain (AI, Engineering, Law, etc.)
   
2. **Login** with your credentials

3. **Update Profile** - Go to Profile and add:
   - Your skills and interests
   - Your achievements (hackathons, internships, etc.)
   - This calculates your InCoScore

4. **Scrape Opportunities** - Click "Scrape New Opportunities" on dashboard
   - This fetches opportunities from Ivy League universities
   
5. **Browse & Apply** - View opportunities matching your domain
   - Click "Apply Now" for one-click submission
   
6. **Join Community** - Create posts, comment, and like
   
7. **Check Leaderboard** - See your ranking among students

## Testing the System

### Test Scenario 1: Student Registration & Profile
- Register as "John Doe" with domain "Artificial Intelligence"
- Add 5 hackathons, 2 internships, 800 coding score
- Check InCoScore calculation

### Test Scenario 2: Opportunity Discovery
- Click "Scrape New Opportunities"
- View opportunities filtered by your domain
- Apply to 2-3 opportunities

### Test Scenario 3: Community Engagement
- Create a post about your recent achievement
- Like and comment on other posts
- Check engagement metrics

### Test Scenario 4: Ranking System
- Go to Leaderboard
- Filter by domain
- Compare your InCoScore with others

## Stopping the Application

Press `Ctrl + C` in the terminal where the app is running.

## Need Help?

- Check the full README.md for detailed documentation
- Review the code comments for understanding
- All routes and functions have docstrings explaining their purpose
