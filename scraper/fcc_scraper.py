import re
import urllib2
import traceback

from time import sleep
from datetime import datetime, date
from dateutil.parser import parse as dateparse

from scrape_settings import settings

from BeautifulSoup import BeautifulSoup

# from models import PDF_File, Folder
# from local_log import fcc_logger
from utils import read_url

size_re = re.compile(r'<div class="size">(.*?)</div>')
type_re = re.compile(r'<div class="type">(.*?)</div>')
date_re = re.compile(r'<div class="date">(.*?)</div>')

folder_re = re.compile(r'<div class="(.*?)"><a href="(.*?)">', re.I)

# old style:
# pdf_re = re.compile(r'<div id="(.*?)" class="(.*?)"><a target="_blank" title="(.*?)" href="(.*?)">')

# Now there may be multiple files, some of which are converted pdfs. We want the converted pdfs only. It would be nice to grab the original files too, but unclear about sane way to process these... 
pdf_re = re.compile(r'<div id="(.*?)" class="(.*?)">.*<a target="_blank" title="(.*?)" href="(.*?\.pdf)">', re.DOTALL|re.IGNORECASE)


# assumes we're looking at 2012
folder_url_re = re.compile(r'https://stations.fcc.gov/station-profile/(.*?)/political-files/browse->(.*)')
file_url_re = re.compile(r'https://stations.fcc.gov/collect/files/(\d+)/Political File/(.+)')


SCRAPE_DELAY_TIME = settings['SCRAPE_DELAY_TIME']

today = datetime.today()
todays_date = today.strftime("%m/%d/%Y")

# my_logger=fcc_logger()
# my_logger.info("starting run...")

def clean_path(url):
    url = url.replace('&gt;', '>')
    url = url.replace('%3e', '>')
    url = url.replace('%3E', '>')
    return url

def parse_folder_url(url):
    url_parts = re.findall(folder_url_re, url)
    (callSign, pathArray) = (None, None)
    if url_parts:
        callSign = url_parts[0][0]
        path = url_parts[0][1]
        path = path.replace('&gt;', '>')
        path = path.replace('%3e', '>')        
        pathArray = path.split('->')
    else: 
        print "Couldn't parse folder file path %s" % (url)
        
    return callSign, pathArray
    
def parse_file_url(url):
    url_parts = re.findall(file_url_re, url)
    (fac_id, pathArray) = (None, None)
    if url_parts:
        fac_id = url_parts[0][0]
        path = url_parts[0][1]
        pathArray = path.split('/')
    else: 
        print "Couldn't parse file path %s" % (url)
        
    return fac_id, pathArray


def parse_li(li_html):
    #print "<<<" + li_html + ">>>"
    size = re.findall(size_re, li_html)
    linktype = re.findall(type_re, li_html)
    date = re.findall(date_re, li_html)
    
    (sizefound, typefound, datefound) = (None, None, None)
    if size:
        sizefound = size[0]
    else:
        print "** Size missing in " + li_html
        
    if linktype:
        typefound = linktype[0]
    else:
        print "** Type missing in " + li_html
    
    if date:
        datefound = date[0]
    else:
        print "** Date missing in " + li_html
    
    return (sizefound, typefound, datefound)

def parse_folder_div(div_html):
    # <div class="name folder   public"><a href="https://stations.fcc.gov/station-profile/ksgw-tv/political-files/browse-%3e2012-%3efederal-&gt;US_Senate">US_Senate"&gt;<span class="icon "></span> &nbsp;&nbsp;&nbsp;US Senate</a></div>
    folder = re.findall(folder_re, div_html)
    (folder_class, folder_link) = (None, None)
    if folder:
        folder_class = folder[0][0]
        folder_link = folder[0][1]
    else:
        print "No match in folder re: %s" % div_html
    return (folder_class, folder_link)

def parse_pdf_div(div_html):
    pdf = re.findall(pdf_re, div_html)
    (fileid, fileclass, title, href) = (None, None, None, None)
    if pdf:
        [fileid, fileclass, title, href] = pdf[0]
        print "Found file %s match in %s " % (href, div_html)
    else:
        print "****No match in file re %s" % (div_html)
    return (fileid, fileclass, title, href)



