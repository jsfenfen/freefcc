import csv
from os import sys, path

## As of 12/15/15 the nab files have generated contracts and scanned disclosure forms in them
## so pdf2text converts the pages that are generated. 

## other observed file types are "CANCELLATION"

## Scanned files from Producer 'Xerox WorkCentre 7775' seem to not work. 

# add one directory up to sys.path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from multiline_parser import multiline_parser
from capture_formats import line_captures

# where the data on the files is
manifest_file = "../../manifest_files/WMUR-TV.csv"

infile = open(manifest_file,'rb')
# Skip the first line, but instead write it to the output file.  
filedata = next(infile)

# where the result csv goes. Put in this dir for now.
outfilename = "WMUR_read.csv"
outfile = open(outfilename, 'w')
# write the file data row to the first line of the output file
outfile.write(filedata)


reader = csv.DictReader(infile)
dataheaders = reader.fieldnames

parser = multiline_parser(line_captures)
field_names = parser.get_keys(dataheaders)

outfile.write(",".join(field_names) +"\n")
dw = csv.DictWriter(outfile, fieldnames=field_names, restval='', extrasaction='ignore')

(contracts, invoices, orders, nabs) = (0,0,0,0) 
total_rows = 0
for row in reader:
    

    total_rows += 1
    filename = "../../" + row['txt_location']
    # print "Reading filename %s" % (filename)
    fileid = row['fcc_id']
    intid = int(fileid)
    url_fixed = row['file_url'].upper()
    url_fixed = url_fixed.replace("%20", "+")
    url_fixed = url_fixed.replace("%2D", "+")

    # ignore the scanned in ones, they aren't converted. 
    if row['Producer'].find('Xerox WorkCentre') > -1:
        continue
        
    #print url_fixed
    #print "\n\n" + row['file_url']
    this_file_types = 0
    
    # THESE AREN'T REALLY ALL NABS, BUT WE'RE NOT GONNA PROCESS THEM
    if url_fixed.find('REV') > -1 or url_fixed.find('NAB') > -1 or url_fixed.find('PREBOOK') > -1 or url_fixed.find('PRE+') > -1:
        contracts +=1
        this_file_types += 1
        result = parser.process_file(filename, row)
        
        dw.writerow(result)
        
        # print "type = contract"
        
    elif url_fixed.find('INV') > -1:
        invoices +=1
        this_file_types += 1
        
        #print "type = invoice"
        #print "filename = %s original = %s" % (filename, row['file_url'])
        
        ## only parse if it's a contract
        #result = parser.process_file(filename, row)
        #dw.writerow(result)
        dw.writerow(row)
        
        

    if this_file_types == 0:
        
        print "*** Unknown type: %s" % url_fixed
        dw.writerow(row)
        
    
    # make sure we haven't tagged anything as being two types of files. 
    if (this_file_types  > 1 ): 
        print "*** Found multi part %s" % (url_fixed)
    
        
print "(contracts=%s, invoices=%s, orders=%s, nabs=%s) , total classified =  %s" % (contracts, invoices, orders, nabs, (contracts + invoices + orders + nabs) )
print "total files = %s" % (total_rows)
    
    # try to figure out what kind it is. 
