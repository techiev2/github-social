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
import argparse
import getpass

# Boolean checklist. Could be a case for ast ?
TRUE = [True, 1, '1', 'True']
FALSE = [False, [], None, 0, '0', 'False', 'None']

ARG_PARSER = argparse.ArgumentParser(description="Creds loader")
ARG_PARSER.add_argument("--creds", help="Credentials file name")


def load_json_file(file_name=None):
    """
    JSON file loader helper.
    Could be used with get_auth or its replacements.
    :param file_name:str Path for json(ic) file to load from disk.
    """
    response = {}
    if not file_name:
        raise Exception("No file name specified for loading")
    try:
        with open(file_name, "r") as data_file:
            response = [x for x in data_file.readlines() if x.find('//') % 4 != 0]
            response = reduce(lambda a, b: a.strip() + b.strip(), response)
    except IOError:
        raise Exception("Unable to find specified file")  # Fail gracefully and send {} ?

    if (isinstance(response, str) or isinstance(response, unicode)):
        try:
            response = json.loads(response)
        except ValueError:
            raise Exception("Unable to parse ")
        except TypeError:
            raise Exception("Unable to parse ")

    return response


def get_auth(returns=True, creds_file=False):
    """
    Get authentication data
    :param returns:bool Boolean check to return data from get_auth
    """
    (creds, client, uname, upass, client_id, client_secret)\
        = (None, None, None, None, None, None)
    user_creds = {}
    msgs = {
        'no_creds': "No credentials file provided. Defaulting to shell input",
        'uname_input': "Please enter your GitHub username to authenticate: ",
        'upass_input': "Please enter your GitHub password to authenticate: ",
        'client_id_input': "Please enter your GitHub client ID: ",
        'client_secret_input': "Please enter your GitHub client secret: ",
        'exit_msg': "\nKeyboard interrupt. Exiting",
        'no_creds_msg': "No credentials found. Exiting"
    }
    creds_file = ARG_PARSER.parse_args().__getattribute__('creds')

    if not creds_file:
        print msgs['no_creds']
        try:
            uname = raw_input(msgs['uname_input'])
            upass = getpass.getpass(msgs['upass_input'])
            client_id = raw_input(msgs['client_id_input']) or ''
            client_secret = raw_input(['client_secret_input']) or ''
        except KeyboardInterrupt:
            quit(msgs['exit_msg'])

        if uname and upass:
            creds = (uname, upass)

        client = {
            'client_id': client_id,
            'client_secret': client_secret
        }

    else:
        #TODO: Fix a loadable json config loader.
        with open(creds_file, "r") as cfile:
            creds = cfile.read()

        try:
            data = json.loads(creds)
            creds = (data.get('uname', None), data.get('upass', None))
            client = {
                'client_id': data.get('client_id', ''),
                'client_secret': data.get('client_secret', '')
            }
        except TypeError:
            pass

    if not creds:
        raise Exception(msgs['no_creds_msg'])

    user_creds['creds'] = creds
    user_creds['client'] = client

    if returns:
        return user_creds


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
             "Invalid data passed in. Requires an iterable."
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
        data = self.client_data
        data.update({
            'scopes': [
                'repo'
            ]
        })  # Needs to be updatable from config. #TODO

        self.response = self.session.post(
            'https://api.github.com/authorizations',
            auth=self.auth,
            data=json.dumps(data)
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
        allowed_actions = ['repos']
        user_name = user_name or self.uname

        if not action in allowed_actions:
            action = "repos"
        action = action.lower()
        username = user_name.lower()

        if returns:
            return self._get_data(base_url.format(
                username, action), returns=returns)

    def get_repo_info(self, user_name=None,
                      repo_name=None, fields=None, returns=False):
        """Get repository information
        :rtype : None
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
            self.response = json.loads(self.response)
            response = deepcopy(self.response)
            response_copy = deepcopy(response)
            for key in response_copy.iterkeys():
                if key not in fields:
                    response.pop(key)
            self.response = response

        if returns:
            return self.response

    def search_repos(self, query=None, returns=False, fields=[]):
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
        if not (isinstance(fields, list) or isinstance(fields, tuple)):
            raise TypeError(self.msgs['invalid_iterable'])

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

    def get_user_events(self, user_name=None,
                        organization=False, returns=False):
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
        if returns:
            return self.response

__all__ = ['GitHub', 'get_auth', 'ARG_PARSER']
