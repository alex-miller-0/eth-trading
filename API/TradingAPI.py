## Retrieve ETH/BTC trading data from Bitfinex
import requests, json
from datetime import datetime
import time
import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from util import file_util

DATA_DIR = os.environ['ETH_TRADING_DATA_DIR']
HEADERS = ["mid", "bid", "ask", "last_price", "low", "high", "volume", "timestamp"]

# Plug into Bitfinex API for trading
class TradingAPI():
	def __init__(self):
		self.base_req = "https://api.bitfinex.com/v1/pubticker/ETHBTC"
		self.data = list()
		self.execute()
	

	# Add row to data list (for csv later)
	def add_row(self, new_data):
		new_datum = list()
		for h in HEADERS:
			new_datum.append(new_data[h])
		return new_datum

	# Make the API request
	def make_request(self):
		res = requests.get(self.base_req)
		new_data = json.loads(res.text)
		new_data['volume'] = int(round(float(new_data['volume']), 0))
		new_data['timestamp'] =  datetime.fromtimestamp(int(round(float(new_data['timestamp'])))).strftime('%Y-%m-%d %H:%M:%S') 
		self.data.append(self.add_row(new_data))
	

	# Dump file every hour
	# I basically just do this so I can run my db locally and don't have to rent out an RDS instance :P
	def file_dump(self):
		if datetime.now().minute == 0 and datetime.now().second < 5:
			next_file = "%s/%s.csv"%(DATA_DIR, int(time.time()))
			
			# Write the csv file into the data directory
			file_util.write_csv(next_file, self.data, HEADERS)

			# Drain the data
			self.data = list()
			print "Data written to %s"%next_file
		
		elif datetime.now().second%10 == 0:
			print "Process operating normally (%s)"%datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


	# Run this as a process
	def execute(self):
		while True:
			self.make_request()
			self.file_dump()
			time.sleep(1)



