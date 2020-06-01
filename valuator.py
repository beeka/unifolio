#!/usr/bin/env python

# Might want to use decimal.Decimal() type for the calculations
def xgetPortfolioValueAt(date, inclusive = True, portfolio = None):
	import portfolio as folio
	import tracker
	from decimal import Decimal
	
	sum = Decimal('0.0')

	if portfolio == None:
		portfolio = folio.getPortfolioAt(date, inclusive)
	
	for (identifier, type) in portfolio.getEquities():
		value = tracker.valueAt(identifier, date)
		if value == None:
			print '*** No value for equity', identifier, portfolio[identifier].quantity
			portfolio[identifier].lastPrice = Decimal('0.0')
			continue
		
		quantity = portfolio[identifier].quantity
		holding = quantity * Decimal(value)
		print date, identifier, 'x', quantity, '@', value, '=', holding
		portfolio[identifier].lastPrice = Decimal(value)

		sum = sum + holding
	
	#print "total =", sum, 'GBP'
	return sum

# Might want to use decimal.Decimal() type for the calculations
def updatePorfolioPricesFor(date, portfolio):
	import tracker
	from decimal import Decimal


	for (identifier, type) in portfolio.getEquities():
		value = tracker.valueAt(identifier, date)
		if value == None:
			print '*** No value for equity', identifier, portfolio[identifier].quantity
			portfolio[identifier].lastPrice = Decimal('0.0')
			continue
		
		#quantity = portfolio[identifier].quantity
		#holding = quantity * Decimal(value)
		portfolio.updatePrice(identifier, value)


# Might want to use decimal.Decimal() type for the calculations
def getPortfolioValueAt(date, inclusive = True, portfolio = None):
	import portfolio as folio
	import tracker
	from decimal import Decimal
	
	sum = Decimal('0.0')

	if portfolio == None:
		portfolio = folio.getPortfolioAt(date, inclusive)
	
	updatePorfolioPricesFor(date, portfolio)
	return portfolio.value()
	
	for (identifier, type) in portfolio.getEquities():
		value = tracker.valueAt(identifier, date)
		if value == None:
			print '*** No value for equity', identifier, portfolio[identifier].quantity
			portfolio[identifier].lastPrice = Decimal('0.0')
			continue
		
		quantity = portfolio[identifier].quantity
		holding = quantity * Decimal(value)
		print date, identifier, 'x', quantity, '@', value, '=', holding
		portfolio[identifier].lastPrice = Decimal(value)

		sum = sum + holding
	
	#print "total =", sum, 'GBP'
	return sum


def getPortfolioValueBefore(date):
	return getPortfolioValueAt(date, inclusive = False)


def getPortfolioCurrentValue():
	from datetime import datetime
	return getPortfolioValueAt(datetime.now())


if __name__ == "__main__":
	# execute only if run as a script
	value = getPortfolioCurrentValue()
	print "Current portfolio value is", value
