# coding=utf-8
"""Github social"""

__author__ = 'sriramm'

#pylint:disable=W0511,R0914,W0142
# Disables
# W0511 : TODO tracks
# R0914 : Instance attribute count
# W0412 : magic calls

import sys
sys.dont_write_bytecode = True

from GitHubAccess import GitHub, get_auth, load_json_file
from copy import deepcopy


if __name__ == '__main__':
    RUN_METHODS = load_json_file("RUN_METHODS.json")
    USER_CREDS = get_auth()
    GH_OBJ = GitHub(creds=USER_CREDS['creds'],
                    config={
                        'reverse': False,
                        'auth': False,
                        'safe_json': True,
                        'client_data': USER_CREDS['client']
                    })

    for (key, val) in RUN_METHODS.get('RUN_METHODS').iteritems():
        GH_OBJ.__getattribute__(key)(**val)
        return_toggle_call_data = deepcopy(val)
        returns = return_toggle_call_data.get('returns')
        print "Attempting method {0} from GitHub access".format(key)
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
