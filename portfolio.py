#!/usr/bin/env python

# Manage the portfolio of shares

from decimal import Decimal

class Equity(object):
	type = 'fund'
	name = ''
	isin = None
	sedol = None
	quantity = Decimal('0.0')
	lastPrice = Decimal('0.0')
	
	def __init__(self, type, sedol, quantity = '0.0'):
		self.type = type
		self.sedol = sedol
	
	def __str__(self):
		return "Equity('%s', '%s', %s, %s)" % (self.type, self.sedol, self.quantity, self.lastPrice)


class Fund(Equity):
	def __init__(self, sedol):
		super(Fund, self).__init__('fund', sedol)


class Share(Equity):
	def __init__(self, sedol):
		super(Share, self).__init__('share', sedol)


class Portfolio(object):
	equities = dict()
	capital = Decimal('0.0')
	
	def __init__(self):
		self.equities = dict()
		self.capital = Decimal('0.0')

	def __getitem__(self, item):
		return self.equities[item]

	def buy(self, identifier, quantity, price):
		#print "Buying", identifier, "x", quantity, "@", price, "each"
		if identifier not in self.equities:
			self.equities[identifier] = Equity('', identifier, quantity)

		self.equities[identifier].quantity = self.equities[identifier].quantity + Decimal(quantity)
		self.equities[identifier].lastPrice = price


	def sell(self, identifier, quantity, price):
		#print "Selling", identifier, "x", quantity, "@", price, "each"
		if identifier not in self.equities:
			print "Error: Selling something we don't have:", identifier
			return

		self.equities[identifier].quantity = self.equities[identifier].quantity - Decimal(quantity)
		self.equities[identifier].lastPrice = price
		
		if self.equities[identifier].quantity < 0:
			#print "Error: Selling more than we have of", identifier, self.equities[identifier].quantity
			del self.equities[identifier]
		elif self.equities[identifier].quantity == 0:
			del self.equities[identifier]

	def getEquities(self):
		"""Return a list of equities, in (sedol, type) tuples, for which prices should be tracked."""
		equities = list()

		for identifier in self.equities:
			equities.append( ( identifier, self.equities[identifier].type ) )
		
		return equities


	def updatePrice(self, identifier, price):
		if price == None:
#			print '*** No value for equity', identifier, portfolio[identifier].quantity
			self.equities[identifier].lastPrice = Decimal('0.0')
		else:
			self.equities[identifier].lastPrice = Decimal(price)


	def value(self):
		"""Return the current value of the equtity holdings, as indicated by the quantities and the last price."""
		sum = Decimal('0.0')

		for identifier in self.equities:
			price = self.equities[identifier].lastPrice
			quantity = self.equities[identifier].quantity
			holding = quantity * Decimal(price)
			#print identifier, 'x', quantity, '@', price, '=', holding

			sum = sum + holding
	
		#print "total =", sum, 'GBP'
		return sum


	def dump(self):
		if len(self.equities) == 0:
			print "The portfolio is empty"
			return

		for equity in self.equities:
			print self.equities[equity].sedol, 'x',self.equities[equity].quantity, '@', self.equities[equity].lastPrice, 'each'


def getPortfolio():
	from datetime import datetime
	return getPortfolioAt(datetime.now())


def getPortfolioAt(date, inclusive = True):
	import transactions
	
	portfolio = Portfolio()
	actions = transactions.allTransactions()
	
	for actionDate in sorted(actions.keys()):
		if actionDate < date or (inclusive and actionDate == date):
			for equityId in actions[actionDate]:
				t = actions[actionDate][equityId]
				if t['action'] == 'buy':
					portfolio.buy(equityId, t['quantity'], t['price'])
				elif t['action'] == 'sell':
					portfolio.sell(equityId, t['quantity'], t['price'])

	return portfolio


def getPortfolioBefore(date):
	"""More readable version of getPortfolioAt(date, inclusive = False)"""
	return getPortfolioAt(date, inclusive = False)


def getEquities():
	"""Return a list of equities, in (sedol, type) tuples, for which prices should be tracked."""
	return getPortfolio().getEquities()
