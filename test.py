#!/usr/bin/env python
# Exercise some of the functionality. Probably not a unit test per-se

from portfolio import *
from transactions import *
from tracker import *
from fetch import *

from datetime import datetime

def valueToPounds():
	from decimal import Decimal
	with open('prices/0263494.csv') as f:
		n = 0
		first = True
		for line in f:
			n = n + 1
			if first:
				first = False
				print line.strip()
			else:
				l = line.strip().split(',')
				if len(l) < 2 or l[1] == 'null':
					continue
				d = Decimal(l[1]) / 100
				print ','.join([ l[0], str(d)] )
			

#valueToPounds()

def writeHistoricPrices(prices, csvpath):
	with open(csvpath, 'w') as csvfile:
		csvfile.write("date,value\n")
		for date in sorted(prices.iterkeys()):
			value = prices[date]
			csvfile.write("%s,%s\n" % (date.strftime('%Y-%m-%d %H:%M:%S.%f'), value))


#def readFtPrices(ftPath):

# E.g. exporting historical pricess from https://www.vanguard.co.uk/adviser/adv/detail/mf/overview?portId=9156&assetCode=EQUITY##pricesanddistributions
# https://www.vanguard.co.uk/adviser/adv/detail/mf/overview?portId=9210&assetCode=EQUITY##pricesanddistributions
# https://www.vanguard.co.uk/adviser/adv/detail/mf/overview?portId=9142&assetCode=BOND##pricesanddistributions
# https://www.vanguard.co.uk/adviser/adv/detail/mf/overview?portId=9231&assetCode=BALANCED##pricesanddistributions [LS100 gives download error]
def readVanguardPrices(vanguardPath):
	# FTSE Developed World ex-U.K. Equity Index Fund
	#
	# Date,Price
	# "=""01-06-2020""","=""<A3>389.2502"""

	from datetime import datetime
	from decimal import Decimal
	import csv

	values = dict()

	#with open(csvpath, 'a', newline='') as csvfile:
	with open(vanguardPath) as csvfile:
		title = csvfile.readline()
		csvfile.readline()
		reader = csv.DictReader(csvfile)
		for row in reader:
			try:
				if row['Price'] == None:
					break # Run out of useful values, just small print now
					
				dateStr = row['Date'][2:-1]
				date = datetime.strptime(dateStr, '%d-%m-%Y')
				value = row['Price'][3:-1] # Slice is to skip the pound sign and quotes
				values[date] = Decimal(value)
			except:
				import sys
				print "Unexpected error:", sys.exc_info()[0], row

	return values

# Read a csv file that has been tweaked
def readProcessedVanguardPrices(vanguardPath):
	# Date,Value
	# 01-06-2020,?181.4393
	from datetime import datetime
	from decimal import Decimal
	import csv

	values = dict()

	#with open(csvpath, 'a', newline='') as csvfile:
	with open(vanguardPath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print row
			try:
				date = datetime.strptime(row['Date'], '%d-%m-%Y')
				value = row['Value'][2:] # Slice is to skip the pound sign
				values[date] = Decimal(value)
			except:
				import sys
				print "Unexpected error:", sys.exc_info()[0]

	return values


	
# e.g. from https://www.blackrock.com/uk/individual/products/230271/blackrock-emerging-markets-equity-tracker-fund-class-d-acc-fund?switchLocale=y&siteEntryPassthrough=true
def readIShares(xmlpath, csvpath):
	from decimal import Decimal
	from datetime import datetime

	with open(xmlpath) as f:

		values = dict()

#		csvfile = open(csvpath, 'w')
#		csvfile.write("date,value\n")
		csvfile = None
		
		title = None
		isinNext = False
		isin = None
		
		date = None
		value = None
		for line in f:
			#print line.strip()
			if 'Worksheet' in line and 'Performance' in line:
				from pprint import pprint
				#pprint(values)
				print isin, len(values), 'values'
				return # already read 'Historical' worksheet
			elif 'ISIN' in line:
				isinNext = True
			elif '<ss:Data' in line:
				if isinNext == True:
					a = line.find('>')
					b = line.find('<', a)
					isin = line[a+1:b]
					isinNext = False
					csvpath = 'prices/%s.csv' % (isin)
					csvfile = open(csvpath, 'w')
					csvfile.write("date,value\n")

				elif 'String' in line: # This has the date
					# <ss:Data ss:Type=""String"">06-May-20</ss:Data>
					a = line.find('>')
					b = line.find('<', a)
					try:
						dateStr = line[a+1:b]
						date = datetime.strptime(dateStr, '%d-%b-%y')
					except:
						pass
				elif 'Number' in line:
					# "<ss:Data ss:Type=""Number"">1.517</ss:Data>"
					a = line.find('>')
					b = line.find('<', a)
					value = Decimal(line[a+1:b])
			if '</ss:Row>' in line:
				if date != None and value != None:
					csvfile.write("%s,%s\n" % (date.strftime('%Y-%m-%d %H:%M:%S.%f'), value))

					#print "%s,%s" % (date.strftime('%Y-%m-%d %H:%M:%S'), value)
					values[date] = value

				date = None
				value = None

values = readVanguardPrices('csvs/HistoricalPrices_Global_Bond_Index_Fund.csv')
writeHistoricPrices(values, 'prices/IE00B50W2R13.csv')
exit(0)

values = readVanguardPrices('csvs/HistoricalPrices_FTSE_Developed_World_ex-U.K._Equity_Index_Fund.csv')
writeHistoricPrices(values, 'prices/GB00B59G4Q73.csv')
exit(0)

values = readVanguardPrices('csvs/B3X7QG6.csv')
writeHistoricPrices(values, 'prices/GB00B3X7QG63.csv')
exit(0)

csvpath =  'prices/emerging.csv'
readIShares('csvs/iShares-Emerging-Markets-Equity-Index-Fund-UK-Class-D-Acc_fund.xls', csvpath)
readIShares('csvs/iShares-Global-Property-Secs-Eq-Index-Fund-UK-Class-D-Acc_fund.xls', None)

exit(0)

values = readDateValues('prices/0263494.csv')
from pprint import pprint
pprint(values)
exit(0)

date = datetime.strptime('2014-04-30', '%Y-%m-%d')
print valueAt('0263494', date)
exit(0)

#(name, price) = getCurrentEquityPrice('B5BFJG71')
#print name, price
#(name, price) = getCurrentEquityPrice('B545NX9')
#print name, price
#exit(0)

#t = allTransactions()
#print t
#exit(0)

#p = getPortfolioAt(datetime.now())
#print "======== test ========"
#p.dump()
#exit(0)

#print "======== test ========"

q = getPortfolioAt(datetime.strptime('2015-02-19', '%Y-%m-%d'))
print "======== test ========"
q.dump()
