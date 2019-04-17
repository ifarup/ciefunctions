#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot: Generate matplotlib plots for the tc1_97 package.

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

import tc1_97.plot as tc


def xyz(axis, plots, options):
    return tc.XYZ(axis, plots, options)


def xy(axis, plots, options):
    return tc.xy(axis, plots, options)


def lms(axis, plots, options):
    return tc.LMS(axis, plots, options)


def lms_base(axis, plots, options):
    return tc.LMS_base(axis, plots, options)


def bm(axis, plots, options):
    return tc.ls_mb(axis, plots, options)


def lm(axis, plots, options):
    return tc.lm_mw(axis, plots, options)


def xyz31(axis, plots, options):
    return tc.XYZ31(axis, plots, options)


def xyz64(axis, plots, options):
    return tc.XYZ64(axis, plots, options)


def xy31(axis, plots, options):
    return tc.xy31(axis, plots, options)


def xy64(axis, plots, options):
    return tc.xy64(axis, plots, options)


def xyz_purples(axis, plots, options):
    return tc.XYZ_purples(axis, plots, options)


def xy_purples(axis, plots, options):
    return tc.xy_purples(axis, plots, options)
