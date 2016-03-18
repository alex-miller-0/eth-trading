import csv


def write_csv(file, data, headers):
	with open(file, 'w') as f:
		writer = csv.writer(f)
		if headers: 
			writer.writerow(headers)
		for r in data:
			print r
			writer.writerow(r)