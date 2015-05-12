'''
__init__.py
===========

ratex init module

:copyright: (c) 2014 by Jeff Perry
'''

from flask import Flask

# create our application
application = Flask(__name__)
application.config.from_object('config')
from config import SECRET_KEY

# Views must be imported after the application is created because the views
# module imports the application object
from application import views
from application.runkeeper.views import runkeeper
application.register_blueprint(runkeeper)
application.secret_key = SECRET_KEY
