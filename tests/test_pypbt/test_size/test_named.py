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

""" Tests for named methods of Range objects. """

# isort: STDLIB
import string
import unittest
from fractions import Fraction
import random

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists

# isort: LOCAL
from justbytes import (
    ROUND_DOWN,
    ROUND_HALF_DOWN,
    ROUND_HALF_UP,
    ROUND_TO_ZERO,
    ROUND_UP,
    ROUNDING_METHODS,
    B,
    BaseConfig,
    Config,
    DigitsConfig,
    DisplayConfig,
    Range,
    StringConfig,
    StripConfig,
    ValueConfig,
)
from justbytes._constants import UNITS, BinaryUnits, DecimalUnits

from utils import SIZE_DOMAIN


"""Test conversion methods."""

@forall(size = SIZE_DOMAIN,
        unit = UNITS() | 
        domains.DomainPyObject(Range,domains.Int(min_value = 1),UNITS())
        | None ,n_samples = 500)
def test_precision(size,unit):
    """Test precision of conversion."""
    factor = int(unit) if unit else int(B)
    return (int(size.convertTo(unit) * factor)) == int(size)



@forall(size = SIZE_DOMAIN,
        config = domains.DomainPyObject(ValueConfig, binary_units=domains.Boolean(),
        max_places=domains.Int(),
        min_value=domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1)),
        exact_value=domains.Boolean(),
        unit= (UNITS()+[None])),n_samples = 500)
def test_results(size, config):
    """Test component results."""
    (magnitude, unit) = size.components(config) 
    if magnitude * int(unit) != size.magnitude:
        return False

    if unit == B:
        return True

    if config.unit is None:
        if config.binary_units:
            if unit in BinaryUnits.UNITS():
                return True
        else:
            if unit in DecimalUnits.UNITS():
                return True
        return abs(magnitude) >= config.min_value
    else:
        return unit == config.unit


# """
# Test some aspects of the getString() method.
# """

@forall(a_size = SIZE_DOMAIN,
        config = domains.DomainPyObject(
        DisplayConfig,
        show_approx_str=domains.Boolean(),
        base_config= BaseConfig(),
        digits_config=DigitsConfig(use_letters=False),
        strip_config=StripConfig()
        ),
        base = domains.Int(min_value = 2, max_value =16),n_samples = 500)
def test_config(a_size, config, base):
    """
    Test properties of configuration.
    """
    result = a_size.getString(
        StringConfig(
            ValueConfig(base=base), config, Config.STRING_CONFIG.DISPLAY_IMPL_CLASS
        )
    )

    if config.base_config.use_prefix and base == 16:
        return result.find("0x") != -1
    else: return True

# """
# Test digits config.
# """
@forall(a_size = SIZE_DOMAIN,
        config = domains.DomainPyObject(DigitsConfig,
            separator=domains.String(alphabet= domains.exhaustible(['-','/','*','j',':']),max_len = 1),
            use_caps=domains.Boolean(),
            use_letters=domains.Boolean()),n_samples = 500)
def test_digits_config(a_size, config):
    """
    Test some basic configurations.
    """
    result = a_size.getString(
        StringConfig(
            Config.STRING_CONFIG.VALUE_CONFIG,
            DisplayConfig(digits_config=config),
            Config.STRING_CONFIG.DISPLAY_IMPL_CLASS,
        )
    )
    if config.use_letters:
        (number, _, _) = result.partition(" ")
        letters = [r for r in number if r in string.ascii_letters]
        if config.use_caps:
            return all(r in string.ascii_uppercase for r in letters)
        else:
            return all(r in string.ascii_lowercase for r in letters)
    else : return True


# """Test rounding methods."""

@forall(size = SIZE_DOMAIN,
        unit = SIZE_DOMAIN | UNITS(),
        rounding = domains.DomainFromIterable(ROUNDING_METHODS(),True),
        bounds = domains.Tuple(None | SIZE_DOMAIN,None | SIZE_DOMAIN),n_samples=500)
def test_bounds(size, unit, rounding, bounds):
    """
    Test that result is between the specified bounds,
    assuming that the bounds are legal.
    """
    (lower, upper) = bounds
    
    if lower is not None and upper is not None and lower > upper:
        return True
    rounded = size.roundTo(unit, rounding, bounds)
    if lower is not None and lower > rounded:
        return False
    if upper is not None and upper < rounded:
        return False
        
    return True


@forall(size = SIZE_DOMAIN,
        unit = SIZE_DOMAIN | UNITS(),
        rounding = domains.DomainFromIterable(ROUNDING_METHODS(),True),n_samples = 500)
def test_roundTo_results(size, unit, rounding):
    """Test roundTo results."""
    # pylint: disable=too-many-branches
    rounded = size.roundTo(unit, rounding)

    if (isinstance(unit, Range) and unit.magnitude == 0) or (
        not isinstance(unit, Range) and int(unit) == 0):
        return rounded == Range(0)

    converted = size.convertTo(unit)
    if converted.denominator == 1:
        return rounded == size

    factor = getattr(unit, "magnitude", None) or int(unit)
    (quotient, remainder) = divmod(converted.numerator, converted.denominator)
    ceiling = Range((quotient + 1) * factor)
    floor = Range(quotient * factor)
    if rounding is ROUND_UP:
        return rounded == ceiling

    if rounding is ROUND_DOWN:
        return rounded == floor

    if rounding is ROUND_TO_ZERO:
        if size > Range(0):
            return rounded == floor
        else:
            return rounded == ceiling

    remainder = abs(Fraction(remainder, converted.denominator))
    half = Fraction(1, 2)
    if remainder > half:
        return rounded == ceiling
    elif remainder < half:
        return rounded == floor
    else:
        if rounding is ROUND_HALF_UP:
            return rounded == ceiling
        elif rounding is ROUND_HALF_DOWN:
            return rounded == floor
        else:
            if size > Range(0):
                return rounded == floor
            else:
                return rounded == ceiling
