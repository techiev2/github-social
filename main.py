# coding=utf-8
"""Github social"""

__author__ = 'sriramm'

import sys
sys.dont_write_bytecode = True

from GitHubAccess import GitHub
import getpass
import argparse


def get_auth(returns=True):
    """Get authentication data"""
    creds = None
    arg_parser = argparse.ArgumentParser(description="Creds loader")
    arg_parser.add_argument("--creds", help="Credentials file name")
    creds_file = arg_parser.parse_args().__getattribute__('creds')
    no_creds = "No credentials file provided. Defaulting to shell input"
    uname_input = "Please enter your GitHub username to authenticate: "
    upass_input = "Please enter your GitHub password to authenticate: "
    # client_id_input = "Please enter your GitHub client ID: "
    # client_secret_input = "Please enter your GitHub client secret: "
    if not creds_file:
        print no_creds
        uname = raw_input(uname_input)
        upass = getpass.getpass(upass_input)
        if (uname and upass):
            creds = (uname, upass)
    else:
        #TODO: Fix a loadable json config loader.
        with open(creds_file, "r") as cfile:
            creds = cfile.read()
        creds = tuple([x.strip() for x in creds.split(",")])

    if not creds:
        raise Exception("No credentials found. Exiting")

    if returns:
        return creds


if __name__ == '__main__':
    USER_CREDS = {
        'creds': get_auth(returns=True),
        'client': {
            'client_id': '',
            'client_secret': ''
        }
    }
    GH_OBJ = GitHub(creds=USER_CREDS['creds'],
                        config={
                            'reverse': False,
                            'auth': True,
                            'safe_json': True,
                            'client_data': USER_CREDS['client']
                        })
    print GH_OBJ.response
