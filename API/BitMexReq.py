## Retrieve ETH/XBT exchange price data from bitmex
import requests, json
import numpy as np
from datetime import datetime, timedelta
import time
import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from util import mysql_util

# Plug into an API to get the price (here I use BitMEX because it provides data at minute resolution)
# Bitmex also very nicely provides historical data
class BitMexReq():
	def __init__(self, **kwargs):

		self.last_startTime = "2015-08-10%2005%3A00%3A00"
		self.next_startTime = "2015-08-10%2005%3A00%3A00"
		self.base_req = "https://www.bitmex.com/api"
		self.endpoint = None
		self.sql_table = None
		self.sql_mapping = None
		self.delay = 1.3
		self.query_count = 500
		self.data = np.array(list())
		self.init_process(kwargs)
		self.init_timestamps()
		self.execute()

	# Convert their timestamp format
	def reformat_time(self, t):
		parsed = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.000Z")
		return datetime.strftime(parsed, "%Y-%m-%d%%20%H%%3A%M%%3A%S")

	# Convert timestamp to readable format
	def readable_ts(self, ts):
		return datetime.strftime(datetime.strptime(ts, "%Y-%m-%d%%20%H%%3A%M%%3A%S"), "%Y-%m-%d %H:%M:%S")

	# While iterating, shift the startTime used in the request to the next minute
	def update_startTime(self, new_data):
		self.last_startTime = self.reformat_time(new_data[0]['timestamp'])
		self.next_startTime = self.reformat_time(new_data[len(new_data)-1]['timestamp'])
		print self.readable_ts(self.last_startTime)
		print self.readable_ts(self.next_startTime)

	# Get the most recent timestamp from the db
	def init_timestamps(self):
		last_startTime = mysql_util.query("SELECT max(timestamp) as t FROM %s"%self.sql_table)[0]['t']
		if last_startTime:
			self.last_startTime = datetime.strftime(last_startTime, "%Y-%m-%d%%20%H%%3A%M%%3A%S")
			next_startTime = last_startTime + timedelta(minutes=1)
			self.next_startTime = datetime.strftime(next_startTime, "%Y-%m-%d%%20%H%%3A%M%%3A%S")


	# Initialize the process
	def init_process(self, kwargs):
		if "call" in kwargs:
			if kwargs["call"] == "trades":
				self.endpoint = "/v1/trade/bucketed?binSize=1m&symbol=ETH&count=%s"%self.query_count
				self.sql_table = "BitMexTrades"
				self.sql_mapping = mysql_util.map_bitmex_trades
			elif kwargs["call"] == "price":
				self.endpoint = "/v1/trade?symbol=.ETHXBT&count=%s"%self.query_count
				self.sql_table = "BitMexPrice"
				self.sql_mapping = mysql_util.map_bitmex_price

	# Make a request and shift the timestamp afterward
	def make_request(self):
		uri = self.base_req + self.endpoint
		if self.next_startTime != "":
			uri += "&startTime=" + self.next_startTime
		res = requests.get(uri)
		new_data = json.loads(res.text)
		self.data = np.hstack((self.data, new_data))
		self.update_startTime(new_data)



	# Dump the data into the db
	def db_dump(self):
		if len(self.data) == 0:
			return
		cols = mysql_util.get_cols(self.data[0], self.sql_mapping)
		cols_q = mysql_util.stringify_items(cols)
		vals_q = mysql_util.vals_query(self.data, cols)
		q = "INSERT INTO %s %s VALUES %s"%(self.sql_table, cols_q, vals_q)

		try:
			mysql_util.query(q)
		except Exception as e:
			if str(tuple(e)[0]) != "1062":
				print("Exception raised: %s"%e)

		self.data = list()
			


	# Run this as a process
	def execute(self):
		while True:
			self.make_request()
			self.db_dump()
			time.sleep(self.delay)