from flask import Blueprint, current_app
from pyarrow import csv as cv
import os, re, glob, datetime, pathlib, csv
import secrets, numpy, json
import pandas as pd
import dask.dataframe as dd
import shutil
from pymongo import MongoClient
# import MySQLdb
import pymysql
import warnings
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from flaskmain import db, bcrypt, mail
from flaskmain.projects.forms import (ProjectDetails, VisualizationForm,
                                      GraphForm, GraphFile, FormData, FormChat,
                                      FormChart, Duplicatebylines, Mysqlconnect, MysqlFile)
from flaskmain.main.forms import SearchForm
from flaskmain.models import User, Projects, Chats, Report
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from flask_mail import Message
from flaskmain.chartsall.chartsformat import barchart, piechart, lineplot, areaplot, bubblechart
from flaskmain.projects.utils import supportmessage
import sqlalchemy

projects = Blueprint('projects', __name__)


@projects.route('/project/<int:project_id>/visualization/dataset', methods=['GET', 'POST'])
@login_required
def dataset(project_id):
    formsearch = SearchForm()
    formdata = FormData()
    chatform = FormChat()
    formduplicate = Duplicatebylines()
    allvalue = supportmessage(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)
    prouid = project.user_id

    location = str(current_user.id) + '_projectfile'

    datasetnameappend = []
    filenames = []
    dirname = str(project_id) + "_report"
    location_file = str(prouid) + '_projectfile'
    locationbar_path_data = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file,
                                         dirname + '/*.csv')
    all_files = glob.glob(locationbar_path_data)
    for lines in all_files:
        value = lines
        reval = re.sub('\D+.*\\\\|\.csv|\.csv', "", value)
        re_lines = re.sub('\D+.*/|.csv|.csv', "", value)
        datasetnameappend.append(reval)
        filenames.append(re_lines)

    selectvalue = formdata.collectionname.data
    re_lines_selectvalue = re.sub('\D+.*/|\.csv|\.csv', "", str(selectvalue))
    file_name = 'tempfilename.txt'
    file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location, file_name)
    if selectvalue != '':
        with open(file_path, 'w') as file:
            file.write(str(selectvalue))

    selectedfilename = formduplicate.filenameselected.data
    if selectedfilename:
        file_name = str(selectedfilename) + '.csv'
    else:
        file_name = str(selectvalue) + '.csv'
    dirname = str(project_id) + "_report"
    location_file = str(prouid) + '_projectfile'
    file_path_data = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)


    try:
        table = cv.read_csv(file_path_data)
        df1 = table.to_pandas()

        selectvaluedup = formduplicate.selectedfilename.data
        if selectvaluedup == 'Linewise Duplicate Remove':
            df1 = df1.drop_duplicates(subset=None)
            df1.to_csv(file_path_data, index=False)

        
        countall = len(df1)
        dedupe_line = df1.drop_duplicates(subset=None)
        duplicates = countall - len(dedupe_line)
        include = ['object', 'float', 'int']
        data_describe = df1.describe(include=include).reset_index(level=0)
        df1 = df1.head(500)

        return render_template('projects/dataset.html', chatform=chatform, messageuser=allvalue,
                               title=project.pname + ' | Dataset | ', project=project, formsearch=formsearch,
                               image_file=image_file, adminval=adminval, column_names=df1.columns.values,
                               row_data=list(df1.values.tolist()), zip=zip, formdata=formdata,
                               tablenames=zip(filenames, datasetnameappend), selectvalue=re_lines_selectvalue,
                               products=products, linedup=duplicates, data_describe=list(data_describe.values.tolist()),
                               data_describe_column=data_describe.columns.values, countall=countall, formduplicate=formduplicate,
                               selectedfilename=selectedfilename)
    except:
        return render_template('projects/dataset.html', chatform=chatform, messageuser=allvalue,
                               title=project.pname + ' | Dataset | ', project=project, formsearch=formsearch,
                               image_file=image_file, adminval=adminval, zip=zip, formdata=formdata,
                               tablenames=zip(filenames, datasetnameappend), selectvalue=re_lines_selectvalue,
                               products=products, formduplicate=formduplicate, selectedfilename=selectedfilename)
    else:
        with open(file_path, 'r') as read:
            for val in read:
                selectvalue = val

        file_name = str(selectvalue) + '.csv'
        dirname = str(project_id) + "_report"
        location_file = str(prouid) + '_projectfile'
        locationbar_path_data = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file,
                                             dirname + '/*.csv')
        file_path_data = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)
        # df1 = pd.read_csv(file_path_data, quoting=3, error_bad_lines=False, low_memory=False)
        table = cv.read_csv(file_path_data)
        df1 = table.to_pandas()
        df1 = df1.head(2000)
        # columns = df1.columns

        colappen = []
        for vals in cols:
            thead = '<th>{}</th>'.format(vals)
            colappen.append(thead)
        resub = re.sub("\[|\]|\'|,", "", str(colappen))
        return render_template('projects/dataset.html', chatform=chatform, messageuser=allvalue,
                               title=project.pname + ' | Dataset | ', formsearch=formsearch, image_file=image_file,
                               adminval=adminval, formdata=formdata, tablenames=tablenames, selectvalue=selectvalue,
                               thead=resub, products=products, formduplicate=formduplicate, selectedfilename=selectedfilename)


