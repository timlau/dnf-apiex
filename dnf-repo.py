# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

from base import DnfBase

from dnf.yum.config import RepoConf

# we need 0.4.16 or later for the progress to work
from dnf.callback import DownloadProgress
class MDProgress(DownloadProgress):

    def __init__(self):
        super(MDProgress, self).__init__()
        self._last = None

    def start(self, total_files, total_size):
        #print("Start : ", total_files, total_size)
        self._last = None

    def end(self,payload, status, msg):
        #print ("End : ", str(payload), status, msg)
        pass

    def progress(self, payload, done):
        if not self._last:
            print ("  Getting repo metadata : %s " % str(payload))
            self._last = payload



class DnfExample(DnfBase):
    '''
    This example shows how to get packages matching a given
    package name.
    '''

    def __init__(self):
        DnfBase.__init__(self,setup_sack=False) # dont load the sack yet
        self.progress = MDProgress()
        # Find some repositories matching a filter
        print("Find *-source repos")
        for repo in self.find_repos("*-source"):
            print("  : %s" % repo.id)
        # Enable & disable some repositories
        self.enable_repos(['updates-testing'])
        self.disable_repos(['Dropbox'])
        self.repos.all.set_progress_bar(self.progress)  # Not public api
        print("Enabled repositories : ")
        for repo in self.repos.iter_enabled():
            print("  : %s" % repo.id)
        print("Setting up the package sack")
        self.fill_sack()
        print("show repo attributes")
        self.get_repo_attr('updates')

    def find_repos(self, filter):
        return self.repos.get_multiple(filter) # not public api

    def enable_repos(self, to_enable):
        for repo in self.repos.all: # not public api
            if repo.id in to_enable:
                repo.enable()

    def disable_repos(self, to_disable): # not public
        for repo in self.repos.all:
            if repo.id in to_disable:
                repo.disable()

    def find_repo(self,id):
        for repo in self.repos.all:
            if repo.id == id:
                return repo
        return None
                
    def get_repo_attr(self, id):
        repo = self.find_repo(id)
        if repo:
            print("%-20s : %s" % ("id", str(repo.id)))
            for attr in repo.iterkeys():
                res = getattr(repo, attr)
                print("%-20s : %s" % (attr, str(res)))

        

if __name__ == "__main__":
    de = DnfExample()
    del de


