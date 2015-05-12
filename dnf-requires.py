from __future__ import absolute_import
from __future__ import print_function

import functools
import hawkey
import subprocess
import sys

import dnf.subject

from base import DnfBase

ARCH = subprocess.check_output(
    '/usr/bin/rpm --eval %_arch', shell=True).decode("utf-8")[:-1]


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
            req_dict = self._get_requirements(pkg)
            self.show_req(req_dict)

    def _get_requirements(self, pkg):
        req_dict = {}
        requires = pkg.requires
        q = self.sack.query()
        for req in requires:
            req_str = str(req)
            if 'solvable:' in req_str:
                continue
            providers = self.by_provides(self.sack, [req_str], q)
            req_dict[req_str] = []
            for prov in providers.latest().run():
                if prov.arch == ARCH or prov.arch == 'noarch':
                    req_dict[req_str].append(prov)
        return req_dict

    def show_req(self, req_dict):
        for key in req_dict:
            print(' {}'.format(key))
            for po in req_dict[key]:
                print(' --> {}'.format(str(po)))

    @staticmethod
    def by_provides(sack, pattern, query):
        """Get a query for matching given provides."""
        try:
            reldeps = list(map(functools.partial(hawkey.Reldep, sack),
                               pattern))
        except hawkey.ValueException:
            return query.filter(empty=True)
        return query.filter(provides=reldeps)


if __name__ == "__main__":
    de = DnfExample()
    del de