@projects.route('/project/<int:project_id>/visualization/csv', methods=['GET', 'POST'])
@login_required
def visualization(project_id):
    form = VisualizationForm()
    formsearch = SearchForm()
    chatform = FormChat()
    allvalue = supportmessage(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    prouid = project.user_id

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)
    if form.validate_on_submit():
        timenow = datetime.datetime.now()
        timedate = timenow.strftime("%Y-%m-%d_%H%M%S")
        file = request.files['filecsv']
        _, f_ext = os.path.splitext(file.filename)

        dirname = str(project_id) + "_report"
        locationreport = str(prouid) + '_projectfile'
        path = os.path.join(current_app.root_path, 'static/graphfiles', locationreport, dirname)
        try:
            os.mkdir(path)
        except:
            pass

        file_name = _ + f_ext
        location_file = str(prouid) + '_projectfile'
        file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)
        file.save(file_path)

        # location = _
        # mydbcreate = 'dp_'+str(project.id)
        # dbcreate = client[f'{ mydbcreate }']
        # tablecol = dbcreate.list_collection_names()

        # if location in tablecol:
        # 	flash(f'File with same name already exist. Please upload a file with different filename', 'danger')
        # 	return redirect(url_for('projects.visualization', project_id=project.id))
        # else:

        # 	dbcreate.create_collection(f'{ location }')
        # 	mydb = client[f"{ mydbcreate }"]

        # try:
        # 	df = pd.read_csv(file_path, encoding='latin1' or 'cp1252' or 'iso-8859-1' or 'utf-8', sep=',', low_memory=False)
        # except:
        # 	df = pd.read_excel(file_path, encoding='latin1' or 'cp1252' or 'iso-8859-1' or 'utf-8')
        # df.columns = df.columns.str.replace('.', '')
        # df = df.head(2000)
        # jsonfile = df.to_dict(orient='records')

        # coll = mydb[f'{location}']
        # coll.insert_many(jsonfile)

        flash(f'File successfully uploaded. Please create the visulization below', 'success')
        return redirect(url_for('projects.createvisualization', project_id=project.id))

    return render_template('projects/datasource/datasourcecsv.html', title=project.pname + ' | CSV | ', project=project,
                           form=form,
                           formsearch=formsearch, image_file=image_file, adminval=adminval,
                           products=products, chatform=chatform, messageuser=allvalue)


@projects.route('/project/<int:project_id>/visualization/mysql', methods=['GET', 'POST'])
@login_required
def mysql(project_id):
    form = VisualizationForm()
    formsearch = SearchForm()
    chatform = FormChat()
    mysqlconnect = Mysqlconnect()
    mysqlform = MysqlFile()
    allvalue = supportmessage(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)
    cur = ''
    hostname = ''
    curtable = ''
    uid = Projects.query.filter_by(id=project_id)
    for vid in uid:
        usersid = vid.user_id

    dirname = str(usersid) + '_projectfile'
    # pidname = str(project_id)+'_report\\dbmysql.json'
    path = os.path.join(current_app.root_path, 'static/graphfiles', dirname, 'dbmysql.json')

    if mysqlconnect.hostname.data != '':
        if mysqlconnect.validate_on_submit():
            hostname = mysqlconnect.hostname.data
            port = mysqlconnect.port.data
            databasename = mysqlconnect.databasename.data
            username = mysqlconnect.username.data
            password = mysqlconnect.password.data

            dict1 = {
                "dbdata": {
                    "hostname": hostname,
                    "port": port,
                    "databasename": databasename,
                    "username": username,
                    "password": password
                }
            }

            out_file = open(path, "w")
            json.dump(dict1, out_file)
            out_file.close()

            try:

                conn = pymysql.connect(user=username, password=password, host=hostname, database=databasename,
                                       port=port)
                cur = conn.cursor()
                cur.execute("SHOW TABLES")

                flash(f'Connection Successful', 'success')
                return redirect(url_for('projects.mysqlsuccess', project_id=project.id))
                conn.close()

            except:
                flash(f'Connection Unsuccessful ! Please check your credentials.', 'danger')
                return redirect(url_for('projects.mysql', project_id=project.id))

    return render_template('projects/datasource/datasourcemysql.html', title=project.pname + ' | MySQL | ',
                           project=project, form=form,
                           formsearch=formsearch, image_file=image_file, adminval=adminval,
                           products=products, chatform=chatform, messageuser=allvalue,
                           mysqlconnect=mysqlconnect, cur=cur, hostname=hostname, mysqlform=mysqlform,
                           curtable=curtable)


