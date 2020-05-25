#!/usr/bin/env python

# Manage the portfolio of shares

portfolio = [
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
	return portfolio

def getEquities():
	"""Return a list of equities, in (sedol, type) tuples, for which prices should be tracked."""
	equities = list()
	for item in getPortfolio():
		equities.append( ( item['sedol'], item['type'] ) )
	
	return equities
