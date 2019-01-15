# -*- coding: utf-8 -*-

# Import Python libs
import re

# Import SQ-Black libs
from sqblack._version import get_versions

__version__ = get_versions()['version']
del get_versions

# Define __version_info__ attribute
regex = re.compile(
    r'(?P<year>[\d]{4})\.(?P<month>[\d]{1,2})\.(?P<day>[\d]{1,2})(?:\.dev0\+(?P<commits>[\d]+)\.(?:.*))?'
)
try:
    __version_info__ = tuple([int(p) for p in regex.match(__version__).groups() if p])
except AttributeError:
    __version_info__ = (0, 0, 0)
finally:
    del regex
