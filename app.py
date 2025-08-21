from flask import Flask, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, Post, Comment
from forms import SignupForm, LoginForm, PostForm, CommentForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
#jwt = JWTManager(app)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirect users to 'login' if not logged in
login_manager.login_message_category = 'info'

# --- User loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Tell JWT to read token from cookies
"""app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # True if using HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # optional for now

migrate = Migrate(app, db)"""

@app.route('/')
def home():
    return redirect(url_for('posts'))

# Signup
@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('posts'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts'))
        else:
            flash('Login failed. Check email and password.', 'error')
    return render_template('login.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# View all posts
@app.route('/posts')
def posts():
    posts = Post.query.all()
    comment_form = CommentForm()
    return render_template('posts.html', posts=posts, comment_form=comment_form)

# Create post
@app.route('/posts/create', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts'))
    return render_template('create_post.html', form=form)

# Edit post
@app.route('/posts/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        flash('You are not authorized!', 'error')
        return redirect(url_for('posts'))
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts'))
    return render_template('create_post.html', form=form)

# Delete post
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        flash('You are not authorized!', 'error')
        return redirect(url_for('posts'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts'))

# Add comment
@app.route('/posts/<int:post_id>/comment', methods=['POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
    else:
        flash('Comment cannot be empty.', 'error')
    return redirect(url_for('posts'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if not exist
    app.run(debug=True)