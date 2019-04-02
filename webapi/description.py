#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description: Generate html description strings for the tc1_97 package.

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

import tc1_97.description as tc

def xyz(data, heading, options, include_head=False):
    return tc.XYZ(data, heading, options, include_head)

def xy(data, heading, options, include_head=False):
    return tc.xyz(data, heading, options, include_head)

def lms(data, heading, options, include_head=False):
    return tc.LMS(data, heading, options, include_head)

def lms_base(data, heading, options, include_head=False):
    return tc.LMS_base(data, heading, options, include_head)

def bm(data, heading, options, include_head=False):
    return tc.lms_mb(data, heading, options, include_head)

def lm(data, heading, options, include_head=False):
    return tc.lms_mw(data, heading, options, include_head)

def xyz31(data, heading, options, include_head=False):
    return tc.XYZ31(data, heading, options, include_head)

def xyz64(data, heading, options, include_head=False):
    return tc.XYZ64(data, heading, options, include_head)

def xy31(data, heading, options, include_head=False):
    return tc.xyz31(data, heading, options, include_head)

def xy64(data, heading, options, include_head=False):
    return tc.xyz64(data, heading, options, include_head)

def xyz_purples(data, heading, options, include_head=False):
    return tc.XYZ_purples(data, heading, options, include_head)

def xy_purples(data, heading, options, include_head=False):
    return tc.xyz_purples(data, heading, options, include_head)
