#!/bin/python

import sys

# In Python, any variable can be re-bound at will -- and modules don't let you
# define special methods such as an instance's __setattr__ to stop attribute
# re-binding. Easy solution (in Python 2.1 and up): use an instance as
# "module"...
# Source: http://code.activestate.com/recipes/65207-constants-in-python/?in=user-97991

# Put in const.py...:
class _const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name]=value

sys.modules[__name__]=_const()

