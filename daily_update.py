'''----------------------------------------------------------------------------
Name:        Daily Update Command (daily_update.py)
Purpose:     To run the required maintenence commands daily.

Author:      Nicholas Chong
Created:     2020-06-24 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import logging

logging.basicConfig(filename='application.txt', level=logging.INFO, format='%(asctime)s %(levelname)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import twitter.bot as tb
import site_data.update_data as ud
import heroku_api.commands as hc
from site_data.models import *
from datetime import timedelta

def main():
    ud.update()
    ud.regional_update()
    ud.vaccine_update()

    today = Daily_Report.select().order_by(Daily_Report.id.desc()).get()
    tb.main(today)
    
    hc.restart_app()


if __name__=='__main__':
    main()
