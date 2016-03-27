
# A trader that will do a few things
# 1: Grab the last 2 days of chart data (in 15 min windows) and calculate the 24_hour_avg prices for the more recent 24 hours of data
# 2: Determine if we should buy, sell, or hold given the most recent 15 min window's close
# 3: Get the ticker data and set the price for a trade (if applicable)
# 4: Execute the trade
# 5: Expire all trades >4 hours old
# 6: Wait for the next 15 minute window to close

class Trader():
	__init__(self):
		self.api = None