'''
config.py
===========

ratex config module

:copyright: (c) 2014 by Jeff Perry
'''

CSRF_ENABLED = True
DEBUG = False

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime
START_DATE = datetime(2014, 6, 1)

ROUTE = [
    {'lat': 30.128190, 'lng': -93.699668},   # ORANGE
    {'lat': 30.289748, 'lng': -97.737843},   # AUSTIN
    {'lat': 32.003416, 'lng': -106.582532},  # EL_PASO
    ]

# Stormpath
STORMPATH_API_KEY_FILE = '.stormpath.apiKey.properties'
STORMPATH_APPLICATION = 'ratex'

# Secret stuff
from secret import GMAPS_API_KEY

# Ratex
from secret import SECRET_KEY

# Runkeeper
from secret import RK_CLIENT_ID
from secret import RK_CLIENT_SECRET
