# scrape lots of stations at once:
from run_scrape import run_scrapes

# station_list = [ 'KCAU-TV', 'KCCI', 'KCRG-TV', 'KCWI-TV', 'KDMI', 'KDSM-TV', 'KFPX-TV', 'KFXA', 'KFXB-TV', 'KGAN', 'KGCW', 'KIMT', 'KLJB', 'KMEG', 'KPTH', 'KPXR-TV', 'KTIV', 'KWKB', 'KWQC-TV', 'KWWF', 'KWWL', 'KYOU-TV', 'WBXF-CA', 'WHO-DT', 'WOI-DT']

station_list = [ 'KWWL', 'KYOU-TV', 'WBXF-CA', 'WHO-DT', 'WOI-DT']

# doesn't exist? KWWF
for station in station_list:
    run_scrapes(station_list, True, True)
    