'''
Created on Jul 26, 2013

@author: sriramm
'''
import sys
sys.dont_write_bytecode = True
from functools import wraps


def authenticated(instance_method):
    """Authentication check decorator for GitHub class"""
    @wraps(instance_method)
    def wrapper(self, *args, **kwargs):
        """Wrapper method for authentication check decorator"""
        if not self.auth:
            raise Exception(self.msgs['no_auth'])

        return instance_method(self, *args, **kwargs)

    return wrapper


__all__ = ['authenticated']
