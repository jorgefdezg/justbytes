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

# isort: THIRDPARTY
from hypothesis import assume, example, given, settings, strategies

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

#use this import if you are running this file with pytest
#from tests.test_hypothesis.test_size.utils import SIZE_STRATEGY


#use this import if you are running this file with pypbt
from utils import SIZE_STRATEGY  # isort:skip


class ConversionTestCase(unittest.TestCase):
    """Test conversion methods."""

    @given(
        strategies.builds(Range, strategies.integers()),
        strategies.one_of(
            strategies.none(),
            strategies.sampled_from(UNITS()),
            strategies.builds(Range, strategies.integers(min_value=1)),
        ),
    )
    @settings(max_examples=500)
    def test_precision(self, size, unit):
        """Test precision of conversion."""
        factor = int(unit) if unit else int(B)
        self.assertEqual(size.convertTo(unit) * factor, int(size))


class ComponentsTestCase(unittest.TestCase):
    """Test components method."""

    @given(
        SIZE_STRATEGY,
        strategies.builds(
            ValueConfig,
            min_value=strategies.fractions().filter(lambda x: x >= 0),
            binary_units=strategies.booleans(),
            exact_value=strategies.booleans(),
            max_places=strategies.integers(min_value=0, max_value=5),
            unit=strategies.sampled_from(UNITS() + [None]),
        ),
    )
    @settings(max_examples=500)
    def test_results(self, size, config):
        """Test component results."""
        (magnitude, unit) = size.components(config)
        self.assertEqual(magnitude * int(unit), size.magnitude)
        if unit == B:
            return

        if config.unit is None:
            if config.binary_units:
                self.assertIn(unit, BinaryUnits.UNITS())
            else:
                self.assertIn(unit, DecimalUnits.UNITS())
            self.assertTrue(abs(magnitude) >= config.min_value)
        else:
            self.assertEqual(unit, config.unit)


class DisplayConfigTestCase(unittest.TestCase):
    """
    Test some aspects of the getString() method.
    """

    @given(
        SIZE_STRATEGY,
        strategies.builds(
            DisplayConfig,
            show_approx_str=strategies.booleans(),
            base_config=strategies.just(BaseConfig()),
            digits_config=strategies.just(DigitsConfig(use_letters=False)),
            strip_config=strategies.just(StripConfig()),
        ),
        strategies.integers(min_value=2, max_value=16),
    )
    @settings(max_examples=500)
    def test_config(self, a_size, config, base):
        """
        Test properties of configuration.
        """
        result = a_size.getString(
            StringConfig(
                ValueConfig(base=base), config, Config.STRING_CONFIG.DISPLAY_IMPL_CLASS
            )
        )

        if config.base_config.use_prefix and base == 16:
            self.assertNotEqual(result.find("0x"), -1)


class DigitsConfigTestCase(unittest.TestCase):
    """
    Test digits config.
    """

    @given(
        SIZE_STRATEGY,
        strategies.builds(
            DigitsConfig,
            separator=strategies.text(alphabet="-/*j:", max_size=1),
            use_caps=strategies.booleans(),
            use_letters=strategies.booleans(),
        ),
    )
    @settings(max_examples=500)
    def test_config(self, a_size, config):
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
                self.assertTrue(all(r in string.ascii_uppercase for r in letters))
            else:
                self.assertTrue(all(r in string.ascii_lowercase for r in letters))


class RoundingTestCase(unittest.TestCase):
    """Test rounding methods."""

    @given(
        SIZE_STRATEGY,
        strategies.one_of(
            SIZE_STRATEGY.filter(lambda x: x.magnitude >= 0),
            strategies.sampled_from(UNITS()),
        ),
        strategies.sampled_from(ROUNDING_METHODS()),
        strategies.tuples(
            strategies.one_of(strategies.none(), SIZE_STRATEGY),
            strategies.one_of(strategies.none(), SIZE_STRATEGY),
        ),
    )
    @settings(max_examples=500)
    def test_bounds(self, size, unit, rounding, bounds):
        """
        Test that result is between the specified bounds,
        assuming that the bounds are legal.
        """
        (lower, upper) = bounds
        assume(lower is None or upper is None or lower <= upper)
        rounded = size.roundTo(unit, rounding, bounds)
        self.assertTrue(lower is None or lower <= rounded)
        self.assertTrue(upper is None or upper >= rounded)

    @given(
        SIZE_STRATEGY,
        strategies.one_of(
            SIZE_STRATEGY.filter(lambda x: x.magnitude >= 0),
            strategies.sampled_from(UNITS()),
        ),
        strategies.sampled_from(ROUNDING_METHODS()),
    )
    @settings(max_examples=500)
    def test_results(self, size, unit, rounding):
        """Test roundTo results."""
        # pylint: disable=too-many-branches
        rounded = size.roundTo(unit, rounding)

        if (isinstance(unit, Range) and unit.magnitude == 0) or (
            not isinstance(unit, Range) and int(unit) == 0
        ):
            self.assertEqual(rounded, Range(0))
            return

        converted = size.convertTo(unit)
        if converted.denominator == 1:
            self.assertEqual(rounded, size)
            return

        factor = getattr(unit, "magnitude", None) or int(unit)
        (quotient, remainder) = divmod(converted.numerator, converted.denominator)
        ceiling = Range((quotient + 1) * factor)
        floor = Range(quotient * factor)
        if rounding is ROUND_UP:
            self.assertEqual(rounded, ceiling)
            return

        if rounding is ROUND_DOWN:
            self.assertEqual(rounded, floor)
            return

        if rounding is ROUND_TO_ZERO:
            if size > Range(0):
                self.assertEqual(rounded, floor)
            else:
                self.assertEqual(rounded, ceiling)
            return

        remainder = abs(Fraction(remainder, converted.denominator))
        half = Fraction(1, 2)
        if remainder > half:
            self.assertEqual(rounded, ceiling)
        elif remainder < half:
            self.assertEqual(rounded, floor)
        else:
            if rounding is ROUND_HALF_UP:
                self.assertEqual(rounded, ceiling)
            elif rounding is ROUND_HALF_DOWN:
                self.assertEqual(rounded, floor)
            else:
                if size > Range(0):
                    self.assertEqual(rounded, floor)
                else:
                    self.assertEqual(rounded, ceiling)
