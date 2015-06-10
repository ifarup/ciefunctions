#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_lm_quantum_threshold_constant: CIE TC1-82 Computations

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

fs_range = np.arange(1, 11)
age_range = np.arange(20, 71, 5)
consts = []
for fs in fs_range:
    for age in age_range:
        abt = tc182.absorpt(fs)
        lmsq = tc182.lms_quantal(fs, age)
        const = abt[:, 1] * lmsq[:, 2] / (abt[:, 2] * lmsq[:, 1])
        consts.append(const[0])
consts = np.array(consts)
plt.plot(consts, '.')

age = 32
fs = 2
abt = tc182.absorpt(fs)
lmsq = tc182.lms_quantal(fs, age)
const = abt[:, 1] * lmsq[:, 2] / (abt[:, 2] * lmsq[:, 1])
print(const[0])

ocul = tc182.ocular(age)
tau = 10**(-tc182.d_mac_max(fs)*tc182.VisualData.macula[:, 1]/.35 - ocul[:, 1])
i_max_alpha_L = np.argmax(abt[:, 1])
i_max_alpha_M = np.argmax(abt[:, 2])

const2 = (lmsq[i_max_alpha_M, 2] * tau[i_max_alpha_L] /
          (lmsq[i_max_alpha_L, 1] * tau[i_max_alpha_M]))
print(const2)

plt.show()
