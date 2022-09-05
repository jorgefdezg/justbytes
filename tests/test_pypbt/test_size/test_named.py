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


"""Test conversion methods."""

@forall(size = domains.DomainPyObject(Range,domains.Int(),UNITS()),n_samples = 5)
@forall(ranges = domains.DomainPyObject(Range,domains.Int(min_value=1),UNITS()),n_samples = 5)
@forall(units = domains.DomainFromIterable(UNITS(),True))
def test_precision(size, ranges, units):
    list_choice= [ranges,units,None]
    choice = random.choice(list_choice)
    """Test precision of conversion."""
    factor = int(choice) if choice else int(B)
    return (size.convertTo(choice) * factor) == int(size)



@forall(size = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),n_samples = 15)
@forall(config = domains.DomainPyObject(ValueConfig, binary_units=domains.Boolean(),
    max_places=domains.Int(),
    min_value=domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1)),
    exact_value=domains.Boolean(),
    unit= (UNITS()+[None])),n_samples = 15)
def test_results(size, config):
    """Test component results."""
    (magnitude, unit) = size.components(config)
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

@forall(size = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),n_samples = 15)
@forall(config = domains.DomainPyObject(ValueConfig, binary_units=domains.Boolean(),
    max_places=domains.Int(),
    min_value=domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1)),
    exact_value=domains.Boolean(),
    unit= (UNITS()+[None])),n_samples = 15)
def test_results_magnitude(size,config):
    """Test magnitude results."""
    (magnitude, unit) = size.components(config)
    return magnitude * int(unit) == size.magnitude
# """
# Test some aspects of the getString() method.
# """

@forall(a_size = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),n_samples = 10)
@forall(config = domains.DomainPyObject(
        DisplayConfig,
        show_approx_str=domains.Boolean(),
        base_config= BaseConfig(use_prefix= domains.Boolean(),use_subscript= domains.Boolean()),
        digits_config=DigitsConfig(use_letters=False),
        strip_config=StripConfig(strip_exact=domains.Boolean(), strip_whole=domains.Boolean())
    ),n_samples = 5)
@forall(base = domains.Int(min_value = 16, max_value =16),n_samples = 10)
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

# """
# Test digits config.
# """
@forall(a_size = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),n_samples = 5)
@forall(config = domains.DomainPyObject(DigitsConfig,
        separator=domains.String(coding = "ascii",max_len = 1),
        use_caps=domains.Boolean(),
        use_letters=domains.Boolean()))
def test_digits_config(a_size, config):
    """
    Test some basic configurations.
    """
    text = "-/*j:"
    if config.separator in text:
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
    else: return True

# """Test rounding methods."""

@forall(size = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),n_samples = 6)
@forall(bounds = domains.Tuple(domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS())),n_samples=5)
@forall(unit = domains.DomainFromIterable(UNITS(),True))
@exists(rounding = domains.DomainFromIterable(ROUNDING_METHODS(),True))
def test_bounds(size, unit, rounding, bounds):
    """
    Test that result is between the specified bounds,
    assuming that the bounds are legal.
    """
    (lower, upper) = bounds
    if lower > upper:
        return True
    rounded = size.roundTo(unit, rounding, bounds)
    if lower is not None and lower > rounded:
        return False
    if upper is not None and upper < rounded:
        return False
    return True


@forall(size = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),UNITS()),n_samples = 15)
@forall(unit = domains.DomainFromIterable(UNITS(),True))
@exists(rounding = domains.DomainFromIterable(ROUNDING_METHODS(),True))
def test_roundTo_results(size, unit, rounding):
    """Test roundTo results."""
    # pylint: disable=too-many-branches
    rounded = size.roundTo(unit, rounding)

    if (isinstance(unit, Range) and unit.magnitude == 0) or (
        not isinstance(unit, Range) and int(unit) == 0):
        if rounded != Range(0):
            return False

    converted = size.convertTo(unit)
    if converted.denominator == 1:
        if rounded != size:
            return False

    factor = getattr(unit, "magnitude", None) or int(unit)
    (quotient, remainder) = divmod(converted.numerator, converted.denominator)
    ceiling = Range((quotient + 1) * factor)
    floor = Range(quotient * factor)
    if rounding is ROUND_UP:
        if rounded != ceiling:
            return False

    if rounding is ROUND_DOWN:
        if rounded != floor:
            return False

    if rounding is ROUND_TO_ZERO:
        if size > Range(0):
            if rounded != floor:
                return False
        else:
            if rounded != ceiling:
                return False

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
