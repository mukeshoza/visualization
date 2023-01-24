# import pandas as pd
# import re
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/usermessage')
# instable = engine.execute(ins, idproject={}, usermessage='{}', userid={}, username='{}', timeposted='{}', admincheck='{}').format(3, 'Hello', 1, 'Mukesh Ojha', '2020,05,12', 'Yes')

# inserttable = engine.execute("INSERT into userquery(idproject, usermessage, userid, username, timeposted, admincheck) values ({}, '{}', {}, '{}', '{}', '{}')".format())

allval = engine.execute('select * from {} order by timeposted;'.format('userquery'))
print(allval)
for val in allval:
	namechar = val.username[0][0]
	print(namechar)

# import json

# with open('D:\\testdesign\\newflask_test\\flaskapp\\flaskmain\\static\\graphfiles\\1_projectfile\\dbmysql.json') as read:
# 	for lines in read:
# 		js = json.loads(lines)
# 		host = js['dbdata']['hostname']
# 		print(host)