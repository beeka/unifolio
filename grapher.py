#!/usr/bin/env python
# Generate graphable data

from portfolio import *


def addMonths(sourcedate, months):
	import datetime
	import calendar
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	return datetime.datetime(year, month, day, sourcedate.hour, sourcedate.minute, sourcedate.second, sourcedate.microsecond)

def addDays(sourcedate, days):
	from datetime import datetime, timedelta
	return sourcedate + timedelta(days = days)


def timeline():
	from datetime import datetime
	import transactions
	
	t = sorted(transactions.allTransactions())
	if len(t) == 0:
		return t

	# Use the earliest transaction as the initial time
	datapoint = t[0]
	
	# Standardise the reference time as the end of the day
	datapoint = datapoint.replace(hour = 23, minute = 59, second = 59, microsecond = 0)

	# Round to the first day of the next month
	if datapoint.day != 1:
		datapoint = datapoint.replace(day = 1)
		if datapoint.month == 12:
			datapoint = datapoint.replace(year = datapoint.year + 1)
			datapoint = datapoint.replace(month = 1)
		else:
			datapoint = datapoint.replace(month = datapoint.month + 1)

	# Generate a time series with a datapoint every month
	now = datetime.now()
	while datapoint < now:
		if datapoint not in t:
			t.append(datapoint)
		#datapoint = addMonths(datapoint, 1)
		datapoint = addDays(datapoint, 1)
		
	t.append(now)

	return sorted(t)


class Unitiser(object):
	"""A simple class to count the units in a portolio. This allows true performance to be separated from value increasing through investments"""
	
	from decimal import Decimal
	
	def __init__(self):
		self.units = None
		self.invested = Decimal('0.0') # A very simple measure of money put in

	def invest(self, amount, currentValue):
		#print("investing", amount, ", current value is", currentValue)
		price = self.pricePerUnit(currentValue)
		boughtUnits = amount / price
		self.invested = self.invested + amount
		#print("buying", boughtUnits, "units at", price, "each")
		if self.units == None:
			# First investment, so just note the new units
			self.units = boughtUnits
		else:
			self.units = self.units + boughtUnits

	def divest(self, amount, currentValue):
		#print("divesting", amount, ", current value is", currentValue)
		price = self.pricePerUnit(currentValue)
		soldUnits = amount / price
		self.invested = self.invested - amount
		#print("selling", soldUnits, "units at", price, "each")
		if self.units == None:
			print("*** Selling before we have any units!")
		elif self.units < soldUnits:
			print("*** Selling more than we have! (selling %s, of %s units)" % (soldUnits, self.units))
			self.units = None
		else:
			self.units = self.units - soldUnits

	def pricePerUnit(self, currentValue):
		#print(self.units, "units, current value is", currentValue, 'so ppu=', currentValue / self.units)
		if self.units == None:
			return Decimal('100.0') # Starting price of 100 pounds
		else:
			return currentValue / self.units

	def numberOfUnits(self):
		if self.units == None:
			return Decimal('0.0')
		else:
			return self.units


def subtractYears(date, n=1):
	try:
		return date.replace(year=date.year-n)
	except ValueError:
		# Assume we failed on a leap-year check (e.g. 29th Feb - 1yr)
		return date.replace(year=date.year-n, day=28)


def getEntryBefore(entries, date):
	if date in entries:
		return entries[date]
	else:
		bestDate = None
		for thisDate in entries.keys():
			if thisDate < date:
				if bestDate == None or thisDate > bestDate:
					bestDate = thisDate

		if bestDate == None:
			# No match
			return None
		else:
			return entries[bestDate]

# https://www.fool.com/knowledge-center/how-to-calculate-annualized-holding-period-return.aspx
def annualisedReturn(totalReturn, years):
	"""Calculate the annualised rate of return (i.e. compounded equivalent) for a rate acheived over a given number of years.
	The rate is in human-readable form, i.e. 54.12 for 54.12%, as is the returned value."""
	# (1 + totalReturn) ^ (1 / Time(years)) -1
	if totalReturn < 0:
		return 0.0 - annualisedReturn(abs(totalReturn), years)
	else:
		totalReturn = totalReturn / 100
		arr = (1.0 + totalReturn) ** (1.0 / years) - 1
		return arr * 100


def ppuIncrease(entries, startDate, endDate):
	"""Return the percentage increase from one date to another. Returns the value in human-readable form, e.g. 20.42 rather than 0.2842. Returns 0.0 on error."""
	try:
		startEntry = getEntryBefore(entries, startDate)
		#print("start = %s => %s" % (startDate, startEntry))
		endEntry = getEntryBefore(entries, endDate)
		#print("end = %s => %s" % (endDate, endEntry))
		startPrice = float(startEntry['price'])
		endPrice = float(endEntry['price'])
		ppuChangePercent = ((endPrice - startPrice) / startPrice) * 100
		#print("ppuChangePercent = ((%s - %s) / %s) * 100 == %s" % (endPrice, startPrice, startPrice, ppuChangePercent))
		return ppuChangePercent
	except:
		return 0.0


