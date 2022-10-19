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

""" Test for constants classes. """
# isort: STDLIB
import unittest

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists
# isort: LOCAL
from justbytes._constants import BinaryUnits, DecimalUnits

"""Exercise methods of constants classes."""

@forall(bexp = domains.Int(min_value = 0, max_value = BinaryUnits.max_exponent()),
        dexp = domains.Int(min_value=0, max_value=DecimalUnits.max_exponent()),n_samples = 500)
def test_exp_method_binary(bexp,dexp):
    return (
        BinaryUnits.unit_for_exp(bexp).factor == BinaryUnits.FACTOR**bexp and
        DecimalUnits.unit_for_exp(dexp).factor == DecimalUnits.FACTOR**dexp
    )



