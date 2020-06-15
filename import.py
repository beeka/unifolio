#!/usr/bin/env python
# Supports importing of downloaded price data


	
# e.g. from https://www.blackrock.com/uk/individual/products/230271/blackrock-emerging-markets-equity-tracker-fund-class-d-acc-fund?switchLocale=y&siteEntryPassthrough=true
def readIShares(xmlpath, csvpath = None):
	from decimal import Decimal
	from datetime import datetime, time

	with open(xmlpath) as f:

		values = dict()

		csvfile = None
		
		title = None
		isinNext = False
		isin = None
		
		date = None
		value = None
		for line in f:
			if 'Worksheet' in line and 'Performance' in line:
				#print(isin, len(values), 'values')
				break # already read 'Historical' worksheet
			elif 'ISIN' in line:
				isinNext = True
			elif '<ss:Data' in line:
				if isinNext == True:
					a = line.find('>')
					b = line.find('<', a)
					isin = line[a+1:b]
					isinNext = False
					csvpath = 'prices/%s.csv' % (isin)
					csvfile = open(csvpath, 'w')
					csvfile.write("date,value\n")

				elif 'String' in line: # This has the date
					# <ss:Data ss:Type=""String"">06-May-20</ss:Data>
					a = line.find('>')
					b = line.find('<', a)
					dateStr = line[a+1:b]
					if len(dateStr) == 9:
						try:
							# NB: The Date/Value is likely to be closing price on that date
							date = datetime.strptime(dateStr, '%d-%b-%y')
							date = datetime.combine(date, time(23, 59, 59))
						except:
							print("Error converting", dateStr)
							raise
				elif 'Number' in line:
					# "<ss:Data ss:Type=""Number"">1.517</ss:Data>"
					a = line.find('>')
					b = line.find('<', a)
					value = Decimal(line[a+1:b])
			if '</ss:Row>' in line:
				if date != None and value != None:
					csvfile.write("%s,%s\n" % (date.strftime('%Y-%m-%d %H:%M:%S.%f'), value))
					values[date] = value
					date = None
					value = None

				date = None
				value = None
	
	return csvpath


if __name__ == "__main__":
	# execute only if run as a script
	from glob import glob
	for xlsPath in glob('import/*.xls'):
		print("Importing BlackRock data from", xlsPath)
		csvPath = readIShares(xlsPath)
		print("Saved as", csvPath)
