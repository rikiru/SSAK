from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Regexp
import json
class loginform(FlaskForm):
	login=StringField('Login',validators=[DataRequired()])
	password=PasswordField('Password',validators=[DataRequired()])
	submit=SubmitField('Sign in')

class changeform(FlaskForm):
	json_data=open("config.json").read()
	data = json.loads(json_data)
	username = StringField('New Login',validators=[DataRequired(),Length(min=3)],default=data['User']['Login'])
	newpassword=PasswordField('New Password',validators=[DataRequired(),Length(min=3)])	
	confpassword=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('newpassword')])
	submit=SubmitField('Change')

class adddevice(FlaskForm):
	adresmac = StringField('Adres Mac',validators=[DataRequired(),Length(min=12),Regexp('^[0-9A-F]+$')])
	name = StringField('Name',validators=[DataRequired()])
	submit=SubmitField('Add')
