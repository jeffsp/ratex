#!v/bin/python

from flask import Flask, session
from application.runkeeper.views import runkeeper
from config import SECRET_KEY
from test_utils import shutdown_server

app = Flask(__name__)
app.register_blueprint(runkeeper)
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    session.clear()
    html = '''
        <a href="/runkeeper/auth">Authorize Run Keeper</a>
        '''
    return html


@app.route('/authorized')
def authorized():
    html = '''
        Authorized!<br>
        <br>
        <a href="/">Restart test</a><br>
        <a href="/shutdown">Quit</a>
        '''
    return html


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...<br><a href="/">home</a>'

if __name__ == '__main__':
    app.run(debug=True)
