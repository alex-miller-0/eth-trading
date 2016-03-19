import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from API import BitFinexReq

def main(arg):
	kwargs = {}

	# Parse commnad line options for Bitfinex API
	
	# Get the order book: a list of outstanding trades closest to the center
	if arg == "book":
		kwargs = {"endpoint": "/v1/book/ethbtc", "data_dir": os.environ["ETH_BFX_BOOK_DATA"]}
	# Get the most recent executed trades
	elif arg == "trades":
		kwargs = {"endpoint": "/v1/trades/ethbtc", "data_dir": os.environ["ETH_BFX_TRADES_DATA"]}
	# Get the current ticker data
	elif arg == "ticker":
		kwargs = {"endpoint": "/v1/pubticker/ethbtc", "data_dir": os.environ["ETH_BFX_TICKER_DATA"]}

	t = BitFinexReq(**kwargs)

if __name__=="__main__":
	main(sys.argv[1])