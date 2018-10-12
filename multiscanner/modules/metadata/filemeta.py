# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from collections import Counter
from hashlib import md5, sha1, sha256

import math

try:
    import magic
except ImportError:
    print("python-magic module not installed...")
    magic = False

try:
    import ssdeep
except ImportError:
    print("ssdeep module not installed...")
    ssdeep = False

__author__ = "Patrick"
__license__ = "MPL 2.0"

TYPE = "metadata"
NAME = "filemeta"


def check():
    return True


def scan(filelist):
    results = []

    for fname in filelist:
        with open(fname, 'rb') as fh:
            buf = fh.read()

            meta_dict = {}

            meta_dict['filesize'] = len(buf)

            if magic:
                filetype = magic.from_buffer(buf)
                mimetype = magic.from_buffer(buf, mime=True)
                meta_dict['filetype'] = filetype
                meta_dict['mimetype'] = mimetype

            # hashes
            meta_dict['md5'] = md5(buf).hexdigest()
            meta_dict['sha1'] = sha1(buf).hexdigest()
            meta_dict['sha256'] = sha256(buf).hexdigest()

            if ssdeep:
                ssdeep_hash = ssdeep.hash(buf)
                chunksize, chunk, double_chunk = ssdeep_hash.split(':')
                chunksize = int(chunksize)
                ssdeep_doc = {
                    'ssdeep_hash': ssdeep_hash,
                    'chunksize': chunksize,
                    'chunk': chunk,
                    'double_chunk': double_chunk,
                    'analyzed': 'false',
                    'matches': {},
                }
                meta_dict['ssdeep'] = ssdeep_doc

            chars, lns = Counter(buf), float(len(buf))
            meta_dict['entropy'] = -sum(count / lns * math.log(count / lns, 2) for count in chars.values())

        results.append((fname, meta_dict))

    metadata = {}
    metadata["Name"] = NAME
    metadata["Type"] = TYPE
    metadata["Include"] = False
    return (results, metadata)
