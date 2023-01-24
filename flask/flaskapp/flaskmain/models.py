from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskmain import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	admincheck = db.Column(db.String(3), nullable=False, default='No')
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	password = db.Column(db.String(60), nullable=False)
	address = db.Column(db.String(50))
	companyname = db.Column(db.String(50))
	user_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
	projects = db.relationship('Projects', backref='user', lazy=True)


	@staticmethod
	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.address}', '{self.companyname}','{self.user_created}')"

class Projects(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pname = db.Column(db.String(120), nullable=False)
	ptype = db.Column(db.String(50), nullable=False)
	pmessage = db.Column(db.Text, nullable=False)
	estbudget = db.Column(db.Integer)
	totalbudget = db.Column(db.Integer)
	pstatus = db.Column(db.String(50), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Projects('{self.pname}', '{self.ptype}', '{self.estbudget}','{self.totalbudget}','{self.date_posted}')"


class Chats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	idproject = db.Column(db.Integer, nullable=False)
	usermessage = db.Column(db.Text, nullable=False)
	userid = db.Column(db.Integer, nullable=False)
	username = db.Column(db.String(20), nullable=False)
	timeposted = db.Column(db.DateTime, nullable=False, default=datetime.now)
	admincheck = db.Column(db.String(5), nullable=False, default='No')
	userimage = db.Column(db.String(500), nullable=False)

	def __repr__(self):
		return f"Chats('{self.idproject}', '{self.usermessage}', '{self.userid}','{self.username}','{self.timeposted}', '{self.admincheck}', '{self.userimage}')"


class Report(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, nullable=False)
	reportpid = db.Column(db.Integer, nullable=False)
	reportname = db.Column(db.String(120), nullable=False)
	reportnamefile = db.Column(db.String(120), nullable=False)
	reporttype = db.Column(db.String(50), nullable=False)
	reportmetrices = db.Column(db.String(50), nullable=False)
	reportcreatedby = db.Column(db.String(50), nullable=False)
	reportcreatedon = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __repr__(self):
		return f"Report('{self.userid}', '{self.reportpid}'. '{self.reportname}', '{self.reportnamefile}', '{self.reporttype}', '{self.reportmetrices}','{self.reportcreatedby}','{self.reportcreatedon}')"