import os

class Config:
	# SECRET_KEY = os.environ.get('SECRET_KEY')
	SECRET_KEY = 'd967935d947f5dff7e9c4325'
	# SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
	# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_MYSQL')
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5435/mydatabase_viz'
	MAIL_SERVER = 'r272.lon7.mysecurecloudhost.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	# MAIL_USERNAME = os.environ.get('EMAIL_USER')
	# MAIL_USERNAME = ''
	# MAIL_PASSWORD = ''
	# MAIL_PASSWORD = os.environ.get('EMAIL_PASS')