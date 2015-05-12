#!v/bin/python

import unittest

from application import application
from application import forms


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testStartDateForm(self):

        with application.app_context():
            with application.test_request_context():
                f = forms.StartDateForm()
                print f.dt

if __name__ == '__main__':
    unittest.main()
