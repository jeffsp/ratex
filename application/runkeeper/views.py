'''
views.py
========

runkeeper views

:copyright: (c) 2014 by Jeff Perry
'''

from flask import (
    Blueprint,
    flash,
    redirect,
    session,
    url_for,
    request,
)
from application import application
from application.models import Activity
from requests_oauthlib import OAuth2Session
from dateutil import parser
import requests

client_id = application.config['RK_CLIENT_ID']
client_secret = application.config['RK_CLIENT_SECRET']

AUTHORIZATION_BASE_URL = 'https://runkeeper.com/apps/authorize'
DEAUTHORIZATION_BASE_URL = 'https://runkeeper.com/apps/de-authorize'
TOKEN_URL = 'https://runkeeper.com/apps/token'

# Define the blueprint: 'runkeeper', set its url prefix: <app_url>/runkeeper
runkeeper = Blueprint('runkeeper', __name__, url_prefix='/runkeeper')


@runkeeper.route('/auth')
def auth():
    """
    Call runkeeper to get OK from user
    """

    redirect_uri = url_for('runkeeper.callback', _external=True)
    rk = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = rk.authorization_url(AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    return redirect(authorization_url)


@runkeeper.route("/callback", methods=["GET"])
def callback():
    """
    User gave their OK, get the token.
    """

    redirect_uri = url_for('runkeeper.callback', _external=True)
    rk = OAuth2Session(client_id,
                       state=session['oauth_state'],
                       redirect_uri=redirect_uri)
    token = rk.fetch_token(TOKEN_URL,
                           client_secret=client_secret,
                           authorization_response=request.url)

    session.access_token = token['access_token']

    application.logger.debug('access_token = %s' % session.access_token)

    flash('Runkeeper authorized')

    return redirect(url_for('authorized'))


@runkeeper.route("/get_activities", methods=["GET"])
def get_activities():
    """
    Get activities from RK
    """

    assert session.access_token

    application.logger.debug('access_token = %s' % session.access_token)
    headers = {
        'Authorization': 'Bearer ' + session.access_token,
        'Accept': 'application/vnd.com.runkeeper.FitnessActivityFeed+json',
        }

    page = 0
    activities = []

    while True:
        rv = requests.get('https://api.runkeeper.com/fitnessActivities?page=%d'
                          % page, headers=headers)
        if rv.status_code != 200:
            flash('get_activities(): Invalid response status code: %d'
                  % rv.status_code, 'error')
            return redirect(url_for('index'))
        items = rv.json()['items']
        n = len(items)
        if len(items) == 0:
            break
        for i in range(n):
            t = parser.parse(items[i]['start_time'])
            d = float(items[i]['total_distance'])
            a = Activity(start_time=t, distance=d)
            activities.append(a.jsonify())
        page = page+1

    # make it chronological
    activities = activities[::-1]

    fmt = 'Got %d activities'
    application.logger.debug(fmt % len(activities))
    flash(fmt % len(activities))

    return redirect(url_for('index'))


@runkeeper.route('/deauth')
def deauth():
    """
    Call runkeeper to deauthorize user
    """
    assert session.access_token

    application.logger.debug('deauthorizing')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    rv = requests.post(DEAUTHORIZATION_BASE_URL,
                       headers=headers,
                       data={'access_token': session.access_token})

    if rv.status_code != 204:
        flash('Could not de-authorize', 'error')
        return redirect(url_for('index'))

    session.access_token = None
    flash('Runkeeper de-authorized')

    return redirect(url_for('index'))
