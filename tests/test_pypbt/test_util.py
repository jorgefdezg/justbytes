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

""" Test for utility functions. """

# isort: STDLIB

# isort: THIRDPARTY
from pypbt import domains
from pypbt.quantifiers import forall,exists
# isort: LOCAL
from justbytes._util.generators import next_or_last, takeuntil
"""
Test next_or_last.
"""

# @given(strategies.lists(strategies.integers()), strategies.integers())
# @settings(max_examples=10)
@forall(value = domains.List(domains.Int()),n_samples = 3)
@forall(default = domains.Int(),n_samples = 3)
def test_results_true(value, default):
    """
    Test results when the predicate is always True.
    """
    # self.assertEqual(
    #     next_or_last(lambda x: True, value, default),
    #     value[0] if value != [] else default,
    # )
    return next_or_last(lambda x: True, value, default) == (value[0] if value != [] else default)

# @given(strategies.lists(strategies.integers()), strategies.integers())
# @settings(max_examples=10)
@forall(value = domains.List(domains.Int()),n_samples = 3)
@forall(default = domains.Int(),n_samples = 3)
def test_results_false(value, default):
    """
    Test results when the predicate is always False.
    """
    # self.assertEqual(
    #     next_or_last(lambda x: False, value, default),
    #     value[-1] if value != [] else default,
    # )
    return next_or_last(lambda x: False, value, default) == (value[-1] if value != [] else default)

"""
Test takeuntil.
"""

@forall(value = domains.List(domains.Int()),n_samples = 10)
def test_results_false(value):
    """
    Test results when none are sastifactory.
    """
    return list(takeuntil(lambda x: False, value)) == value

@forall(value = domains.List(domains.Int()),n_samples = 10)
def test_results_true(value):
    """
    Test results when all are satisfactory.
    """
    return list(takeuntil(lambda x: True, value)) == value[:1]
