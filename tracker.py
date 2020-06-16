#!/usr/bin/env python
# Updates the price history for equities in the portfolio
# Call this periodically as a cron job

history_root = 'prices'

def priceHistoryPathFor(identifier):
	"""Determines the path for the equity price history, creating / copying seed file as necessary"""

	import paths
	historyPath = paths.dataFilePath(history_root)
	
	import os
	csvpath = os.path.join(historyPath, identifier + '.csv')

	if not os.path.exists(csvpath):
		#print("Warning:", csvpath, "does not exist, seeing if we have a seed file for", identifier)
		# See if we have a seed file from the repo
		seedPath = os.path.join(history_root, identifier + '.csv')
		if os.path.exists(seedPath):
			# Copy the seed file, making any required directories first
			csvDir = os.path.dirname(csvpath)
			if not os.path.exists(csvDir):
				os.makedirs(csvDir)
			print("Info: Copying seed file", seedPath, "to bootstrap prices for", identifier)
			from shutil import copyfile
			copyfile(seedPath, csvpath)

	return csvpath


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
	csvpath = priceHistoryPathFor(identifier)
	
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


def readDateValues(csvpath):
	from datetime import datetime
	from decimal import Decimal
	import csv

	values = dict()
	
	#with open(csvpath, 'a', newline='') as csvfile:
	with open(csvpath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			try:
				date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')
				value = row['value']
				values[date] = Decimal(value)
			except:
				import sys
				print("Unexpected error:", sys.exc_info()[0], csvpath)
				raise

	return values

_csv_cache = dict()

def equityValues(identifier):
	import csv
	import os

	if identifier not in _csv_cache:
		csvpath = priceHistoryPathFor(identifier)
				
		if not os.path.exists(csvpath):
			print("Warning: No history of prices for", identifier, " [expecting ", csvpath, "]")
			values = dict()
		else:
			values = readDateValues(csvpath)

		_csv_cache[identifier] = values
	else:
		values = _csv_cache[identifier]
	
	#print len(values), "datapoints for", identifier
	return values


def valueAt(identifier, date):
	#print "valueAt(id='%s', date=%s)" % (identifier, date)

	from datetime import datetime

	values = equityValues(identifier)
	
	if values == None:
		return None
	
	# Try our luck first with an exact match
	if date in values:
		return values[date]
	
	(beforeDate, beforeValue) = (None, None)
	(afterDate, afterValue) = (beforeDate, beforeValue)

	for thisDate in values.keys():
		if thisDate < date:
			if beforeDate == None or thisDate > beforeDate:
				(beforeDate, beforeValue) = (thisDate, values[thisDate])
		elif thisDate > date:
			if afterDate == None or thisDate < afterDate:
				(afterDate, afterValue) = (thisDate, values[thisDate])

	#print "best matches: before=", beforeDate, beforeValue, ", after=", afterDate, afterValue
	if beforeDate == None and afterDate != None:
		# No prior history of this equity so use the oldest value we found
		#print date, identifier, "best match is", afterDate, afterValue
		if afterDate.year != date.year:
			print("Using out-of-date data for", identifier, ": wanted", date, "but using data from", afterDate)
		return afterValue
	else:
		#print date, identifier, "best match is", beforeDate, beforeValue
		return beforeValue


def updateAll():
	import portfolio
	import fetch

	from datetime import datetime
	now = datetime.now()
	
	for (sedol, type) in portfolio.getEquities():
		(title, value) = fetch.getCurrentEquityPrice(sedol)

		print(now, sedol, value, title)
		if value > 0:
			store(now, sedol, value, title)


if __name__ == "__main__":
	# execute only if run as a script
	updateAll()
