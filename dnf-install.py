# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import absolute_import

import os
from base import DnfBase

# we need 0.4.16 or later for the progress to work
from dnf.callback import DownloadProgress
class Progress(DownloadProgress):

    def __init__(self):
        super(Progress, self).__init__()

    def start(self, total_files, total_size):
        print("Start : ", total_files, total_size)

    def end(self,payload, status, msg):
        print ("End : ", str(payload), status, msg)

    def progress(self, payload, done):
        print ("Progress : ", str(payload), done)



class DnfExample(DnfBase):
    '''
    This example shows how to install a package
    '''

    def __init__(self):
        DnfBase.__init__(self)
        self.progress = Progress()
        print("=============== install btanks =====================")
        if os.getuid() != 0:
            print("You need to run this as root")
            return
        rc = self.install('btanks')
        print("# of packages added : %d" % rc)
        rc = self.resolve()
        to_dnl = []
        for tsi in self.transaction:
            print("   "+tsi.active_history_state+" - "+ str(tsi.active) )
            if tsi.installed:
                to_dnl.append(tsi.installed)
        print(to_dnl)
        print("Downloading Packages")
        print(self.download_packages(to_dnl, self.progress))
        print("Running Transaction")
        print(self.do_transaction())

if __name__ == "__main__":
    de = DnfExample()
    del de

