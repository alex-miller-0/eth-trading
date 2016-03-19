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
		self.data = list()
		self.endpoint = self.set_endpoint(kwargs)
		self.data_dir = self.set_data_dir(kwargs)
		self.headers = self.set_headers()
		self.execute()
	
	# Set the endpoint. Default to /v1/pubticker/ETHBTC
	def set_endpoint(self, kwargs):
		if "endpoint" in kwargs:
			return kwargs["endpoint"]
		else:
			return "/v1/pubticker/ethbtc"

	# Set the data dir. Default to ETH_PUBTICKER_DATA_DIR
	def set_data_dir(self, kwargs):
		if "data_dir" in kwargs:
			return kwargs["data_dir"]
		else:
			return os.environ['ETH_TICKER_DATA']


	# Set the csv headers based on which API call is being made
	def set_headers(self):
		if self.endpoint == "/v1/book/ethbtc":
			return ["type", "price", "amount", "timestamp"]
		elif self.endpoint == "/v1/trades/ethbtc":
			return ["type", "price", "amount", "timestamp", "tid", "exchange"]
		else:
			return ["mid", "bid", "ask", "last_price", "low", "high", "volume", "timestamp"]



	# Parse the API response to build the data object
	def parse_response(self, data):
		if self.endpoint == "/v1/book/ethbtc":
			return api_util.parse_bfx_book(data, self.headers)
		elif self.endpoint == "/v1/trades/ethbtc":
			return api_util.parse_bfx_flat(data, self.headers)
		else:
			return api_util.parse_bfx_flat([data], self.headers)

	# Make the API request
	def make_request(self):
		res = requests.get("%s%s"%(self.base_req, self.endpoint))
		new_data = json.loads(res.text)
		parsed_data = self.parse_response(new_data)
		for datum in parsed_data:
			self.data.append(datum)
	

	# Dump file every hour
	# I basically just do this so I can run my db locally and don't have to rent out an RDS instance :P
	def file_dump(self):
		if datetime.now().minute == 0 and datetime.now().second < 20:
			next_file = "%s/%s.csv"%(self.data_dir, int(time.time()))
			
			# Write the csv file into the data directory
			file_util.write_csv(next_file, self.data, self.headers)

			# Drain the data
			self.data = list()
			print "Data written to %s"%next_file
		
		else:
			print "Process operating normally (%s)"%datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


	# Run this as a process
	def execute(self):
		while True:
			self.make_request()
			self.file_dump()
			time.sleep(10)



