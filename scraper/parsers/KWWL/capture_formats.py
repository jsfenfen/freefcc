"""

Based on observations

"""
import re

line_captures = [
    
    {'name':'contract',
    'regex': re.compile("Contract \#\s+(\d+)"),
    'num_values':1,
    'debug':False,
    'return_keys':['contract_number']
    },
    {'name':'flight dates',
    'regex': re.compile("Schedule Dates\s+(\d\d/\d\d/\d\d)\-(\d\d/\d\d/\d\d)"),
    'num_values':2,
    'debug':False,
    'return_keys':['flight_date_start', 'flight_date_end']
    },
    {'name':'totals',
    'regex': re.compile("Grand Total:\s+(\d+)\s{5,}\$([\d\,\.]+)"),
    'num_values':2,
    'debug':False,
    'return_keys':['number_of_spots', 'gross_amount']
    },
    {'name':'name_advertiser',
    'regex': re.compile("KWWL Television Inc\s+(.+?)\s+Entered By"),
    'num_values':1,
    'debug':True,
    'return_keys':['advertiser_name']
    },
    {'name':'name_agency',
    'regex': re.compile("\n\s+(.+?)\s+Buyer Name"),
    'num_values':1,
    'debug':True,
    'return_keys':['agency_name']
    },
    {'name':'date_entered',
    'regex': re.compile("Date Entered\s+(\d\d/\d\d/\d\d)"),
    'num_values':1,
    'debug':True,
    'return_keys':['date_entered']
    },
    {'name':'date_modified',
    'regex': re.compile("Last Modified\s+(\d\d/\d\d/\d\d)"),
    'num_values':1,
    'debug':True,
    'return_keys':['date_modified']
    },
    #Date Entered           07/02/14
    
    # Great American Media --EDI                                     Buyer Name
    
    
    
    #KWWL Television Inc                                      Democratic Senate Campaign Com (23311)                     Entered By
    
]