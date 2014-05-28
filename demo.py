#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo: Quick demo of the tc182 package

Copyright (C) 2014 Ivar Farup

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

import tc182 # the base package, includes the computational part
import tc182.plot # if you want to do the plots as well
import tc182.html # if you want to generate the html descriptions

import matplotlib.pyplot as plt

# Setup for plotting:

fig = plt.figure()
ax = fig.add_subplot(111)

# Leave the real work to the package

results, plots = tc182.compute_tabulated(2, 20, 390, 830, 1)
options = { 'grid' : True,
            'cie31' : False,
            'cie64' : False,
            'labels' : True }
tc182.plot.bm(ax, plots, options)
html_string = tc182.html.xy(results,'Heading')

# Show the result

print(html_string)
plt.show()
