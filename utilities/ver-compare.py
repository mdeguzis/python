#!/bin/python
# apt_pkg.version_compare(a: str, b: str) → int
# requires python-apt or equiv. package
# https://pypi.python.org/pypi/apt

import apt_pkg
import argparse

apt_pkg.init_system()

aparser = argparse.ArgumentParser(description="Comare debian versions")
aparser.add_argument('-a', help="version a")
aparser.add_argument('-b', help="vesion b")
args = aparser.parse_args()

a = args.a
b = args.b

vc = apt_pkg.version_compare(a,b)
if vc > 0:
    print('version a > version b')
elif vc == 0:
    print('version a == version b')
elif vc < 0:
    print('version a < version b')
