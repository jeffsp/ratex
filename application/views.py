'''
views.py
========

ratex views

:copyright: (c) 2014 by Jeff Perry
'''

from flask import (
    jsonify,
    render_template,
    flash,
    redirect,
    session,
    url_for,
    request,
    g,
    )
from flask.ext.stormpath import login_required, user, StormpathManager

from application import application
from application.models import Activity
from application.forms import StartDateForm
from application import runkeeper
from requests_oauthlib import OAuth2Session
from flask.ext.gravatar import Gravatar
import requests
import json

gravatar = Gravatar(application)
stormpath_manager = StormpathManager(application)


def set_globals():
    g.user = user
    g.total_activities = 0
    g.total_meters = 0
    g.route_activities = 0
    g.route_meters = 0
    if hasattr(user, 'custom_data'):
        if user.custom_data['start_date'] is None:
            user.custom_data['start_date'] = application.config['START_DATE']
            user.save()
        if user.custom_data['route'] is None:
            user.custom_data['route'] = application.config['ROUTE']
            user.save()
        route_activities = []
        for a in user.custom_data['activities']:
            g.total_activities = g.total_activities + 1
            g.total_meters = g.total_meters + a['distance']
            if a['start_time'] >= user.custom_data['start_date']:
                g.route_activities = g.route_activities + 1
                g.route_meters = g.route_meters + a['distance']
                route_activities.append(a)
        # save the custom data
        user.custom_data['route_activities'] = route_activities
        user.save()


@application.before_request
def before_request():
    set_globals()


@application.route('/', methods=['POST', 'GET'])
@login_required
def index():
    form = StartDateForm()
    if form.validate_on_submit():
        start_date = form.dt.data.strftime(Activity.DATE_FORMAT)
        user.custom_data['start_date'] = start_date
        user.save()
        set_globals()
    return render_template('index.html', form=form)

@application.route('/routes', methods = ['GET'])
def routes():
    func_list = {}
    for rule in application.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = application.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

@application.route('/_set_route')
@login_required
def set_route():
    user.custom_data['route'] = json.loads(request.args.get('route_markers'))
    user.save()
    return redirect(url_for('index'))
