#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
purpletest: CIE TC1-82 Computations

Copyright (C) 2014 Ivar Farup and Jan Henrik Wold

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

import tc182
import numpy as np
import matplotlib.pyplot as plt

res, plots = tc182.compute_tabulated(2, 32)
plt.plot(plots['purple_xyz_N'][:,0], plots['purple_xyz_N'][:,3:0:-1], '.')
plt.show()
