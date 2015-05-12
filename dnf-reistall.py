from __future__ import absolute_import
from __future__ import print_function

import hawkey
import itertools
import sys

import dnf.subject

from base import DnfBase


class DnfExample(DnfBase):
    '''
    This examples shows how to use the dnf.subject.Subject to
    find packages matching a wildcard like yum*
    '''

    def __init__(self):
        DnfBase.__init__(self)
        if len(sys.argv) < 2:
            print("USAGE: dnf-updateinfo <packagename>")
            sys.exit(1)
        key = sys.argv[1]
        subj = dnf.subject.Subject(key)
        qa = subj.get_best_query(self.sack, with_provides=False)
        qa = qa.available()
        print("==== latest matching {} =====".format(key))
        for pkg in qa.latest():
            print("pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))
            self.package_reinstall(pkg)
            rc = self.resolve()
            print(rc)

if __name__ == "__main__":
    de = DnfExample()
    del de


