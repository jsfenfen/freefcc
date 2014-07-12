import csv
from os import sys, path

# add one directory up to sys.path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from multiline_parser import multiline_parser
from capture_formats import invoice_line_captures as line_captures


from adspot_parser import process_file
# where the data on the files is
manifest_file = "../../manifest_files/KYW-TV.csv"

infile = open(manifest_file,'rb')
# Skip the first line, but instead write it to the output file.  
filedata = next(infile)

# where the result csv goes. Put in this dir for now.
outfilename = "KYW_invoice_spots_read.csv"
outfile = open(outfilename, 'w')
# write the file data row to the first line of the output file
outfile.write(filedata)


reader = csv.DictReader(infile)
dataheaders = reader.fieldnames

parser = multiline_parser(line_captures)
summary_field_names = parser.get_keys(dataheaders)
field_names = ['advertiser_name', 'agency_name', 'product', 'invoice_num', 'contract_num', 'contract_date_start', 'contract_date_end', 'number_of_spots', 'gross_amount', 'file_url', 'ad_number', 'name', 'contract_start', 'contract_stop', 'rundays', 'dur', 'spots', 'rate', 'make_good', 'air_date', 'day', 'air_time', 'mg_for_date', 'material', 'ad_dur', 'ad_rate', 'mg_debit_credit', 'mg_remarks']



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
    if url_fixed.find(' BASEFILE') > 0 or url_fixed.find(' NAB') > 0 or url_fixed.find(' PIQ') > 0:
        nabs +=1
        this_file_types += 1
        #print "type = nab / basefile"
        
    if url_fixed.find(' CONTRACT') > 0 or url_fixed.find(' TRACT') > 0:
        contracts +=1
        this_file_types += 1
        #print "filename = %s original = %s" % (filename, row['file_url'])        

    if url_fixed.find(' ORDER') > 0:
        orders +=1
        this_file_types += 1
        #print "type = order"
        
    if url_fixed.find(' INVOICE') > 0:
        invoices +=1
        this_file_types += 1
        print "type = invoice: %s" % (filename)
        
        results = process_file(filename)
        
        file_result = parser.process_file(filename, row)
        for ad in results:
            this_data = dict(ad.items() + file_result.items())
            #print this_data
            #print "\n"
            dw.writerow(this_data)
            
        
    
    if this_file_types == 0:
        print "Unknown type: %s" % url_fixed
    
    # make sure we haven't tagged anything as being two types of files. 
    assert this_file_types < 2, row['file_url']
            
print "(contracts=%s, invoices=%s, orders=%s, nabs=%s) , total classified =  %s" % (contracts, invoices, orders, nabs, (contracts + invoices + orders + nabs) )
print "total files = %s" % (total_rows)
    
    # try to figure out what kind it is. 
