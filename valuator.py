#!/usr/bin/env python

# Might want to use decimal.Decimal() type for the calculations
def getPortfolioValueAt(date):
	import portfolio
	import tracker
	from decimal import Decimal
	
	sum = Decimal('0.0')

	p = portfolio.getPortfolioAt(date)
	
	for (identifier, type) in p.getEquities():
		value = tracker.valueAt(identifier, date)
		if value == None:
			#print '*** No value for equity', identifier, p[identifier].quantity
			continue
		
		quantity = p[identifier].quantity
		holding = quantity * Decimal(value)
		#print identifier, value, 'x', quantity, '=', holding

		sum = sum + holding
	
	#print "total =", sum, 'GBP'
	return sum


def getPortfolioCurrentValue():
	from datetime import datetime
	return getPortfolioValueAt(datetime.now())


if __name__ == "__main__":
	# execute only if run as a script
	value = getPortfolioCurrentValue()
	print "Current portfolio value is", value
