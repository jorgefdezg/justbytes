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

""" Tests for operations on Range objects. """

# isort: STDLIB
import copy
import unittest
from decimal import Decimal
from fractions import Fraction

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists

# isort: LOCAL
from justbytes import Range,UNITS

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 5)
def test_addition(units,size_1,size_2):
    """Test addition."""
    return (size_1 + size_2) == Range(size_1.magnitude + size_2.magnitude)


@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
def test_divmod_with_range(units,size_1,size_2):
    """Test divmod with a size."""
    (div, rem) = divmod(size_1.magnitude, size_2.magnitude)
    return divmod(size_1, size_2) == (div, Range(rem))


@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = domains.DomainPyObject(Fraction,domains.Int(min_value=1),domains.Int(min_value=1,max_value=100)),n_samples = 5)
def test_divmod_with_number(units,size_1, size_2):
    """Test divmod with a number."""
    (div, rem) = divmod(size_1.magnitude, Fraction(size_2))
    return divmod(size_1, size_2) == (Range(div), Range(rem))


@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
def test_floordiv_with_range(units,size_1, size_2):
    """Test floordiv with a size."""
    return (size_1 // size_2) == (size_1.magnitude // size_2.magnitude)

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = domains.DomainPyObject(Fraction,domains.Int(min_value=1),domains.Int(min_value=1,max_value=100)),n_samples = 5)
def test_floordiv_with_number(units, size_1, size_2):
    """Test floordiv with a number."""
    return size_1 // size_2 == Range(size_1.magnitude // Fraction(size_2))

# """Test mod."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
def test_mod_with_range(units, size_1, size_2):
    """Test mod with a size."""
    return size_1 % size_2 == Range(size_1.magnitude % size_2.magnitude)

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = domains.DomainPyObject(Fraction,domains.Int(min_value=1),domains.Int(min_value=1,max_value=100)),n_samples = 5)
def test_mod_with_number(units, size_1, size_2):
    """Test mod with a number."""
    return size_1 % size_2 == Range(size_1.magnitude % Fraction(size_2))


# """Test multiplication."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(num = domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value=1,max_value=100)),n_samples = 5)
def test_multiplication(units, size, num):
    """Test multiplication."""
    return size * num == Range(Fraction(num) * size.magnitude)


# """Test rdivmod."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_rdivmod_with_range(units, size_1, size_2):
    """Test divmod with a size."""
    (div, rem) = divmod(size_2.magnitude, size_1.magnitude)
    return size_1.__rdivmod__(size_2) == (div, Range(rem))


# """Test rfloordiv."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_ffloordiv_with_range(units, size_1, size_2):
    """Test floordiv with a size."""
    return size_1.__rfloordiv__(size_2) == size_2.magnitude // size_1.magnitude


# """Test rmod."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_rmod_with_range(units, size_1, size_2):
    """Test rmod with a size."""
    return size_1.__rmod__(size_2) == Range(size_2.magnitude % size_1.magnitude)


# """Test rsub."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_rsub(units, size_1, size_2):
    """Test __rsub__."""
    return size_1.__rsub__(size_2) == Range(size_2.magnitude - size_1.magnitude)


# """Test rtruediv."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_rtruediv_with_range(units, size_1, size_2):
    """Test truediv with a size."""
    return size_1.__rtruediv__(size_2) == size_2.magnitude / size_1.magnitude


# """Test subtraction."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_subtraction(units, size_1, size_2):
    """Test subtraction."""
    return size_1 - size_2 == Range(size_1.magnitude - size_2.magnitude)


# """Test truediv."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.Int(min_value=1),units),n_samples = 5)
def test_truediv_with_range(units, size_1, size_2):
    """Test truediv with a size."""
    return size_1 / size_2 == size_1.magnitude / size_2.magnitude

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
@forall(size_2 = domains.DomainPyObject(Fraction,domains.Int(min_value=1),domains.Int(min_value=1,max_value=100)),n_samples = 5)
def test_truediv_with_number(units, size_1, size_2):
    """Test truediv with a number."""
    return size_1 / size_2, Range(size_1.magnitude / Fraction(size_2))


# """Test unary operators."""

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size_1 = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 5)
@forall(size_2 = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 5)
def test_hash(units, size_1, size_2):
    """Test that hash has the necessary property for hash table lookup."""
    size_3 = copy.deepcopy(size_1)
    if not hash(size_1) == hash(size_3):
        return False
    return size_1 != size_2 or hash(size_1) == hash(size_2)

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 25)
def test_abs(units, size):
    """Test absolute value."""
    return abs(size) == Range(abs(size.magnitude))

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 25)
def test_neg(units, size):
    """Test negation."""
    return -size == Range(-size.magnitude)

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(size = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 25)
def test_pos(units, size):
    """Test positive."""
    return +size == size


# # """
# # Verify that distributive property holds.
# # """


@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(s = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 3)
@forall(n = domains.Int(),n_samples = 3)
@forall(m = domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value=1,max_value=100)),n_samples = 3)
# pylint: disable=invalid-name
def test_distributivity1(units, s, n, m):
    """
    Assert distributivity across numbers.
    """
    return (n + m) * s == n * s + m * s

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(p = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 3)
@forall(q = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 3)
@forall(n = domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value=1,max_value=100)),n_samples = 3)
# pylint: disable=invalid-name
def test_distributivity2(units, p, q, n):
    """
    Assert distributivity across sizes.
    """
    return (p + q) * n == p * n + q * n

@forall(units = domains.DomainFromIterable(UNITS(),True))
@forall(p = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 3)
@forall(q = lambda units: domains.DomainPyObject(Range,domains.Int(),units),n_samples = 3)
@forall(r = lambda units: domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1,max_value = 100)),units),n_samples = 3)
# pylint: disable=invalid-name
def test_associativity(units, p, q, r):
    """
    Assert associativity across sizes.
    """
    return (p + q) + r == p + (r + q)