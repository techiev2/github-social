"""Github access helper module"""

# coding=utf-8
__author__ = 'sriramm'

#pylint:disable=W0511,R0902
# Disables
# W0511 : TODO tracks
# R0902 : Instance attribute count

import sys
sys.dont_write_bytecode = True

import requests
from requests.auth import HTTPBasicAuth
import json
import logging

# Boolean checklist. Could be a case for ast ?
TRUE = [True, 1, '1', 'True']
FALSE = [False, [], None, 0, '0', 'False', 'None']


class GitHub(object):
    """Github base class"""

    def __init__(self, creds, config=False):
        """
        Github base class init
        :param creds: Tuple of username, password for authenticating a session
        :param config: Instance configuration.
                        Houses reverse/auth/pretty print configs
                reverse: Reversed user password boolean
                auth: Boolean for dry run switch.
                            Doesn't initiate auth method if False
                pretty: Boolean to pretty print response data wherever applicable
                safe_json: Boolean to return safe JSON for use with Javascript.
        """
        ex_msg = "Invalid data structure passed in. Need a creds tuple"
        default_config_msg = "Invalid config construct. Defaulting"
        if not isinstance(creds, tuple):
            raise Exception(ex_msg)

        self.config = config
        self.base_url = "https://api.github.com"
        (self.session, self.request,
         self.response, self.token,
         self.auth) = (None, None, None, None, None)

        if not isinstance(self.config, dict):
            logging.warning(default_config_msg)
            self.config = {
                'pretty': True,
                'reverse': True,
                'auth': False,
                'safe_json': True
            }

        if not self.config.get('pretty') in TRUE:
            self.config['pretty'] = False

        self.uname = creds[0]
        self.upass = creds[1]

        if self.config.get('reverse', None):
            self._reverse_upass()

        self.creds = (self.uname, self.upass)

        if self.config.get('auth', None):
            self._auth_session()

    def _load_response(self, content, returns=False):
        """
        JSON response loader helper
        :param content:str JSON String content to load into response member
        :param returns:bool Boolean param to toggle return for testing.
                            Method returns response if True;
                            else updates response class member
        """
        if not (isinstance(content, str) or isinstance(content, unicode)):
            raise Exception("Invalid load data")

        content = json.loads(content)
        if not returns:
            self.response = content
        else:
            return content

    def _auth_session(self):
        """
        Authorize session helper class method. Depends on authorization
        credentials provided during instance invocation.
        """
        self.session = requests.Session()
        self.auth = HTTPBasicAuth(*self.creds)

        self.response = self.session.post(
            'https://api.github.com/authorizations',
            auth=self.auth,
            data=json.dumps({
                'scopes': [
                    'repo'
                ],
                'client_id': '5296b27cb26ad43f3d8a',
                'client_secret': '4c1282c5438883d3cdd3b0d109254cefdb74bb06'
            })
        )
        content = self.response.__getattribute__('_content')
        if content:
            self._load_response(content)
            self.token = self.response.get('token', None)
            if self.token:
                self.session.headers["Authorization"] = "token %s" % self.token

    def _reverse_upass(self):
        """
        Return a reversed upass for use with _auth_session method
        :rtype : None
        """
        plen = len(self.upass)
        plen_mid = plen / 2
        self.upass = self.upass[0:plen_mid][
            ::-1] + self.upass[plen_mid:plen][::-1]

    def _get_data(self, url, method='get', data=None, returns=False):
        """
        Requests get data helper class method
        :param data:dict HTTP data for helper method
        :param url:str URL to fetch data for.
        :param method:str HTTP method for data request. Defaults to GET.
        :param returns:bool Boolean param to toggle return for testing.
                            Method returns response if True;
                            else updates response class member
        """
        method = method.lower()
        if not url:
            raise Exception("No URL specified for HTTP Request")
        if self.session:
            if method == 'post':
                self.response = self.session.post(url, data=data)
            else:
                self.response = self.session.get(url, data=data)

            self.response = self.response.__getattribute__('_content')
            if self.response:
                if returns:
                    return self._load_response(self.response, returns=returns)

    @classmethod
    def _construct_query(cls, query):
        """
        GitHub API legacy search end point friendly converter
        :param query:dict Construct for query
        """
        allowed = ['sort', 'order']
        keyword_warn = "No keyword provided for search. Defaulting to Python"
        if not isinstance(query, dict):
            raise TypeError("Invalid data construct provided")

        keyword = query.get('keyword', None)

        if not keyword:
            logging.warning(keyword_warn)
            keyword = 'python'

        query_res = keyword + ":"

        for (key, val) in query.iteritems():
            if key in allowed:
                query_res += key + ":" + val

        return query_res

    def get_user_info(self, username=None, action=None, returns=False):
        """
        Get user information helper.
        :param username:str Username for users end point search
        :param action:str Action for user to search for.
                        Currently supports only repos.
        """
        base_url = 'https://api.github.com/users/{0}/{1}'
        allowed_actions = ['repos']
        username = username or self.uname

        if action not in allowed_actions:
            action = "repos"
        action = action.lower()
        username = username.lower()

        if returns:
            return self._get_data(base_url.format(
                username, action), returns=returns)

    def get_repo_info(self, user_name=None, repo_name=None):
        """Get repository information
        :rtype : None
        :param user_name:str Username for repository search.
                            Defaults to session user
        :param repo_name:str Repository name to fetch information for.
        """
        url = "{0}/repos/{1}/{2}"
        if not repo_name:
            raise Exception("No repository name provided")
        if not user_name:
            user_name = self.uname

        url = url.format(self.base_url, user_name, repo_name)
        self._get_data(url)

    def search_repos(self, query=None, returns=False):
        """
        Search users interface method
        :param query:str Query construct for search.
                        Currently picks up only a dict.
                        #TODO: Flexibility with list/tuple/string (regex)
        :param returns:bool Boolean param to toggle return for testing.
                    Method returns response if True;
                    else updates response class member
        """
        url = self.base_url + "/legacy/repos/search/"
        url += self._construct_query(query)
        response = self._get_data(url, returns=returns)
        if returns:
            return response

__all__ = ['GitHub']
