import csv

def write_csv(file, data, headers):
	#print "data: %s"%str(data)
	with open(file, 'w') as f:
		writer = csv.writer(f)
		if headers: 
			writer.writerow(headers)
		for r in data:
			writer.writerow(list(r))