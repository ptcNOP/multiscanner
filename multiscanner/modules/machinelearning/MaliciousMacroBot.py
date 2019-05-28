# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, unicode_literals
import logging

__authors__ = "Austin West"
__license__ = "MPL 2.0"

TYPE = "MachineLearning"
NAME = "MaliciousMacroBot"
REQUIRES = ['filemeta']
DEFAULTCONF = {
    'ENABLED': False
}

logger = logging.getLogger(__name__)

try:
    from mmbot import MaliciousMacroBot
    has_mmbot = True
except ImportError as e:
    logger.error("mmbot module not installed...")
    has_mmbot = False


def check(conf=DEFAULTCONF):
    if not conf['ENABLED'] or \
       not has_mmbot or \
       None in REQUIRES:
        return False
    return True


def scan(filelist, conf=DEFAULTCONF):
    results = []
    filemeta_results, _ = REQUIRES[0]

    mmb = MaliciousMacroBot()
    mmb.mmb_init_model()

    for fname, filemeta_result in filemeta_results:
        if fname not in filelist:
            logger.debug("File not in filelist: {}".format(fname))
        if 'Microsoft' not in filemeta_result.get('filetype', ''):
            continue

        result = mmb.mmb_predict(fname, datatype='filepath')
        prediction = result.iloc[0].get('prediction', None)
        confidence = result.iloc[0].get('result_dictionary', {}).get('confidence')
        result_dict = {
            'Prediction': prediction,
            'Confidence': confidence
        }
        results.append((fname, result_dict))

    metadata = {}
    metadata["Name"] = NAME
    metadata["Type"] = TYPE
    return (results, metadata)


def _get_libmagicresults(results, fname):
    libmagicdict = dict(results)
    return libmagicdict.get(fname)
