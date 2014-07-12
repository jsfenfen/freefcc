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


invoice_line_captures = [
# Account Exec:         McWilliams, Maggie                             Invoice Num:      1041-571087                          Page 1 of 6

    {'name':'account_exec_invoice',
    'regex': re.compile("Account Exec:\s{5,}(.+?)\s{5,}Invoice Num:\s{5,}(.+?)\s{5,}"),
    'num_values':2, 
    'debug':False,
    'return_keys':['account_exec', 'invoice_num']
    },
#     For:           MARK SMITH FOR PA(361032)                                       Contract Num:         1041-89868                                     Billing Cycle:    Broadcast EOM                       06/24/2014
    {'name':'for_contract',
    'regex': re.compile("For:\s{5,}(.+?)\s{5,}Contract Num:\s{5,}(.+?)\s{5,}Billing Cycle"),
    'num_values':2, 
    'debug':False,
    'return_keys':['advertiser_name', 'contract_num']
    },
#     PO BOX 148                                                      Contract Dates:       05/13/2014-05/20/2014                          Billing Period:   04/28/2014-05/25/2014      PAY BY   Net 30 days
    {'name':'contract_dates',
    'regex': re.compile("Contract Dates:\s+(\d\d/\d\d/\d\d\d\d)\-(\d\d/\d\d/\d\d\d\d)\s{5,}Billing Period"),
    'num_values':2, 
    'debug':False,
    'return_keys':['contract_date_start', 'contract_date_end']
    },
    {'name':'agency_name',
    'regex': re.compile("In Account\s+(.+?)\n"),
    'num_values':1, 
    'debug':True,
    'return_keys':['agency_name']
    },
    #In Account CANAL PARTNERS MEDIA LLC(357268)
# Product Desc:         D LT GOVERNOR PA
    {'name':'product_description',
    'regex': re.compile("Product Desc:\s{5,}(.+?)\n"),
    'num_values':1, 
    'debug':True,
    'return_keys':['product']
    },
    {'name':'totals',
    'regex': re.compile("Air Time Totals\s{5,}(\d+)\s{5,}([\d\,\.]+)\s+"),
    'num_values':2, 
    'debug':True,
    'return_keys':['number_of_spots', 'gross_amount']
    },
# Air Time Totals                        52                    17,150.00            
]



