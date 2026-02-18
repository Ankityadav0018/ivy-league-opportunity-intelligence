# 📖 Project Explanation - Line by Line

## Architecture Overview

This project follows the **MVC (Model-View-Controller)** pattern:
- **Models** (`app/models/`) - Database structure
- **Views** (`app/templates/`) - User interface
- **Controllers** (`app/routes/`) - Business logic

---

## Module 1: Web Scraping (`app/services/scraper.py`)

### How It Works:
```python
class OpportunityScraper:
    IVY_LEAGUE_URLS = {...}  # Dictionary of university URLs
```

**Explanation:**
- Stores URLs of 8 Ivy League universities (Harvard, MIT, Yale, etc.)
- Each URL points to the events/opportunities page

**Scraping Process:**
1. Send HTTP request to university website
2. Parse HTML using BeautifulSoup
3. Find event/opportunity elements using CSS selectors
4. Extract title, description, and links
5. Store in a standardized format

**Key Functions:**
- `scrape_university()` - Scrapes one university
- `scrape_all_universities()` - Scrapes all 8 universities
- `detect_changes()` - Compares new vs existing opportunities

---

## Module 2: AI Classification (`app/services/classifier.py`)

### Domain Classification Algorithm:

```python
def classify_by_keywords(self, text: str) -> str:
    # 1. Convert text to lowercase
    # 2. Loop through each domain's keywords
    # 3. Count how many keywords match
    # 4. Return domain with highest match count
```

**Example:**
```
Text: "Machine Learning Workshop on Neural Networks"
Keywords matched:
- AI domain: "machine learning" (1), "neural network" (1) = Score: 2
- Physics: 0
- Law: 0
Result: Classified as "Artificial Intelligence"
```

**Category Detection:**
- Checks for words like "workshop", "hackathon", "research"
- Returns appropriate category (Workshop, Hackathon, etc.)

---

## Module 3: User Profile (`app/models/user.py`)

### Database Schema:
```python
class User:
    id - Unique identifier
    username - Login username
    email - Email address
    password_hash - Encrypted password (NEVER stored in plain text)
    domain - Student's field (AI, Law, etc.)
    skills - Comma-separated skills
    
    # InCoScore parameters
    hackathons_count - Number of hackathons
    internships_count - Number of internships
    research_papers_count - Papers published
    coding_score - Programming proficiency (0-1000)
    competition_wins - Competitions won
    incoscore - Calculated competency score
```

**Password Security:**
```python
def set_password(self, password):
    # Uses Werkzeug to hash password with salt
    self.password_hash = generate_password_hash(password)
```
- Never stores plain text passwords
- Uses secure hashing algorithm (pbkdf2:sha256)

---

## Module 4: Auto-Application (`app/routes/opportunities.py`)

### Application Process:
```python
@bp.route('/<int:id>/apply', methods=['POST'])
def apply_opportunity(id):
    # 1. Get opportunity details
    # 2. Check if already applied
    # 3. Create application record
    # 4. Set status as 'submitted'
    # 5. Save to database
```

**Why It's "Auto":**
- Uses pre-filled profile information
- One-click submission
- No need to fill forms repeatedly
- Tracks application status automatically

---

## Module 5: Community Platform (`app/routes/community.py`)

### Social Network Features:

**Posts:**
```python
class Post:
    title - Post title
    content - Post body
    user_id - Who created it (foreign key)
    domain - Related field
    likes_count - Number of likes
    comments_count - Number of comments
```

**Comments:**
```python
class Comment:
    post_id - Which post (foreign key)
    user_id - Who commented (foreign key)
    content - Comment text
```

**Likes:**
```python
class Like:
    post_id - Which post
    user_id - Who liked it
    # Unique constraint: Can't like same post twice
```

**Database Relationships:**
- One user → Many posts (one-to-many)
- One post → Many comments (one-to-many)
- One post → Many likes (one-to-many)

---

## Module 6: InCoScore Ranking (`app/services/ranking.py`)

### Calculation Formula:

```python
InCoScore = (hackathons × 10) + 
            (internships × 15) + 
            (research_papers × 20) + 
            (coding_score × 0.5) + 
            (competition_wins × 12)
```

**Why These Weights?**
- Research papers (20) - Highest value, shows deep expertise
- Internships (15) - Professional experience
- Competition wins (12) - Demonstrates skill
- Hackathons (10) - Practical experience
- Coding score (0.5) - Normalized from 0-1000 scale

**Leaderboard Generation:**
```python
def get_leaderboard(domain=None, limit=10):
    # 1. Query users from database
    # 2. Filter by domain (if specified)
    # 3. Sort by InCoScore (descending)
    # 4. Take top N users
    # 5. Return as ranked list
```

---

## Database Design

### Relationships:
```
User (1) -----> (Many) Posts
User (1) -----> (Many) Comments
User (1) -----> (Many) Applications

Post (1) -----> (Many) Comments
Post (1) -----> (Many) Likes

Opportunity (1) -----> (Many) Applications
```

