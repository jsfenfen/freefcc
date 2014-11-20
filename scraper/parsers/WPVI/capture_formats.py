"""

Based on observations

"""
import re

line_captures = [
    
    {'name':'order_number',
    'regex': re.compile("Contract / Revision\s+Alt Order #.*\n\s+4100 City Avenue\s{6,}(\d{5})\s+\/\s+(\d*)\s+"),
    'num_values':2,
    'debug':True,
    'return_keys':['order_number', 'revision']
    },
    
    {'name':'product',
    'regex': re.compile("Product.*\n.+?\(215\) 878-9700(.*?)\n"),
    'num_values':1,
    'debug':True,
    'return_keys':['product']
    },
    
    {'name':'Flight Dates',
    'regex': re.compile("Contract Dates\s+Estimate \#\s*\n\s+(\d\d/\d\d/\d\d)\s+-\s+(\d\d/\d\d/\d\d)"),
    'num_values':2,
    'debug':True,
    'return_keys':['flight_date_start', 'flight_date_end']
    }, 
    
    {'name':'Advertiser, etc',
    'regex': re.compile("Advertiser\s+Original Date /\s+Revision\s*\n\s+(.+?)\s{10,}(\d\d/\d\d/\d\d)\s+\/\s+(\d\d/\d\d/\d\d)"),
    'num_values':3,
    'debug':True,
    'return_keys':['advertiser', 'original_date', 'revision_date']
    }, 
    
    {'name':'agency',
    'regex': re.compile("EOM\/EOC\s+Broadcast\s+Cash\s*\n\s*(.*?)\s*\n"),
    'num_values':1,
    'debug':True,
    'return_keys':['agency_name']
    },
    
    {'name':'demographic',
    'regex': re.compile("Demographic\s*\n\s*(.*?)\s*\n"),
    'num_values':1,
    'debug':True,
    'return_keys':['demographic']
    },
    
    
    #Totals                                       0                $0.00
    
    {'name':'totals',
    'regex': re.compile("\nTotals\s{6,}(\d+)\s{6,}(\$[\d\.\,]+)\s{6,}"),
    'num_values':2,
    'debug':True,
    'return_keys':['spots', 'gross']
    },
    
    {'name':'totals - attempt 2',
    'regex': re.compile("\n\s{6,}Totals\s{6,}(\d+)\s{6,}(\$[\d\.\,]+)\s"),
    'num_values':2,
    'debug':True,
    'return_keys':['spots', 'gross']
    },
    
    {'name':'contract_type',
    'regex': re.compile("\n\s{6,}(.+CONTRACT)\n"),
    'num_values':1,
    'debug':True,
    'return_keys':['contract_type']
    },
    

    
]