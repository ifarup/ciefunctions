#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute: Calculate the CIE functions provided by CIE TC 1-97.

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

import tc1_97

def compute_tabulated(field_size, age, lambda_min=390, lambda_max=830, lambda_step=1):
    return tc1_97.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)