# Copyright (c) 2014 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common functions, mainly configuration parsing."""

from __future__ import absolute_import, print_function, unicode_literals
import logging
import os.path
from six.moves import configparser
try:
    from collections import OrderedDict
except ImportError:  # Python 2.6
    from odict import odict as OrderedDict

LOG = logging.getLogger('launchpadstats')

# use OrderedDict so that configparser keeps the order of sections
DEFAULTS = OrderedDict([
    ('project_type', 'all'),
    ('company', ''),
    ('people', 'all'),
    ('releases', 'all'),
    ('table_type', 'group-metrics'),
    ('metrics', 'filed_bug_count,resolved_bug_count'),
])

# characters used as separator between items in the CSV output
CSV_SEPARATOR = '; '
# how will the reviews be shown
REVIEWS_FORMAT = ['-2', '-1', '1', '2', 'A']
METRICS = set(['loc', 'email_count', 'commit_count', 'drafted_blueprint_count',
               'completed_blueprint_count', 'filed_bug_count',
               'resolved_bug_count', 'patch_set_count', 'reviews'])
# which metrics should be skipped when a sum is made of the metrics
SKIP_FROM_SUM = ['reviews', 'loc']


class ReturnUnknownKeyDict(dict):
    """If a value for the key is not found, return the key."""
    def __missing__(self, key):
        return key


# alternative names for things like metrics, to improve readability in results
PRETTY_NAME = ReturnUnknownKeyDict({
    'reviews': 'reviews (%s)' % ', '.join(['+' + x if x in ['1', '2'] else x
                                           for x in REVIEWS_FORMAT]),
})


class ConfigurationError(Exception):
    pass


def get_config(filepath):
    """Read the .ini configuration file given in filepath.

    If no filepath is given, try reading 'config.ini' in the project directory.

    :returns: ConfigParser object
    """
    LOG.info("Reading configuration file '%s'", filepath)
    if not os.path.isfile(filepath):
        raise ConfigurationError("No such file '%s'" % filepath)

    config = configparser.ConfigParser(DEFAULTS,
                                       dict_type=OrderedDict)
    config.read(filepath)
    return config
