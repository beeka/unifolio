#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

def divideBy100(pence):
	"""Uses string operations to divide a number by 100"""
	i = pence.index('.')
	j = i - 2
	return pence[:j] + '.' + pence[j:].replace('.', '')

#https://www.charles-stanley-direct.co.uk/ViewShare?Sedol=0263494
def getShare(sedol):
	"""Get the current price of the specified share. Returns (title, value)"""
	
	url = 'https://www.charles-stanley-direct.co.uk/ViewShare?Sedol=%s' % (sedol)
	response = urllib2.urlopen(url)
	html_doc = response.read()

	soup = BeautifulSoup(html_doc, 'html.parser')

	#print soup.title
	title = soup.title.contents[0]
	title = title[:title.find(' -')]

	ask = soup.findAll(attrs={"data-val" : "ask"})
	n = ask[0].contents
	#value = float(n[0]) / 100
	value = divideBy100(n[0])
	#value = n[0]

	#print value
	return (title, value)


#https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=B545NX9
def getFund(sedol):
	"""Get the current price of the specified fund. Returns (title, value)"""

	url = 'https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=%s' % (sedol)
	response = urllib2.urlopen(url)
	html_doc = response.read()

	soup = BeautifulSoup(html_doc, 'html.parser')

	#print soup.title
	title = soup.title.contents[0]
	title = title[:title.find(' -')]
	
	fs = soup.findAll(attrs={"class" : "fund-summary"})
	x = fs[0].find_all('span')[0].contents[0]
	num = x.split()[0]
	#value = float(num.replace(',','')) / 100
	#value = num.replace(',','')
	value = divideBy100( num.replace(',','') )

	#print value
	return (title, value)