class folder_placeholder(object):
    url = None
    # This is the css styling of the folder, which tells us what kind of folder it is
    folder_class = None
    # This is our classification of the folder, based on parsing the css class and other info. 
    folder_kind = None
    folder_title = None
    is_parsed = False
    is_downloaded = False
    path = []
    # How many child files are contained. Populated from the FCC site, not by counting the actual files. 
    size = 0
    callSign = None
    childfolders = []
    childfiles = []
    htmlText = None
    numFiles = None
    
    def __init__(self, sourceurl, folder_class, callSign, numFiles=None):
        self.url = clean_path(sourceurl)
        print "Starting folder %s %s %s %s" % (sourceurl, folder_class, callSign, numFiles)
        self.folder_class = folder_class
        self.callSign = callSign.upper()
        if (numFiles):
            self.numFiles = numFiles
            
        self.childfolders = []
        self.childfiles = []
        self.htmlText = None
        self.newly_created = False
        #(folder, created) = Folder.objects.get_or_create(raw_url=self.url, defaults={'size':self.numFiles,'callsign':self.callSign, 'folder_class':self.folder_class})
        #if not created:
        #    now = datetime.now()
        #    folder.scrape_time = now
        #    folder.save()
        #else:
        #    self.newly_created = True
        #self.folder = folder
        
    def read_page(self):
        self.htmlText = read_url(self.url)
        #print "Got html: %s" % (self.htmlText)
        is_downloaded = True
        (callSign, self.path) = parse_folder_url(self.url)
        self.folder_title = self.path[-1:]
        
        
    def parse(self):
        
        page_soup = BeautifulSoup(self.htmlText)
        folder_listings = page_soup.findAll("ol", { "class" : "file-view" })
        for folder in folder_listings:
            print "Got file-view listing from url %s" % (self.url)
            folderlis = folder.findAll("li")
            for folderli in folderlis:
                # Get the size, type and date
                (sizefound, typefound, datefound) = parse_li(str(folderli))
                numfiles = 0
                if sizefound:
                    try:
                        numfiles = int(sizefound)
                    except ValueError: 
                        pass 
                print "\t Typefound:: %s %s %s" % (typefound, sizefound, datefound)


                firstdiv = folderli.find("div")
                #print "firstdiv is: %s" % (str(firstdiv))
                if typefound == 'Folder':
                    (folder_class, folder_link) = parse_folder_div(str(firstdiv))
                    
                    folder_link = folder_link.replace("&gt;", "%3e")
                    folder_link = folder_link.replace("%2C", ",")
                    
                    print "\n\n\t\tFolder Path: %s \n from div %s" % (folder_link, str(firstdiv))
                    print "\tFolder: '%s' link: '%s'" % (folder_class, folder_link)
                    folderstub = {
                        'size':numfiles,
                        'url':folder_link,
                        'folder_class':folder_class,
                        'datefound':datefound,
                        'callSign':self.callSign,
                    }
                    self.childfolders.append(folderstub)
                    # parse the folder link
                    
      
                    #summary_filehandle.write("%s,%s,%s\n" % (numfiles, callSign, str(path) ) )


                else:
                    (fileid, fileclass, title, href) = parse_pdf_div(str(firstdiv))
                    filestub = {
                    'fileid':fileid,
                    'fileclass':fileclass,
                    'title':title,
                    'href':href,
                    'callSign':self.callSign,
                    'datefound':datefound,
                    'sizefound':sizefound
                    }
                    self.childfiles.append(filestub)




    def save_files(self, dictwriter):
        for thisfile in self.childfiles:
            upload_time = None
            try:
                timefound = thisfile['datefound']
                timefound = timefound.replace('Today at', todays_date)
                upload_time = dateparse(timefound)
            except:
                pass
            rowdata = {'file_url':thisfile['href'], 'file_size':thisfile['sizefound'],'callsign':self.callSign, 'upload_time':upload_time }
            
            # ignore rows missing files of unparseable.
            if rowdata['file_url']:
                print "Rowdata is " + str(rowdata)
                dictwriter.writerow(rowdata)
                #thisfile['href'], 'size':thisfile['sizefound'],'callsign':self.callSign, 'upload_time':upload_time})

    

    def process(self, dictwriter, recursive=True):
        try:
            self.read_page()
            self.parse()
            self.save_files(dictwriter)
        
        # If we hit an error just log it and keep rolling. 
        except:
            tb = traceback.format_exc()
            message = "*** Error trying to process URL:%s ***\n%s" % (self.url, tb)
            # my_logger.warn(message)
            print message
            return
        
        
        if recursive:
            for child in self.childfolders:
                if (child['size'] > 0):
                    childfolder = folder_placeholder(child['url'], child['folder_class'], self.callSign, child['size'])
                    childfolder.process(dictwriter)
                    sleep(SCRAPE_DELAY_TIME)
        

    
