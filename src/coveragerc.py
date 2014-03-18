# -*- coding: utf-8 -*-

"""Create .coveragerc file from _coverage_settings.txt file.

   Finding the correct/interesting Python files is dependent on that .rc file.
"""

import os
from . import dkenv





# def create_rc():
#     "Create {DKROOT}/.coveragerc from {DKROOT}/_coverage_settings.txt"
#     dkroot = canonical_path(dkenv.DKROOT, '/')
#     srcroot = canonical_path(os.path.join(dkroot, '..'), '/')
#
#     with open(os.path.join(dkroot, '.coveragerc'), 'w') as fp:
#         for line in open(os.path.join(dkroot, '_coverage_settings.txt')):
#             fp.write(line.replace('{DKROOT}', dkroot)
#                      .replace('{SRCROOT}', srcroot))
