#!/usr/bin/env python
# Exercise some of the functionality. Probably not a unit test per-se

transaction_root = 'transactions'

def transactionFiles():
	from glob import glob
	import os
	return sorted(glob(os.path.join(transaction_root, '*.csv')))

_transactions = None

def allTransactions():
	global _transactions
	
	if _transactions == None:
		#_transactions = _readAllTransactions()
		_transactions = _readEverythingCSV()
	
	return _transactions

def _readAllTransactions():
	import csv
	from datetime import datetime
	import codecs
	
	transactions = dict()
	for csvpath in transactionFiles():
		#print csvpath
		#with open(csvpath, 'a', newline='') as csvfile:
		with open(csvpath) as csvfile:
			reader = csv.DictReader(codecs.EncodedFile(csvfile, 'utf8', 'utf_8_sig'))
			# "Settlement Date","Date","Symbol","Sedol","ISIN","Quantity","Price","Description","Reference","Debit","Credit","Running Balance"
			for row in reader:
				#print row
				#date = datetime.strptime(row['Settlement Date'], '%d/%m/%Y') # or Date?
				date = datetime.strptime(row['Date'], '%d/%m/%Y') # NB: settlement is the date the transaction has cleared?
				identifier = row['Sedol']
				quantity = row['Quantity']
				price = row['Price'][2:] # Range to skip the unicode pound symbol
				debit = row['Debit']
				credit = row['Credit']
				action = None
				value = None
				if debit != '':
					action = 'buy'
					value = debit[2:]
				elif credit != '':
					action = 'sell'
					value = credit[2:] # Range to skip the unicode pound symbol
				#print date, identifier, quantity, 'x', price, debit, credit, action, value
				
				if identifier == '' or quantity == '':
					continue # Probably a subscription, not a buy / sell, or a dividend
					
				# Add the transaction
				if date not in transactions:
					transactions[date] = dict()
				
				if identifier not in transactions[date]:
					transactions[date][identifier] = {
						'action' : action,
						'isin' : identifier,
						'sedol' : identifier,
						'value' : value.replace(',',''), # Remove any thousands separators,
						'quantity' : quantity,
						'price' : price}

	return transactions

def _readEverythingCSV():
	import csv
	from datetime import datetime
	from decimal import Decimal
	import codecs

	transactions = dict()

	with open('everything.csv') as csvfile:
		reader = csv.DictReader(codecs.EncodedFile(csvfile, 'utf8', 'utf_8_sig'))
		# "Settlement Date","Date","Symbol","Sedol","ISIN","Quantity","Price","Description","Reference","Debit","Credit","Running Balance"
		for row in reader:
			#print row
			#date = datetime.strptime(row['Settled'], '%d/%m/%Y %H:%M') # or Date?
			date = datetime.strptime(row['Traded'], '%d/%m/%Y %H:%M') # NB: settlement is the date the transaction has cleared?
			identifier = row['ISIN'][4:11] # GB00B84DY642 => B84DY64
			if identifier == '' or row['Price'] == '':
				continue # Fund merger or dividend?
			quantity = Decimal(row['Quantity'])
			price = Decimal(row['Price'][2:]) # Range to skip the unicode pound symbol
			action = None
			value = None
			if quantity > 0:
				action = 'buy'
				value = quantity * price
			elif quantity < 0:
				action = 'sell'
				value = abs(quantity) * price
				quantity = abs(quantity)
			#print date, identifier, quantity, 'x', price, action, value
			
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
