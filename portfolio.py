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
	
	def x__init__(self):
		pass

	def __getitem__(self, item):
		return self.equities[item]

	def buy(self, identifier, quantity, price):
		if identifier not in self.equities:
			self.equities[identifier] = Equity('', identifier, quantity)

		self.equities[identifier].quantity = self.equities[identifier].quantity + Decimal(quantity)
		self.equities[identifier].lastPrice = price


	def sell(self, identifier, quantity, price):
		#print "Selling", identifier, quantity, price
		if identifier not in self.equities:
			#SGB print "Error: Selling something we don't have:", identifier
			return

		self.equities[identifier].quantity = self.equities[identifier].quantity - Decimal(quantity)
		self.equities[identifier].lastPrice = price

		if self.equities[identifier].quantity < 0:
			#SGB print "Error: Selling more than we have of", identifier, self.equities[identifier].quantity
			del self.equities[identifier]
		elif self.equities[identifier].quantity == 0:
			del self.equities[identifier]

	def getEquities(self):
		"""Return a list of equities, in (sedol, type) tuples, for which prices should be tracked."""
		equities = list()

		for identifier in self.equities:
			equities.append( ( identifier, self.equities[identifier].type ) )
		
		return equities


	def dump(self):
		for equity in self.equities:
			print self.equities[equity]

portfolio = dict()

xportfolio = [
# https://markets.ft.com/data/funds/tearsheet/historical?s=GB00B545NX97:GBP
# https://uk.finance.yahoo.com/quote/0P0000TKZP.L/history?p=0P0000TKZP.L
{
'type': "fund",
'name': "vanguard LS100",
'isin': "GB00B545NX97",
'sedol': "B545NX9",
'quantity': 195.4309
},
# https://markets.ft.com/data/funds/tearsheet/historical?s=GB00B5BFJG71:GBX
{
'type': "fund",
'name': "BLACKROCK FUND MANAGERS LTD ISHARES GBL PROP SECS EQTY IDX D GBP ACC",
'sedol': "B5BFJG7",
'quantity': 10923.857
},
# https://markets.ft.com/data/funds/tearsheet/summary?s=gb00b84dy642:gbx
{
'type': "fund",
'name': "BLACKROCK FUND MANAGERS LTD ISHARES EMG MKTS EQUITY INDEX UK D ACC",
'isin': "GB00B84DY642",
'sedol': "B84DY64",
'quantity': 7777.118
},
# https://markets.ft.com/data/funds/tearsheet/summary?s=IE00B50W2R13:GBP
{
'type': "fund",
'name': "VANGUARD INVESTMENT SERIES GLOBAL BOND INDEX HEDGED GBP ACC NAV",
'isin': "IE00B50W2R13",
'sedol': "B50W2R1",
'quantity': 39.61
},
# https://markets.ft.com/data/funds/tearsheet/summary?s=GB00B59G4Q73:GBP
{
'type': "fund",
'name': "VANGUARD INVESTMENTS UK LTD FTSE DEVELOPED WORLD EX UK EQTY IDX ACC",
'isin': "GB00B59G4Q73",
'sedol': "B59G4Q7",
'quantity': 145.6241
},
# https://markets.ft.com/data/funds/tearsheet/summary?s=GB00B3X7QG63:GBP
{
'type': "fund",
'name': "VANGUARD INVESTMENTS UK LTD FTSE UK ALL SHARE INDEX UNIT TRUST A ACC",
'isin': "GB00B3X7QG63",
'sedol': "B3X7QG6",
'quantity': 273.7872
},
# https://markets.ft.com/data/equities/tearsheet/summary?s=BA.:LSE
{
'type': "share",
'name': "BAE",
'isin': "GB0002634946",
'sedol': "0263494",
'quantity': 601
},
]


def getStartingPoint():
	pass

def getTransactionHistory():
	pass

def calculateValueHistory():
	pass

def getPortfolio():
	from datetime import datetime
	return getPortfolioAt(datetime.now())
#	return portfolio

def buy(portfolio, identifier, quantity, price):
	
	pass

def sell(portfolio, identifier, quantity, price):
	pass

def getPortfolioAt(date):
	import transactions
	
	portfolio = Portfolio()
	
	actions = transactions.readAllTransactions()
	
	for actionDate in sorted(actions.keys()):
		from pprint import pprint
		#pprint(actions[actionDate])
		if actionDate <= date:
			#print '\n', actionDate
			for equityId in actions[actionDate]:
				t = actions[actionDate][equityId]
				#print equityId, t
				if t['action'] == 'buy':
					portfolio.buy(equityId, t['quantity'], t['price'])
				elif t['action'] == 'sell':
					portfolio.sell(equityId, t['quantity'], t['price'])
			#portfolio.dump()

	return portfolio

def getEquities():
	"""Return a list of equities, in (sedol, type) tuples, for which prices should be tracked."""
	return getPortfolio().getEquities()
	equities = list()
	for item in getPortfolio():
		print item
		equities.append( ( item['sedol'], item['type'] ) )
	
	return equities
