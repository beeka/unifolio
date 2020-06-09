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

	# Use the earliest transaction as the initiate time
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
		#print "investing", amount, ", current value is", currentValue
		price = self.pricePerUnit(currentValue)
		boughtUnits = amount / price
		self.invested = self.invested + amount
		#print "buying", boughtUnits, "units at", price, "each"
		if self.units == None:
			# First investment, so just note the new units
			self.units = boughtUnits
		else:
			self.units = self.units + boughtUnits

	def divest(self, amount, currentValue):
		#print "divesting", amount, ", current value is", currentValue
		price = self.pricePerUnit(currentValue)
		soldUnits = amount / price
		self.invested = self.invested - amount
		#print "selling", soldUnits, "units at", price, "each"
		if self.units == None:
			print "*** Selling before we have any units!"
		elif self.units < soldUnits:
			print "*** Selling more than we have! (selling %s, of %s units)" % (soldUnits, self.units)
			self.units = None
		else:
			self.units = self.units - soldUnits

	def pricePerUnit(self, currentValue):
		#print self.units, "units, current value is", currentValue, 'so ppu=', currentValue / self.units
		if self.units == None:
			return Decimal('100.0') # Starting price of 100 pounds
		else:
			return currentValue / self.units

	def numberOfUnits(self):
		if self.units == None:
			return Decimal('0.0')
		else:
			return self.units


TWOPLACES = Decimal(10) ** -2

# TOOD: Generate a csv file (rather than output to stdout)
def graph():
	unitTracker = Unitiser()
	
	import transactions
	trades = transactions.allTransactions()
	
	print "date,value,numberOfUnits,pricePerUnit"

	for date in timeline():
		#print "\ntimelime:", date.strftime('%Y-%m-%d %H:%M:%S')
		import valuator
		value = valuator.getPortfolioValueAt(date)
		if date in trades:
			prior = getPortfolioBefore(date)
			prior_value = valuator.getPortfolioValueAt(date, portfolio = prior)
			
			invested = Decimal('0.0')
			for equity in trades[date]:
				trade = trades[date][equity]
				#print equity, trade
				if trade['action'] == 'buy':
					invested = invested + Decimal(trade['value'])
				elif trade['action'] == 'sell':
					invested = invested - Decimal(trade['value'])

			since = getPortfolioAt(date)
			since_value = valuator.getPortfolioValueAt(date, portfolio = since)

			#print "change amount is", invested
			if invested > 0:
				unitTracker.invest(invested, prior_value) # TBD: prior_value
			elif invested < 0:
				unitTracker.divest(abs(invested), prior_value)

		print date.strftime('%Y-%m-%d %H:%M:%S'), ',', value.quantize(TWOPLACES), ',', unitTracker.numberOfUnits().quantize(TWOPLACES), ',', unitTracker.pricePerUnit(value).quantize(TWOPLACES)


if __name__ == "__main__":
	# execute only if run as a script
	graph()
