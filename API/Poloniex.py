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
class Poloniex():
	def __init__(self, **kwargs):

		self.last_startTime = 1439164800	# Unix time of 08-10-2015
		self.next_startTime = 1439164800
		self.period = None					# Period of 15 minutes
		self.base_req = "https://poloniex.com/public"
		self.endpoint = None
		self.sql_table = None
		self.sql_mapping = None
		self.delay = 1.3
		self.data = np.array(list())
		self.init_process(kwargs)
		self.init_timestamps()
		self.execute()

	# Convert their timestamp format
	def to_unix_time(self, t):
		parsed = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
		return int(time.mktime(parsed.timetuple()))

	def from_unix_time(self, t):
		return datetime.fromtimestamp(int(t)).strftime('%Y-%m-%d %H:%M:%S')


	# While iterating, shift the startTime used in the request to the next minute
	def update_startTime(self, new_data):
		self.last_startTime = int(new_data[0]['date'])
		self.next_startTime = int(new_data[0]['date']) + self.period

	# Get the most recent timestamp from the db
	def init_timestamps(self):
		last_startTime = mysql_util.query("SELECT max(date) as t FROM %s"%self.sql_table)[0]['t']
		if last_startTime:
			self.last_startTime = int(last_startTime)
			self.next_startTime = int(last_startTime) + self.period


	# Initialize the process
	def init_process(self, kwargs):
		if "call" in kwargs:
			if kwargs["call"] == "chart":
				self.endpoint = "?command=returnChartData&currencyPair=BTC_ETH"
				self.sql_table = "PoloCharts"
				self.sql_mapping = mysql_util.map_polo_charts
				self.period = 7200


	# Make a request and shift the timestamp afterward
	def make_request(self):
		uri = self.base_req + self.endpoint
		if self.next_startTime != "":
			uri += "&period=%s&start=%s&end=9999999999"%(self.period, self.next_startTime)
		print uri
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