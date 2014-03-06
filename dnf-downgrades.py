# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

from base import DnfBase

class DnfExample(DnfBase):
    '''
    This example shows how to find available downgradess for a given
    package name.
    '''

    def __init__(self):
        DnfBase.__init__(self)
        name = 'yum'
        arch = 'noarch'
        ipkg, downgrades = self._get_downgrades(name, arch)
        if ipkg:
            print("Installed : %s " % str(ipkg))
            print("# of downgrades = %d" % (len(downgrades)))
            for pkg in downgrades:
                print(str(pkg))

    def _get_downgrades(self, name, arch):
        ''' Find available downgrades for a given name.arch'''
        q = self.sack.query()         # get the sack query object
        avail = q.available().filter(name=name, arch=arch).run()
        inst = q.installed().filter(name=name, arch=arch).run()
        downgrades = []
        ipkg = None
        if inst:
            ipkg = inst[0]
            for apkg in avail:
                if ipkg.evr_gt(apkg):
                    downgrades.append(apkg)
        return (ipkg, downgrades)

if __name__ == "__main__":
    de = DnfExample()
    del de