**SQLAlchemy ORM Benefits:**
- Automatic SQL generation
- Protection against SQL injection
- Easy relationship management
- Database migration support

---

## Flask Application Structure

### Application Factory Pattern (`app/__init__.py`):
```python
def create_app():
    app = Flask(__name__)
    # 1. Configure app settings
    # 2. Initialize database
    # 3. Setup authentication
    # 4. Register blueprints (routes)
    # 5. Create database tables
    return app
```

**Blueprints:**
- `auth` - Login, register, profile
- `opportunities` - Browse, apply, scrape
- `community` - Posts, comments, likes
- `ranking` - Leaderboard, rankings

---

## Security Implementations

### 1. Password Hashing:
```python
generate_password_hash(password)
# Creates: pbkdf2:sha256:260000$salt$hash
```

### 2. Login Protection:
```python
@login_required
def dashboard():
    # Only accessible if logged in
```

### 3. SQL Injection Prevention:
```python
User.query.filter_by(username=username)
# SQLAlchemy escapes all inputs
```

### 4. Session Management:
- Flask-Login handles secure sessions
- CSRF protection built-in

---

## How Data Flows Through the System

### Example: Applying to an Opportunity

1. **User clicks "Apply Now"**
   - Browser sends POST request to `/opportunities/<id>/apply`

2. **Route Handler (`opportunities.py`)**
   - Verifies user is logged in
   - Gets opportunity from database
   - Checks if already applied

3. **Create Application Record**
   - Creates Application object
   - Links to user and opportunity
   - Sets status to 'submitted'

4. **Save to Database**
   - SQLAlchemy generates SQL
   - Executes INSERT query
   - Commits transaction

5. **Response**
   - Flash success message
   - Redirect to applications page

6. **Template Renders**
   - Jinja2 processes HTML
   - Shows updated application list

---

## API Request Flow

```
Browser → Flask Route → Service Layer → Database
   ↓                                        ↓
Response ← Template ← Data ← Query Results
```

---

## File Organization Logic

```
app/
├── __init__.py          # App creation
├── models/              # Database structure
│   ├── user.py         # User/Student data
│   ├── opportunity.py  # Opportunities & applications
│   └── community.py    # Social features
├── routes/              # URL handlers (controllers)
│   ├── auth.py         # Login/register
│   ├── opportunities.py # Opportunity management
│   ├── community.py    # Social network
│   └── ranking.py      # Leaderboards
├── services/            # Business logic
│   ├── scraper.py      # Web scraping
│   ├── classifier.py   # AI classification
│   └── ranking.py      # Score calculation
└── templates/           # HTML pages
```

**Separation of Concerns:**
- Models = Data structure
- Services = Business logic
- Routes = Request handling
- Templates = Presentation

---

## Key Python Concepts Used

### 1. Object-Oriented Programming:
```python
class User(UserMixin, db.Model):
    # Inheritance from UserMixin and db.Model
```

### 2. Decorators:
```python
@bp.route('/login')
@login_required
# Modifies function behavior
```

### 3. List Comprehensions:
```python
domains = [d[0] for d in domains if d[0]]
# Concise list creation
```

### 4. Context Managers:
```python
with app.app_context():
    db.create_all()
# Automatic resource management
```

### 5. Type Hints:
```python
def calculate_score(user: User) -> float:
# Specifies expected types
```

---

## Testing Strategy

### Manual Testing Checklist:
- [ ] User can register
- [ ] User can login
- [ ] Profile updates work
- [ ] InCoScore calculates correctly
- [ ] Scraping fetches opportunities
- [ ] Opportunities are classified
- [ ] Applications are tracked
- [ ] Posts can be created
- [ ] Comments work
- [ ] Likes toggle correctly
- [ ] Leaderboard shows rankings

---

## Common Issues & Solutions

### Issue 1: Database not found
**Solution:** Run `python run.py` to create tables

### Issue 2: Module not found
**Solution:** Activate virtual environment: `source .venv/bin/activate`

### Issue 3: Port already in use
**Solution:** Change port in run.py or kill existing process

### Issue 4: Template not found
**Solution:** Check templates/ folder structure

---

## Performance Considerations

1. **Database Queries:**
   - Uses indexes on foreign keys
   - Lazy loading for relationships
   - Pagination for large lists

2. **Scraping:**
   - Timeout limits (10 seconds)
   - Error handling for failed requests
   - Limits results per university

3. **Caching:**
   - Static files cached by browser
   - Database connection pooling

---

## Extending the Project

### Add Email Notifications:
1. Install: `pip install flask-mail`
2. Configure SMTP settings
3. Send email on new opportunities

### Add Real-time Updates:
1. Install: `pip install flask-socketio`
2. Implement WebSocket connections
3. Push live updates to clients

### Add API:
1. Create `/api/` blueprint
2. Return JSON responses
3. Add authentication tokens

---

This explanation covers all major aspects of the project implementation!
