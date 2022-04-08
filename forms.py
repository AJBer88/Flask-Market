from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegistrationForm(FlaskForm):
	username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
	email = StringField(label='Email Address', validators=[Email(), DataRequired()])
	password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
	password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
	submit = SubmitField(label='Create Account')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError("Email already registered")

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username is already in use')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class PurchaseItemForm(FlaskForm):
	submit = SubmitField(label="Purchase Item")

class SellItemForm(FlaskForm):
	submit = SubmitField(label="Sell Item!")