import re

class atomic_line_parser(object):
    """ 
    A simple style of parser where each value captured can be completely described by a single regex that spans just one line.
    Multiple values are allowed. Only the first line that matches the regular expression is included.
    
    The data to be captured must be passed in in a structure that looks like the below. Return keys is always an array
    even if it contains just one element. 
    
    
    line_captures = [

        {'name':'Top Line printing summary',
        'regex': re.compile("Print Date\s+(\d\d/\d\d/\d\d)\s+(\d\d\:\d\d:\d\d)\s+Page\s+(\d+)\s+of\s+(\d+)"),
        'num_values':4,
        'debug':True,
        'return_keys':['print_date', 'print_time', 'start_page', 'num_pages']
        },
        {'name':'Another thing',
        'regex': re.compile("a regex that captures one (1) value"),
        'num_values':1,
        'debug':True,
        'return_keys':['some_thing'']
        }
        ...
        ]
        
        
        Parsing is not sped up or optimized in any way. Every regex that hasn't been found is checked in every line. 
        Best practice is to put them in the approximate order they are likely to appear.
        
        For more sensitive parsing, look at nested_line_parser.
        
    """
    
    line_captures = None
    
    def __init__(self, line_captures):
        self.line_captures = line_captures
    
    def get_keys(self, default_dict=None):
        """ return just the keys -- suitable for constructing a header row. """
        capture_keys = []
        for line_capture in line_captures:
            capture_keys = capture_keys + line_capture['return_keys']
        
        # Deal with defaults--which could be existing keys or new ones.
        if default_dict:
            for key in default_dict:
                if key not in capture_keys:
                    capture_keys.append(key)
                    
        return capture_keys
    
    def process_file(self, filename, default_dict=None):
        # defaults dict can be default values for things that we're trying to capture--
        # or supplementary data that gets added to every row. 
        
        # reset values:
        for capture in self.line_captures:
            capture['found'] = False
            capture['results'] = None

        print "\nReading %s" % (filename)
        infile = open(filename, "r")
        for line in infile:
            for capture_attempt in self.line_captures:
                if not capture_attempt['found']:
                    result = re.search(capture_attempt['regex'], line)
                    if result:
                        capture_attempt['found'] = True

                        results = []
                        for i in range(1,capture_attempt['num_values']+1):
                            results.append(result.group(i))
                        capture_attempt['results'] = results

        
        return_dict = {}
        if default_dict:
            return_dict = default_dict
            
        for capture in self.line_captures:
            if capture['debug']:
                if capture['found']:
                    print "Got %s : '%s'" % (capture['name'], capture['results'])
                else:
                    print "**Missing %s" % (capture['name'])
            if capture['found']:
                for i in range(0,capture['num_values']):
                    return_key = capture['return_keys'][i]
                    return_value = capture['results'][i]
                    return_dict[return_key] = return_value
        
                
        return return_dict



if __name__ == "__main__":

    line_captures = [

        {'name':'Top Line printing summary',
        'regex': re.compile("Print Date\s+(\d\d/\d\d/\d\d)\s+(\d\d\:\d\d:\d\d)\s+Page\s+(\d+)\s+of\s+(\d+)"),
        'num_values':4,
        'debug':True,
        'return_keys':['print_date', 'print_time', 'start_page', 'num_pages']
        },

        {'name':'Order / Revision',
        'regex': re.compile("Orders\s+Order / Rev:\s+([\d\w\s]+)\s+\Z"),
        'num_values':1, 
        'debug':True,
        'return_keys':['order_revision']
        },

        {'name':'Alt Order / Revision',
        'regex': re.compile("Alt Order #:\s+([\d\w\s]+)\s+\Z"),
        'num_values':1, 
        'debug':False,
        'return_keys':['alt_order_revision']

        },

        {'name':'Product Description',
        'regex': re.compile("Product Desc:\s+(.+)\s+\Z"),
        'num_values':1, 
        'debug':True,
        'return_keys':['product_description']
        },

        {'name':'Flight Dates',
        'regex': re.compile("Flight Dates:\s+(\d\d/\d\d/\d\d)\s+\-\s+(\d\d/\d\d/\d\d)\s+"),
        'num_values':2, 
        'debug':True,
        'return_keys':['flight_date_start', 'flight_date_end']
        },

        {'name':'Original Date / Revision Date',
        'regex': re.compile("Original Date / Rev:\s+(\d\d/\d\d/\d\d)\s+/\s+(\d\d/\d\d/\d\d)\s+"),
        'num_values':2, 
        'debug':True,
        'return_keys':['original_date', 'revision_date']
        },

        {'name':'Agency name',
        'regex': re.compile("Agency\s+Name:\s+(.+)\s+\Z"),
        'num_values':1, 
        'debug':True,
        'return_keys':['agency_name']
        },

        {'name':'Advertiser name',
        'regex': re.compile("Advertiser\s+Name:\s+(.+)\s+\Z"),
        'num_values':1, 
        'debug':True,
        'return_keys':['advertiser_name']
        },

        {'name':'Demographic',
        'regex': re.compile("Demographic:\s+(.+?)\s+New"),
        'num_values':1, 
        'debug':True,
        'return_keys':['demographic']
        },

        {'name':'Product Codes',
        'regex': re.compile("Product Codes:\s+(.+?)\s+Order"),
        'num_values':1, 
        'debug':True, 
        'return_keys':['product_codes']
        },

        {'name':'Priority',
        'regex': re.compile("Priority:\s+(.+?)\s+Advertiser"),
        'num_values':1, 
        'debug':True,
        'return_keys':['priority']
        },

        {'name':'Revenue Codes',
        'regex': re.compile("Revenue Codes: \s+(.+?)\s+Agency"),
        'num_values':1, 
        'debug':True,
        'return_keys':['revenue codes']
        },

        # # Spots      Gross Amount      Net Amount         Rating
        {'name':'Totals',
        'regex': re.compile("Totals\s+([\d,]+)\s+(\$[\d\.,]+)\s+(\$[\d\.,]+)\s+([\d\.,]+)"),
        'num_values':4, 
        'debug':True,
        'return_keys':['number_of_spots', 'gross_amount', 'net_amount', 'rating']
        },

        {'name':'WBTV share',
        'regex': re.compile("\AWBTV\s+(\d+)\%\s+(\$[\d\.,]+)\s+"),
        'num_values':2, 
        'debug':True,
        'return_keys':['wbtv_share', 'wbtv_total']
        },
        {'name':'Market total',
        'regex': re.compile("\Market\s+100\%\s+(\$[\d\.,]+)\s+"),
        'num_values':1, 
        'debug':True,
        'return_keys':['market_total']
        },
    ]

    parser = atomic_line_parser(line_captures)
    defaults = {'journal':1}
    keys = parser.get_keys(defaults)
    print keys
    result = parser.process_file("/Users/jfenton/political_ad_sleuth/text_extract_experiments/scripts/pdfs/14006947688403.txt", defaults)
    print result