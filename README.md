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

### Yahoo

Yahoo can sometimes be useful for share prices in companies, e.g. the "historical data" on https://uk.finance.yahoo.com/quote/BA.L/history?p=BA.L
although there is no direct support for importing this as yet.

### ft.com

Another source might be e.g. https://markets.ft.com/data/funds/tearsheet/historical?s=GB00B545NX97:GBP although
there is no direct support for computer-based download.

### Company site

Sometimes the company will have downloadable historical data from their website, e.g. https://investors.baesystems.com/share-price-information/share-monitor
