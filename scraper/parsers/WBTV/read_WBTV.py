import csv
from os import sys, path

# add one directory up to sys.path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from atomic_line_parser import atomic_line_parser
from capture_formats import line_captures_current, line_captures_2013ish

# where the data on the files is
manifest_file = "../../manifest_files/WBTV.csv"

infile = open(manifest_file,'rb')
# Skip the first line, but instead write it to the output file.  
filedata = next(infile)

# where the result csv goes. Put in this dir for now.
outfilename = "WBTV_read.csv"
outfile = open(outfilename, 'w')
# write the file data row to the first line of the output file
outfile.write(filedata)


reader = csv.DictReader(infile)
dataheaders = reader.fieldnames

parser = atomic_line_parser(line_captures_current)
oldparser = atomic_line_parser(line_captures_2013ish)
field_names = parser.get_keys(dataheaders)

outfile.write(",".join(field_names) +"\n")
dw = csv.DictWriter(outfile, fieldnames=field_names, restval='', extrasaction='ignore')

for row in reader:
    #print row
    filename = "../../" + row['txt_location']
    fileid = row['fcc_id']
    intid = int(fileid)
    if intid < 13886716046591:
        result = oldparser.process_file(filename, row)
    else:
        result = parser.process_file(filename, row)
    dw.writerow(result)
    #print result
    