def determinePerformance(history):
	"""Determine performance for the last 1,2..10 years.
	This calculates performance backwards from the last entry in the history. This could cause the figures to be unstable as it measures the performance between different days each time the history is extended."""

	performance = dict()

	n = 1
	recentDate = sorted(history.keys())[-1]

	while True:
		lastYear = subtractYears(recentDate, n)
		if lastYear == None:
			break;

		entry = getEntryBefore(history, lastYear)
		if entry != None:
			ppuChangePercent = ppuIncrease(history, lastYear, recentDate)

			if n > 1:
				yearEnd = subtractYears(recentDate, n-1)
				oneYearPerformance = ppuIncrease(history, lastYear, 		yearEnd)
			else:
				oneYearPerformance = ppuChangePercent

			arr = annualisedReturn(ppuChangePercent, n)
			print("Year -%s performance was %s%%. Cummulative AER of %s%% (%s%% total return)" % (n, round(oneYearPerformance, 2), round(arr, 2), round(ppuChangePercent, 2)))
			performance[n] = {
				'duration' : n,
				'indvidual' : oneYearPerformance,
				'cumulative' : ppuChangePercent,
				'effective' : arr
			}
			n = n + 1
			if n > 10:
				break
		else:
			# run out of whole years
			firstDate = sorted(history.keys())[0]
			ppuChangePercent = ppuIncrease(history, firstDate, recentDate)
			n = float((recentDate - firstDate).days) / 365
			arr = annualisedReturn(ppuChangePercent, n)
			#print "All-time increase: %s%% over %s years (%s%% annualised)" % ( round(ppuChangePercent, 2), round(n, 2), "{:.2f}".format(arr))
			print("%s%% effective annual rate of return over %s years (%s%% total return)" % (round(arr, 2), round(n, 2), round(ppuChangePercent, 2)))
			performance[n] = {
				'duration' : n,
				'indvidual' : None,
				'cumulative' : ppuChangePercent,
				'effective' : arr
			}
			break

	return performance


TWOPLACES = Decimal(10) ** -2

def graph(historyCsvFilePath = 'units.csv'):
	unitTracker = Unitiser()
	
	import transactions
	trades = transactions.allTransactions()
	
	history = dict()
	
	csvfile = open(historyCsvFilePath,'w')
	csvfile.write("date,value,numberOfUnits,pricePerUnit,invested\n")

	for date in timeline():
		#print("\ntimelime:", date.strftime('%Y-%m-%d %H:%M:%S'))
		import valuator
		value = valuator.getPortfolioValueAt(date)
		if date in trades:
			prior = getPortfolioBefore(date)
			prior_value = valuator.getPortfolioValueAt(date, portfolio = prior)

			invested = Decimal('0.0')
			for equity in trades[date]:
				trade = trades[date][equity]
				#print(equity, trade)
				if trade['action'] == 'buy':
					invested = invested + Decimal(trade['value'])
				elif trade['action'] == 'sell':
					invested = invested - Decimal(trade['value'])

			since = getPortfolioAt(date)
			since_value = valuator.getPortfolioValueAt(date, portfolio = since)

			#print("change amount is", invested)
			if invested > 0:
				unitTracker.invest(invested, prior_value)
			elif invested < 0:
				unitTracker.divest(abs(invested), prior_value)

		history[date] = {
			  'date' : date,
			  'value' : value.quantize(TWOPLACES),
			  'units' : unitTracker.numberOfUnits().quantize(TWOPLACES),
			  'price' :  unitTracker.pricePerUnit(value).quantize(TWOPLACES),
			  'invested' : unitTracker.invested
			  }

		csvfile.write("%s,%s,%s,%s,%s\n" % (date.strftime('%Y-%m-%d %H:%M:%S'), value.quantize(TWOPLACES),  unitTracker.numberOfUnits().quantize(TWOPLACES),  unitTracker.pricePerUnit(value).quantize(TWOPLACES),
			unitTracker.invested))

		#print date.strftime('%Y-%m-%d %H:%M:%S'), ',', value.quantize(TWOPLACES), ',', unitTracker.numberOfUnits().quantize(TWOPLACES), ',', unitTracker.pricePerUnit(value).quantize(TWOPLACES), unitTracker.invested

	perf = determinePerformance(history)
	#from pprint import pprint
	#pprint(perf)
	
	return history


if __name__ == "__main__":
	# execute only if run as a script
	graph()
