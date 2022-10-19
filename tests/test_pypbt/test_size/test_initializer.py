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
from fractions import Fraction



# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists
# isort: LOCAL
from justbytes import UNITS, Range

"""Test conversions."""
@forall(size = domains.Int(min_value = -10_000) | domains.DomainPyObject(Fraction,domains.Int(min_value = -10_000),domains.Int(min_value = 1)),
    unit = UNITS() | 
        domains.DomainPyObject(Fraction,domains.Int(min_value = -10_000),domains.Int(min_value = 1)) | 
        domains.DomainPyObject(Range,domains.DomainPyObject(Fraction,domains.Int(min_value = -10_000),domains.Int(min_value = 1))),n_samples = 500)
def test_initialization(size,unit):
    """Test the initializer."""
    factor = getattr(unit, "factor", getattr(unit, "magnitude", None))
    if factor is None:
        factor = Fraction(unit)
    return Range(size, unit).magnitude == Fraction(size) * factor