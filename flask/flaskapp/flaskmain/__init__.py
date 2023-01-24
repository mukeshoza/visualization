# import os
import warnings

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flaskmain.config import Config

with warnings.catch_warnings():
	warnings.filterwarnings("ignore", category=DeprecationWarning)

# logging.basicConfig(filename='error.log',level=logging.DEBUG)
app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskmain.users.routes import users
	from flaskmain.projects.routes import projects
	from flaskmain.main.routes import main
	from flaskmain.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(projects)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app
