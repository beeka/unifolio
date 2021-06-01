#!/usr/bin/env python
# Updates the price history for equities in the portfolio
# Call this periodically as a cron job

from __future__ import print_function

history_root = 'prices'

def priceHistoryPathFor(identifier):
	"""Determines the path for the equity price history, creating / copying seed file as necessary"""

	import paths
	historyPath = paths.dataFilePath(history_root)
	
	import os
	csvpath = os.path.join(historyPath, identifier + '.csv')

	if not os.path.exists(csvpath):
		print("Warning:", csvpath, "does not exist, seeing if we have a seed file for", identifier)
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
	
	#print('Storing value of', identifier, 'at', date, 'as', value)
	
	fieldnames = ['date', 'value']
	csvpath = priceHistoryPathFor(identifier)
	
	if not os.path.exists(csvpath):
		print("Creating new store for", identifier, "in", csvpath)
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
_csv_dates = dict()

def equityValues(identifier):
	'''Return a dictionary of equity values indexed by date'''
	import csv
	import os

	csvpath = priceHistoryPathFor(identifier)
	if not os.path.exists(csvpath):
		print("Warning: No history of prices for", identifier, " [expecting ", csvpath, "]")
		values = dict()
	else:
		csvdate = os.path.getmtime(csvpath)
		if identifier not in _csv_cache or _csv_dates.get(csvpath) != csvdate:
			values = readDateValues(csvpath)
			_csv_cache[identifier] = values
			_csv_dates[csvpath] = csvdate
		else:
			values = _csv_cache[identifier]
	
	#print(len(values), "datapoints for", identifier)
	return values


def valueAt(identifier, date):
	#print("valueAt(id='%s', date=%s)" % (identifier, date))

	# Cash is always £1
	if identifier == 'CASH':
		#print("Defaulting CASH to £1.0")
		return 1.0

	values = equityValues(identifier)

	# Update values with portfolio buy/sell prices
	import transactions
	values.update(transactions.allTransactionsFor(identifier))

	# Quit now if there are no values to go on
	if len(values) == 0:
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
		if value > 0 and valueAt(sedol, now) != value:
			# Value looks valid and changed from the previous value, so storing it
			store(now, sedol, value, title)


if __name__ == "__main__":
	# execute only if run as a script
	updateAll()
