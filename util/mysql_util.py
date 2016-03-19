import MySQLdb
import os, sys

host = os.environ['ETH_SQL_HOST']
password = os.environ['ETH_SQL_PASSWORD']
user = os.environ['ETH_SQL_USER']
db = os.environ['ETH_SQL_DB']


def connect():
	return MySQLdb.connect(host=host, user=user, passwd=password, db=db)


## Standard query
def query(query, **kwargs):
	if "con" in kwargs:
		con = kwargs["con"]
	else:
		con = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
	
	cursor = con.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	con.commit()
	if "con" not in kwargs:
		con.close()
	
	return data


## Mapping API data to SQL columns
def map_ticker(d):
	return {
		'24_hr_volume': d["volume"], 
		'timestamp': d["timestamp"], 
		'bid': d["bid"], 
		'last_price': d["last_price"],
		'mid': d["mid"], 
		'24_hr_high': d["high"], 
		'24_hr_low': d["low"], 
		'ask': d["ask"]
	}

def map_trades(d):
	return {
		'txn_id': d["tid"],
		'timestamp': d["timestamp"],
		'buy': d["type"] == "buy",
		"price": d["price"],
		"amount": d["amount"],
		"exchange": d["exchange"]
	}

def map_book(d):
	return {
		"buy": d["type"] == "buy",
		"timestamp": d["timestamp"],
		"price": d["price"],
		"amount": d["amount"]
	}

# Unzip a datum into col names and values
def unzip(d):
	cols = list()
	vals = list()
	for k, v in d.iteritems():
		cols.append(k)
		vals.append(v)
	return cols, vals


# Stringify the columns to be inserted into the db
def stringify_cols(cols):
	col_str = "("
	for c in cols:
		col_str += "%s,"%c
	return "%s) "%col_str[0:-1]