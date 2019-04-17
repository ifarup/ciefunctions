#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
table: Generate html tables for the tc1_97 package.

Copyright (C) 2019 Ivar Farup

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import tc1_97.table as tc


def xyz(results, options, include_head=False):
    return tc.XYZ(results, options, include_head)


def xy(results, options, include_head=False):
    return tc.xyz(results, options, include_head)


def lms(results, options, include_head=False):
    return tc.LMS(results, options, include_head)


def lms_base(results, options, include_head=False):
    return tc.LMS_base(results, options, include_head)


def bm(results, options, include_head=False):
    return tc.lms_mb(results, options, include_head)


def lm(results, options, include_head=False):
    return tc.lms_mw(results, options, include_head)


def xyz31(results, options, include_head=False):
    return tc.XYZ31(results, options, include_head)


def xyz64(results, options, include_head=False):
    return tc.XYZ64(results, options, include_head)


def xy31(results, options, include_head=False):
    return tc.xyz31(results, options, include_head)


def xy64(results, options, include_head=False):
    return tc.xyz64(results, options, include_head)


def xyz_purples(results, options, include_head=False):
    return tc.XYZ_purples(results, options, include_head)


def xy_purples(results, options, include_head=False):
    return tc.xyz_purples(results, options, include_head)
