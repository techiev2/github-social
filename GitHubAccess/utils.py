"""
GitHub access class helper methods

Created on Jul 26, 2013

@author: sriramm
"""

# coding=utf-8
__author__ = 'sriramm'


#pylint:disable=W0511,R0902
# Disables
# W0511 : TODO tracks

import sys
sys.dont_write_bytecode = True

from functools import wraps
import argparse
import getpass
import json

ARG_PARSER = argparse.ArgumentParser(description="Creds loader")
ARG_PARSER.add_argument("--creds", help="Credentials file name")


def authenticated(instance_method):
    """Authentication check decorator for GitHub class"""
    @wraps(instance_method)
    def wrapper(self, *args, **kwargs):
        """Wrapper method for authentication check decorator"""
        if not self.auth:
            raise Exception(self.msgs['no_auth'])

        return instance_method(self, *args, **kwargs)

    return wrapper


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
            response = [x for x in data_file.readlines()
                         if x.find('//') % 4 != 0]
            response[-3:-2] = response[-3:-2][0].replace(',\n', '\n')
            response = reduce(lambda a, b: a.strip()
                               + b.strip(), response)
    except IOError:
        # Fail gracefully and send {} ?
        raise Exception("Unable to find specified file")


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
            client_secret = raw_input(msgs['client_secret_input']) or ''
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


def is_iterable(iterable):
    """
    Helper to check if an object is an iterable.
    Used with methods where data filter is used. Returns the
    an isinstance response for list|tuple.
    :param iterable:object Object to check for iterability.
    """
    return isinstance(iterable, list) or isinstance(iterable, tuple)

def is_stringy(in_string):
    """
    Helper to check if an object is stringy.
    Used with methods that do json.loads(). Returns the
    an isinstance response for str|unicode.
    :param iterable:object Object to check for iterability.
    """
    if in_string:
        return isinstance(in_string, str) or isinstance(in_string, unicode)

__all__ = ['authenticated', 'get_auth',
           'load_json_file', 'is_iterable',
           'is_stringy']
