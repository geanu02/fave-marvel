from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

class SearchForm(FlaskForm):
    marvel_char = StringField("Name", validators=[DataRequired()])
    marvel_submit = SubmitField("Search")

class MarvelForm(FlaskForm):
    nickname = StringField('Nickname')
    superpower = StringField('Superpower')
    submit = SubmitField('Add to Favorites')

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
