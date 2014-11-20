The folders in this dir named for callsigns contain scripts to help parsing pdf files retrieved from those stations and then converted to text. In a few cases we've uploaded the actual .csv files that are the result of them.

This stuff is incredibly messy, but in general the best approach is to pick only one file type and sum ads of that type. Some stations include both orders and contracts--the best bet is to pick the one that appears most consistently. Conscientious station maintainers will do a good job of uploading copies of both, but clearly this is very personality driven. 

These parsers require the two scripts in the parent directory have already been run--specifically, run_scrape to get a current snapshot of files in the stations' stations.fcc.gov page, and retrieve_files to grab the files and run pdfinfo on them. The output of retrieve_files is a manifest file that's saved in a location determined by the scrape_settings.py file (also up a directory). That settings file also determines a file location for the downloaded pdfs to go, as well as the text files converted from the pdfs. 

The manifest file is generally worth a look. Image-based pdfs tend to be much bigger, and sorting the manifest file by memory per page can help show whether (and which) files are available as text-based pdfs. 

The parsing scripts preserve the data in the manifest file and add columns to it. The columns are generally defined in the capture_formats.py file in each station subdirectory. 

Note that different parsers pull different data. Some station formats allow certain data to be pulled. For instance, WCAU includes a line that says DELETED CONTRACT in deleted contracts. 

In general the parsers use one of two approaches--an atomic line parser--which grabs data using collections of regexes that operate against a single line only, or with a multiline parser, which allows regexes to span multiple lines. 

The return_keys defined in the capture formats function as a hash, so multiple attempts can be made to find the data. For instance, if the totals sometimes appear in a line that discloses a commission, and sometimes doesn't, regexes can search for both variations of these lines. Just remember that data retrieved through the last regex successfully applied will replace data from the same return_key.