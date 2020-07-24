import site_data.update_data as ud
import heroku_api.commands as hc

def update():
    ud.update()
    hc.restart_app()


if __name__=='__main__':
    update()