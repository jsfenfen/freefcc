"""

Based on observations

"""
import re

line_captures = [
    
    {'name':'contract',
    'regex': re.compile('Contract\s*\/\s*Revision\s+Alt Order \#\n.+?(\d\d\d\d\d\d+)\s*/\s*(\d*)\s*'),
    'num_values':2,
    'debug':False,
    'return_keys':['contract_number', 'revision']
    },
    {'name':'flight dates',
    'regex': re.compile("www.thewmurchannel.com\s+(\d\d/\d\d/\d\d)\s*\-\s*(\d\d/\d\d/\d\d)"),
    'num_values':2,
    'debug':False,
    'return_keys':['flight_date_start', 'flight_date_end']
    },
    {'name':'totals',
    'regex': re.compile("Totals\s+(\d+)\s{5,}\$([\d\,\.]+)\s{5,}\(\$([\d\,\.]+)\)\s{5,}"),
    'num_values':3,
    'debug':False,
    'return_keys':['number_of_spots', 'gross_amount', 'agency_commission']
    },
    {'name':'advertiser',
    'regex': re.compile("Advertiser\s*Original\s+Date\s*\/\s*Revision\s*\n\s*(.+?)\s+(\d\d\/\d\d\/\d\d)\s*\/\s*(\d\d\/\d\d\/\d\d)"),
    'num_values':3,
    'debug':False,
    'return_keys':['advertiser', 'original_date', 'revision_date']
    },
    {'name':'demographic',
    'regex': re.compile("Demographic\s*\n\s*(.+?)\s*\n"),
    'num_values':1,
    'debug':False,
    'return_keys':['demographic']
    },
    {'name':'print_date',
    'regex': re.compile("Print Date\s{5,}(\d\d\/\d\d\/\d\d)\s{5,}Page"),
    'num_values':1,
    'debug':True,
    'return_keys':['print_date']
    },
    
    # Print Date       10/20/15               Page
]