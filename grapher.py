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
	return datetime.datetime(year, month, day)


def timeline():
	from datetime import datetime
	import transactions
	
	t = sorted(transactions.readAllTransactions())
	if len(t) == 0:
		return t

	# Use the earliest transaction as the initiate time
	datapoint = t[0]
	
	# Standardise the reference time as the end of the day
	datapoint.replace(hour = 23, minute = 59, second = 59, microsecond = 0)

	# Round to the first day of the next month
	if datapoint.day != 1:
		datapoint.day = 1
		if datapoint.month == 12:
			datapoint.year = datapoint.year + 1
			datapoint.month = 1
		else:
			datapoint.month = datapoint.month + 1

	# Generate a time series with a datapoint every month
	now = datetime.now()
	while datapoint < now:
		if datapoint not in t:
			t.append(datapoint)
		datapoint = addMonths(datapoint, 1)
		
	t.append(now)

	#print t
	return sorted(t)


class Unitiser(object):
	"""A simple class to count the units in a portolio. This allows true performance to be separated from value increasing through investments"""
	
	units = None
#	pricePerUnit = Decimal('1.0')
	
	def __init__(self):
		units = None

	def invest(self, amount, currentValue):
		#if self.units == None:
		#	self.units = Decimal(amount) / pricePerUnit(currentValue)
		#	return
			
		print "investing", amount, ", current value is", currentValue
		price = self.pricePerUnit(currentValue)
		boughtUnits = amount / price
		print "buying", boughtUnits, "units at", price, "each"
		if self.units == None:
			# First investment, so just not the new units
			self.units = boughtUnits
		else:
			self.units = self.units + boughtUnits

	def divest(self, amount, currentValue):
		print "divesting", amount, ", current value is", currentValue
		price = self.pricePerUnit(currentValue)
		soldUnits = amount / price
		print "selling", soldUnits, "units at", price, "each"
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

def graph():
	unitTracker = Unitiser()
	
	import transactions
	trades = transactions.readAllTransactions()
	
	for date in timeline():
		#print date.strftime('%Y-%m-%d')# %H:%M:%S')
		import valuator
		value = valuator.getPortfolioValueAt(date)
		if date in trades:
			invested = Decimal('0.0')
			for equity in trades[date]:
				trade = trades[date][equity]
				print trade
				if trade['action'] == 'buy':
					invested = invested + Decimal(trade['value'])
				elif trade['action'] == 'sell':
					invested = invested - Decimal(trade['value'])
			# TODO: Check the value used is the pre-change value
			print "change amount is", invested
			if invested > 0:
				unitTracker.invest(invested, value)
			elif invested < 0:
				unitTracker.divest(abs(invested), value)
		print date.strftime('%Y-%m-%d'), value, unitTracker.numberOfUnits().quantize(TWOPLACES), unitTracker.pricePerUnit(value).quantize(TWOPLACES)


if __name__ == "__main__":
	# execute only if run as a script
	graph()
