## Retrieve ETH/XBT exchange price data from bitmex
import requests, json
import numpy as np
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from util import mysql_util

# Plug into an API to get the price (here I use BitMEX because it provides data at minute resolution)
class PriceAPI():
	def __init__(self):
		self.last_startTime = ""
		self.next_startTime = ""
		self.base_req = "https://testnet.bitmex.com/api/v1/trade?symbol=.ETHXBT&count=500&columns=price"
		self.data = np.array(list())
		self.init_timestamps()

	# I'm using an API with a different timestamp format
	def reformat_time(self, t):
		parsed = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.000Z")
		return datetime.strftime(parsed, "%Y-%m-%d %H:%M:%S")


	# While iterating, shift the startTime used in the request to the next minute
	def update_startTime(self, new_data):
		self.last_startTime = self.reformat_time(new_data[0]['timestamp'])
		self.next_startTime = self.reformat_time(new_data[len(new_data)-1]['timestamp'])
		return


	# Get the most recent timestamp from the db
	def init_timestamps(self):
		last_startTime = mysql_util.query("SELECT max(timestamp) as t FROM EthBtcPrice")[0]['t']
		self.last_startTime = datetime.strftime(last_startTime, "%Y-%m-%d %H:%M:%S")
		next_startTime = last_startTime + timedelta(minutes=1)
		self.next_startTime = datetime.strftime(next_startTime, "%Y-%m-%d %H:%M:%S")

	# Make a request to the API I'm using and shift the timestamp afterward
	def make_request(self):
		uri = self.base_req
		if self.next_startTime != "":
			uri += "&startTime=" + self.next_startTime
		
		res = requests.get(uri)
		new_data = json.loads(res.text)
		#assert type(new_data) == list(), "Bad request: %s"%str(new_data)

		self.data = np.hstack((self.data, new_data))
		print("lenggth of self.data: %s"%len(self.data))
		self.update_startTime(new_data)



	# Dump the data into the db
	def db_dump(self):
		for d in range(max(len(self.data)/1000, 1)):
			# Form a query of 1000 bulk inserts
			if d*1000 + 1000 > len(self.data):
				start = d*1000
				end = len(self.data)
				inserts = reduce( lambda i,j: i+""+j, map(lambda d:"('%s', '%s'),"%(d['timestamp'], d['price']), self.data[start:end]) )[0:-1]
			else:
				start = d*1000
				end = start + 1000
				inserts = reduce( lambda i,j: i+""+j, map(lambda d:"('%s', '%s'),"%(d['timestamp'], d['price']), self.data[start:end]) )[0:-1]
			
			# Form the query
			q = "INSERT INTO EthBtcPrice (timestamp, eth_btc_price) VALUES %s"%inserts
			
			# Execute
			try:
				mysql_util.query(q)
			except Exception as e:
				print("Exception raised: %s"%e)
