# Unifolio

Unit-isation of a share portfolio transactions.


## Using within Docker

Build with:

	docker build --rm -t unifolio .


Run with:

	docker run --rm --volume data:/home/appuser/data -t -i unifolio


## Places to fetch data

The scripts need historic price data to generate sensible unitised past performance. The author has passive investing 
funds, such as BlackRock and Vanguard. Price data can be downloaded from the providers for these funds.

Data should be saved in a directory called "import" and the import.py script run to read the files in there and update
the csv files in the "prices" directory.

### BlackRock

After finding the product information page, e.g. https://www.blackrock.com/uk/individual/products/230271/blackrock-emerging-markets-equity-tracker-fund-class-d-acc-fund,
there is a "Download" link in the top-right of the page. This downloads as a fund-name.xls file, although no application wants to open it.

### Vanguard

Vanguard price history is available on the "Prices & Distributions" tab of the product information, e.g. 
https://www.vanguard.co.uk/adviser/adv/detail/mf/overview?portId=9156&assetCode=EQUITY##pricesanddistributions
A start date can be entered (e.g. 04-04-2014) and once the display updates the "export data" facility can be used to save
a csv file that must be named after the isin of the fund, e.g. GB00B3X7QG63.csv. The naming is important as the isin is
not contained in the downloaded file.

