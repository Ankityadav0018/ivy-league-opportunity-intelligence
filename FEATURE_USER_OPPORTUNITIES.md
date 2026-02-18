# 🎯 User-Generated Opportunities Feature

## Overview
This feature allows users to create, manage, and share their own opportunities (hackathons, internships, jobs, etc.) with the community.

## Features Implemented

### 1. Create Opportunities ✅
- **Route:** `/opportunities/create`
- **Access:** All logged-in users
- **Features:**
  - Create hackathons, internships, jobs, research positions, scholarships, etc.
  - Categorize by domain (AI, Engineering, Law, etc.)
  - Add deadline, location, requirements, and external URL
  - Automatic tracking of creator

### 2. View My Opportunities ✅
- **Route:** `/opportunities/my-opportunities`
- **Access:** Creator only
- **Features:**
  - List all opportunities created by the user
  - See application count for each opportunity
  - Quick access to edit, deactivate, or delete
  - Visual indication of active/inactive status

### 3. Edit Opportunities ✅
- **Route:** `/opportunities/<id>/edit`
- **Access:** Creator only
- **Features:**
  - Update title, description, category, domain
  - Modify deadline, location, requirements
  - Change company/organization name
  - Update external URL

### 4. Delete Opportunities ✅
- **Route:** `/opportunities/<id>/delete`
- **Access:** Creator only
- **Features:**
  - Permanent deletion of opportunity
  - Confirmation dialog to prevent accidental deletion
  - Cascading delete of related applications

### 5. Toggle Active/Inactive Status ✅
- **Route:** `/opportunities/<id>/toggle-status`
- **Access:** Creator only
- **Features:**
  - Activate or deactivate opportunities
  - Inactive opportunities won't show in main feeds
  - Easy toggle button

## Database Changes

### New Field Added to Opportunity Model:
```python
created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
```

This field:
- Tracks which user created the opportunity
- Allows filtering opportunities by creator
- Enables permission checks (only creator can edit/delete)

## User Interface

### Navigation Menu
- Added "Create Opportunity" link in main navigation
- Always accessible for logged-in users

### Dashboard
- Added "My Created Opportunities" button
- Orange colored for easy identification

### Create Form
Fields:
- Title* (required)
- Category* (Hackathon, Internship, Job, etc.)
- Domain* (AI, Engineering, Law, etc.)
- Description* (required)
- Requirements
- Company/Organization
- Location
- Deadline
- External URL

### My Opportunities Page
Displays:
- All opportunities created by the user
- Active/Inactive status badges
- Category and domain tags
- Application count
- Action buttons (View, Edit, Activate/Deactivate, Delete)
- Creation date

### Edit Page
- Pre-filled form with current values
- Same fields as create form
- Save or cancel options

## Security & Permissions

### Access Control:
1. **Create:** Any logged-in user ✅
2. **Edit:** Only the creator ✅
3. **Delete:** Only the creator ✅
4. **Toggle Status:** Only the creator ✅

### Validation:
- Title, description, domain, and category are required
- Deadline must be in YYYY-MM-DD format
- Creator ID automatically set to current user
- Unauthorized access redirects with error message

## Use Cases

### Scenario 1: Student Organizing a Hackathon
1. Click "Create Opportunity" in navigation
2. Fill in hackathon details (title, description, deadline)
3. Select category "Hackathon" and domain "Computer Science"
4. Add location and external registration URL
5. Submit - opportunity is now visible to all users

### Scenario 2: Company Posting an Internship
1. Navigate to "Create Opportunity"
2. Select category "Internship" and domain
3. Add detailed requirements and company name
4. Set application deadline
5. Monitor applications from "My Created Opportunities"

### Scenario 3: Managing Posted Opportunities
1. Go to "My Created Opportunities"
2. View all posted opportunities
3. Edit to update deadline or requirements
4. Deactivate if position is filled
5. Delete if no longer relevant

## Code Structure

### Routes (`app/routes/opportunities.py`):
- `create_opportunity()` - Create new opportunity
- `my_opportunities()` - List user's opportunities
- `edit_opportunity(id)` - Edit existing opportunity
- `delete_opportunity(id)` - Delete opportunity
- `toggle_opportunity_status(id)` - Activate/deactivate

### Models (`app/models/opportunity.py`):
- Added `created_by` field
- Added `creator` relationship to User model

### Templates:
- `create_opportunity.html` - Creation form
- `my_opportunities.html` - List of user opportunities
- `edit_opportunity.html` - Edit form

## Benefits

### For Students:
- Share opportunities they discover
- Help peers find relevant positions
- Build a collaborative community
- Track who applies to their posted opportunities

### For Recruiters/Organizations:
- Post job openings and internships
- Reach targeted audience by domain
- Track applications
- Manage multiple postings easily

### For the Platform:
- User-generated content increases engagement
- More diverse opportunity sources
- Community-driven growth
- Reduces dependency on web scraping

## Type Hints & Code Quality

Following PEP 8 and best practices:
```python
def create_opportunity() -> Response:
    """
    Allow users to create their own opportunities.
    
    Returns:
        Rendered template for GET or redirect for POST.
    """
    if request.method == 'POST':
        title: str = request.form.get('title', '').strip()
        # Type hints for all variables
        ...
```

## Error Handling

- Try-catch blocks for database operations
- Rollback on failure
- User-friendly error messages
- Permission validation
- Input sanitization (strip whitespace)

## Future Enhancements

Potential improvements:
- [ ] Email notifications when someone applies
- [ ] Analytics dashboard (views, applications)
- [ ] Featured/promoted opportunities
- [ ] Duplicate detection
- [ ] Bulk upload via CSV
- [ ] Share to social media
- [ ] Save as draft
- [ ] Application management (accept/reject)
- [ ] Expiry notifications before deadline

## Testing the Feature

### Test Steps:
1. **Create Test:**
   - Login to the application
   - Click "Create Opportunity"
   - Fill in all required fields
   - Submit and verify success message

2. **List Test:**
   - Navigate to "My Created Opportunities"
   - Verify your opportunity appears
   - Check all information is displayed correctly

3. **Edit Test:**
   - Click "Edit" on an opportunity
   - Modify some fields
   - Save and verify changes

4. **Toggle Test:**
   - Click "Deactivate" on an opportunity
   - Verify it's marked as inactive
   - Click "Activate" to reactivate

5. **Delete Test:**
   - Click "Delete" on an opportunity
   - Confirm deletion
   - Verify it's removed from the list

6. **Permission Test:**
   - Login as different user
   - Try to edit another user's opportunity
   - Verify access is denied

## Integration with Existing Features

### Applications:
- Students can apply to user-generated opportunities
- Same application tracking system
- Same auto-application feature

### Dashboard:
- User-generated opportunities appear alongside scraped ones
- Filtered by domain for personalization
- Same viewing and application interface

### Community:
- Users can post about their opportunities in community
- Link from community posts to opportunities
- Increase visibility

## Summary

✅ **Fully functional feature with:**
- Complete CRUD operations
- Security and permissions
- Clean UI/UX
- Type hints and documentation
- Error handling
- Database integration
- Seamless integration with existing features

The feature is now **live and ready to use** at http://localhost:5001! 🚀
