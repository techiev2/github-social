"""Github social tests"""
# coding=utf-8
__author__ = 'sriramm'

import sys
sys.dont_write_bytecode = True

import unittest
from GitHubAccess import GitHub
from main import get_auth


class BaseTests(unittest.TestCase):
    def setUp(self):
        """Base tests setup. Initialize a github object instance."""
        self.response = None
        self.creds = get_auth(returns=True)
        self.github_obj = GitHub(creds=self.creds,
                                 config={
                                     'reverse': False,
                                     'auth': True,
                                     'safe_json': True
                                 })

    def testGetData(self):
        """Test get data method. Must return <dict>"""
        self.response = self.github_obj._get_data(
            'https://api.github.com/users/techiev2', returns=True)
        self.assertIsNotNone(self.response.get("public_repos", None))
        assert self.response.get('public_repos', None) is not None
        self.assertIsInstance(self.response, dict)

    def testAuth(self):
        """Test private session authorize method"""
        self.github_obj._auth_session()
        self.assertIsInstance(self.github_obj.response, dict)


if __name__ == '__main__':
    unittest.main()
