## Usage

```
Usage: run_scrape.py [options] stationcallsigns 
 'Stationcallsigns' is a space-delimited list of station callsigns

Options:
  -h, --help  show this help message and exit
  -v          Print debugging output
 
```

Output from run_scrape goes by default to station_listing/CALLSIGN.csv. Note that sometimes callsigns include '-TV' and sometimes they don't. The script will look for the list of years specified in scrape_settings.py under YEAR_LIST.

The output csvs include a timestamped header row like this:

	This file contains political files uploaded by WCAU during the years 2014 as of 2014-06-20 15:14:44.459634. This station serves PHILADELPHIA, PA in the PHILADELPHIA market and FCC's partyName--generally the owner-- is NBC TELEMUNDO LICENSE LLC. FCC records give the rfChannel as 34, virtualChannel as 10 and network affiiliate as NBC.