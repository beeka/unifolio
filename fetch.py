#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

from decimal import Decimal


#https://www.charles-stanley-direct.co.uk/ViewShare?Sedol=0263494
def getCurrentSharePrice(sedol):
	"""Get the current price of the specified share. Returns (title, value)"""
	
	url = 'https://www.charles-stanley-direct.co.uk/ViewShare?Sedol=%s' % (sedol)
	response = urllib2.urlopen(url)
	html_doc = response.read()

	soup = BeautifulSoup(html_doc, 'html.parser')

	#print soup.title
	title = soup.title.contents[0]
	title = title[:title.find(' -')]

	ask = soup.findAll(attrs={"data-val" : "ask"})
	if len(ask) == 0:
		# Probabably not a valid share id
		return (None, 0.0)
	value = Decimal(ask[0].contents[0]) / 100

	return (title, value)

# TODO: Consider using youinvest, as it gives NAV: https://www.youinvest.co.uk/market-research/FUND%3AB5BFJG7
#https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=B545NX9
def getCurrentFundPrice(sedol):
	"""Get the current price of the specified fund. Returns (title, value)"""

		#  https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=B545NX9
	url = 'https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=%s' % (sedol)
	response = urllib2.urlopen(url)
	html_doc = response.read()

	soup = BeautifulSoup(html_doc, 'html.parser')

	title = soup.title.contents[0]
	title = title[:title.find(' -')]
	
	fs = soup.findAll(attrs={"class" : "fund-summary"})
	if len(fs) == 0:
		# Probabably not a valid fund id
		print('Invalid sedol of', sedol)
		return (None, 0.0)
	x = fs[0].find_all('span')[0].contents[0]
	num = x.split()[0].replace(',','')
	value = Decimal(num) / 100

	return (title, value)


def getCurrentEquityPrice(sedol):
	if len(sedol) == 12: # probably an ISIN
		# extract what is likely to be the sedol
		sedol = sedol[4:11] # GB00B84DY642 => B84DY64

	#print "fetching price for '%s'" % (sedol)
	result = getCurrentSharePrice(sedol)
	if result[0] == None:
		result = getCurrentFundPrice(sedol)

	return result
