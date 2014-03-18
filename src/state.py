# -*- coding: utf-8 -*-

foo = {
    "root": "/absolute/path/",
    "files": {
        'dira/file1': {
            "version": '12345',
            "tests": ['dira/tests/test_foo'],
        },
        'dira/file2': ['dira/tests/test_foo'],
        'dirb/file1': ['dira/tests/test_foo'],
        'dirb/file2': ['dira/tests/test_foo'],
    }
}
