import unittest

class TestJob(unittest.TestCase):
    def __init__(self, params, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.params = self.validate_params(params)

    def validate_params(self, params):
        return params
