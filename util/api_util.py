# Utility functions for parsing API response data or doing other things related to the API
from datetime import datetime

##############################################################
## BITFINEX API
##############################################################

# Turn a UNIX timestamp to a string of format YYYY-mm-dd HH:MM:SS
def stringify_ts(datum):
	datum['timestamp'] = datetime.fromtimestamp(int(round(float(datum['timestamp'])))).strftime('%Y-%m-%d %H:%M:%S')
	return datum

# Assuming we have a flat array with headers that match
def parse_bfx_flat(data, headers):
	new_data = map(lambda i: stringify_ts(i), data)
	parsed = map(lambda d: map(lambda h: d[h], headers), data)
	return parsed


# The order book is a snapshot in time, which may lead to some redundancies across calls
# This will need to be sorted out downstream (e.g. by a unique constraint on multiple keys)
def parse_bfx_book(data, headers):
	# First I want to flatten the object I have
	bids = data["bids"]
	for b in bids: b["type"] = "bid"
	asks = data["asks"]
	for a in asks: a["type"] = "ask"
	new_data = bids + asks

	# Now return the normal array
	return parse_bfx_flat(new_data, headers)


##############################################################
## BITMEX API
##############################################################
