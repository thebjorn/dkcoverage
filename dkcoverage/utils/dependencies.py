# -*- coding: utf-8 -*-


from modulefinder import ModuleFinder
from ..path import normpath


def dependencies(fname, root=None):
    """Find all dependencies (i.e. imported modules) from fname without
       running it.

       If `root` is specified, only modules having __file__ attributes
       under this root is included.

       This function is quite slow..
    """
    global count
    assert fname.endswith('.py')

    res = set()
    finder = ModuleFinder()
    try:
        finder.run_script(fname)
    except:
        return []

    root = normpath(root, slash='/')
    prefix = len(root) + 1  # for trailing slash

    for name, mod in finder.modules.iteritems():
        if name.startswith('_'):
            continue
        modpath = normpath(mod.__file__, slash='/')
        if modpath.startswith(root):
            # print 'name:', name
            # print 'mod.__file__:', mod.__file__
            # print 'normpath:', modpath
            # print 'root:', root
            # print

            res.add(modpath[prefix:])

    return list(sorted(res))
