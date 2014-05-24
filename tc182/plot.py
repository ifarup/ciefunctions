#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot: Generate plots for the tc182 package.

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

import numpy as np

def test(axes):
    axes.clear()
    x = np.linspace(0, 1)
    y = np.sin(2 * np.pi * x)
    axes.plot(x, y)

def xyz(axes, plots, options):
    """
    Plot the XYZ functions onto the given axes.
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['xyz'][:,0], plots['xyz'][:,1], 'r')
    axes.plot(plots['xyz'][:,0], plots['xyz'][:,2], 'g')
    axes.plot(plots['xyz'][:,0], plots['xyz'][:,3], 'b')
    if options['cie31']:
        axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,1], 'r--')
        axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,2], 'g--')
        axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,3], 'b--')
    if options['cie64']:
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,1], 'r-.')
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,2], 'g-.')
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,3], 'b-.')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    axes.set_xlabel('Wavelength [nm]', fontsize=12)
    axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
    axes.set_title(('CIE XYZ fundamental CMFs\nField size: %.1f' % plots['field_size'] +
                    u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                    u' yr,  Domain: %0.1f\u2013%0.1f nm' % (plots['lambda_min'],
                                                            plots['lambda_max']) +
                    ',  Step: %0.1f nm' % plots['lambda_step']), fontsize=12)
