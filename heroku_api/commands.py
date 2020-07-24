import heroku3
import os 

def restart_app():
    heroku_conn = heroku3.from_key(os.getenv('TOKEN'))
    app = heroku_conn.apps()['mighty-gorge-03520']
    return app.restart()

if __name__=='__main__':
    restart_app()