import re
import pandas as pd
from datetime import datetime
import pathlib
import secrets
from flask import render_template, url_for, flash, redirect, request, jsonify, abort, Blueprint, current_app
from flaskmain import db, bcrypt, mail
from flaskmain.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, UserType)
from flaskmain.projects.forms import (ProjectDetails)
from flaskmain.main.forms import (SearchForm)
from flaskmain.models import User, Projects, Report
from flask_login import login_user, current_user, logout_user, login_required
from flaskmain.users.utils import save_picture, send_reset_email
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import imp

users = Blueprint('users', __name__)

appendestbudget = []
appendtotalbudget = []
projectscreated = []
monthproject = []
monthcount = []
amountfinal = []

@users.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	formsearch = SearchForm()
	formproject = ProjectDetails()
	appendestbudget.clear()
	appendtotalbudget.clear()
	monthproject.clear()
	monthcount.clear()
	projectscreated.clear()
	amountfinal.clear()
	admin = User.query.filter_by(id=current_user.id).all()
	
	for adminval in admin:
		if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
			reportid = Report.query.all()
			projectall = Projects.query.all()
			# page = request.args.get('page', 1, type=int)
			projects = Projects.query.order_by(Projects.date_posted.desc()).limit(5)
			products = [row.pname for row in Projects.query.all()]
		else:
			projectall = Projects.query.filter_by(user_id=current_user.id).all()
			reportid = Report.query.filter_by(reportpid=current_user.id).all()
			# page = request.args.get('page', 1, type=int)
			projects = Projects.query.filter_by(user_id=current_user.id).order_by(Projects.date_posted.desc()).limit(5)
			products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
	for val in projectall:
		appendestbudget.append(val.estbudget)
		appendtotalbudget.append(val.totalbudget)
		timeproject = val.date_posted
		timedata = timeproject.strftime("%m-%Y")
		projectscreated.append(timedata)


	df = pd.DataFrame(projectscreated, columns=['Months'])
	df1 = pd.DataFrame(appendtotalbudget, columns=['Amount'])
	try:
		grpcount = df.groupby(projectscreated).size().reset_index(name='count')
		grpamount = df1.groupby(projectscreated)['Amount'].sum().reset_index(name='Amount')

		grpcount = grpcount.head(7)
		grpamount = grpamount.head(7)
		for months in grpcount['index']:
			monthproject.append(months)
		for monthcounts in grpcount['count']:
			monthcount.append(monthcounts)
		for amountcount in grpamount['Amount']:
			amountfinal.append(amountcount)
	except:
		pass


	sumestbudget = sum(appendestbudget)
	sumtotalbudget = sum(appendtotalbudget)
	sumestbudget = '{:,}'.format(sumestbudget)
	sumtotalbudget = '{:,}'.format(sumtotalbudget)
	projectcount = len(projectall)
	reportcount = len(reportid)
	image_file = url_for('static', filename="images/" + current_user.image_file)
	return render_template('users/dashboard.html', projects=projects, products=products, sumestbudget=sumestbudget, sumtotalbudget=sumtotalbudget, projectcount=projectcount,
													formsearch=formsearch, image_file=image_file, adminval=adminval, formproject=formproject, monthproject=monthproject, monthcount=monthcount, amountfinal=amountfinal, reportcount=reportcount)

@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('users.dashboard'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email=form.email.data, password=hashed_password, 
					address=form.address.data, companyname=form.companyname.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created successfully. Please login to create project.', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/signup.html', title='Signup | ', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('users.dashboard'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('projects.createproject'))
		else:
			flash('Login Unsuccessful. Please check your email and password.', 'danger')
	return render_template('users/login.html', title='Login | ', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))

@users.route('/account/update', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	formsearch=SearchForm()
	admin = User.query.filter_by(id=current_user.id).all()
	for adminval in admin:
		adminval = adminval
		if adminval.admincheck=='Yes' or adminval.admincheck=='Super':
			products = [row.pname for row in Projects.query.all()]
		else:
			products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.address = form.address.data
		current_user.companyname = form.companyname.data

		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.address.data = current_user.address
		form.companyname.data = current_user.companyname

	image_file = url_for('static', filename="images/" + current_user.image_file)
	return render_template('users/account.html', title='Profile | ', image_file=image_file, form=form, formsearch=formsearch, adminval=adminval, products=products)

appendestbudget = []
appendtotalbudget = []
@users.route('/projectall/user/<string:username>', methods=['GET', 'POST'])
@login_required
def user_projects(username):
	formsearch = SearchForm()
	formproject = ProjectDetails()
	appendestbudget.clear()
	appendtotalbudget.clear()
	user = User.query.filter_by(username=username).first_or_404()
	admin = User.query.filter_by(id=current_user.id).all()
	for adminval in admin:
		if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
			projectall = Projects.query.all()
			page = request.args.get('page', 1, type=int)
			projects = Projects.query.filter_by(user=user)\
			.order_by(Projects.date_posted.desc())\
			.paginate(page=page, per_page=5)
			products = [row.pname for row in Projects.query.all()]
		else:
			projectall = Projects.query.filter_by(user_id=current_user.id).all()
			page = request.args.get('page', 1, type=int)
			projects = Projects.query.filter_by(user=user)\
			.order_by(Projects.date_posted.desc())\
			.paginate(page=page, per_page=5)
			products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
	for val in projectall:
		appendestbudget.append(val.estbudget)
		appendtotalbudget.append(val.totalbudget)
	sumestbudget = sum(appendestbudget)
	sumtotalbudget = sum(appendtotalbudget)
	sumestbudget = '{:,}'.format(sumestbudget)
	sumtotalbudget = '{:,}'.format(sumtotalbudget)
	projectcount = len(projectall)
	image_file = url_for('static', filename="images/" + current_user.image_file)
	return render_template('users/project_all.html', projects=projects, products=products, sumestbudget=sumestbudget, sumtotalbudget=sumtotalbudget, projectcount=projectcount, formsearch=formsearch, image_file=image_file, adminval=adminval, formproject=formproject, user=user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('users.dashboard'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instruction to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('users/reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('users.dashboard'))
	user = User.verify_reset_token(token)
	if not user:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password has been updated. You are now able to login', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/reset_token.html', title='Reset Password', form=form)

@users.route('/settings/user/superadmin', methods=['GET', 'POST'])
@login_required
def spuer_admin():
	formsearch = SearchForm()
	form = UserType()
	adminall = User.query.all()
	admin = User.query.filter_by(id=current_user.id).all()
	for adminval in admin:
		adminval = adminval
		if adminval.admincheck=='Yes' or adminval.admincheck=='Super':
			products = [row.pname for row in Projects.query.all()]
		else:
			products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
	if form.validate_on_submit():
		utype = form.selectusertype.data
		for admin in adminall:
			if utype == "Admin":
				utype = "Yes"
				admin.admincheck = utype
			else:
				admin.admincheck = "Super"
			
		db.session.commit()
	appendimage = []
	for img in adminall:
		imgfile = img.image_file
		imgfile = url_for('static', filename="images/" + imgfile)
		appendimage.append(imgfile)

	image_file = url_for('static', filename="images/" + current_user.image_file)

	return render_template('users/admin_setting.html', title='Settings', formsearch=formsearch, adminval=adminval, products=products,
														image_file=image_file, adminall=adminall, appendimage=appendimage, zip=zip, form=form)