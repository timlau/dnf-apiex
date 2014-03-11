# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

from base import DnfBase

class DnfExample(DnfBase):
    '''
    This example shows how to get packages matching a given
    reponame.
    '''

    def __init__(self):
        DnfBase.__init__(self)
        print("======= packages with reponame = dnf-daemon-test ======")
        q = self.sack.query()         # get the sack query object
        print("Available in repositories: ")
        a = q.available()             # get all available package
        a = a.filter(reponame='dnf-daemon-test')    # filter packages with the name kernel
        for pkg in a:                 # a only gets evaluated here
            print("  pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))

if __name__ == "__main__":
    de = DnfExample()
    del de


