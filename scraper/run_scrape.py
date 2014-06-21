# Note: Gotta put quotes around single URL's if processing one at a time
# https://stations.fcc.gov/station-profile/ksgw-tv/political-files/browse->2012
# The > in the url breaks the command line
import sys, csv, os
from scrape_settings import settings

import optparse
from fcc_scraper import folder_placeholder
from utils import mandated_stations, parse_folder_url, get_data_about_callsign, write_station_metadata, printif

YEAR_LIST = settings['YEAR_LIST']
CSV_LOCATION = settings['CSV_LOCATION']

def check_output(csvoutputfile):
    exists = os.path.isfile(csvoutputfile)
    if exists:
        not_valid_response = True
        response = None
        while not_valid_response:
            response = raw_input("The csv file already exists. Do you want to overwrite? (y or n) ")
            if response.upper() in ['Y', 'N']:
                not_valid_response = False
                if response.upper() == 'N':
                    print "Exiting"
                    sys.exit()
            else:
                print "Please respond y or n. "
    return True
    
if __name__ == '__main__':
    
    usage = "usage: %prog [options] stationcallsigns \n 'Stationcallsigns' is a space-delimited list of station callsigns"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-v', action="store_true", default=False, dest='verbose', help='Print debugging output')
    options, args = parser.parse_args()

    if len(args) == 0:
        print parser.print_help()
        sys.exit()
    
    # We used to allow a single folder to be scraped, but that's not all that useful. 
    process_recursively = True
    verbose = options.verbose
                    
    for this_callsign in args:
        this_callsign = this_callsign.upper()
        printif("Processing TV station %s" % (this_callsign), verbose)
        station_data = get_data_about_callsign(this_callsign)
        printif(station_data, verbose)
        csvoutputfile = CSV_LOCATION % (this_callsign)
        # Don't overwrite without confirmation
        check_output(csvoutputfile)
        
        print "Writing output to %s" % (csvoutputfile)
        fh = open(csvoutputfile, 'w')
        write_station_metadata(fh, station_data, YEAR_LIST)        
        fieldnames = ['file_url', 'file_size', 'callsign', 'upload_time']
        fh.write(",".join(fieldnames) + "\n")
        dictwriter = csv.DictWriter(fh, fieldnames=fieldnames, restval='', extrasaction='ignore')
        
        
        # There's confusion as to when files need to get uploaded
        for year in (YEAR_LIST):
            url = "https://stations.fcc.gov/station-profile/%s/political-files/browse->%s" % (this_callsign, year)
            printif ("Collection files from year=%s with root folder=%s" % (year, url), verbose)
            this_folder = folder_placeholder(url, 'root', this_callsign)
            this_folder.process(dictwriter)
            
            print "\n\n*** now printing childfiles: *****\n\n"
            print this_folder.childfiles
