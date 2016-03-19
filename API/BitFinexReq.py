## Retrieve ETH/BTC trading data from Bitfinex
import requests, json
from datetime import datetime
import time
import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from util import file_util, api_util

# Plug into Bitfinex API for trading
class BitFinexReq():
	def __init__(self, **kwargs):
		self.base_req = "https://api.bitfinex.com"
		self.iterations = 0							# Track the number of iterations this process has done
		self.endpoint = None						# The BitFenix API endpoint we are calling
		self.data_dir = None						# The location for the CSV files to be written
		self.headers = None							# The headers to go in the CSV dump files
		self.delay = None							# Delay (in seconds) between calls
		self.data = list()							# Internal data store to be dumped to a file on the hour
		self.last_trade_ts = None 					# Last trade timestamp (only used for calls to /trades)
		self.setup(kwargs)							# Set some of the attributes
		self.execute()								# Run a process upon instantiation of this object
	
	# Set the endpoint. Default to /v1/pubticker/ETHBTC
	def set_endpoint(self, kwargs):
		if "endpoint" in kwargs:
			self.endpoint = kwargs["endpoint"]
		else:
			self.endpoint = "/v1/pubticker/ethbtc"

	# Set the data dir. Default to ETH_PUBTICKER_DATA_DIR
	def set_data_dir(self, kwargs):
		if "data_dir" in kwargs:
			self.data_dir = kwargs["data_dir"]
		else:
			self.data_dir = os.environ['ETH_TICKER_DATA']


	# Set the csv headers based on which API call is being made
	def setup(self, kwargs):
		self.set_endpoint(kwargs)				
		self.set_data_dir(kwargs)
		if self.endpoint == "/v1/book/ethbtc":
			self.delay = 120
			self.headers = ["type", "price", "amount", "timestamp"]
		elif self.endpoint == "/v1/trades/ethbtc":
			self.delay = 2
			self.headers = ["type", "price", "amount", "timestamp", "tid", "exchange"]
		else:
			self.delay = 10
			self.headers = ["mid", "bid", "ask", "last_price", "low", "high", "volume", "timestamp"]



	# Parse the API response to build the data object
	def parse_response(self, data):
		if self.endpoint == "/v1/book/ethbtc":
			return api_util.parse_bfx_book(data, self.headers)
		elif self.endpoint == "/v1/trades/ethbtc":
			return api_util.parse_bfx_flat(data, self.headers)
		else:
			return api_util.parse_bfx_flat([data], self.headers)


	# If we are looking for trades, add a timestamp to prevent collection of redundant data
	def set_last_trade_ts(self, data):
		self.last_trade_ts = data[0]["timestamp"]			# Trades are displayed in descending order of timestamp


	# Make the API request
	def make_request(self):
		ep_req = self.endpoint if not self.last_trade_ts else "%s?timestamp=%s"%(self.endpoint, self.last_trade_ts+1)
		req = "%s%s"%(self.base_req, ep_req)
		res = requests.get(req)
		new_data = json.loads(res.text)
		
		# Update the last trade timestamp if applicable
		if self.endpoint == "/v1/trades/ethbtc":
			if len(new_data) == 0: return					# Skip if no new data was pulled
			self.set_last_trade_ts(new_data)
		
		# Parse the response and update the internal data
		parsed_data = self.parse_response(new_data)
		for datum in parsed_data:
			self.data.append(datum)
	

	# Dump file every 100 iterations
	# I basically just do this so I can run my db locally and don't have to rent out an RDS instance :P
	def file_dump(self):
		if self.iterations%1 == 0:

			next_file = "%s/%s.csv"%(self.data_dir, int(time.time()))
			
			if len(self.data) == 0: return								# Skip if no new data was pulled
			file_util.write_csv(next_file, self.data, self.headers)		# Write the csv file into the data directory

			# Drain the data
			self.data = list()
			print "Data written to %s"%next_file
		
		else:
			print "Process (%s) operating normally (%s)"%(self.endpoint, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))


	# Run this as a process
	def execute(self):
		while True:
			self.iterations += 1
			self.make_request()
			self.file_dump()
			time.sleep(self.delay)



