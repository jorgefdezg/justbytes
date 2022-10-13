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
from utils import SIZE_DOMAIN, NUMBERS_DOMAIN

@forall(size_1 = SIZE_DOMAIN,
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_addition(size_1,size_2):
    """Test addition."""
    return (size_1 + size_2) == Range(size_1.magnitude + size_2.magnitude)


@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != Range(0), SIZE_DOMAIN),n_samples = 500)
def test_divmod_with_range(size_1,size_2):
    """Test divmod with a size."""
    (div, rem) = divmod(size_1.magnitude, size_2.magnitude)
    return divmod(size_1, size_2) == (div, Range(rem))


@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != 0,NUMBERS_DOMAIN),n_samples = 500)
def test_divmod_with_number(size_1, size_2):
    """Test divmod with a number."""
    (div, rem) = divmod(size_1.magnitude, Fraction(size_2))
    return divmod(size_1, size_2) == (Range(div), Range(rem))


@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != Range(0), SIZE_DOMAIN),n_samples = 500)
def test_floordiv_with_range(size_1, size_2):
    """Test floordiv with a size."""
    return (size_1 // size_2) == (size_1.magnitude // size_2.magnitude)


@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != 0,NUMBERS_DOMAIN),n_samples = 500)
def test_floordiv_with_number(size_1, size_2):
    """Test floordiv with a number."""
    return size_1 // size_2 == Range(size_1.magnitude // Fraction(size_2))

# """Test mod."""

@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != Range(0), SIZE_DOMAIN),n_samples = 500)
def test_mod_with_range(size_1, size_2):
    """Test mod with a size."""
    return size_1 % size_2 == Range(size_1.magnitude % size_2.magnitude)


@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != 0,NUMBERS_DOMAIN),n_samples = 500)
def test_mod_with_number(size_1, size_2):
    """Test mod with a number."""
    return size_1 % size_2 == Range(size_1.magnitude % Fraction(size_2))


# """Test multiplication."""

@forall(size = SIZE_DOMAIN,
        num = NUMBERS_DOMAIN,n_samples = 500)
def test_multiplication(size, num):
    """Test multiplication."""
    return size * num == Range(Fraction(num) * size.magnitude)


# """Test rdivmod."""

@forall(size_1 = filter(lambda x: x != Range(0), SIZE_DOMAIN),
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_rdivmod_with_range(size_1, size_2):
    """Test divmod with a size."""
    (div, rem) = divmod(size_2.magnitude, size_1.magnitude)
    return size_1.__rdivmod__(size_2) == (div, Range(rem))


# """Test rfloordiv."""

@forall(size_1 = filter(lambda x: x != Range(0), SIZE_DOMAIN),
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_ffloordiv_with_range(size_1, size_2):
    """Test floordiv with a size."""
    return size_1.__rfloordiv__(size_2) == size_2.magnitude // size_1.magnitude


# """Test rmod."""

@forall(size_1 = filter(lambda x: x != Range(0), SIZE_DOMAIN),
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_rmod_with_range(size_1, size_2):
    """Test rmod with a size."""
    return size_1.__rmod__(size_2) == Range(size_2.magnitude % size_1.magnitude)


# """Test rsub."""

@forall(size_1 = SIZE_DOMAIN,
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_rsub(size_1, size_2):
    """Test __rsub__."""
    return size_1.__rsub__(size_2) == Range(size_2.magnitude - size_1.magnitude)


# """Test rtruediv."""

@forall(size_1 = filter(lambda x: x != Range(0), SIZE_DOMAIN),
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_rtruediv_with_range(size_1, size_2):
    """Test truediv with a size."""
    return size_1.__rtruediv__(size_2) == size_2.magnitude / size_1.magnitude


# """Test subtraction."""

@forall(size_1 = SIZE_DOMAIN,
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_subtraction(size_1, size_2):
    """Test subtraction."""
    return size_1 - size_2 == Range(size_1.magnitude - size_2.magnitude)


# """Test truediv."""

@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != Range(0), SIZE_DOMAIN),n_samples = 500)
def test_truediv_with_range(size_1, size_2):
    """Test truediv with a size."""
    return size_1 / size_2 == size_1.magnitude / size_2.magnitude

@forall(size_1 = SIZE_DOMAIN,
        size_2 = filter(lambda x: x != 0,NUMBERS_DOMAIN),n_samples = 500)
def test_truediv_with_number(size_1, size_2):
    """Test truediv with a number."""
    return size_1 / size_2, Range(size_1.magnitude / Fraction(size_2))


# """Test unary operators."""

@forall(size_1 = SIZE_DOMAIN,
        size_2 = SIZE_DOMAIN,n_samples = 500)
def test_hash(size_1, size_2):
    """Test that hash has the necessary property for hash table lookup."""
    size_3 = copy.deepcopy(size_1)
    if not hash(size_1) == hash(size_3):
        return False
    return size_1 != size_2 or hash(size_1) == hash(size_2)


@forall(size = SIZE_DOMAIN,n_samples = 500)
def test_abs(size):
    """Test absolute value."""
    return abs(size) == Range(abs(size.magnitude))

@forall(size = SIZE_DOMAIN,n_samples = 500)
def test_neg(size):
    """Test negation."""
    return -size == Range(-size.magnitude)

@forall(size = SIZE_DOMAIN,n_samples = 500)
def test_pos(size):
    """Test positive."""
    return +size == size


# """
# Verify that distributive property holds.
# """

@forall(s= SIZE_DOMAIN,
        n = NUMBERS_DOMAIN,
        m = NUMBERS_DOMAIN,n_samples = 500)
# pylint: disable=invalid-name
def test_distributivity1(s, n, m):
    """
    Assert distributivity across numbers.
    """
    return (n + m) * s == n * s + m * s

@forall(p = SIZE_DOMAIN,
        q = SIZE_DOMAIN,
        n = NUMBERS_DOMAIN,n_samples = 500)
# pylint: disable=invalid-name
def test_distributivity2(p, q, n):
    """
    Assert distributivity across sizes.
    """
    return (p + q) * n == p * n + q * n

@forall(p = SIZE_DOMAIN,
        q = SIZE_DOMAIN,
        r = SIZE_DOMAIN,n_samples = 500)
def test_associativity(p, q, r):
    """
    Assert associativity across sizes.
    """
    return (p + q) + r == p + (r + q)