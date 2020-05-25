#!/usr/bin/env python

# Might want to use decimal.Decimal() type for the calculations
def getPortfolioValueAt(date):
	import portfolio
	import tracker
	
	sum = 0.0

	for item in portfolio.getPortfolio():
		identifier = item['sedol']
		value = tracker.valueAt(identifier, date)
		
		quantity = item['quantity']
		holding = quantity * float(value)
		print identifier, value, 'x', quantity, '=', holding

		sum = sum + holding
	
	print "total =", sum, 'GBP'


def getPortfolioCurrentValue():
	from datetime import datetime
	return getPortfolioValueAt(datetime.now())


if __name__ == "__main__":
	# execute only if run as a script
	getPortfolioCurrentValue()
