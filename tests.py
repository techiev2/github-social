"""Github social tests"""
# coding=utf-8
__author__ = 'sriramm'

import sys
sys.dont_write_bytecode = True

import unittest
from GitHubAccess import GitHub


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.response = None
        self.github_obj = GitHub(creds=('', ''),
                                 config={
                                     'reverse': False,
                                     'auth': True,
                                     'safe_json': True
                                 })

    def testGetData(self):
        self.response = self.github_obj._get_data(
            'https://api.github.com/users/techiev2', returns=True)
        self.assertIsInstance(self.response, dict)


if __name__ == '__main__':
    unittest.main()
