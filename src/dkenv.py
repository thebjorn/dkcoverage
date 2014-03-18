# -*- coding: utf-8 -*-

import os
import sys
from .path import normpath

PYVERSION = '%d.%d' % sys.version_info[:2]
PYVERSION_DOTLESS = PYVERSION.replace('.', '')
DKROOT = normpath(os.environ['DKROOT'])
VIRTUAL_ENV = normpath(os.environ.get("VIRTUAL_ENV"))
WIN32 = sys.platform == 'win32'

PYTEST = 'c:/Python%s/Scripts/py.test-%s-script.py' % (PYVERSION_DOTLESS,
                                                       PYVERSION)

if VIRTUAL_ENV:
    if WIN32:
        PYTEST = os.path.join(
            VIRTUAL_ENV,
            'Scripts',
            'py.test-%s-script.py' % PYVERSION).replace('\\', '/')
    else:
        PYTEST = os.path.join(VIRTUAL_ENV, 'bin', 'py.test')


CONFIGRC = os.path.join(DKROOT, '.coveragerc').replace('\\', '/')
_cov_cmd = 'coverage run -p {PYTEST} --cov-config={CONFIGRC} {FILENAME}'
COVERAGE = _cov_cmd.replace("{CONFIGRC}", CONFIGRC).replace("{PYTEST}", PYTEST)

SKIPDIRS = ['node_modules', '.svn', 'templates', 'less', 'js', 'docs']

# def dkroot(pth=None):
#     "The root of the (datakortet) source tree."
#     root = DKROOT
#     if pth is None:
#         return canonical_path(root, '/')
#     return canonical_path(os.path.join(root, pth), '/')
