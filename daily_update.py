'''----------------------------------------------------------------------------
Name:        Daily Update Command (daily_update.py)
Purpose:     To run the required maintenence commands daily.

Author:      Nicholas Chong
Created:     2020-06-24 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import twitter.bot as tb
import site_data.update_data as ud
import heroku_api.commands as hc
from site_data.models import *
from datetime import timedelta

def main():
    todays_date = (
        Daily_Report
        .select()
        .order_by(Daily_Report.id.desc())
        .get()
        .date 
        +timedelta(days=1)
    )

    tb.main(todays_date)
    ud.update()
    ud.regional_update()
    hc.restart_app()


if __name__=='__main__':
    main()
