from flask import Blueprint, render_template, redirect, request

from myblog.models import Post

# Create blueprint for core views
core_blueprint = Blueprint('core', __name__)

# Index view
@core_blueprint.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)

    return render_template('index.html', posts=posts, page=page)

# About view
@core_blueprint.route('/about')
def about():

    return render_template('about.html')