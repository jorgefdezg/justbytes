# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

""" Test for configuration classes. """
import unittest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes._config import DisplayConfig
from justbytes._config import InputConfig
from justbytes._config import RangeConfig
from justbytes._config import ValueConfig

from justbytes._constants import RoundingMethods
from justbytes._constants import UNITS

from justbytes._errors import RangeValueError


class ConfigTestCase(unittest.TestCase):
    """ Exercise methods of output configuration classes. """
    # pylint: disable=too-few-public-methods

    def testValueConfigObject(self):
        """ Miscellaneous tests for string configuration. """
        self.assertIsInstance(str(RangeConfig.VALUE_CONFIG), str)

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(RangeValueError):
            ValueConfig(min_value=-1)
        with self.assertRaises(RangeValueError):
            ValueConfig(min_value=3.2)
        with self.assertRaises(RangeValueError):
            ValueConfig(unit=2)
        with self.assertRaises(RangeValueError):
            ValueConfig(base=1)

class InputTestCase(unittest.TestCase):
    """ Exercise methods of input configuration classes. """
    # pylint: disable=too-few-public-methods

    def testInputConfigObject(self):
        """ Miscellaneous tests for input configuration. """
        self.assertIsInstance(str(RangeConfig.INPUT_CONFIG), str)

class RangeTestCase(unittest.TestCase):
    """ Test Range configuration. """
    # pylint: disable=too-few-public-methods

    def setUp(self):
        self.display_config = RangeConfig.DISPLAY_CONFIG
        self.input_config = RangeConfig.INPUT_CONFIG
        self.str_config = RangeConfig.VALUE_CONFIG

    def tearDown(self):
        RangeConfig.DISPLAY_CONFIG = self.display_config
        RangeConfig.INPUT_CONFIG = self.input_config
        RangeConfig.VALUE_CONFIG = self.str_config

    @given(
       strategies.builds(
          DisplayConfig,
          show_approx_str=strategies.booleans()
       )
    )
    @settings(max_examples=30)
    def testSettingDisplayConfig(self, config):
        """ Test that new str config is the correct one. """
        RangeConfig.set_display_config(config)
        self.assertEqual(str(config), str(RangeConfig.DISPLAY_CONFIG))

    @given(
       strategies.builds(
          ValueConfig,
          binary_units=strategies.booleans(),
          max_places=strategies.integers().filter(lambda x: x >= 0),
          min_value=strategies.fractions().filter(lambda x: x >= 0),
          exact_value=strategies.booleans(),
          unit=strategies.sampled_from(UNITS())
       )
    )
    @settings(max_examples=30)
    def testSettingValueConfig(self, config):
        """ Test that new str config is the correct one. """
        RangeConfig.set_value_config(config)
        self.assertEqual(str(config), str(RangeConfig.VALUE_CONFIG))

    @given(
       strategies.builds(
          InputConfig,
          method=strategies.sampled_from(RoundingMethods.METHODS()),
          unit=strategies.sampled_from(UNITS())
       )
    )
    @settings(max_examples=10)
    def testSettingInputConfig(self, config):
        """ That that new input config is the correct one. """
        RangeConfig.set_input_config(config)
        self.assertEqual(str(config), str(RangeConfig.INPUT_CONFIG))
