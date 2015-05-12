#!v/bin/python

from flask import Flask, redirect, url_for
from flask.ext.stormpath import StormpathManager, user, login_required
from stormpath.client import Client
from test_utils import shutdown_server

app = Flask(__name__)
app.config.from_object('config')

stormpath_manager = StormpathManager(app)


@app.route('/')
def index():
    if user.is_authenticated():
        return redirect(url_for('success'))
    client = Client(api_key_file_location=app.config['STORMPATH_API_KEY_FILE'])
    a = client.applications.search(app.config['STORMPATH_APPLICATION'])[0]

    html = ''
    # delete user if it already exists
    email = 'john@example.com'
    for i in a.accounts:
        if i.email == email:
            html = html + 'deleting account ' + i.email + '<br>'
            i.delete()

    # create the account
    password = 'asdfASDF1234'
    username = 'john'
    html = html + 'creating account ' + email + '<br>'
    account = a.accounts.create({
        'given_name': 'John',
        'surname': 'Doe',
        'username': username,
        'email': email,
        'password': password,
        })

    html = html + '''
        Login using these credentials:<br>
        <b>%s <br></b>
        <b>%s <br></b>
        <a href="/login">Login</a>
        ''' % (email, password)
    return html


@app.route('/success')
@login_required
def success():
    html = '''
    success<br>
    <a href="/shutdown">Shutdown</a>
    '''
    return html


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...<br><a href="/">home</a>'

if __name__ == '__main__':
    app.run(debug=True)
