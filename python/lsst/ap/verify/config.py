#
# LSST Data Management System
# Copyright 2017 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

from __future__ import absolute_import, division, print_function

from future.utils import raise_from

from lsst.daf.persistence import Policy


class Config(object):
    """Confuration manager for ``ap_verify``.

    This is a singleton `lsst.daf.persistence.Policy` that may be accessed
    from other modules in ``ap_verify`` as needed using `Config.instance`.
    Please do not construct objects of this class directly.
    """

    def __init__(self):
        path = Policy.defaultPolicyFile('ap_verify', 'dataset_config.yaml', 'config')
        self._allInfo = Policy(path)
        self._validate()

    def _validate(self):
        """Test that the loaded configuration is correct.

        Raises
        ------
        `RuntimeError`
            Validation failed
        """
        try:
            datasetMap = self._allInfo['datasets']
            if not isinstance(datasetMap, Policy):
                raise TypeError('`datasets` is not a dictionary')
        except (KeyError, TypeError) as e:
            raise_from(RuntimeError('Invalid config file.'), e)

        try:
            measurementMap = self._allInfo['measurements']
            if not isinstance(measurementMap, Policy):
                raise TypeError('`measurements` is not a dictionary')
            timingMap = measurementMap['timing']
            if not isinstance(timingMap, Policy):
                raise TypeError('`measurements.timing` is not a dictionary')
        except (KeyError, TypeError) as e:
            raise_from(RuntimeError('Invalid config file.'), e)


# Hack, but I don't know how else to make Config.instance act like a dictionary of config options
Config.instance = Config()._allInfo
