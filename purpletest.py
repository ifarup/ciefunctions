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

res, plots = tc182.compute_tabulated(10, 70)

lambda_b = plots['purple_line_cc'][0, 0]
lambda_r = plots['purple_line_cc'][1, 0]
x_b = plots['purple_line_cc'][0, 1]
y_b = plots['purple_line_cc'][0, 2]
x_r = plots['purple_line_cc'][1, 1]
y_r = plots['purple_line_cc'][1, 2]
ind_b = plots['xyz'][:, 0] == lambda_b
ind_r = plots['xyz'][:, 0] == lambda_r
X_b = plots['xyz'][ind_b, 1]
X_r = plots['xyz'][ind_r, 1]
Y_b = plots['xyz'][ind_b, 2]
Y_r = plots['xyz'][ind_r, 2]
Z_b = plots['xyz'][ind_b, 3]
Z_r = plots['xyz'][ind_r, 3]

print(lambda_b, X_b, Y_b, Z_b)
print(lambda_r, X_r, Y_r, Z_r)

lambdas = []
alphas = []
for i in range(len(plots['xyz'][:, 0])):
    l = plots['xyz'][i, 0]
    if l > lambda_b and l < lambda_r:
        x_l = plots['cc'][i, 1]
        y_l = plots['cc'][i, 2]
        alpha = (((y_r - 1./3) * (x_l - y_l) - (x_r - y_r) * (y_l - 1./3)) /
                 ((x_b - y_b - x_r + y_r) * (y_l - 1./3) -
                  (y_b - y_r) * (x_l - y_l)))
        if alpha >= 0 and alpha <= 1:
            lambdas.append(l)
            alphas.append(alpha)
lambdas = np.array(lambdas)
alphas = np.array(alphas)
Y = alphas * Y_b + (1 - alphas) * Y_r
x = alphas * x_b + (1 - alphas) * x_r
y = alphas * y_b + (1 - alphas) * y_r
X = x * Y / y
Z = (1 - x - y) * Y / y
plt.plot(lambdas, Z)
plt.plot(lambdas, Y)
plt.plot(lambdas, X)
plt.show()
