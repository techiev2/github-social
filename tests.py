"""Github social tests"""
# coding=utf-8
__author__ = 'sriramm'

import sys
sys.dont_write_bytecode = True

import unittest
from GitHubAccess import GitHub
from main import get_auth
import logging


class BaseTests(unittest.TestCase):
    """
    Base set of tests for GitHubAccess module's GitHub class.
    setUp sets up an instance of GitHub access and provides
    access to instance methods.
    """
    def __init__(self, *args, **kwargs):
        """Base tests setup. Initialize a github object instance."""
        super(BaseTests, self).__init__(*args, **kwargs)
        self.response = None
        self.creds = get_auth()
        self.github_obj = GitHub(creds=self.creds['creds'],
                                 config={
                                     'reverse': False,
                                     'auth': True,
                                     'safe_json': True,
                                     'client_data': self.creds['client']
                                 })

    def test_get_data(self):
        """Test get data method. Must return <dict>"""
        url = 'https://api.github.com/users/techiev2'
        self.github_obj.__getattribute__('_get_data')(url)
        self.response = self.github_obj.response
        self.assertIsNotNone(self.response.get("public_repos", None))
        assert self.response.get('public_repos', None) is not None
        self.assertIsInstance(self.response, dict)

    def test_auth_flow(self):
        """Test private session authorize method"""
        self.github_obj.__getattribute__('_auth_session')()
        self.assertIsInstance(self.github_obj.response, dict)


if __name__ == '__main__':
    unittest.main()
