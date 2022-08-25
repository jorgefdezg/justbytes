# Copyright (C) 2015 - 2019 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

""" Test for configuration classes. """
# isort: STDLIB
import unittest

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists
from fractions import Fraction

# isort: LOCAL
from justbytes._config import Config, DisplayConfig, ValueConfig
from justbytes._constants import UNITS


"""Test Range configuration."""


@forall(config = domains.DomainPyObject(DisplayConfig,show_approx_str=domains.Boolean()))
def test_setting_display_config(config):
    """Test that new str config is the correct one."""
    Config.set_display_config(config)
    return str(config) == str(Config.STRING_CONFIG.DISPLAY_CONFIG)


@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(config = lambda units: domains.DomainPyObject(ValueConfig, binary_units=domains.Boolean(),
    max_places=domains.Int(),
    min_value=domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1)),
    exact_value=domains.Boolean(),
    unit=units),n_samples = 10)
def test_setting_value_config(units,config):
    """Test that new str config is the correct one."""
    Config.set_value_config(config)
    return str(config) == str(Config.STRING_CONFIG.VALUE_CONFIG)
