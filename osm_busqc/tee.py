"""
Assertion/exception decorator
"""
import sys
from traceback import print_exc

from .config import DEBUG_STACKTRACE

def good_wrong(*args):
    return WrongCtxMan(args)


class WrongCtxMan:
    def __init__(self, *args):
        self.tokens = args

    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is None:
            return
            
        # else
        print("wrong on", *self.tokens, file=sys.stderr)
        print_exc(DEBUG_STACKTRACE)
        
        return True
# end WrongCtxMan

