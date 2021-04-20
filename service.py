#!/usr/bin/env python
# Script runs the fetch and evaluation nightly

from datetime import *

def updatePrices():
	try:
		import tracker
		tracker.updateAll()
	except:
		print("Error updating prices, using what we have")
		import traceback
		traceback.print_exc()



def updateAnalysis():
	from datetime import datetime
	now = datetime.now()
	
	import portfolio as folio
	portfolio = folio.getPortfolioAt(now)
	
	if len(portfolio.getEquities()) == 0:
		print("Nothing in the portfolio, so doing nothing")
		return

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



def nextOccurrenceOf(hours, minutes, seconds):
	# Set the next run time for the next 3am 
	nextTime = datetime.combine(date.today(), time(hours, minutes, seconds, 0))
	while datetime.now() > nextTime:
		nextTime = nextTime + timedelta(days = 1)

	return nextTime



def runScheduler():
	from time import sleep
	
	# Run on startup, as it proves things are working (if nothing else)
	updatePrices()
	updateAnalysis()
	
	nextPricesUpdateAt = nextOccurrenceOf(23, 0, 0) # Fetch prices at the end of the day
	nextAnalysisAt = nextOccurrenceOf(3, 0, 0) # 3am

	print("Prices will next update at", nextPricesUpdateAt.strftime('%d/%m/%Y %H:%M'))
	print("Analysis will next update at", nextAnalysisAt.strftime('%d/%m/%Y %H:%M'))
	
	# Check the timings every five minutes, forever
	while True:
		if datetime.now() > nextPricesUpdateAt:

			print("Running price update at", datetime.now().strftime('%d/%m/%Y %H:%M'))
			updatePrices()

			nextPricesUpdateAt = nextPricesUpdateAt + timedelta(days = 1)
			print("Sleeping until", nextPricesUpdateAt.strftime('%d/%m/%Y %H:%M'))

		if datetime.now() > nextAnalysisAt:

			print("Running analysis update at", datetime.now().strftime('%d/%m/%Y %H:%M'))
			updateAnalysis()

			nextAnalysisAt = nextAnalysisAt + timedelta(days = 1)
			print("Sleeping until", nextAnalysisAt.strftime('%d/%m/%Y %H:%M'))

		# Wait a while before checking again
		sleep(300) # 300 seconds -> 5 minutes


if __name__ == "__main__":
	# execute only if run as a script
	runScheduler()
