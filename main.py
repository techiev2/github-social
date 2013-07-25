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
from copy import deepcopy


if __name__ == '__main__':
    methods = load_json_file("methods.json")
    failure_methods = load_json_file("failure_methods.json")
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
        return_toggle_call_data = deepcopy(val)
        returns = return_toggle_call_data.get('returns')
        if returns:
            if returns == False:
                return_toggle_call_data['returns'] = True
            if returns == True:
                return_toggle_call_data['returns'] = False
            GH_OBJ.__getattribute__(key)(**return_toggle_call_data)

        try:
            assert isinstance(GH_OBJ.response, dict)
        except AssertionError:
            pass