@projects.route('/project/<int:project_id>/visualization/mysqlsuccess', methods=['GET', 'POST'])
@login_required
def mysqlsuccess(project_id):
    form = VisualizationForm()
    formsearch = SearchForm()
    chatform = FormChat()
    mysqlconnect = Mysqlconnect()
    mysqlform = MysqlFile()
    allvalue = supportmessage(project_id)
    co = int(0)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    uid = Projects.query.filter_by(id=project_id)
    for vid in uid:
        usersid = vid.user_id

    dirname = str(usersid) + '_projectfile'
    # pidname = str(project_id)+'_report\\dbmysql.json'
    path = os.path.join(current_app.root_path, 'static/graphfiles', dirname, 'dbmysql.json')
    with open(path, 'r') as read:
        for lines in read:
            data = json.loads(lines)
            hostname = data['dbdata']['hostname']
            port = data['dbdata']['port']
            databasename = data['dbdata']['databasename']
            username = data['dbdata']['username']
            password = data['dbdata']['password']

            tablename = mysqlform.tablename.data

            conn = pymysql.connect(user=username, password=password, host=hostname, database=databasename, port=port)
            cur = conn.cursor()
            cur.execute("SHOW TABLES")
            conn.close()

    if mysqlform.validate_on_submit():
        with open(path, 'r') as read:
            for lines in read:
                data = json.loads(lines)
                hostname = data['dbdata']['hostname']
                port = data['dbdata']['port']
                databasename = data['dbdata']['databasename']
                username = data['dbdata']['username']
                password = data['dbdata']['password']

                tablename = mysqlform.tablename.data

                dict1 = {
                    "dbdata": {
                        "hostname": hostname,
                        "port": port,
                        "databasename": databasename,
                        "username": username,
                        "password": password,
                        "tablename": tablename

                    }
                }

                out_file = open(path, "w")
                json.dump(dict1, out_file)
                out_file.close()

                conn = pymysql.connect(user=username, password=password, host=hostname, database=databasename,
                                       port=port)
                curtable = conn.cursor()
                curtable.execute("desc {}".format(tablename))
                columns = [column[0] for column in curtable.fetchall()]

                appendtablevalue = []
                curtable.execute("SELECT * from {}".format(tablename))
                for val in curtable:
                    appendtablevalue.append(val)
                df = pd.DataFrame(appendtablevalue)
                co = len(df)
                df = df.head(1000)

                return render_template('projects/datasource/mysqlsuccessful.html', title=project.pname + ' | MySQL | ',
                                       project=project, form=form,
                                       formsearch=formsearch, image_file=image_file, adminval=adminval,
                                       products=products, chatform=chatform, messageuser=allvalue,
                                       mysqlconnect=mysqlconnect, cur=cur, hostname=hostname, mysqlform=mysqlform,
                                       curtable=curtable, columns=columns, row_data=list(df.values.tolist()), zip=zip,
                                       co=co)

    return render_template('projects/datasource/mysqlsuccessful.html', title=project.pname + ' | MySQL | ',
                           project=project, form=form,
                           formsearch=formsearch, image_file=image_file, adminval=adminval,
                           products=products, chatform=chatform, messageuser=allvalue,
                           mysqlconnect=mysqlconnect, mysqlform=mysqlform, cur=cur, co=co)


@projects.route('/project/<int:project_id>/visualization/mysqlsuccess/usedata', methods=['GET', 'POST'])
@login_required
def usedata(project_id):
    # form = VisualizationForm()
    formsearch = SearchForm()
    chatform = FormChat()
    mysqlconnect = Mysqlconnect()
    mysqlform = MysqlFile()
    allvalue = supportmessage(project_id)
    co = int(0)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    prouid = project.user_id

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    uid = Projects.query.filter_by(id=project_id)
    for vid in uid:
        usersid = vid.user_id

    dirname = str(usersid) + '_projectfile'
    # pidname = str(project_id)+'_report\\dbmysql.json'
    path = os.path.join(current_app.root_path, 'static/graphfiles', dirname, 'dbmysql.json')
    with open(path, 'r') as read:
        for lines in read:
            data = json.loads(lines)
            hostname = data['dbdata']['hostname']
            port = data['dbdata']['port']
            databasename = data['dbdata']['databasename']
            username = data['dbdata']['username']
            password = data['dbdata']['password']
            tablename = data['dbdata']['tablename']

            conn = pymysql.connect(user=username, password=password, host=hostname, database=databasename, port=port)
            cur = conn.cursor()
            cur.execute("desc {}".format(tablename))
            columns = [column[0] for column in cur.fetchall()]

            appendtablevalue = []
            cur.execute("SELECT * from {}".format(tablename))
            for val in cur:
                appendtablevalue.append(val)
            df = pd.DataFrame(appendtablevalue, columns=columns)
            co = len(df)

            # timenow = datetime.datetime.now()
            # timedate = timenow.strftime("%Y%m%d%H%M%S")

            dirname = str(project_id) + "_report"
            locationreport = str(prouid) + '_projectfile'
            paths = os.path.join(current_app.root_path, 'static/graphfiles', locationreport, dirname)
            try:
                os.mkdir(paths)
            except:
                pass

            file_name_mongo = tablename + "_mysql"

            mydbcreate = 'dp_' + str(project.id)
            dbcreate = client[f'{mydbcreate}']

            tablecol = dbcreate.list_collection_names()

            if file_name_mongo in tablecol:
                dbcreate[f'{file_name_mongo}'].drop()
                dbcreate.create_collection(f'{file_name_mongo}')

            else:
                dbcreate.create_collection(f'{file_name_mongo}')
            df.columns = df.columns.str.replace('.', '')
            df = df.head(2000)
            jsonfile = df.to_dict(orient='records')

            coll = dbcreate[f'{file_name_mongo}']
            coll.insert_many(jsonfile)

            file_name = tablename + "_mysql.csv"
            location_file = str(prouid) + '_projectfile'
            file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)
            df.to_csv(file_path, index=False)

            dirname = str(usersid) + '_projectfile'
            # pidname = str(project_id)+'_report\\dbmysql.json'
            path = os.path.join(current_app.root_path, 'static/graphfiles', dirname, 'dbmysql.json')

            conn.close()

            dict1 = {
                "dbdata": {
                    "hostname": '',
                    "port": '',
                    "databasename": '',
                    "username": '',
                    "password": '',
                    "tablename": ''

                }
            }
            out_file = open(path, "w")
            json.dump(dict1, out_file)
            out_file.close()

            flash(f'MySql data processed successfully. Choose data file to visualize below.', 'success')
            return redirect(url_for('projects.createvisualization', project_id=project.id))


