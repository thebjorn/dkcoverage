# -*- coding: utf-8 -*-
import hashlib


def file_digest(fname):
    md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        while 1:
            data = f.read(2**13)  # 8196
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()
