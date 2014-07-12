"""

Based on observations

line_captures_current <=> FCC id >= 13886716046591
line_captures_2013ish <=> FCC id < 13886716046591

"""
import re

line_captures_2013ish = [
    # Print Date     04/23/13          Page   1 of 2
    
    {'name':'Top Line printing summary',
    'regex': re.compile("Print Date\s+(\d\d/\d\d/\d\d)\s+Page\s+(\d+)\s+of\s+(\d+)"),
    'num_values':3,
    'debug':True,
    'return_keys':['print_date', 'start_page', 'num_pages']
    },
    
    {'name':'Contract / Revision',
    'regex': re.compile("Contract / Revision\s+(.+?)\s+Alt Order #\s+(.*)\s*\Z"),
    'num_values':2, 
    'debug':True,
    'return_keys':['order_revision', 'alt_order']
    },
    {'name':'Product Description',
    'regex': re.compile("Product\s+(\w+)\s+Estimate"),
    'num_values':1, 
    'debug':True,
    'return_keys':['product_description']
    },
    {'name':'Flight Dates',
    'regex': re.compile("Flight Dates\s+(\d\d/\d\d/\d\d)\s*\-\s*(\d\d/\d\d/\d\d)\s+"),
    'num_values':2, 
    'debug':True,
    'return_keys':['flight_date_start', 'flight_date_end']
    },
    
    {'name':'Original Date / Revision Date',
    'regex': re.compile("(\d\d/\d\d/\d\d)\s+(\d\d/\d\d/\d\d)\s+Billing Contact"),
    'num_values':2, 
    'debug':True,
    'return_keys':['original_date', 'revision_date']
    },
    
    {'name':'Agency name',
    'regex': re.compile("\AAgency\s+(.+)\s+\Z"),
    'num_values':1, 
    'debug':True,
    'return_keys':['agency_name']
    },
    
    {'name':'Advertiser name',
    'regex': re.compile("Advertiser\s+(.+)\s+Billing"),
    'num_values':1, 
    'debug':True,
    'return_keys':['advertiser_name']
    },

    {'name':'Demographic',
    'regex': re.compile("Demographic\s+(.+?)\s+\Z"),
    'num_values':1, 
    'debug':True,
    'return_keys':['demographic']
    },
    
    {'name':'Product Codes',
    'regex': re.compile("Product Codes\s+(.*)\s+\Z"),
    'num_values':1, 
    'debug':True, 
    'return_keys':['product_codes']
    },
    
    {'name':'Priority',
    'regex': re.compile("Priority\s+(.+?)\s+\Z"),
    'num_values':1, 
    'debug':True,
    'return_keys':['priority']
    },
    
    {'name':'Revenue Codes',
    'regex': re.compile("Rev Codes\s+(.+?)\s+Agency"),
    'num_values':1, 
    'debug':True,
    'return_keys':['revenue codes']
    },
    
    # # Spots      Gross Amount      Net Amount         Rating
    {'name':'Totals',
    'regex': re.compile("Totals\s+([\d,]+)\s+(\$[\d\.,]+)\s+(\$[\d\.,]+)\s+([\d\.,]+)"),
    'num_values':4, 
    'debug':True,
    'return_keys':['number_of_spots', 'net_amount', 'gross_amount', 'rating']
    },
    
    
    {'name':'Market total',
    'regex': re.compile("Order\s+Share\s+(\d+)\%\s+Market\s+Value\s+([\d\.,]+)"),
    'num_values':2, 
    'debug':True,
    'return_keys':['station_percent', 'market_total']
    },
]

line_captures_current = [
    
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