# return render_template('projects/datasource/usedata.html', title=project.pname + ' | MySQL Usedata | ', project=project,
# 										  formsearch=formsearch, image_file=image_file, adminval=adminval, products=products,
# 										  chatform=chatform, messageuser=allvalue, mysqlconnect=mysqlconnect, cur=cur,
# 										  hostname=hostname, mysqlform=mysqlform, co=co)

appendfiles = []


@projects.route('/project/<int:project_id>/visualization/createvisualization', methods=['GET', 'POST'])
@login_required
def createvisualization(project_id):
    appendfiles.clear()
    form = GraphForm()
    formfile = GraphFile()
    formsearch = SearchForm()
    chatform = FormChat()
    allvalue = supportmessage(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        # adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    prouid = project.user_id

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)
    location = str(prouid) + '_projectfile'
    datasetnameappendcreate = []
    dirname = str(project_id) + "_report"
    location_file = str(prouid) + '_projectfile'
    locationbar_path_data = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file,
                                         dirname + '/*.csv')
    all_files = glob.glob(locationbar_path_data)
    for lines in all_files:
        value = lines
        reval = re.sub('^\D+.*/|\.csv', "", value)
        datasetnameappendcreate.append(reval)
    # mydb = 'dp_'+str(project.id)
    # dbmongo = client[f'{ mydb }']
    # tablenames = dbmongo.list_collection_names()

    metricescol = ['Count']

    selectvalue = formfile.selectfile.data
    file_name = 'tempfilename.txt'
    file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location, file_name)
    if selectvalue != '':
        with open(file_path, 'w') as file:
            file.write(str(selectvalue))

        # mydb = 'dp_'+str(project.id)
        # db = client[f'{ mydb }']
        # tname = selectvalue
        # coll = db[f'{tname}']

        # appendjson = []
        # abc = list(coll.find({}, {'_id': False}))
        # for val in abc:
        #     appendjson.append(val)

        # df1 = pd.DataFrame(appendjson)
        columns = ''
        file_name = str(selectvalue) + '.csv'
        dirname = str(project_id) + "_report"
        location_file = str(prouid) + '_projectfile'
        file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)
        print(file_path)
        try:
            df1 = pd.read_csv(file_path, quoting=3, error_bad_lines=False, low_memory=False, encoding='latin-1')
            columns = df1.columns
        except:
            pass

        return render_template('projects/createvisualization.html', messageuser=allvalue, metricescol=metricescol,
                               project=project, chatform=chatform, title=project.pname + ' | Create Visualization | ',
                               formfile=formfile, form=form, formsearch=formsearch, sub=datasetnameappendcreate,
                               columns=columns, image_file=image_file, selectvalue=selectvalue, adminval=adminval,
                               products=products)

    else:

        appen1 = []
        appen2 = []
        appen3 = []
        appen4 = []
        appen5 = []

        gtitle = form.gtitle.data
        gtype = form.gtype.data
        gcolumn = form.gcolumn.data
        gcolumnline = form.gcolumnline.data
        gmetrics = form.gmetrics.data
        colorpicker = form.colorpicker.data

        # multiselect = request.form.getlist('gcolumn')
        #
        # gcolumn = multiselect[0]
        # try:
        # 	gcolumnline = multiselect[1]
        # except:
        # 	pass

        with open(file_path, 'r') as read:
            for val in read:
                selectvalue = val

        file_name = selectvalue + '.csv'
        dirname = str(project_id) + "_report"
        location_file = str(prouid) + '_projectfile'
        file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)

        if gmetrics == 'Sum' or gmetrics == 'Average':
            df1 = pd.read_csv(file_path, encoding='latin', sep=',', usecols=[gcolumn, gcolumnline])
        else:
            df1 = pd.read_csv(file_path, encoding='latin', sep=',', usecols=[gcolumn])

        try:
            dt = df1[gcolumnline].dtypes
            colsum = df1[gcolumnline]

            if gmetrics == 'Sum' or gmetrics == 'Average' and dt == str or dt == object:
                flash(f'The second column is of {dt} datatype. It should be Integer for metrics Sum and Average',
                      'danger')
                redirect(url_for('projects.createvisualization', project_id=project.id))
            elif gmetrics == 'Sum' or gmetrics == 'Average' and colsum.isnull().all():
                flash(f'{gcolumnline} have no value', 'danger')
                redirect(url_for('projects.createvisualization', project_id=project.id))
        except:
            pass

        # Read data from database

        # mydb = 'dp_'+str(project.id)
        # db = client[f'{ mydb }']
        # tname = selectvalue
        # coll = db[f'{tname}']

        # appendjson = []
        # abc = list(coll.find({}, {'_id': False}))
        # for val in abc:
        #     appendjson.append(val)

        # df = pd.DataFrame(appendjson)
        # end read data from database

        file_name = str(selectvalue) + '.csv'
        dirname = str(project_id) + "_report"
        location_file = str(prouid) + '_projectfile'
        file_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname, file_name)
        df = pd.read_csv(file_path, quoting=3, error_bad_lines=False, low_memory=False, encoding='latin-1')
        columns = df.columns

        col = df1[gcolumn]
        if col.isnull().all():
            flash(f'No records found for {gcolumn} column. Please select some other column.', 'danger')
            redirect(url_for('projects.createvisualization', project_id=project.id))
        else:
            if gmetrics == 'Count':
                grp = col.groupby(col).size().reset_index(name="count")
            elif gmetrics == 'Sum':
                grp = df1.groupby(gcolumn)[gcolumnline].sum().reset_index(name="count")

            # elif gmetrics == 'Average':
            # 	grp = df1.groupby(gcolumn)[gcolumnline].mean().reset_index(name="count")

            ##Bar Graph##

            fields_grp = grp[gcolumn]
            for val1 in fields_grp:
                appen1.append(val1)
            graph_grp = grp['count']
            for val1 in graph_grp:
                appen2.append(val1)

            fields = str(appen1)
            graph = appen2

            refields = re.sub("'", "'", fields)

            graphline = ''
            fieldsline = ''
            countmain = ''

            if gtype == 'Bar Graph with Line':
                dfline = pd.read_csv(file_path, encoding='latin', sep=',', usecols=[gcolumn, gcolumnline])
                col1 = dfline[gcolumnline]
                col2 = dfline[gcolumn]
                if col1.isnull().all():
                    flash(f'No records found for {gcolumnline} column. Please select some other column.', 'danger')
                    redirect(url_for('projects.createvisualization', project_id=project.id))
                else:
                    # grpline = dfline.groupby(col1).size().reset_index(name="count")
                    b = dfline.groupby(gcolumn)[gcolumnline].size().reset_index(name='count')
                    c = dfline.groupby(gcolumn)[gcolumn].count().reset_index(name='count')

                    graph_grp_line_field = b[gcolumn]
                    for valline in graph_grp_line_field:
                        appen3.append(valline)

                    graph_grp_line = b['count']
                    for valline1 in graph_grp_line:
                        appen4.append(valline1)

                    graph_grp_count = c['count']
                    for valline2 in graph_grp_count:
                        appen5.append(valline2)

                    fieldsline = appen3
                    countmain = appen4
                    graphline = appen5

            filenamesave = form.savegraph.data
            if gtype == 'Bar Graph':
                timenow = datetime.datetime.now()
                timedate = timenow.strftime("%Y%m%d%H%M%S")
                timedatedb = timenow.strftime("%Y-%m-%d %H:%M:%S")
                barsaveloc = timedate + '_' + filenamesave
                locationbar = str(prouid) + '_projectfile'
                locationbar_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname,
                                                barsaveloc + '.html')

                barchart(gtype, gmetrics, gtitle, refields, gcolumn, graph, selectvalue, locationbar_path, filenamesave)
            ##End Bar Graph##

            ##Pie Chart##
            appendpieval = []
            for piecatg, pieval in zip(fields_grp, graph_grp):
                comval = '["{}",{}],'.format(piecatg, pieval)
                appendpieval.append(comval)
            reappendval = re.sub("\['|\,\'|\s\'|\]$", "", str(appendpieval))
            ##End Pie Chart##

            ##Bubble plott##
            appendbubbleval = []
            for bubblecatg, bubbleval in zip(fields_grp, graph_grp):
                bubbleval = '{{value: {}, name: "{}"}},'.format(bubbleval, bubblecatg)
                appendbubbleval.append(bubbleval)
            reappendvalbubble = re.sub("\['|\,\'|\s\'|\]$", "", str(appendbubbleval))
            ##End Bubble plott##

            if gtype == 'Pie Chart':
                timenow = datetime.datetime.now()
                timedate = timenow.strftime("%Y%m%d%H%M%S")
                timedatedb = timenow.strftime("%Y-%m-%d %H:%M:%S")
                barsaveloc = timedate + '_' + filenamesave
                locationpie = str(prouid) + '_projectfile'
                locationpie_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname,
                                                barsaveloc + '.html')

                piechart(gtitle, selectvalue, gcolumn, reappendval, filenamesave, locationpie_path)

            if gtype == 'Line Plot':
                timenow = datetime.datetime.now()
                timedate = timenow.strftime("%Y%m%d%H%M%S")
                timedatedb = timenow.strftime("%Y-%m-%d %H:%M:%S")
                barsaveloc = timedate + '_' + filenamesave
                locationline = str(prouid) + '_projectfile'
                locationline_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname,
                                                 barsaveloc + '.html')

                lineplot(gtitle, selectvalue, refields, gmetrics, gcolumn, graph, colorpicker, filenamesave,
                         locationline_path)

            if gtype == 'Area Plot':
                timenow = datetime.datetime.now()
                timedate = timenow.strftime("%Y%m%d%H%M%S")
                timedatedb = timenow.strftime("%Y-%m-%d %H:%M:%S")
                barsaveloc = timedate + '_' + filenamesave
                locationarea = str(prouid) + '_projectfile'
                locationarea_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname,
                                                 barsaveloc + '.html')

                areaplot(gtitle, selectvalue, refields, gmetrics, gcolumn, graph, colorpicker, filenamesave,
                         locationarea_path)

            if gtype == 'Bubble Chart':
                timenow = datetime.datetime.now()
                timedate = timenow.strftime("%Y%m%d%H%M%S")
                timedatedb = timenow.strftime("%Y-%m-%d %H:%M:%S")
                barsaveloc = timedate + '_' + filenamesave
                locationbubble = str(prouid) + '_projectfile'
                locationbubble_path = os.path.join(current_app.root_path, 'static/graphfiles/' + location_file, dirname,
                                                   barsaveloc + '.html')

                bubblechart(gtitle, selectvalue, gcolumn, colorpicker, reappendvalbubble, filenamesave,
                            locationbubble_path)

                if filenamesave:
                    flash(
                        f'Report with name {filenamesave} has been saved successfully. Go to View Visualization to view it.',
                        'success')
            if filenamesave:
                report_details = Report(userid=current_user.id, reportpid=project.id, reportname=filenamesave,
                                        reportnamefile=barsaveloc, reporttype=gtype,
                                        reportmetrices=gmetrics, reportcreatedby=current_user.username)
                db.session.add(report_details)
                db.session.commit()

            return render_template('projects/createvisualization.html', chatform=chatform, colorpicker=colorpicker,
                                   reappendvalbubble=reappendvalbubble, metricescol=metricescol, messageuser=allvalue,
                                   project=project, title=project.pname + ' | Create Visualization | ',
                                   formfile=formfile, form=form, formsearch=formsearch, sub=datasetnameappendcreate,
                                   columns=columns, image_file=image_file, gtype=gtype, gtitle=gtitle, gcolumn=gcolumn,
                                   gcolumnline=gcolumnline, gmetrics=gmetrics, selectvalue=selectvalue, catg=refields,
                                   value=graph, adminval=adminval, products=products, comval=reappendval,
                                   graphline=graphline, fieldsline=fieldsline, countmain=countmain)
        return render_template('projects/createvisualization.html', chatform=chatform, colorpicker=colorpicker,
                               metricescol=metricescol, messageuser=allvalue, project=project,
                               title=project.pname + ' | Create Visualization | ', formfile=formfile, form=form,
                               formsearch=formsearch, sub=datasetnameappendcreate, columns=columns,
                               image_file=image_file, gtype=gtype, gtitle=gtitle, gcolumn=gcolumn,
                               gcolumnline=gcolumnline, gmetrics=gmetrics, selectvalue=selectvalue, adminval=adminval,
                               products=products)


