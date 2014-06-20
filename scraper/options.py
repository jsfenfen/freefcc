import optparse, sys

usage = "usage: %prog [options] stationcallsigns \n 'Stationcallsigns' is a space-delimited list of station callsigns"
parser = optparse.OptionParser(usage=usage)
parser.add_option('-v', action="store_true", default=False, dest='verbose', help='Print debugging output')
parser.add_option('-m', action="store", default=False, dest='manifest_file', help='Save the manifest file to a specific location')


options, args = parser.parse_args()

if len(args) == 0:
    print parser.print_help()

not_valid_response = True
response = None
while not_valid_response:
    response = raw_input("Do you want to overwrite? (y or n) ")
    if response.upper() in ['Y', 'N']:
        not_valid_response = False
        if response.upper() == 'N':
            print "Exiting"
            sys.exit()
    else:
        print "Please respond y or n. "

print "Still live"

# https://data.fcc.gov/mediabureau/v01/tv/facility/search/KCCI.json