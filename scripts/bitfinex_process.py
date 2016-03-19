import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from API import BitFinexReq

def main(arg):
	kwargs = {}
	print "arg: %s"%arg
	# Parse commnad line options for Bitfinex API
	if arg == "book":
		kwargs = {"endpoint": "/v1/book/ethbtc", "data_dir": os.environ["ETH_BFX_BOOK_DATA"]}
	elif arg == "trades":
		kwargs = {"endpoint": "/v1/trades/ethbtc", "data_dir": os.environ["ETH_BFX_TRADES_DATA"]}
	elif arg == "ticker":
		kwargs = {"endpoint": "/v1/pubticker/ethbtc", "data_dir": os.environ["ETH_BFX_TICKER_DATA"]}

	t = BitFinexReq(**kwargs)

if __name__=="__main__":
	main(sys.argv[1])