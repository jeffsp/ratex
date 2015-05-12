'''
forms.py
========

ratex forms

:copyright: (c) 2014 by Jeff Perry
'''

from wtforms.fields.html5 import DateField
from flask_wtf import Form


class StartDateForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')
