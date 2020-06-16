#!/usr/bin/env python
# Mangage reading of portfolio transactions


def numberIn(s):
	"""Return a Decimal from a string that might have unicode pound symbols and commas"""
	number = str()
	for c in s:
		if c in '0123456789.':
			number = number + c
	
	if len(number) > 0:
		from decimal import Decimal
		return Decimal(number)
	else:
		return None


_transactions = None


def determineTransactionsFilePath():
	import paths
	transactionsPath = paths.dataFilePath("transactions.csv")

	import os
	if not os.path.exists(transactionsPath):
		# Not in the data root, so guess at the current directory
		transactionsPath = 'transactions.csv'

	#print("Using a transactions path of", transactionsPath)
	return transactionsPath


def allTransactions():
	global _transactions
	
	if _transactions == None:
		_transactions = _readTransactionsCSV(determineTransactionsFilePath())
	
	return _transactions


def _readTransactionsCSV(transactionsFilePath = 'transactions.csv'):
	import csv
	from datetime import datetime
	from decimal import Decimal
	import codecs

	transactions = dict()

	with open(transactionsFilePath) as csvfile:
		#reader = csv.DictReader(codecs.EncodedFile(csvfile, 'utf8', 'utf_8_sig'))
		reader = csv.DictReader(csvfile)
		# "Settlement Date","Date","Symbol","Sedol","ISIN","Quantity","Price","Description","Reference","Debit","Credit","Running Balance"
		for row in reader:
			#print(row)
			#date = datetime.strptime(row['Settled'], '%d/%m/%Y %H:%M') # or Date?
			date = datetime.strptime(row['Traded'], '%d/%m/%Y %H:%M') # NB: settlement is the date the transaction has cleared?
			isin = row['ISIN'] # e.g. GB00B84DY642
			sedol = isin[4:11] # GB00B84DY642 => B84DY64
			identifier = isin
			if identifier == '' or row['Price'] == '':
				continue # Fund merger or dividend?
			quantity = Decimal(row['Quantity'])
			price = numberIn(row['Price'])
			action = None
			value = None
			if quantity > 0:
				action = 'buy'
				value = quantity * price
			elif quantity < 0:
				action = 'sell'
				value = abs(quantity) * price
				quantity = abs(quantity)
			#print(date, identifier, quantity, 'x', price, action, value)
			
			if identifier == '' or quantity == '':
				continue # Probably a subscription, not a buy / sell, or a dividend
				
			# Add the transaction
			if date not in transactions:
				transactions[date] = dict()
			
			if identifier not in transactions[date]:
				transactions[date][identifier] = {
				'action' : action,
				'isin' : isin,
				'sedol' : sedol,
				'value' : value,
				'quantity' : quantity,
				'price' : price}
			else:
				print("*** Already have a transaction on", date, "for", identifier, "x", quantity)

	return transactions


if __name__ == "__main__":
	# execute only if run as a script
	from pprint import pprint
	pprint( allTransactions() )
