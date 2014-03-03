# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from base import DnfBase

# we need 0.4.16 or later for the progress to work
from dnf.callback import DownloadProgress
class Progress(DownloadProgress):

    def __init__(self):
        super(Progress, self).__init__()
        self.total_files = 0
        self.total_size = 0.0
        self.download_files = 0
        self.download_size = 0.0
        self.dnl = {}
        self.last_pct = 0

    def start(self, total_files, total_size):
        print("Downloading :  %d files,  %d bytes" % (total_files, total_size))
        self.total_files = total_files
        self.total_size = total_size
        self.download_files = 0
        self.download_size = 0.0


    def end(self,payload, status, msg):
        if not status: # payload download complete
            self.download_files += 1
            self.update()
        else: # dnl end with errors
            self.update()

    def progress(self, payload, done):
        pload = str(payload)
        if not pload in self.dnl:
            self.dnl[pload] = 0.0
            print("Starting to download : %s " % str(payload))
        else:
            self.dnl[pload] = done
            pct = self.get_total()
            if pct > self.last_pct:
                self.last_pct = pct
                self.update()


    def get_total(self):
        """ Get the total downloaded percentage"""
        tot = 0.0
        for value in self.dnl.values():
            tot += value
        pct = int((tot / float(self.total_size)) * 100)
        return pct

    def update(self):
        """ Output the current progress"""
        sys.stdout.write("Progress : %-3d %% (%d/%d)\r" % (self.last_pct,self.download_files, self.total_files))



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
        self.apply_transaction()

    def apply_transaction(self):
        rc = self.resolve()
        print("Depsolve rc: ", rc)
        if rc:
            to_dnl = self.get_packages_to_download()
            # Downloading Packages
            self.download_packages(to_dnl, self.progress)
            print("\nRunning Transaction")
            print(self.do_transaction())
        else:
            print("Depsolve failed")

    def get_packages_to_download(self):
        to_dnl = []
        for tsi in self.transaction:
            print("   "+tsi.active_history_state+" - "+ str(tsi.active) )
            if tsi.installed:
                to_dnl.append(tsi.installed)
        return to_dnl
if __name__ == "__main__":
    de = DnfExample()
    del de