@projects.route('/createproject')
@login_required
def createproject():
    formsearch = SearchForm()
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    project = Projects.query.filter_by(user_id=current_user.id).first()
    image_file = url_for('static', filename="images/" + current_user.image_file)
    if not project and adminval.admincheck == 'No':
        dirname = str(current_user.id) + '_projectfile'
        path = os.path.join(current_app.root_path, 'static/graphfiles', dirname)
        try:
            os.mkdir(path)
        except:
            pass
        flash(f'You have no project created yet. Please proceed by creating a project.', 'info')
        return render_template('projects/createproject.html', title='Create Project | ', image_file=image_file,
                               adminval=adminval, products=products, formsearch=formsearch)
    else:
        return redirect(url_for('users.dashboard'))


@projects.route('/project/newproject', methods=['GET', 'POST'])
@login_required
def project():
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    form = ProjectDetails()
    formsearch = SearchForm()

    image_file = url_for('static', filename="images/" + current_user.image_file)
    if form.validate_on_submit():
        project_add = Projects(pname=form.pname.data, ptype=form.ptype.data,
                               pmessage=form.pmessage.data, pstatus=form.pstatus.data, estbudget=form.estbudget.data,
                               totalbudget=form.totalbudget.data, user=current_user)
        db.session.add(project_add)
        db.session.commit()
        dirname = str(current_user.id) + '_projectfile'
        path = os.path.join(current_app.root_path, 'static/graphfiles', dirname)
        try:
            os.mkdir(path)
        except:
            pass
        flash(f'Project {form.pname.data} Created Successfully!', 'success')
        return redirect(url_for('users.dashboard'))
    choices = ['Data Visualization', 'Data Cleaning', 'Data Cleaning and Visualization', 'Custom']
    status = ['In Review', 'In Progress', 'Completed', 'Cancelled']
    return render_template('projects/projectpage.html', title='projectpage | ', form=form, choices=choices,
                           formsearch=formsearch, image_file=image_file, adminval=adminval,
                           products=products, legend='Create Project', status=status)


