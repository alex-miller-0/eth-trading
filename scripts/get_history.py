import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from datetime import datetime, timedelta
import time
from API import BitMexReq



# This should be run on a machine with direct access to the DB

# Existing CL options:
#	trades --> pulls a batch of trades, binned by minute:
#				timestamp, 
#				trades --> number of trades in bin 
#				volume --> amount of ETH trades in bin 
#				lastSize --> volume of most recent trade in bin
#	
#	price --> pulls a batch of trades with minute resolution:
#				timestamp,
#				price --> price of the trade
#				size --> volume of the trade
def main(arg):
	BitMexReq(call=arg)



if __name__=="__main__":
	main(sys.argv[1])