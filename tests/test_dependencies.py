# -*- coding: utf-8 -*-

import os
from dkcoverage.utils.dependencies import dependencies


def test_selfdeps():
    deps = list(sorted(dependencies(__file__, os.getcwd())))
    assert deps == [
        'dkcoverage/__init__.py',
        'dkcoverage/path.py',
        'dkcoverage/utils/__init__.py',
        'dkcoverage/utils/dependencies.py',
        ]
    
