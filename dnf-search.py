# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import dnf.subject
import dnf.util
import dnf.match_counter
import hawkey

from base import DnfBase

class DnfExample(DnfBase):
    '''
    Test keyword searching
    '''
    def __init__(self):
        DnfBase.__init__(self)
        self.simple_search()
        self.highlevel_search()

    def highlevel_search(self):
        fields = ["name","summary","description"]
        values = ['yum','plugin']
        pkgs = self.search(fields,values)
        print("%d packages found (match_all)" % len(pkgs))
        #for pkg in pkgs:
        #    print(pkg)
        pkgs = self.search(fields,values, match_all=False)
        print("%d packages found" % len(pkgs))
        pkgs = self.search(fields,values, showdups=True)
        print("%d packages found (showdups)" % len(pkgs))

    def simple_search(self):
        q = self.get_search_query("description","yum")
        for pkg in q.run():
            print("%s" % str(pkg))
            print("=========================================================================")
            print("%s" % (pkg.description))
            print("-------------------------------------------------------------------------")

    def search(self, fields, values, match_all=True, showdups=False):
        '''
        search in a list of package fields for a list of keys
        :param fields: package attributes to search in
        :param values: the values to match
        :param match_all: match all values (default)
        :param showdups: show duplicate packages or latest (default)
        :return: a list of package objects
        '''
        num_val = len(values)
        counter = dnf.match_counter.MatchCounter() # not public api
        for arg in values:
            for field in fields:
                self.search_counted(counter, field, arg) # not public api
        if match_all and num_val > 1:
            res = []
            for pkg in counter:
                if len(counter.matched_needles(pkg)) == num_val:
                    res.append(pkg)
        else:
            res = counter.keys()
        if not showdups:
            limit = self.sack.query().filter(pkg=res).latest()
            return limit
        else:
            return res

    def get_search_query(self, attr, needle, query = None):
        fdict = self._hawkey_search_dict(attr, needle)
        if query: # filter a existing query
            return query.filter(hawkey.ICASE, **fdict)
        else: # filter the full sack
            return self.sack.query().filter(hawkey.ICASE, **fdict)

    def _hawkey_search_dict(self, attr, needle):
        fdict = {'%s__substr' % attr : needle}
        if dnf.util.is_glob_pattern(needle):
            fdict = {'%s__glob' % attr : needle}
        return fdict

if __name__ == "__main__":
    de = DnfExample()
    del de


