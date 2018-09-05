#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils: Utility functions for CIE functions provided by CIE TC 1-97.

Copyright (C) 2012-2018 Ivar Farup and Jan Henrik Wold

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

import numpy as np


def ndarray_to_list(dictionary):
    """
    Convert all the ndarrays in the dictionary to lists.
    """
    for key in dictionary:
        if type(dictionary[key]) is np.ndarray:
            dictionary[key] = dictionary[key].tolist()


def list_to_ndarray(dictionary):
    """
    Convert all the lists in the dictionary to ndarrays.
    """
    for key in dictionary:
        if type(dictionary[key]) is list:
            dictionary[key] = np.array(dictionary[key])
