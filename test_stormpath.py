#!v/bin/python

import unittest
from stormpath.client import Client
from stormpath.error import Error
from config import STORMPATH_API_KEY_FILE
from config import STORMPATH_APPLICATION


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_client(self):

        # get the client
        print 'STORMPATH_API_KEY_FILE =', STORMPATH_API_KEY_FILE
        print 'STORMPATH_APPLICATION =', STORMPATH_APPLICATION
        client = Client(api_key_file_location=STORMPATH_API_KEY_FILE)

        # get the app
        apps = client.applications.search(STORMPATH_APPLICATION)
        assert len(apps) == 1
        app = apps[0]

        # delete user if it already exists
        email = 'john@example.com'
        for i in app.accounts:
            print 'email', i.email
            if i.email == email:
                print 'deleting existing account', i
                i.delete()

        # create the account
        password = 'MyPassword123'
        print 'creating account', email
        account = app.accounts.create({
            'given_name': 'John',
            'surname': 'Doe',
            'username': 'john',
            'email': email,
            'password': password,
            })

        # authenticate
        app.authenticate_account(email, password)

        # bad authentication
        caught_bad_password = False
        try:
            app.authenticate_account(email, 'badpassword')
        except Error as re:
            # Will output: 400
            print 'caught error', re.status
            # Will output: "Invalid username or password."
            print 'caught error', re.message
            # Will output: "mailto:support@stormpath.com"
            print 'caught error', re.more_info
            caught_bad_password = True

        assert caught_bad_password

        # cleanup
        account.delete()

if __name__ == '__main__':
    unittest.main()