@projects.route('/project/<int:project_id>/visualization/support', methods=['GET', 'POST'])
@login_required
def projectdetail(project_id):
    form = VisualizationForm()
    formsearch = SearchForm()
    chatform = FormChat()
    allvalue = supportmessage(project_id)

    image_file = url_for('static', filename="images/" + current_user.image_file)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        userimage = adminval.image_file
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    project = Projects.query.get_or_404(project_id)
    prouid = project.user_id

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    if chatform.validate_on_submit():
        chatdata = chatform.chatinput.data
        timenow = datetime.datetime.now()
        timedate = timenow.strftime("%Y-%m-%d %H:%M:%S")
        chat_add = Chats(idproject=project.id, usermessage=chatdata, userid=current_user.id,
                         username=current_user.username,
                         admincheck=adminval.admincheck, userimage=userimage)
        db.session.add(chat_add)
        db.session.commit()
        return redirect(url_for('projects.projectdetail', project_id=project.id))

    return render_template('projects/projectdetail.html', title=project.pname + ' | Support |', messageuser=allvalue,
                           chatform=chatform, project=project, form=form, formsearch=formsearch, image_file=image_file,
                           adminval=adminval, products=products)


@projects.route('/project/<int:project_id>/visualization/update', methods=['GET', 'POST'])
@login_required
def project_update(project_id):
    formsearch = SearchForm()

    project = Projects.query.get_or_404(project_id)
    admin = User.query.filter_by(id=current_user.id).all()

    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)
    form = ProjectDetails()
    if form.validate_on_submit():
        project.pname = form.pname.data
        project.ptype = form.ptype.data
        project.pmessage = form.pmessage.data
        project.estbudget = form.estbudget.data
        project.totalbudget = form.totalbudget.data
        project.pstatus = form.pstatus.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('projects.projectdetail', project_id=project.id))
    elif request.method == 'GET':
        form.pname.data = project.pname
        form.ptype.data = project.ptype
        form.pmessage.data = project.pmessage
        form.estbudget.data = project.estbudget
        form.totalbudget.data = project.totalbudget
        form.pstatus.data = project.pstatus
    image_file = url_for('static', filename="images/" + current_user.image_file)
    choices = ['Data Visualization', 'Visualization with Scraping', 'Comparative visualization with insights', 'Custom']
    status = ['In Review', 'In Progress', 'Completed', 'Cancelled']
    return render_template('projects/projectpage.html', title='UpdateProject | ', form=form, choices=choices,
                           formsearch=formsearch, image_file=image_file,
                           products=products, adminval=adminval, legend='Update Project', status=status,
                           pdata=form.ptype.data, prostatus=form.pstatus.data)


