# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, unicode_literals
import hashlib
import logging
import time
from multiscanner.common.utils import hashfile

__author__ = "Drew Bonasera"
__license__ = "MPL 2.0"

TYPE = "Metadata"
NAME = "SHA256"

logger = logging.get_logger(__name__)


def check():
    return True


def scan(filelist):
    results = []

    for fname in filelist:
        goodtogo = False
        i = 0
        # Ran into a weird issue with file locking, this fixes it
        while not goodtogo and i < 5:
            try:
                results.append((fname, hashfile(fname, hashlib.sha256())))
                goodtogo = True
            except Exception as e:
                logger.error('SHA256: {}'.format(e))
                time.sleep(3)
                i += 1

    metadata = {}
    metadata["Name"] = NAME
    metadata["Type"] = TYPE
    metadata["Include"] = False
    return (results, metadata)
