# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import with_statement

__author__ = "Patrick Copeland"
__license__ = "MPL 2.0"

TYPE = "Metadata"
NAME = "filesize"


def check():
    return True


def scan(filelist):
    results = []

    for fname in filelist:
        with open(fname, 'rb') as fh:
            filesize = len(fh.read())
            results.append((fname, filesize))

    metadata = {}
    metadata["Name"] = NAME
    metadata["Type"] = TYPE
    metadata["Include"] = False
    return (results, metadata)
