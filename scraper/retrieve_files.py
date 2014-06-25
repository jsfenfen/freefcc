# get the files specified in the station_listing file, get info about them from pdfinfo, parse them with the layout option
# and print the layout option to another file. 

import optparse, csv, sys, os, re, urllib2, subprocess
from scrape_settings import settings
from wrap_pdfinfo import pdfinfo
from urlparse import urlparse
from time import sleep


CSV_LOCATION = settings['CSV_LOCATION']
MANIFEST_LOCATION = settings['MANIFEST_LOCATION']
PDF_DIR = settings['PDF_DIR']
TXT_DIR = settings['TXT_DIR']
SCRAPER_USER_AGENT_STRING = settings['SCRAPER_USER_AGENT_STRING']
SCRAPE_DELAY_TIME = settings['SCRAPE_DELAY_TIME']

fcc_infile_identifier = re.compile(r'\((\d{14})\)')

# row {'upload_time': '2014-06-03 16:38:00', 'callsign': 'KMGH-TV', 'file_url': 'https://stations.fcc.gov/collect/files/40875/Political File/2014/Federal/US Senate/Gardner 6-10-6-16 412189 (14018279082972).pdf', 'file_size': '20.90 Kb'}

def read_url(url, dry_run=False):
    # read url with our headers.
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', SCRAPER_USER_AGENT_STRING)]
    parsed_url = urlparse(url)
    final_url = "%s://%s%s" % (parsed_url.scheme, parsed_url.netloc, urllib2.quote(parsed_url.path))
    
    # deal with comma issue
    final_url = final_url.replace("%2C", ",")
    final_url = final_url.replace("%2c", ",")
    final_url = final_url.replace("%27", "'")
    
    #print("trying to read url: %s" % (final_url))
    page = None
    if not dry_run:
        page = opener.open(final_url).read()
    return page

if __name__ == '__main__':
    
    usage = "usage: %prog [options] stationcallsigns \n 'Stationcallsigns' is a space-delimited list of station callsigns"
    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()


    if len(args) == 0:
        print parser.print_help()
        sys.exit()
    
    field_names = ['file_url', 'upload_time', 'callsign', 'file_size', 'fcc_id', 'pdf_location', 'txt_location', 'Tagged', 'Producer', 'Creator', 'Encrypted', 'Author', 'File size', 'Optimized', 'PDF version', 'Title', 'Page size', 'CreationDate', 'Pages']
    
    
    for this_callsign in args:
        
        this_callsign = this_callsign.upper()
        csvlisting = CSV_LOCATION % (this_callsign)
        
        manifestfile = MANIFEST_LOCATION % (this_callsign)
        outfile = open(manifestfile, 'w')
        
        
        infile = open(csvlisting,'rb')
        # Skip the first line, but instead write it to the output file.  
        filedata = next(infile)        
        outfile.write('"' + filedata + '"' + "\n")
        # write the header row
        outfile.write(",".join(field_names) +"\n")
        dw = csv.DictWriter(outfile, fieldnames=field_names, restval='', extrasaction='ignore')
        
        reader = csv.DictReader(infile)
        for row in reader:
            if not row['file_url']:
                continue
            print "handling row " + str(row)
            fcc_id = re.search(fcc_infile_identifier, row['file_url']).group(1)
            pdf_location = PDF_DIR + fcc_id + ".pdf"
            
            row['callsign'] = this_callsign
            row['fcc_id'] = fcc_id
            row['pdf_location'] = pdf_location
            url = row['file_url']
            # only download it if we don't need it. 
            if not os.path.isfile(pdf_location):
                try:
                    print "retrieving file from %s" % (url)
                    result = read_url(url)
                    pdfout = open(pdf_location, 'wg')
                    pdfout.write(result)
                    pdfout.close()
                    
                    print "Sleeping %s seconds" % (SCRAPE_DELAY_TIME)
                    sleep(SCRAPE_DELAY_TIME)

                except urllib2.HTTPError:
                    print "MISSING %s" % url
                    continue
            
            # get pdfinfo data
            pdf_data = None
            try:
                pdf_data = pdfinfo(pdf_location)
            except subprocess.CalledProcessError:
                # if the file is totally broken sometimes we'll get this--just continue.
                pass
            print pdf_data
            # Data should look like: {'Tagged': 'no', 'Producer': 'ReportBuilder', 'Creator': '', 'Encrypted': 'no', 'Author': '', 'File size': '20931 bytes', 'Optimized': 'no', 'PDF version': '1.3', 'Title': '', 'Page size': '612 x 792.003 pts (letter)', 'CreationDate': 'Wed Jun  4 06:24:34 2014', 'Pages': '2'}
            txt_location = TXT_DIR + fcc_id + ".txt"
            row['txt_location'] = txt_location
            if not os.path.isfile(txt_location):
                print "converting to text"
                # assumes we can execute pdflayout
                cmd = "pdftotext -layout %s %s" % (pdf_location, txt_location)
                print "Running cmd: " + cmd
                # use the less problematic older style of shell execution; assumes access to pdftotext from whatever is getting called.
                os.system(cmd)
            
            if pdf_data:
                result_dict = dict(row.items() + pdf_data.items())
            else:
                result_dict = row
                
            dw.writerow(result_dict)
        
        outfile.close()
        infile.close()