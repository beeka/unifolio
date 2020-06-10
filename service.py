#!/usr/bin/env python
# Script runs the fetch and evaluation nightly

def update():
	print("Updating!")

	import tracker
	tracker.updateAll()

	from datetime import datetime
	now = datetime.now()
	
	import portfolio as folio
	portfolio = folio.getPortfolioAt(now)

	import valuator
	value = valuator.getPortfolioValueAt(now, portfolio = portfolio)
	
	print("Portfolio at", now.strftime('%Y-%m-%d %H:%M:%S'), "is")
	portfolio.dump()
	print("Current portfolio value is", value)
	
	import grapher
	grapher.graph()


def runScheduler():
	import time
	
	# Simple schedule to start with... every five minutes
	while True:
		update()
		time.sleep(300) # 300 seconds -> 5 minutes


if __name__ == "__main__":
	# execute only if run as a script
	runScheduler()
