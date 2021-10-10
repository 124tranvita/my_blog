# users/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from myblog.models import User

### LOGIN FORM ###
class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email) -> None:
        if not User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has not registered yet!')
    
    def validate_password(self, email) -> None:
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None and not user.password_check(self.password.data):
            raise ValidationError('Password incorrect!')           

### REGISTER FORM ###
class RegisterForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25), Regexp('^\w+$', message='Special characters not allowed.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Password must match!')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email) -> None:
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has register already!')
    
    def validate_username(self, username) -> None:
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has registered already!')

### UPDATE FORM ###
class UpdateForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25), Regexp('^\w+$', message='Special characters not allowed.')])
    profile_image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Description (Note: 128 chars only)', validators=[Length(min=1, max=128)])
    submit = SubmitField('Update')

    def validate_username(self, username) -> None:
        if current_user.username != self.username.data and User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has taken!')
    
### CHANGE PASSWORD ###
class ChangePasswordForm(FlaskForm):

    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password_confirm', message='Password must match!')])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change')