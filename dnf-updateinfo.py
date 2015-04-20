from __future__ import absolute_import
from __future__ import print_function

import hawkey
import itertools
import sys

import dnf.subject

from base import DnfBase


ADV_INFO = """\
============================ Advisory ==========================
ID          : {0.id}
Title       : {0.title}
Type        : {1}

Description:
============
{0.description}

Files:
======
{2}

"""

REF_INFO = """\
 {0.id} - {0.title}
           {0.url}
"""

# Advisory types
ADV_TYPES = {
hawkey.ADVISORY_BUGFIX: "Bugfix",
hawkey.ADVISORY_SECURITY: "Security",
}



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
            # Get advisories for this package only
            # hawkey.LT for versions Less than
            # hawkey.GT for versions Greater than
            advs = pkg.get_advisories(hawkey.EQ)
            if advs:
                adv = advs[0]
                fns = "\n".join(adv.filenames)
                print(ADV_INFO.format(adv, ADV_TYPES[adv.type], fns))
                if adv.references:
                    print("References :\n")
                    for ref in adv.references:
                        print(REF_INFO.format(ref))

            else:
                print("  No advisory found for this packages")

if __name__ == "__main__":
    de = DnfExample()
    del de


