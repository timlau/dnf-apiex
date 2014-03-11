# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

from base import DnfBase

class DnfExample(DnfBase):
    '''
    This example shows how to get packages matching a given
    package name.
    '''

    def __init__(self):
        DnfBase.__init__(self, setup_sack=False)
        for repo in self.repos.all():
            if repo.id == 'dnf-daemon-test':
                repo.enable()
            else:
                repo.disable()
        self.setup_base()
        q = self.sack.query()         # get the sack query object
        print("Available in repositories: all")
        a = q.available()             # get all available package
        for pkg in a:                 # a only gets evaluated here
            print("  pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))
        print("Available in repositories: latest")
        a = q.available().latest()             # get all available package
        for pkg in a:                 # a only gets evaluated here
            print("  pkg : %-40s repo :  %-20s" % (pkg, pkg.reponame))

if __name__ == "__main__":
    de = DnfExample()
    del de


