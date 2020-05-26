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
	
	units = Decimal('1.0')
#	pricePerUnit = Decimal('1.0')
	
	def invest(self, amount, currentValue):
		pricePerUnit = currentValue / self.units
		boughtUnits = amount / pricePerUnit
		self.units = self.units + boughtUnits

	def divest(self, amount, currentValue):
		pricePerUnit = currentValue / self.units
		soldUnits = amount / pricePerUnit
		self.units = self.units - soldUnits

	def pricePerUnit(self, currentValue):
		return currentValue / self.units

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
				#print trade
				if trade['action'] == 'buy':
					invested = invested + Decimal(trade['value'])
				elif trade['action'] == 'sell':
						invested = invested - Decimal(trade['value'])
			# TODO: Check the value used is the pre-change value
			if invested > 0:
				unitTracker.invest(invested, value)
			elif invested < 0:
				unitTracker.divest(-invested, value)
		print date.strftime('%Y-%m-%d'), value, unitTracker.units.quantize(TWOPLACES), unitTracker.pricePerUnit(value).quantize(TWOPLACES)


if __name__ == "__main__":
	# execute only if run as a script
	graph()
