# Dump data files collected from remote server to the database
import sys, os, csv
sys.path.append(os.path.realpath("%s/.."%os.path.dirname(__file__)))
from util import mysql_util

# Dump a file full of ticker data into the db
#def dump_ticker_data(data):



def form_insert_query(table, cols, vals):
	return "INSERT INTO %s %s VALUES %s"%(table, mysql_util.stringify_cols(cols), str(tuple(vals)))

def dump_files(sql_table, dir, map_func):
	# Form a sql connection to use for a large volume of commits
	con = mysql_util.connect()

	# Iterate through all the files in the data directory
	for file in os.listdir(dir):
		filepath = "%s/%s"%(dir, file)
		reader = csv.DictReader(open(filepath))
		for row in reader:
			cols, vals = mysql_util.unzip(map_func(row))
			try:
				mysql_util.query(form_insert_query(sql_table, cols, vals), con=con)
			except Exception as e:
				print "Exception raised: %s"%str(e)
		
		# Delete the file when we're done with it
		os.remove(filepath)
	
	# Close the connection
	con.close()

def main():

	# Load files with Bitfinex data into the db
	print("Beginning Bitfinex dump...")
	dump_files("BfxTicker", os.environ["ETH_BFX_TICKER_DATA"], mysql_util.map_ticker)
	dump_files("BfxBook", os.environ["ETH_BFX_BOOK_DATA"], mysql_util.map_book)
	dump_files("BfxTrades", os.environ["ETH_BFX_TRADES_DATA"], mysql_util.map_trades)
	print("Finished with Bitfinex dump.")

if __name__=="__main__":
	main()