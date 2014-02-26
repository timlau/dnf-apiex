# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import dnf.subject

from base import DnfBase

class DnfExample(DnfBase):
    '''
    This examples shows how to use the dnf.subject.Subject to
    find packages matching a wildcard like yum*
    '''

    def __init__(self):
        DnfBase.__init__(self)
        print("=============== packages matching yum* =====================")
        subj = dnf.subject.Subject("yum*")
        qa = subj.get_best_query(self.sack, with_provides=False)
        print("==== all packages  matching yum* =====")
        for pkg in qa:
            print("  pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))
        print("==== latest matching yum* =====")
        for pkg in qa.latest():
            print("  pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))
        print("==== Installed matching yum* =====")
        for pkg in qa.installed():
            print("  pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))

if __name__ == "__main__":
    de = DnfExample()
    del de


