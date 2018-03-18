from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from ..models import User

class LoginForm(Form):
	username = StringField('Username',validators = [Required(),Length(1,32)])
	password = PasswordField('Password',validators=[Required()])
	remember_me = BooleanField('Keep me loggin in')
	submit = SubmitField('Log in')
	
class RegistrationForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,32),Email()])
	
	username = StringField('Username',validators=[Required(),
		Length(1,32),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
		'Usernames must have only letters,numbers,dots or underscores')])
	
	password = PasswordField('Password',validators=[Required(),
		EqualTo('password2',message='Passwords must match!')])
	
	password2 = PasswordField('Confirm password',validators=[Required()])
	
	submit = SubmitField('Register')
	
	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValueError('Email already registered!')
	
	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValueError('Username already in use!')

	