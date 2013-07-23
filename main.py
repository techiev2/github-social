# coding=utf-8
"""Github social"""

__author__ = 'sriramm'

import sys
sys.dont_write_bytecode = True

from GitHubAccess import GitHub
import getpass
import argparse


AP = argparse.ArgumentParser(description="Creds loader")
AP.add_argument("--creds", help="Credentials file name")


if __name__ == '__main__':
    creds = None
    creds_file = AP.parse_args().__getattribute__('creds')
    no_creds = "No credentials file provided. Defaulting to shell input"
    uname_input = "Please enter your GitHub username to authenticate: "
    upass_input = "Please enter your GitHub password to authenticate: "
    if not creds_file:
        print no_creds
        uname = raw_input(uname_input)
        upass = getpass.getpass(upass_input)
        if (uname and upass):
            creds = (uname, upass)
    else:
        with open(creds_file, "r") as cfile:
            creds = cfile.read()
        creds = tuple([x.strip() for x in creds.split(",")])

    if not creds:
        raise Exception("No credentials found. Exiting")

    github_obj = GitHub(creds=creds,
                        config={
                            'reverse': False,
                            'auth': True,
                            'safe_json': True
                        })
    print github_obj.response
