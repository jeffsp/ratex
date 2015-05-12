'''
models.py
===========

ratex models module

:copyright: (c) 2014 by Jeff Perry
'''


class Activity():

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, start_time, distance):
        self.start_time = start_time
        self.distance = distance

    def jsonify(self):
        return {
            "start_time": self.start_time.strftime(self.DATE_FORMAT),
            "distance": self.distance,
            }
