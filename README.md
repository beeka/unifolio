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
