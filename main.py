# coding=utf-8
"""Github social"""

__author__ = 'sriramm'

#pylint:disable=W0511,R0914
# Disables
# W0511 : TODO tracks
# R0914 : Instance attribute count

import sys

sys.dont_write_bytecode = True

from GitHubAccess import GitHub
import getpass
import argparse
import json


def get_auth(returns=True):
    """Get authentication data
    :param returns:bool Boolean check to return data from get_auth
    """
    (creds, client) = (None, None)
    user_creds = {}
    arg_parser = argparse.ArgumentParser(description="Creds loader")
    arg_parser.add_argument("--creds", help="Credentials file name")
    creds_file = arg_parser.parse_args().__getattribute__('creds')
    no_creds = "No credentials file provided. Defaulting to shell input"
    uname_input = "Please enter your GitHub username to authenticate: "
    upass_input = "Please enter your GitHub password to authenticate: "
    client_id_input = "Please enter your GitHub client ID: "
    client_secret_input = "Please enter your GitHub client secret: "
    if not creds_file:
        print no_creds
        try:
            uname = raw_input(uname_input)
            upass = getpass.getpass(upass_input)
            client_id = raw_input(client_id_input) or ''
            client_secret = raw_input(client_secret_input) or ''
        except KeyboardInterrupt:
            quit("\nKeyboard interrupt. Exiting")

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
        raise Exception("No credentials found. Exiting")

    user_creds['creds'] = creds
    user_creds['client'] = client

    if returns:
        return user_creds


if __name__ == '__main__':
    USER_CREDS = get_auth()
    GH_OBJ = GitHub(creds=USER_CREDS['creds'],
                    config={
                        'reverse': False,
                        'auth': True,
                        'safe_json': True,
                        'client_data': USER_CREDS['client']
                    })
    repo_info = GH_OBJ.get_repo_info('Imaginea', 'Stitchemapp', fields=['owner'],
                                     returns=True)
    print repo_info
