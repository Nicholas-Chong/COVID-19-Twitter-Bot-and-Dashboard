'''----------------------------------------------------------------------------
Name:        Daily Update Command (daily_update.py)
Purpose:     To run the required maintenence commands daily.

Author:      Nicholas Chong
Created:     2020-06-24 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import twitter.bot as tb
import site_data.update_data as ud
import heroku_api.commands as hc

def main():
    tb.main()
    ud.update()
    ud.regional_update()
    hc.restart_app()


if __name__=='__main__':
    main()
