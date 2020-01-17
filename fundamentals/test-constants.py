#!/bin/python
import constant

#  bind an attribute ONCE:
constant.magic = 23
# but NOT re-bind it:
constant.magic = 88      # raises const.ConstError
# you may also want to add the obvious __delattr_
