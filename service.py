#!/usr/bin/env python
# Script runs the fetch and evaluation nightly

from datetime import *

def update():
	try:
		import tracker
		tracker.updateAll()
	except:
		print("Error updating prices, using what we have")

	from datetime import datetime
	now = datetime.now()
	
	import portfolio as folio
	portfolio = folio.getPortfolioAt(now)

	import valuator
	value = valuator.getPortfolioValueAt(now, portfolio = portfolio)
	
	import paths
	statusPath = paths.dataFilePath("portfolio.txt")
	with open(statusPath, 'w') as statusFile:
		print("Portfolio at", now.strftime('%Y-%m-%d %H:%M:%S'), "is", file = statusFile)
		portfolio.dump(statusFile)
		print("Current portfolio value is", value, file = statusFile)
	
	import grapher
	history = grapher.determineUnitHistory()
	historyPath = paths.dataFilePath("history.csv")
	grapher.writeUnitHistory(history, historyPath)

	perf = grapher.determinePerformance(history)
	performancePath = paths.dataFilePath("performance.txt")
	grapher.writePerformance(perf, performancePath)



def runScheduler():
	from time import sleep
	
	# Run on startup, as it proves things are working (if nothing else)
	update()
	
	# Set the next run time for 11pm today
	nextTime = datetime.combine(date.today(), time(23, 0,0 , 0))
	print("Sleeping until", nextTime.strftime('%d/%m/%Y %H:%M'))
	
	# Simple schedule to start with... every five minutes
	while True:
		if datetime.now() > nextTime:

			print("Running portfolio update at", datetime.now().strftime('%d/%m/%Y %H:%M'))
			update()

			nextTime = nextTime + timedelta(days = 1)
			print("Sleeping until", nextTime.strftime('%d/%m/%Y %H:%M'))

		# Wait a while before checking again
		sleep(300) # 300 seconds -> 5 minutes


if __name__ == "__main__":
	# execute only if run as a script
	runScheduler()
