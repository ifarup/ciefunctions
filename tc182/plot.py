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

def xy(axes, plots, options):
    """
    Plot the chromaticity diagram onto the given axes.
    
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
    lambdavalues = np.concatenate(([plots['cc'][0,0]], np.arange(470, 611, 10), [700], [plots['cc'][-1,0]]))
    if options['cie31']:
        axes.plot(plots['cc31'][:,1], plots['cc31'][:,2], 'k--')
        axes.plot(plots['purple_line_cc31'][:,1], plots['purple_line_cc31'][:,2], 'k--')
        for l in lambdavalues: # add wavelength parameters
            ind = np.nonzero(plots['cc31'][:,0] == l)[0]
            axes.plot(plots['cc31'][ind,1], plots['cc31'][ind,2], 'ko')
    if options['cie64']:
        axes.plot(plots['cc64'][:,1], plots['cc64'][:,2], 'k-.')
        axes.plot(plots['purple_line_cc64'][:,1], plots['purple_line_cc64'][:,2], 'k-.')
        for l in lambdavalues: # add wavelength parameters
            ind = np.nonzero(plots['cc64'][:,0] == l)[0]
            axes.plot(plots['cc64'][ind,1], plots['cc64'][ind,2], 'k^')
    axes.plot(plots['cc'][:,1], plots['cc'][:,2], 'k')
    axes.plot(plots['purple_line_cc'][:,1], plots['purple_line_cc'][:,2], 'k')
    for l in lambdavalues: # add wavelength parameters
        ind = np.nonzero(plots['cc'][:,0] == l)[0]
        axes.plot(plots['cc'][ind,1], plots['cc'][ind,2], 'wo')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            if np.shape(ind)[0] > 0:
                axes.text(plots['cc'][ind,1], plots['cc'][ind,2], '   ' + str(l),
                               fontsize=7, verticalalignment=align)
    axes.plot(plots['cc_white'][0], plots['cc_white'][1], 'kx')
    if options['labels']:
        axes.text(plots['cc_white'][0], plots['cc_white'][1], '   E',
                       fontsize=7, verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if (plots['lambda_min'] == 390 and
        plots['lambda_max'] == 830 and
        plots['lambda_step'] == 1):
        axes.set_xlabel('$x_\mathrm{\,F,\,' +
                             str(plots['field_size']) + ',\,' +
                             str(plots['age']) +'}$',
                             fontsize=16)
        axes.set_ylabel('$y_\mathrm{\,F,\,' +
                             str(plots['field_size']) + ',\,' +
                             str(plots['age']) + '}$',
                             fontsize=16)
    else:
        axes.set_xlabel('$x_\mathrm{\,F,\,' +
                             str(plots['field_size']) + ',\,' +
                             str(plots['age']) + '\,(%0.1f-%0.1f,\,%0.1f)}$' % (plots['lambda_min'],
                                                                                plots['lambda_max'],
                                                                                plots['lambda_step']),
                             fontsize=16)
        axes.set_ylabel('$y_\mathrm{\,F,\,' +
                             str(plots['field_size']) + ',\,' +
                             str(plots['age']) + '\,(%0.1f-%0.1f,\,%0.1f)}$' % (plots['lambda_min'],
                                                                                plots['lambda_max'],
                                                                                plots['lambda_step']),
                             fontsize=16)
    axes.set_title('CIE xy fundamental chromaticity diagram\nField size: ' + str(plots['field_size']) +
                        u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                        u' yr,  Domain: %0.1f\u2013%0.1f nm' % (plots['lambda_min'],
                                                                plots['lambda_max']) +
                        ',  Step: %0.1f nm' % plots['lambda_step'], fontsize=12)

def lms(axes, plots, options):
    """
    Plot the lms functions onto the given axes.
    
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
    axes.plot(plots['lms'][:,0], plots['lms'][:,1], 'r')
    axes.plot(plots['lms'][:,0], plots['lms'][:,2], 'g')
    axes.plot(plots['lms'][:,0], plots['lms'][:,3], 'b')
    axes.axis('normal')
    axes.axis([350, 850, -.05, 1.05])
    axes.set_xlabel('Wavelength [nm]', fontsize=12)
    axes.set_ylabel('Relative energy sensitivities', fontsize=12)
    axes.set_title('CIE 2006 LMS cone fundamentals\nField size: ' + str(plots['field_size']) +
                        u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                        u' yr,  Domain: %0.1f\u2013%0.1f nm' % (plots['lambda_min'],
                                                                plots['lambda_max']) +
                        ',  Step: %0.1f nm' % plots['lambda_step'], fontsize=12)

def lms_9(axes, plots, options):
    """
    Plot the chromaticity diagram onto the given axes, 9 sign. figs.
    
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
    axes.plot(plots['lms'][:,0], plots['lms'][:,1], 'r')
    axes.plot(plots['lms'][:,0], plots['lms'][:,2], 'g')
    axes.plot(plots['lms'][:,0], plots['lms'][:,3], 'b')
    axes.axis('normal')
    axes.axis([350, 850, -.05, 1.05])
    axes.set_xlabel('Wavelength [nm]', fontsize=12)
    axes.set_ylabel('Relative energy sensitivities', fontsize=12)
    axes.set_title('CIE 2006 LMS cone fundamentals (9 sign. figs. data)\nField size: ' + str(plots['field_size']) +
                   u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                   u' yr,  Domain: %0.1f\u2013%0.1f nm' % (plots['lambda_min'],
                                                           plots['lambda_max']) +
                   ',  Step: %0.1f nm' % plots['lambda_step'], fontsize=12)
