# coding=utf-8
"""Github social"""

__author__ = 'sriramm'

import sys
sys.dont_write_bytecode = True

from GitHubAccess import GitHub
from copy import deepcopy
import argparse


def main():
    """Main caller method"""
    github_obj = GitHub(creds=(None, None),
                        config={
                            'reverse': True,
                            'auth': True,
                            'safe_json': True
                        })
    repos = github_obj.search_repos({
        'keyword': 'shell',
        'sort': 'followers',
        'order': 'desc'
    }, returns=True).get('repositories', [])
    owners = {}
    for repo in repos:
        owner = repo.get('owner')
        if owner in owners.keys():
            owners[owner] += 1
        else:
            owners[owner] = 1

    owners_dup = deepcopy(owners)
    for (key, val) in owners.iteritems():
        if val < 2:
            owners_dup.pop(key)

    for (username, repo_count) in owners_dup.iteritems():
        print username, len(github_obj.get_user_info(username, action='repos', returns=True))


ArgParser = argparse.ArgumentParser()

ArgParser.add_argument('creds_file', metavar='f', type=str,
                    help='Credentials file')
ArgParser.add_argument('--c', dest='accumulate', action='store_const',
                       const=main, default=max)


if __name__ == '__main__':

    main()
