import os, re, glob, datetime, pathlib
from datetime import datetime
import pandas as pd
import mysql.connector
from flask import url_for, redirect, request, Blueprint
from flaskmain.models import User, Projects, Chats
from flaskmain.projects.forms import (VisualizationForm, FormChat)
from flask_login import current_user
import sqlalchemy

projects = Blueprint('projects', __name__)

# engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/usermessage')

def supportmessage(project_id):
	chatform = FormChat()

	project_id = project_id
	allvalue = Chats.query.filter_by(idproject=project_id).order_by(Chats.timeposted)
	return(allvalue)

