"""
Community Routes - Module 5
Academic Social Network with Posts, Comments, Likes, Groups
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.community import Post, Comment, Like, Group

bp = Blueprint('community', __name__, url_prefix='/community')


@bp.route('/')
@login_required
def index():
    """Community home page with all posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts)


@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new post."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        domain = request.form.get('domain', current_user.domain)
        
        post = Post(
            user_id=current_user.id,
            title=title,
            content=content,
            domain=domain
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('community.index'))
    
    return render_template('create_post.html')


@bp.route('/post/<int:id>')
@login_required
def view_post(id):
    """View a single post with comments."""
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post)


@bp.route('/post/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    """Add a comment to a post."""
    post = Post.query.get_or_404(id)
    content = request.form.get('content')
    
    if content:
        comment = Comment(
            post_id=id,
            user_id=current_user.id,
            content=content
        )
        
        post.comments_count += 1
        
        db.session.add(comment)
        db.session.commit()
        
        flash('Comment added!', 'success')
    
    return redirect(url_for('community.view_post', id=id))


@bp.route('/post/<int:id>/like', methods=['POST'])
@login_required
def like_post(id):
    """Like or unlike a post."""
    post = Post.query.get_or_404(id)
    
    # Check if already liked
    existing_like = Like.query.filter_by(
        post_id=id,
        user_id=current_user.id
    ).first()
    
    if existing_like:
        # Unlike
        db.session.delete(existing_like)
        post.likes_count -= 1
        message = 'Post unliked'
    else:
        # Like
        like = Like(
            post_id=id,
            user_id=current_user.id
        )
        db.session.add(like)
        post.likes_count += 1
        message = 'Post liked!'
    
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'likes': post.likes_count})
    
    flash(message, 'success')
    return redirect(url_for('community.view_post', id=id))


@bp.route('/groups')
@login_required
def groups():
    """View all domain groups."""
    all_groups = Group.query.all()
    return render_template('groups.html', groups=all_groups)


@bp.route('/domain/<domain>')
@login_required
def domain_posts(domain):
    """View posts from a specific domain."""
    posts = Post.query.filter_by(domain=domain).order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts, domain=domain)
