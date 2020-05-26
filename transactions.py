#!/usr/bin/env python
# Exercise some of the functionality. Probably not a unit test per-se

transaction_root = 'transactions'

def transactionFiles():
	from glob import glob
	import os
	return sorted(glob(os.path.join(transaction_root, '*.csv')))
	
def readAllTransactions():
	import csv
	from datetime import datetime
	import codecs
	
	transactions = dict()
	for csvpath in transactionFiles():
		print csvpath
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
					transactions[date][identifier] = dict()
					transactions[date][identifier]['action'] = action
					transactions[date][identifier]['value'] = value
					transactions[date][identifier]['quantity'] = quantity
					transactions[date][identifier]['price'] = price

	return transactions


if __name__ == "__main__":
	# execute only if run as a script
	from pprint import pprint
	pprint( readAllTransactions() )
