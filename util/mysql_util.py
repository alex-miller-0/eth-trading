import MySQLdb
import os, sys

host = os.environ['ETH_SQL_HOST']
password = os.environ['ETH_SQL_PASSWORD']
user = os.environ['ETH_SQL_USER']
db = os.environ['ETH_SQL_DB']



def query(query):
	connection = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
	cursor = connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	connection.commit()
	connection.close()
	return data