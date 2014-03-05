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
        i = 0
        for grp in grps:
            i += 1
            if i % 10 == 0:
                self.show_group_packages(grp)
        cats = self.comps.categories
        for cat in cats:
            print(cat.name)
            for obj in cat.group_ids: # groups_ids is not public api
                grp = self.comps.group_by_pattern(obj.name) # get the dnf group obj
                if grp:
                    print("    ", grp.name, grp.ui_name)
                else:
                    print ("     ******* Not Found : %s " % obj.name)

    def show_group_packages(self, grp):
        print("==== Group : %s ===================================" % grp.id)
        if len(grp.mandatory_packages) > 0:
            print(" === Mandatory Packages ===")
            for pkg in grp.mandatory_packages:
                print("  : %s " % pkg.name)
        if len(grp.default_packages) > 0:
            print(" === Default Packages ===")
            for pkg in grp.default_packages:
                print("  : %s "  % pkg.name)
        if len(grp.optional_packages) > 0:
            print(" === Optional Packages ===")
            for pkg in grp.optional_packages:
                print("  : %s " % pkg.name)

if __name__ == "__main__":
    de = DnfExample()
    del de


