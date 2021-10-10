# posts/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreatePostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=64)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):

    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class UpdateCommentForm(FlaskForm):

    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Update')