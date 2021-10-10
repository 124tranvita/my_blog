# users/views.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from myblog import db
from myblog.users.forms import LoginForm, RegisterForm, UpdateForm,ChangePasswordForm
from myblog.models import Post, User
from myblog.users.pics_handler import process_upload_image

# Create blueprint for users
users_blueprint = Blueprint('users', __name__)

# Register view
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()

    if form.validate_on_submit():

        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully!')

        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)

# Login view
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash(f'"{user.username}" has logged in!')
        next = request.args.get('next')

        if next is None or not next.startswith('/'):

            next = url_for('core.index')

        return redirect(next)

    return render_template('users/login.html', form=form)        

# Logout view
@users_blueprint.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('core.index'))

# Update view
@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateForm()

    if form.validate_on_submit():

        if form.profile_image.data:

            upload_image = form.profile_image.data
            username = current_user.username
            processed_image = process_upload_image(upload_image=upload_image, username=username)
            current_user.profile_image = processed_image

        current_user.username = form.username.data
        current_user.description = form.description.data
        db.session.commit()
        flash('Account was updated!')

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
 
        form.username.data = current_user.username
        form.description.data = current_user.description

    profile_image_path = url_for('static', filename='profile_pics/' + current_user.profile_image)

    return render_template('users/account.html', form=form, profile_image_path=profile_image_path)
    
# User's posts view
@users_blueprint.route('/<username>')
def user_posts(username):

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=5)

    profile_image_path = url_for('static', filename='profile_pics/' + user.profile_image)
    
    return render_template('users/user_posts.html', user=user, posts=posts, profile_image_path=profile_image_path)

# Change password view
@users_blueprint.route('/<username>/change_password', methods=['GET', 'POST'])
@login_required
def change_password(username):

    user = User.query.filter_by(username=username).first()
    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not user.password_check(form.current_password.data):
            flash('Current password incorrect.', 'error')
        else:
            user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password has updated!')

            return redirect(url_for('users.account'))

    return render_template('users/change_password.html', form=form)