import sys, os
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from datetime import datetime, timedelta
import time
from API import PriceAPI

# Get price history based on the most recent data file
def get_price_history():
	
	r = PriceAPI()
	while r.last_startTime == "" or datetime.strptime(r.last_startTime,"%Y-%m-%d %H:%M:%S" )< datetime.now() - timedelta(hours=5):
		r.make_request()
		print("last_startTime: %s"%str(r.last_startTime))
		print("next_startTime: %s"%str(r.next_startTime))
		time.sleep(1.2)
	r.db_dump()


# This should be run on a machine with direct access to the DB
def main():
	get_price_history()



if __name__=="__main__":
	main()