from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError

from app.models import ListingCategory, ShopContainer, ListedItem, User
from app.extensions import bcrypt, app, db

class SignUpForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=3, max=80)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

def validate_username(self, username):
	user = User.query.filter_by(username=username.data).first()
	if user:
		raise ValidationError('Username is taken.')

class LoginForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=3, max=80)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Log In')

def validate_username(self, username):
	user = User.query.filter_by(username=username.data).first()
	if not user:
		raise ValidationError('Username entered does not match our records.')

def validate_password(self, password):
	user = User.query.filter_by(username=self.username.data).first()
	if user and not bcrypt.check_password_hash(
		user.password, password.data
	):
		raise ValidationError('Password entered does not match our records.')
