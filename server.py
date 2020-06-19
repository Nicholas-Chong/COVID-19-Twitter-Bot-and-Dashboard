from flask import Flask

app = Flask(__name__)
app.debug = False 

@app.route('/')
def index():
    return 'Hello World'

app.run()