from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskmain.models import User
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import imp


class ProjectDetails(FlaskForm):
	pname = StringField('Project Name',
							validators=[DataRequired(), Length(min=2, max=50)])
	ptype = StringField('Project Type',
			validators=[DataRequired()])
	pmessage = TextAreaField('Special Instruction', validators=[DataRequired()])
	estbudget = IntegerField('Estimated Budget', default=0)
	totalbudget = IntegerField('Total amount spent (for admin only)', default=0)
	pstatus = StringField('Project Status', default='In Review')
	submit = SubmitField('Create Project')

class VisualizationForm(FlaskForm):
	filecsv = FileField('Upload File', validators=[FileAllowed(['csv','xlsx'])])
	submit = SubmitField('Upload File')

class GraphForm(FlaskForm):
	gmuted = StringField('Selected File')
	gtitle  = StringField('Title',
							validators=[DataRequired(), Length(min=2, max=50)])
	gtype = StringField('Graph Type',
							validators=[DataRequired()])
	gmetrics = StringField('Select Operation Type',
							validators=[DataRequired()])
	gcolumn = StringField('Column Name to Populate',
							validators=[DataRequired()])
	gcolumnline = StringField('Column Name to Populate',
							validators=[DataRequired()])
	colorpicker = StringField('Select color for line',
							validators=[DataRequired()])

	savegraph = StringField('Save Report')
	submit = SubmitField('Create Vusualization')

class GraphFile(FlaskForm):
	selectfile = StringField('Select File')
	submitfile = SubmitField('Submit')

class FormData(FlaskForm):
	collectionname = StringField('Filename')
	submit = SubmitField('Submit')

class FormChat(FlaskForm):
	chatinput = TextAreaField('Send us your query', validators=[DataRequired()])
	submit = SubmitField('Send')

class FormChart(FlaskForm):
	selectfilechart = StringField('Select File')
	submitfile = SubmitField('Submit')

class Duplicatebylines(FlaskForm):
	# uploadfile = FileField('Remove Duplicate', validators=[FileAllowed(['csv'])])
	selectedfilename = StringField('Selected File Name')
	filenameselected = StringField('File Name')
	submit = SubmitField('Remove Duplicate')

class Mysqlconnect(FlaskForm):
	hostname = StringField('Hostname (Server Name)')
	port = IntegerField('Port')
	databasename = StringField('Database')
	username = StringField('Username')
	password = PasswordField('Password')
	submit = SubmitField('Sign In')

class MysqlFile(FlaskForm):
	tablename = StringField('Select File')
	submitfile = SubmitField('Submit')