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
        fields = ["name","summary","description"]
        values = ['yum','plugin']
        pkgs = self.search(fields,values)
        print("%d packages found (match_all)" % len(pkgs))
        pkgs = self.search(fields,values, match_all=False)
        print("%d packages found" % len(pkgs))
        pkgs = self.search(fields,values, showdups=True)
        print("%d packages found (showdups)" % len(pkgs))

    def search(self, fields, values, match_all=True, showdups=False):
        '''
        search in a list of package fields for a list of keys
        :param fields: package attributes to search in
        :param values: the values to match
        :param match_all: match all values (default)
        :param showdups: show duplicate packages or latest (default)
        :return: a list of package objects
        '''
        matches = set()
        for key in values:
            key_set = set()
            for attr in fields:
                pkgs = set(self.contains(attr,key).run())
                key_set |= pkgs
            if len(matches) == 0:
                matches = key_set
            else:
                if match_all:
                    matches &= key_set
                else:
                    matches |= key_set
        result = list(matches)
        if not showdups:
            result = self.sack.query().filter(pkg=result).latest()
        return result

    def contains(self, attr, needle, ignore_case=True):
        fdict = {'%s__substr' % attr : needle}
        if ignore_case:
            return self.sack.query().filter(hawkey.ICASE, **fdict)
        else:
            return self.sack.query().filter(**fdict)


if __name__ == "__main__":
    de = DnfExample()
    del de


