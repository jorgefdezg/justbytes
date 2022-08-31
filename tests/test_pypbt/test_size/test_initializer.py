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

""" Tests for Range initialization. """

# isort: STDLIB
import unittest
from fractions import Fraction

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists
import random
import decimal
# isort: LOCAL
from justbytes import UNITS, Range

"""Test conversions."""
@forall(integers = domains.Int(),n_samples = 5)
@forall(fractions1 = domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1)),n_samples = 4)
@forall(fractions2 = domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1)),n_samples = 5)
@forall(range = domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(),domains.Int(min_value = 1))),n_samples = 5)
@exists(method= domains.DomainFromIterable(UNITS(),True))
def test_initialization(integers,fractions1,fractions2,range,method):
    """Test the initializer."""
    list_choices1 = [integers,fractions1]
    list_choices2 = [range,fractions2,method]
    choice1 = random.choice(list_choices1)
    choice2 = random.choice(list_choices2)
    factor = getattr(choice2, "factor", getattr(choice2, "magnitude", None))
    if factor is None:
        factor = Fraction(choice2)
    return Range(choice1, choice2).magnitude == Fraction(choice1) * factor
