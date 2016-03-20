import MySQLdb
import os, sys

host = os.environ['ETH_SQL_HOST']
password = os.environ['ETH_SQL_PASSWORD']
user = os.environ['ETH_SQL_USER']
db = os.environ['ETH_SQL_DB']


# DIRECT MYSQL FUNCTIONS
#============================================================
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


# BITFINEX-SQL MAPPINGS
#============================================================
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

# BITMEX MAPPINGS
#============================================================
def map_bitmex_trades():
	return {
		"timestamp": "timestamp",
		"trades": "trades",
		"volume": "volume",
		"lastSize": "lastSize"
	}

def map_bitmex_price():
	return {
		"timestamp": "timestamp",
		"price": "price",
		"size": "size"
	}


# GENERAL FUNCTIONS
#============================================================
# Get columns given a datum
def get_cols(d, mapping):
	_cols = list()
	m = mapping()
	for k, v in d.iteritems():
		_cols.append(k)
	cols = filter(lambda x: x, [m[c] if c in m else None for c in _cols])
	return cols


# Stringify items into a tuple that can be used in an insert query
def stringify_items(items, **kwargs):
	i_str = "("
	for i in items:
		if kwargs and 'vals' in kwargs and kwargs['vals']:
			i_str += "'%s',"%i
		else:
			i_str += "%s,"%i
	return "%s) "%i_str[0:-1]

# Pull out the values given columns from a dict
def pull_vals(data, cols):
	return map(lambda d: map(lambda c: d[c] or 0, cols), data)

# Stringify the values into a part of a query (the length of vals should really be limited to about 1000)
#	@param {array} data = [{col1:val1, col2:val2, ...}, ... ]
#	@param {array} cols = [col1, col2, ...]
def vals_query(data, cols):
	vals = pull_vals(data, cols)
	vals_q = reduce(lambda i,j: i+", "+j, [stringify_items(val_set, vals=True) for val_set in vals])
	return vals_q
