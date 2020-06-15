#!/usr/bin/env python
# Supports importing of downloaded price data


def writeHistoricPrices(prices, csvpath):
	with open(csvpath, 'w') as csvfile:
		csvfile.write("date,value\n")
		for date in sorted(prices.keys()):
			value = prices[date]
			csvfile.write("%s,%s\n" % (date.strftime('%Y-%m-%d %H:%M:%S.%f'), value))

	
# e.g. from https://www.blackrock.com/uk/individual/products/230271/blackrock-emerging-markets-equity-tracker-fund-class-d-acc-fund?switchLocale=y&siteEntryPassthrough=true
def readIShares(xmlpath):
	from decimal import Decimal
	from datetime import datetime, time

	with open(xmlpath) as f:

		values = dict()
	
		title = None
		isinNext = False
		isin = None
		
		date = None
		value = None
		for line in f:
			if 'Worksheet' in line and 'Performance' in line:
				#print(isin, len(values), 'values')
				# already read 'Historical' worksheet, so return our work so far
				return (isin, title, values)
			elif 'ISIN' in line:
				isinNext = True
			elif '<ss:Data' in line:
				if isinNext == True:
					a = line.find('>')
					b = line.find('<', a)
					isin = line[a+1:b]
					isinNext = False

				elif 'String' in line: # This has the date
					# <ss:Data ss:Type=""String"">06-May-20</ss:Data>
					a = line.find('>')
					b = line.find('<', a)
					dateStr = line[a+1:b]
					if len(dateStr) == 9:
						try:
							# NB: The Date/Value is likely to be closing price on that date
							date = datetime.strptime(dateStr, '%d-%b-%y')
							date = datetime.combine(date, time(23, 59, 59))
						except:
							print("Error converting", dateStr)
							raise
				elif 'Number' in line:
					# "<ss:Data ss:Type=""Number"">1.517</ss:Data>"
					a = line.find('>')
					b = line.find('<', a)
					value = Decimal(line[a+1:b])
			if '</ss:Row>' in line:
				if date != None and value != None:
					values[date] = value
					date = None
					value = None
	
	# Something didn't go right if we got here
	return (None, None, None)


# E.g. exporting historical prices from www.vanguard.co.uk
def readVanguardPrices(vanguardPath):
	# FTSE Developed World ex-U.K. Equity Index Fund
	#
	# Date,Price
	# "=""01-06-2020""","=""<A3>389.2502"""

	from datetime import datetime, time
	from decimal import Decimal
	import csv

	values = dict()

	#with open(csvpath, 'a', newline='') as csvfile:
	with open(vanguardPath) as csvfile:
		title = csvfile.readline().strip()
		csvfile.readline()
		reader = csv.DictReader(csvfile)
		for row in reader:
			try:
				if row['Price'] == None:
					break # Run out of useful values, just small print now

				# NB: The Date/Value is likely to be closing price on that date
				dateStr = row['Date'][2:-1]
				date = datetime.strptime(dateStr, '%d-%m-%Y')
				date = datetime.combine(date, time(23, 59, 59))
				value = row['Price'][3:-1] # Slice is to skip the pound sign and quotes
				values[date] = Decimal(value)
			except:
				import sys
				print("Unexpected error:", sys.exc_info()[0], row)
				raise

	return (None, title, values)


if __name__ == "__main__":
	# execute only if run as a script
	from glob import glob
	import os

	for vgCsvPath in glob('import/*.csv'):
		print("Importing Vanguard data from", vgCsvPath)
		
		(isin, title, values) = readVanguardPrices(vgCsvPath)
		isin = os.path.split(vgCsvPath)[-1][:-4].upper()
		csvPath = os.path.join('prices', '%s.csv' % (isin))
		writeHistoricPrices(values, csvPath)
		print("Saved %s data points as %s" % (len(values), csvPath))
	
	for xlsPath in glob('import/*.xls'):
		print("Importing BlackRock data from", xlsPath)
		(isin, title, values) = readIShares(xlsPath)
		csvPath = os.path.join('prices', '%s.csv' % (isin))
		writeHistoricPrices(values, csvPath)
		print("Saved %s data points as %s" % (len(values), csvPath))