@projects.route('/project/<int:project_id>/visualization/viewvisualization', methods=['GET', 'POST'])
@login_required
def view_visualization(project_id):
    formsearch = SearchForm()
    form = FormChart()
    chatform = FormChat()
    allvalue = supportmessage(project_id)
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    prouid = project.user_id

    appendre = []
    appgraphp = []
    dirname = str(project_id) + "_report"
    locationbar = str(prouid) + '_projectfile'
    locationbar_path = os.path.join(current_app.root_path, 'static/graphfiles/', locationbar, dirname + '/*.html')
    all_files = glob.glob(locationbar_path)
    for lines in all_files:
        value = lines
        reval = re.sub('^/\w+.*/|.html|.html', "", value)
        appendre.append(reval)
        appendre.sort(reverse=True)
        graphpath1 = 'graphfiles/' + locationbar + '/' + dirname + '/' + reval + '.html'
        appgraphp.append(graphpath1)
        appgraphp.sort(reverse=True)

    reportdata = Report.query.filter_by(reportpid=project.id).order_by(Report.reportcreatedon.desc())

    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    return render_template('projects/viewvisualization.html', title=project.pname + ' | View Visualization | ',
                           formsearch=formsearch, form=form, image_file=image_file,
                           products=products, adminval=adminval, project=project, reval=appendre, graphpath1=appgraphp,
                           zip=zip, messageuser=allvalue, chatform=chatform, reportdata=reportdata)


