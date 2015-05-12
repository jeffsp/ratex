#!v/bin/python

import unittest
import datetime

from application import models
from dateutil import parser


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testActivity(self):

        t = parser.parse("Tue, 1 Mar 2011 07:00:00")
        a = models.Activity(t, 1.234)
        j = a.jsonify()
        assert j['start_time'] == '2011-03-01'

if __name__ == '__main__':
    unittest.main()
