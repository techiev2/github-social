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
from copy import deepcopy
from GitHubAccess.utils import authenticated, is_iterable, is_stringy

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
                pretty: Boolean to pretty print response wherever applicable
                safe_json: Boolean to return safe JSON for use with Javascript.
        """
        self.msgs = {
            'construct_fail':\
             "Invalid data construct provided. Query needs to be a dictionary.",
             'invalid_iterable':\
             "Invalid data passed in. Requires an iterable.",
             "no_auth":\
             "".join(
              ["No authenticated session found.",
               "Please init with auth=True or call ",
               "auth_session manually before proceeding"]),
             "no_token": "No token received.",
             "bad_creds": "Authentication failure. Invalid credentials"
        }

        ex_msg = "Invalid data structure passed in. Need a creds tuple"
        default_config_msg = "Invalid config construct. Defaulting"
        if not isinstance(creds, tuple) or not (creds[0] or creds[1]):
            raise Exception(ex_msg)

        self.config = config
        self.base_url = "https://api.github.com"
        (self.session, self.request,
         self.response, self.token,
         self.auth, self.client_data) = (None, None, None, None, None, None)

        if not isinstance(self.config, dict):
            logging.warning(default_config_msg)
            self.config = {
                'pretty': True,
                'reverse': True,
                'auth': False,
                'safe_json': True
            }

        if not self.config.get('client_data'):
            raise Exception("No API client data available in invocation")

        if not self.config.get('pretty') in TRUE:
            self.config['pretty'] = False

        self.uname = creds[0]
        self.upass = creds[1]
        self.client_data = self.config.get('client_data')

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

        try:
            content = json.loads(content)
            self.response = content
        except Exception:
            pass
        if returns:
            return self.response

    def _auth_session(self):
        """
        Authorize session helper class method. Depends on authorization
        credentials provided during instance invocation.
        """
        self.session = requests.Session()
        self.auth = HTTPBasicAuth(*self.creds)
        self.client_data.update({
            "scopes": [
                "repo"
            ]
        })  # Needs to be updatable from config. #TODO

        # If config brings in an alternative scope requirement
        # update the scope for authorization data
        config_scopes = self.config.get("scopes")
        if config_scopes:
            self.client_data['scopes'] = config_scopes

        self.response = self.session.post(
            'https://api.github.com/authorizations',
            auth=self.auth,
            data=json.dumps(self.client_data)
        )
        content = self.response.__getattribute__('_content')
        if content.find("<html>") == 0:  # Rudimentary exception catching
            raise Exception("API Exception. Try later")

        if content:
            self.response = self._load_response(content, returns=True)
            self.token = self.response.get('token', None)
            if self.token:
                self.session.headers["Authorization"] = "token %s" % self.token
            else:
                response_msg = self.response.get('message', None)
                if response_msg:
                    if response_msg == 'Bad credentials':
                        raise Exception(self.msgs['bad_creds'])
                    else:
                        raise Exception(response_msg)
                else:
                    raise Exception(self.msgs['no_token'])

    def _reverse_upass(self):
        """
        Return a reversed upass for use with _auth_session method
        :rtype : None
        """
        plen = len(self.upass)
        plen_mid = plen / 2
        self.upass = self.upass[0:plen_mid][
            ::-1] + self.upass[plen_mid:plen][::-1]

    @authenticated
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
                self._load_response(self.response)
            if returns:
                return self.response

    def _construct_query(self, query):
        """
        GitHub API legacy search end point friendly converter
        :param query:dict Construct for query
        """
        allowed = ['sort', 'order']
        keyword_warn = "No keyword provided for search. Defaulting to Python"
        if not isinstance(query, dict):
            raise TypeError(self.msgs['construct_fail'])

        keyword = query.get('keyword', None)

        if not keyword:
            logging.warning(keyword_warn)
            keyword = 'python'

        query_res = keyword + ":"

        for (key, val) in query.iteritems():
            if key in allowed:
                query_res += key + ":" + val

        return query_res

    def get_user_info(self, user_name=None, action=None, returns=False):
        """
        Get user information helper.
        :param returns:bool Boolean check to return response data
        :param user_name:str Username for users end point search
        :param action:str Action for user to search for.
                        Currently supports only repos.
        """
        base_url = 'https://api.github.com/users/{0}/{1}'
        allowed_actions = ['repos', 'followers']
        user_name = user_name or self.uname

        if not action in allowed_actions:
            action = "repos"
        action = action.lower()
        username = user_name.lower()

        self.response = self._get_data(base_url.format(
            username, action), returns=returns)
        if action == 'followers':
            self.response = {
                'followers': self.response
            }

        if returns:
            return self.response

    def get_repo_info(self,
                      user_name=None,
                      repo_name=None,
                      fields=None,
                      returns=False):
        """
        Get repository information
        :param user_name:str Username for repository search.
                            Defaults to session user
        :param repo_name:str Repository name to fetch information for.
        :param fields:list|tuple List of fields to retain
                                    in the returned response data.
        :param returns:bool Boolean switch to specify if the
                                    method needs to return response.
        """
        url = "{0}/repos/{1}/{2}"
        if not repo_name:
            raise Exception("No repository name provided")
        if not user_name:
            user_name = self.uname

        url = url.format(self.base_url, user_name, repo_name)
        self._get_data(url)
        if fields and (isinstance(fields, list)
                       or isinstance(fields, tuple)):
            if is_stringy(self.response):
                self.response = json.loads(self.response)
            response = deepcopy(self.response)
            response_copy = deepcopy(response)
            for key in response_copy.iterkeys():
                if key not in fields:
                    response.pop(key)
            self.response = response

        if returns:
            return self.response

    def search_repos(self, query=None, returns=False, fields=None):
        """
        Search users interface method
        :param query:str Query construct for search.
                        Currently picks up only a dict.
                        #TODO: Flexibility with list/tuple/string (regex)
        :param returns:bool Boolean param to toggle return for testing.
                    Method returns response if True;
                    else updates response class member
        :param fields:iterable Iterable specifying the fieds to return
                    in response
        """
        url = self.base_url + "/legacy/repos/search/"
        url += self._construct_query(query)
        response = self._get_data(url, returns=returns)
        if not (isinstance(fields, list) or
                 isinstance(fields, tuple) or fields == None):
            raise TypeError(self.msgs['invalid_iterable'])

        if fields == None:
            fields = []

        return_response = {
            'repositories': []
        }

        for repo in response.get('repositories'):
            data = {}
            for (key, val) in repo.iteritems():
                if key in fields:
                    data.update({key: val})
            if data != {}:
                return_response['repositories'].append(data)


        self.response = return_response

        if returns:
            return self.response

    def get_user_events(self,
                        user_name=None,
                        organization=None,
                        event_types=None,
                        returns=False):
        """
        Get public events initiated by specified user.
        :param user_name:str Username to query against.
        :param returns:bool Boolean param to toggle return for testing.
                    Method returns response if True;
                    else updates response class member
        """
        user_events_url = "{0}/users/{1}/events/public"
        user_org_events_url = "{0}/users/{1}/events/orgs/{2}"
        exception_msg = "No valid organization name provided. Exiting"
        if not (user_name or not (isinstance(user_name, str)
                               or isinstance(user_name, unicode))):
            raise Exception("No valid username provided. Exiting")
        if not organization:
            base_url = user_events_url.format(self.base_url, user_name)
        else:
            if not (organization or not (isinstance(organization, str)
                               or isinstance(organization, unicode))):
                raise Exception(exception_msg)
            base_url = user_org_events_url.format(self.base_url,
                                                  user_name,
                                                  organization)
        self.response = self._get_data(
            url=base_url,
            data={},
            returns=returns)

        if is_iterable(event_types):
            self.response = {
                'user_name': user_name,
                'events': [x for x in self.response
                              if x.get("type") in event_types]
            }
        else:
            logging.warn("Non iterable event types param passed.")
        if returns:
            return self.response

    def get_user_stars(self,
                   user_name=None,
                   returns=False,
                   repo_language=None):
        """
        Get the list of repositories a user has starred.
        :param user_name:str Username to query against.
        :param returns:bool Boolean param to toggle return for testing.
                    Method returns response if True;
                    else updates response class member
        :param repo_language:str Language filter for user starred repositories.
        """
        user_stars_url = "{0}/users/{1}/starred"
        if not (user_name or not (isinstance(user_name, str)
                               or isinstance(user_name, unicode))):
            raise Exception("No valid username provided. Exiting")
        else:
            user_stars_url = user_stars_url.format(self.base_url, user_name)
            self.response = self._get_data(
                               url=user_stars_url,
                               method='GET',
                               data={},
                               returns=returns)
            if repo_language:
                self.response = [x for x in self.response
                                  if x.get('language') == repo_language]
            if returns:
                return self.response


__all__ = "GitHub*get_auth*load_json_file*ARG_PARSER".split("*")