@projects.route('/project/<int:project_id>/visualization/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Projects.query.get_or_404(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    dirname = str(project.id) + "_report"
    locationbar = str(project.user.id) + '_projectfile'
    locationbar_path = os.path.join(current_app.root_path, 'static/graphfiles/', locationbar, dirname)
    try:
        shutil.rmtree(locationbar_path)
    except:
        pass
    for adminval in admin:
        adminval = adminval

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)
    db.session.delete(project)
    db.session.commit()

    # mydb = 'dp_'+str(project.id)
    # client.drop_database(mydb)

    Chats.query.filter_by(idproject=project.id).delete()
    db.session.commit()

    Report.query.filter_by(reportpid=project.id).delete()
    db.session.commit()

    flash('Your project has been deleted successfully!', 'success')
    return redirect(url_for('users.dashboard'))


@projects.route('/project/<int:project_id>/<string:reportname>', methods=['POST'])
@login_required
def delete_report(project_id, reportname):
    project = Projects.query.get_or_404(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    dirname = str(project.id) + "_report"
    locationbar = str(project.user.id) + '_projectfile'
    locationbar_path = os.path.join(current_app.root_path, 'static/graphfiles/', locationbar, dirname,
                                    reportname + '.html')
    print(locationbar_path)
    try:
        os.remove(locationbar_path)
    except:
        pass

    Report.query.filter_by(reportnamefile=reportname).delete()
    db.session.commit()

    for adminval in admin:
        adminval = adminval

    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    flash('Your report has been deleted successfully!', 'success')
    return redirect(url_for('projects.view_visualization', project_id=project.id))


@projects.route('/project/projectsall', methods=['GET', 'POST'])
@login_required
def projectsall():
    formsearch = SearchForm()
    chatform = FormChat()
    form = VisualizationForm()
    image_file = url_for('static', filename="images/" + current_user.image_file)
    admin = User.query.filter_by(id=current_user.id).all()
    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
            page = request.args.get('page', 1, type=int)
            projects = Projects.query.order_by(Projects.date_posted.desc()).paginate(page=page, per_page=8)
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
            page = request.args.get('page', 1, type=int)
            projects = Projects.query.filter_by(user_id=current_user.id).order_by(Projects.date_posted.desc()).paginate(
                page=page, per_page=8)

    return render_template('projects/allprojects.html', title='Projects | ', formsearch=formsearch, adminval=adminval,
                           form=form, products=products, image_file=image_file, chatform=chatform, projects=projects)


@projects.route('/project/<int:project_id>/visualization/new/additionaloperations', methods=['GET', 'POST'])
@login_required
def addoperation(project_id):
    formsearch = SearchForm()
    chatform = FormChat()
    form = VisualizationForm()
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    admin = User.query.filter_by(id=current_user.id).all()
    # proid(project_id)

    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    allvalue = supportmessage(project_id)
    return render_template('projects/additional.html', title=project.pname + ' | ', formsearch=formsearch,
                           adminval=adminval,
                           project=project, form=form, products=products, image_file=image_file, messageuser=allvalue,
                           chatform=chatform)


@projects.route('/project/<int:project_id>/visualization/new/additional operations/removeduplicatebylines',
                methods=['GET', 'POST'])
@login_required
def bylines(project_id):
    formsearch = SearchForm()
    chatform = FormChat()
    form = VisualizationForm()
    formduplicate = Duplicatebylines()
    image_file = url_for('static', filename="images/" + current_user.image_file)
    project = Projects.query.get_or_404(project_id)
    admin = User.query.filter_by(id=current_user.id).all()

    for adminval in admin:
        adminval = adminval
        if adminval.admincheck == 'Yes' or adminval.admincheck == 'Super':
            products = [row.pname for row in Projects.query.all()]
        else:
            products = [row.pname for row in Projects.query.filter_by(user_id=current_user.id).all()]
    if project.user != current_user and adminval.admincheck == 'No':
        abort(403)

    _ = ''
    finalcount = ''
    countfiletotal = ''
    if formduplicate.validate_on_submit():
        appendfile = []
        file = request.files['uploadfile']
        _, f_ext = os.path.splitext(file.filename)
        df = pd.read_csv(file, encoding='latin-1', low_memory=False)
        countfile = len(df)
        countfiletotal = '{:,}'.format(countfile)
        df = df.drop_duplicates()

        countafterdup = len(df)
        finalcount = countfile - countafterdup

    allvalue = supportmessage(project_id)
    return render_template('projects/duplicatebylines.html', title=project.pname + ' | ', formsearch=formsearch,
                           adminval=adminval,
                           project=project, form=form, products=products, image_file=image_file,
                           messageuser=allvalue, chatform=chatform, formduplicate=formduplicate,
                           fileupload=_, finalcount=finalcount, countfiletotal=countfiletotal)