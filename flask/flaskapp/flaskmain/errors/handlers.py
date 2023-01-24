from flask import Blueprint, render_template, url_for, redirect
from flaskmain.main.forms import SearchForm
from flaskmain.models import User, Projects
from flask_login import login_user, current_user, logout_user, login_required

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
	if current_user.is_authenticated:
		formsearch = SearchForm()
		admin = User.query.filter_by(id=current_user.id).all()
		for adminval in admin:
			adminval = adminval
			if adminval.admincheck=='Yes':
				products = [row.pname for row in Projects.query.all()]
			else:
				products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
		image_file = url_for('static', filename="images/" + current_user.image_file)
		return render_template('errors/404.html', formsearch=formsearch, adminval=adminval, products=products, image_file=image_file), 404
	else:
		return redirect(url_for('users.login'))

@errors.app_errorhandler(403)
def error_403(error):
	if current_user.is_authenticated:
		formsearch = SearchForm()
		admin = User.query.filter_by(id=current_user.id).all()
		for adminval in admin:
			adminval = adminval
			if adminval.admincheck=='Yes':
				products = [row.pname for row in Projects.query.all()]
			else:
				products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
		image_file = url_for('static', filename="images/" + current_user.image_file)
		return render_template('errors/404.html', formsearch=formsearch, adminval=adminval, products=products, image_file=image_file), 404
	else:
		return redirect(url_for('users.login'))

@errors.app_errorhandler(500)
def error_500(error):
	if current_user.is_authenticated:
		formsearch = SearchForm()
		admin = User.query.filter_by(id=current_user.id).all()
		for adminval in admin:
			adminval = adminval
			if adminval.admincheck=='Yes':
				products = [row.pname for row in Projects.query.all()]
			else:
				products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
		image_file = url_for('static', filename="images/" + current_user.image_file)
		return render_template('errors/404.html', formsearch=formsearch, adminval=adminval, products=products, image_file=image_file), 404
	else:
		return redirect(url_for('users.login'))