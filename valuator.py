#!/usr/bin/env python

# Might want to use decimal.Decimal() type for the calculations
def updatePorfolioPricesFor(date, portfolio):
	import tracker
	from decimal import Decimal

	for (identifier, type) in portfolio.getEquities():
		value = tracker.valueAt(identifier, date)
		if value == None:
			print('*** No value for equity', identifier, portfolio[identifier].quantity)
			portfolio[identifier].lastPrice = Decimal('0.0')
			continue
		
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


def getPortfolioValueBefore(date):
	return getPortfolioValueAt(date, inclusive = False)


def getPortfolioCurrentValue():
	from datetime import datetime
	return getPortfolioValueAt(datetime.now())


if __name__ == "__main__":
	# execute only if run as a script
	import argparse

	from datetime import datetime

	parser = argparse.ArgumentParser(description='Calculate the value of a portfolio.')
	parser.add_argument('--date', '-d', dest='date', action='store',
		type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
		default=datetime.now(),
		help='The valuation date in YYYY-MM-DD format (default: now)')

	args = parser.parse_args()

	valuation_date = args.date
	
	import portfolio as folio
	portfolio = folio.getPortfolioAt(valuation_date)
	
	value = getPortfolioValueAt(valuation_date, portfolio = portfolio)
	
	print("Portfolio at", valuation_date.strftime('%Y-%m-%d %H:%M:%S'), "was")
	portfolio.dump()
	print("Value at", valuation_date.strftime('%Y-%m-%d %H:%M:%S'), "was", value)
