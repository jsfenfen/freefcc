import re


# 14              WKND NEWS SUN 7-9A                               05/18/2014-05/18/2014                                    ......S                                 15           2               270.00

ad_summary_line = re.compile("\s{3,}(\d+)\s{3,}(.+?)\s{3,}(\d\d/\d\d/\d\d\d\d)\-(\d\d/\d\d/\d\d\d\d)\s+([MTWFS\.]+)\s{3,}(\d+)\s{3,}(\d+)\s{3,}([\d\,\.]+)")

# 05/13/2014           Tu    11:31:44 PM                 DML14MS105H                                   15             650.00
## This will not match *unrun ads* 
ad_detail_result = re.compile("\s{3,}(\d\d/\d\d/\d\d\d\d)\s{3,}(\w\w)\s{3,}(\d\d:\d\d:\d\d \wM)\s{3,}([\w\d]+)\s{3,}(\d+)\s{4,}([\d\,\.]+)")

## WE only will get the makegood ads, not the original ones being replaced. 
ad_makegood_result = re.compile("\s{3,}(\d\d/\d\d/\d\d\d\d)\s{3,}(\w\w)\s{3,}(\d\d:\d\d:\d\d \wM)\s{3,}(\d\d/\d\d/\d\d\d\d)\s{3,}([\w\d]+)\s{3,}(\d+)\s{3,}([\d\,\.]+)\s{3,}([\d\,\.]+)\s{3,}(.+)\n")


def process_file(filename):
    infile = open(filename, "r")
    ad_air_times = []
    current_ads = []
    current_ad = {}
    ad_line_num = 0
    
    for line in infile:
        result = re.search(ad_summary_line, line)
        if result:  
            #print "ad info"
            (current_ad['ad_number'], current_ad['name'], current_ad['contract_start'], current_ad['contract_stop'], current_ad['rundays'], current_ad['dur'], current_ad['spots'], current_ad['rate']) =  result.group(1,2,3,4,5,6,7,8)
            #print current_ad
            if int(current_ad['ad_number']) != ad_line_num+1:
                print "***** Possible ad line mismatch: ad_number='%s' ad_line_num='%s', %s" % (int(current_ad['ad_number']), ad_line_num, line)
            ad_line_num = int(current_ad['ad_number'])
        
        ad_details = re.search(ad_detail_result, line)
        if ad_details:
            #print "\tad details"
            this_ad_details = {'make_good':False}
            (this_ad_details['air_date'], this_ad_details['day'], this_ad_details['air_time'], this_ad_details['material'], this_ad_details['ad_dur'], this_ad_details['ad_rate']) = ad_details.group(1,2,3,4,5,6)
            #print this_ad_details
            complete_ad = dict(current_ad.items() + this_ad_details.items())
            current_ads.append(complete_ad)
        
        makegood_details = re.search(ad_makegood_result, line)
        if makegood_details:
            #print "\tmg details"
            this_ad_details = {'make_good':True}
            (this_ad_details['air_date'], this_ad_details['day'], this_ad_details['air_time'], this_ad_details['mg_for_date'], this_ad_details['material'], this_ad_details['ad_dur'], this_ad_details['ad_rate'], this_ad_details['mg_debit_credit'], this_ad_details['mg_remarks']) = makegood_details.group(1,2,3,4,5,6,7,8,9)
            #print this_ad_details
            complete_ad = dict(current_ad.items() + this_ad_details.items())
            current_ads.append(complete_ad)

    return current_ads
    
if __name__ == '__main__':
    process_file("../../txts/13775490313088.txt")