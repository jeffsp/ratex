#!v/bin/python

import unittest

from application import application


class TestCase(unittest.TestCase):

    def setUp(self):
        application.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_config(self):
        assert len(application.config) > 10
        print 'configuration has', len(application.config), 'entries'
        for i in sorted(application.config):
            print i, '=', application.config[i]

    def test_debug(self):
        assert application.config['DEBUG'] is False

if __name__ == '__main__':
    unittest.main()
