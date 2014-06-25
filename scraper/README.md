## Usage

```
Usage: run_scrape.py [options] stationcallsigns 
 'Stationcallsigns' is a space-delimited list of station callsigns

Options:
  -h, --help  show this help message and exit
  -v          Print debugging output
 
```

Output from run_scrape goes to a location specified by CSV_LOCATION in  scrape_settings.py--probably to station_listing/CALLSIGN.csv. Note that sometimes callsigns include '-TV' and sometimes they don't. The script will look for the list of years specified in scrape_settings.py under YEAR_LIST.

The output csvs include a timestamped info row like the below. A real set of headers follows beneath it. 

```
This file contains political files uploaded by WCAU during the years 2014 as of 2014-06-20 15:14:44.459634. This station serves PHILADELPHIA, PA in the PHILADELPHIA market and FCC's partyName--generally the owner-- is NBC TELEMUNDO LICENSE LLC. FCC records give the rfChannel as 34, virtualChannel as 10 and network affiiliate as NBC.
```

Once the file locations are written to the CSV_LOCATION directory, the actual files can be retrieved, converted to text, and analyzed with pdfinfo. To do this, run retrieve_files.py

```
Usage: retrieve_files.py [options] stationcallsigns 
 'Stationcallsigns' is a space-delimited list of station callsigns
```

The script will check if .pdf and .txt files already exist, and if so, will not redownload or recreate them. Pdfinfo, however, will be run on all of them. 

A csv file including the header row from the input csv file, as well as the data from pdfinfo will be written to MANIFEST_LOCATION - by default in manifest_files/<callsign>.csv. 

## Parsers

Parsers are station specific--and sometimes multiple parsers are required per station. In general these are put in /scrapers/parsers/\<CALLSIGN\>/ directories and called read_\<CALLSIGN\>.py though the -TV that sometimes appears has been cut off. In general these require some amount of curation--possibly lots and lots and lots. 
