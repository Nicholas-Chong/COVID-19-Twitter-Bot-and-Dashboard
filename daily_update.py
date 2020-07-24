'''----------------------------------------------------------------------------
Name:        Daily Update Command (daily_update.py)
Purpose:     To run the required maintenence commands daily.

Author:      Nicholas Chong
Created:     2020-06-24 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import site_data.update_data as ud
import heroku_api.commands as hc

def main():
    ud.update()
    hc.restart_app()


if __name__=='__main__':
    main()