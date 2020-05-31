#!/usr/bin/env python
# Updates the price history for equities in the portfolio
# Call this periodically as a cron job

history_root = 'prices'

def noteNewId(identifier, description):
	"""Associates an identifier with a description by updating the index.csv file (or creating it if missing). Note that duplicates are not prevented."""
	import csv
	import os

	fieldnames = ['identifier', 'description']
	csvpath = os.path.join(history_root, 'index.csv')

	if not os.path.exists(csvpath):
		#with open(csvpath, 'w', newline='') as csvfile:
		with open(csvpath, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()

	#with open(csvpath, 'a', newline='') as csvfile:
	with open(csvpath, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow({'identifier': identifier, 'description': description})


def store(date, identifier, value, description = None):
	"""Store a datapoint for an equity value at the specified date.
	Creates a csv file named after the identifier and adds the description to the index CSV if this is new."""
	import csv
	import os
	
	fieldnames = ['date', 'value']
	csvpath = os.path.join(history_root, identifier + '.csv')
	
	if not os.path.exists(csvpath):
		#with open(csvpath, 'w', newline='') as csvfile:
		with open(csvpath, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
		
		if description != None:
			noteNewId(identifier, description)

	#with open(csvpath, 'a', newline='') as csvfile:
	with open(csvpath, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow({'date': str(date), 'value': value})


def valueAt(identifier, date):
	#print identifier, date
	from datetime import datetime
	import csv
	import os
	
	csvpath = os.path.join(history_root, identifier + '.csv')
	
	if not os.path.exists(csvpath):
		print "No history of prices for", identifier
		return None

	lastDate = None
	value = None
	
	#with open(csvpath, 'a', newline='') as csvfile:
	with open(csvpath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			thisDate = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')
			thisValue = row['value']

			if lastDate == None:
				if thisDate <= date:
					lastDate = thisDate
					value = thisValue
			else:
				if thisDate > lastDate and thisDate <= date:
					lastDate = thisDate
					value = thisValue

	#print "Best match is", thisDate, thisValue
	return thisValue


def updateAll():
	import portfolio
	import fetch

	from datetime import datetime
	now = datetime.now()
	
	for (sedol, type) in portfolio.getEquities():
		(title, value) = fetch.getCurrentEquityPrice(sedol)

		print now, sedol, value, title
		if value > 0:
			store(now, sedol, value, title)


if __name__ == "__main__":
	# execute only if run as a script
	updateAll()
