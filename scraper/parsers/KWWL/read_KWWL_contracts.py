import csv
from os import sys, path

# add one directory up to sys.path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from multiline_parser import multiline_parser
from capture_formats import line_captures

# where the data on the files is
manifest_file = "../../manifest_files/KWWL.csv"

infile = open(manifest_file,'rb')
# Skip the first line, but instead write it to the output file.  
filedata = next(infile)

# where the result csv goes. Put in this dir for now.
outfilename = "KWWL_read.csv"
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
    fileid = row['fcc_id']
    intid = int(fileid)
    url_fixed = row['file_url'].upper()
    
    ## This is a KYW-specific naming convention, apparently. 
    #print "\n\n" + row['file_url']
    this_file_types = 0
    # THESE AREN'T REALLY ALL NABS, BUT WE'RE NOT GONNA PROCESS THEM
    if url_fixed.find('-REQUEST') > 0 or url_fixed.find('-NAB') > 0 or url_fixed.find('-CHECKLIST') > 0 or url_fixed.find('-LOA') > 0 or url_fixed.find('-CERTIFICATION') > 0:
        nabs +=1
        this_file_types += 1
        #print "type = nab / basefile"
        
    if url_fixed.find('-CONTRACT') > 0 or url_fixed.find('-TRACT') > 0:
        contracts +=1
        this_file_types += 1
        #print "type = contract"
        #print "filename = %s original = %s" % (filename, row['file_url'])
        
        ## only parse if it's a contract
        result = parser.process_file(filename, row)
        dw.writerow(result)
        

    if this_file_types == 0:
        print "Unknown type: %s" % row['file_url']
    
    # make sure we haven't tagged anything as being two types of files. 
    assert this_file_types < 2, row['file_url']
            
print "(contracts=%s, invoices=%s, orders=%s, nabs=%s) , total classified =  %s" % (contracts, invoices, orders, nabs, (contracts + invoices + orders + nabs) )
print "total files = %s" % (total_rows)
    
    # try to figure out what kind it is. 
