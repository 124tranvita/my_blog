# posts/views.py
from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask.helpers import flash
from flask_login import current_user, login_required
from myblog import db 
from myblog.models import Post, Comment
from myblog.posts.forms import CreatePostForm, CommentForm

posts_blueprint = Blueprint('posts', __name__)

# Create post view
@posts_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():

        new_post = Post(title=form.title.data,
                        content=form.content.data,
                        user_id=current_user.id)
        
        db.session.add(new_post)
        db.session.commit()
        flash('New post was created!')

        return redirect(url_for('users.user_posts', username=current_user.username))

    return render_template('posts/create_post.html', form=form)

@posts_blueprint.route('/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):

    page = request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post).order_by(Comment.date.desc()).paginate(page=page, per_page=10)

    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(comment=form.comment.data,
                            user_id=current_user.id,
                            post_id=post.id)
        
        db.session.add(new_comment)
        db.session.commit()
        flash('You has commented on this post!')

        return redirect(url_for('posts.view_post', post_id=post.id))

    return render_template('posts/view_post.html', post=post, comments=comments, form=form)

# Update post view
@posts_blueprint.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):

    post = Post.query.get_or_404(post_id)

    if current_user != post.author:
        abort(403)

    form = CreatePostForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post was updated!')

        return redirect(url_for('posts.view_post', post_id=post.id))

    elif request.method == 'GET':

        form.title.data = post.title 
        form.content.data = post.content 

    return render_template('posts/create_post.html', form=form, update=True, post=post)

# Delete post view
@posts_blueprint.route('/<int:post_id>/delete')
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if current_user != post.author:
        abort(403)

    for comment in post.comment:
        db.session.delete(comment)

    db.session.delete(post)
    db.session.commit()
    flash('Post was deleted!')

    return redirect(url_for('core.index'))

# Delete comment
@posts_blueprint.route('/<int:post_id>/<int:comment_id>/delete')
@login_required
def delete_comment(post_id, comment_id):

    comment = Comment.query.get_or_404(comment_id)

    if current_user != comment.user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Comment was deleted!')

    return redirect(url_for('posts.view_post', post_id=post_id))

# Update comment
@posts_blueprint.route('/<int:post_id>/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(post_id, comment_id):

    page = request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post).order_by(Comment.date.desc()).paginate(page=page, per_page=10)
    update_cmt = Comment.query.get_or_404(comment_id)

    if current_user != update_cmt.user:
        abort(403)

    form = CommentForm()

    if form.validate_on_submit():

        update_cmt.comment = form.comment.data
        db.session.commit()
        flash('Comment has updated!')

        return redirect(url_for('posts.view_post', post_id=post_id, _anchor=comment_id))

    elif request.method == 'GET':

        form.comment.data = update_cmt.comment

    return render_template('posts/view_post.html', post_id=post_id, form=form,post=post, comments=comments, update=True)
