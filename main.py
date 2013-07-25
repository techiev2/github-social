# coding=utf-8
"""Github social"""

__author__ = 'sriramm'

#pylint:disable=W0511,R0914
# Disables
# W0511 : TODO tracks
# R0914 : Instance attribute count

import sys
sys.dont_write_bytecode = True

from GitHubAccess import GitHub, get_auth, load_json_file


if __name__ == '__main__':
    methods = load_json_file("methods.json")
    USER_CREDS = get_auth()
    GH_OBJ = GitHub(creds=USER_CREDS['creds'],
                    config={
                        'reverse': False,
                        'auth': True,
                        'safe_json': True,
                        'client_data': USER_CREDS['client']
                    })

    for (key, val) in methods.get('methods').iteritems():
        GH_OBJ.__getattribute__(key)(**val)
        try:
            assert isinstance(GH_OBJ.response, dict)
        except AssertionError:
            pass
