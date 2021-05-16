#!/usr/bin/env python

from bs4 import BeautifulSoup
from decimal import Decimal


def getHttpPage(url):
	"""Fetch a url HTTP page and return the contents"""
	try:
		# Try the Python-3 way first
		import urllib.request, urllib.error, urllib.parse
		try:
			response = urllib.request.urlopen(url)
			html_doc = response.read()
			return html_doc
		except urllib.error.HTTPError as e:
			message = 'HTTP error [%s] "%s" fetching %s' % (e.code, e.reason, url)
			print(message)
			return message
		except urllib.error.URLError as e:
			message = 'URL error "%s" fetching %s' % (e.reason, url)
			print(message)
			return message
	except ModuleNotFoundError:
		# That didn't work, so try Python-2 style
		import urllib2
		response = urllib2.urlopen(url)
		html_doc = response.read()
		return html_doc


#https://www.charles-stanley-direct.co.uk/ViewShare?Sedol=0263494
def getCurrentSharePrice(sedol):
	"""Get the current price of the specified share. Returns (title, value)"""
	
	url = 'https://www.charles-stanley-direct.co.uk/ViewShare?Sedol=%s' % (sedol)
	html_doc = getHttpPage(url)

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


# Use youinvest, as it gives NAV:
# https://www.youinvest.co.uk/market-research/FUND%3AB5BFJG7
def getCurrentFundNav(sedol):
	"""Get the current price of the specified fund in pounds. Returns (title, value)"""

		#  https://www.youinvest.co.uk/market-research/FUND%3AB5BFJG7
	url = 'https://www.youinvest.co.uk/market-research/FUND%%3A%s' % (sedol)
	html_doc = getHttpPage(url)

	soup = BeautifulSoup(html_doc, 'html.parser')
	#print(soup.prettify())
	#exit(0)

    # <span class="securityName">
    # iShares Global Property Securities Equity Index Fund (UK) D Acc
    # </span>
	fs = soup.findAll(attrs={"class" : "securityName"})
	if len(fs) > 0:
		title = fs[0].contents[0]
	else:
		title = soup.title.contents[0]
		title = title[:title.find(' -')]

    # <tr class="alternate" id="KeyStatsLatestNav">
	#	<th scope="row">
	#		NAV
	#		<span class="date">12/06/2020</span>
	#	</th>
	#	<td>
	#		GBX 196.30
	#	</td>
	# </tr>
	try:
		navHtml = soup.find(id='KeyStatsLatestNav')

		# Determine the date of the valuation (not currently used
		date = navHtml.find(attrs={'class': 'date'}).contents[0]

		nav = navHtml.td.contents[0]
		space = nav.find(' ')
		if space != -1:
			currency = nav[:space]
			nav = nav[space+1:]
			# GBX means pence, while GBP means pounds
			if currency == 'GBX':
				# Need to convert to pounds
				value = Decimal(nav) / 100
			else:
				value = Decimal(nav)
		else:
			value = Decimal(nav)

	except:
		print("There was a problem fetching NAV from " + url)
		return (None, None)

	return (title, value)


#https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=B545NX9
def getCurrentFundPrice(sedol):
	"""Get the current price of the specified fund. Returns (title, value)"""

		#  https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=B545NX9
	url = 'https://www.charles-stanley-direct.co.uk/ViewFund?Sedol=%s' % (sedol)
	html_doc = getHttpPage(url)

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

	#print("fetching price for '%s'" % (sedol))

	if sedol == "CASH":
		# CASH is currently used to capture dividend / interest
		result = ("Cash", 1.0)
	else:
		result = getCurrentSharePrice(sedol)
		if result[0] == None:
			#result = getCurrentFundPrice(sedol)
			result = getCurrentFundNav(sedol)

	return result
