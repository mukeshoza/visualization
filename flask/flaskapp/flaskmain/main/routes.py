from flask import render_template, url_for, flash, Blueprint
from flaskmain.main.forms import SearchForm
from flaskmain.models import User, Projects
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	admin = User.query.filter_by(id=current_user.id).all()
	for adminval in admin:
		adminval = adminval
	formsearch = SearchForm()
	image_file = url_for('static', filename="images/" + current_user.image_file)
	inp = formsearch.searchterm.data
	searchinput = "%{}%".format(inp)
	if adminval.admincheck=='Yes'  or 'Super':
		products = [row.pname for row in Projects.query.all()]
		searchresult = Projects.query.filter(Projects.pname.like(searchinput)).order_by(Projects.date_posted.desc()).all()
	else:
		products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
		searchresult = Projects.query.filter_by(user_id=current_user.id).filter(Projects.pname.like(searchinput)).order_by(Projects.date_posted.desc()).all()
	if searchresult:
		return render_template('main/searchresult.html', title= "Searchresult | ", searchresult= searchresult, formsearch=formsearch, image_file=image_file, adminval=adminval, products=products)
	else:
		flash(f'No project found for term {inp}!', 'warning')
		return render_template('main/searchresult.html', title= "Searchresult | ", searchresult= searchresult, formsearch=formsearch, image_file=image_file, adminval=adminval, products=products)