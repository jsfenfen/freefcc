"""

Based on observations

"""
import re

line_captures = [
    
    {'name':'order_number',
    'regex': re.compile("AGREEMENT MADE BETWEEN\s+CONTRACT NO\.\s+REV\..?\n\s+([\d\-]+)"),
    'num_values':1,
    'debug':False,
    'return_keys':['order_number']
    },
    {'name':'date_printed',
    'regex': re.compile("DATE PRINTED\s*\n\s+(\d\d/\d\d/\d\d)"),
    'num_values':1,
    'debug':False,
    'return_keys':['print_date']
    },
    {'name':'name_advertiser',
    'regex': re.compile("NAME\s+(.+?)\s{10,}(.+?)\s*\n"),
    'num_values':2,
    'debug':False,
    'return_keys':['agency_name', 'advertiser_name']
    },
    {'name':'contact_product',
    'regex': re.compile("CONTACT\s+(.+?)\s{10,}PRODUCT(.+?)\s*\n"),
    'num_values':2,
    'debug':False,
    'return_keys':['agency_contact', 'product']
    },
    {'name':'Flight Dates',
    'regex': re.compile("BROADCAST SCHEDULE STARTING\s+(\d\d/\d\d/\d\d)\s+AND ENDING\s+(\d\d/\d\d/\d\d)\s{10,}"),
    'num_values':2, 
    'debug':False,
    'return_keys':['flight_date_start', 'flight_date_end']
    },
    {'name':'Totals',
    'regex': re.compile("Total Contract:\s+(\d+)\s{5,}([\d\.]+)\s*\n"),
    'num_values':2, 
    'debug':True,
    'return_keys':['number_of_spots', 'gross_amount']
    },
    
    
]