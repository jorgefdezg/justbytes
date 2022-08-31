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
import unittest

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists
# isort: LOCAL
from justbytes import UNITS, Range


"""Test conversions."""
@forall(size = domains.Int(),n_samples = 500)
@exists(unit = domains.DomainFromIterable(UNITS(),True))
def test_int(size, unit):
    """Test integer conversions."""
    return int(Range(size, unit)) == (size * int(unit))


@forall(unit = domains.DomainFromIterable(UNITS(),True))
@forall(value = lambda unit: domains.DomainPyObject(Range,domains.Int(),unit),n_samples = 30)
def test_repr(unit,value):
    """Test that repr looks right."""
    return (f"{value !r}") == (f"Range({value.magnitude !r})")
