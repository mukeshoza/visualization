from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField

class SearchForm(FlaskForm):
	searchterm = StringField('Title')
	submit = SubmitField('')