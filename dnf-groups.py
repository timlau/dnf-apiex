# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import dnf.subject

from base import DnfBase

class DnfExample(DnfBase):
    '''
    This examples shows how to use read group info
    '''

    def __init__(self):
        DnfBase.__init__(self)
        self.read_comps()
        grps = self.comps.groups
        for grp in grps:
            print("%-30s : %s" % (grp.id, grp.ui_name))

if __name__ == "__main__":
    de = DnfExample()
    del de


