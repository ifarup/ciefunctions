#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot: Generate matplotlib plots for the tc182 package.

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
import threading

lock = threading.Lock()

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
    lock.acquire()
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
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,1], 'r:')
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,2], 'g:')
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,3], 'b:')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength [nm]', fontsize=12)
        axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
    if options['full_title']:
        axes.set_title(('CIE XYZ fundamental CMFs\nField size: %s' % plots['field_size'] +
                        u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                        u' yr,  Domain: %s\u2013%s nm' % (plots['lambda_min'],
                                                                plots['lambda_max']) +
                        ',  Step: %s nm' % plots['lambda_step']), fontsize=12)
    else:
        axes.set_title('CIE XYZ fundamental CMFs', fontsize=12)
    lock.release()

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
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    lambdavalues = np.concatenate(([plots['xy'][0,0]], np.arange(470, 611, 10), [700], [plots['xy'][-1,0]]))
    if options['cie31']:
        axes.plot(plots['cc31'][:,1], plots['cc31'][:,2], 'k--')
        axes.plot(plots['purple_line_cc31'][:,1], plots['purple_line_cc31'][:,2], 'k--')
        for l in lambdavalues: # add wavelength parameters
            ind = np.nonzero(plots['cc31'][:,0] == l)[0]
            axes.plot(plots['cc31'][ind,1], plots['cc31'][ind,2], 'ko')
    if options['cie64']:
        axes.plot(plots['cc64'][:,1], plots['cc64'][:,2], 'k:')
        axes.plot(plots['purple_line_cc64'][:,1], plots['purple_line_cc64'][:,2], 'k:')
        for l in lambdavalues: # add wavelength parameters
            ind = np.nonzero(plots['cc64'][:,0] == l)[0]
            axes.plot(plots['cc64'][ind,1], plots['cc64'][ind,2], 'ks')
    axes.plot(plots['xy'][:,1], plots['xy'][:,2], 'k')
    axes.plot(plots['purple_line_cc'][:,1], plots['purple_line_cc'][:,2], 'k')
    for l in lambdavalues: # add wavelength parameters
        ind = np.nonzero(plots['xy'][:,0] == l)[0]
        axes.plot(plots['xy'][ind,1], plots['xy'][ind,2], 'wo')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            if np.shape(ind)[0] > 0:
                axes.text(plots['xy'][ind,1], plots['xy'][ind,2], '   ' + "%.0f" % l,
                               fontsize=options['label_fontsize'], verticalalignment=align)
    axes.plot(plots['cc_white'][0], plots['cc_white'][1], 'kx')
    if options['labels']:
        axes.text(plots['cc_white'][0], plots['cc_white'][1], '   E',
                       fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['lambda_min']) == 390 and
            float(plots['lambda_max']) == 830 and
            float(plots['lambda_step']) == 1):
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
                                 str(plots['age']) + '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                                                    plots['lambda_max'],
                                                                                    plots['lambda_step']),
                                 fontsize=16)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) + '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                                                    plots['lambda_max'],
                                                                                    plots['lambda_step']),
                                 fontsize=16)
    if options['full_title']:
        axes.set_title('CIE xy fundamental chromaticity diagram\nField size: ' + str(plots['field_size']) +
                            u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                            u' yr,  Domain: %s\u2013%s nm' % (plots['lambda_min'],
                                                              plots['lambda_max']) +
                            ',  Step: %s nm' % plots['lambda_step'], fontsize=12)
    else:
        axes.set_title('CIE xy fundamental chromaticity diagram', fontsize=12)        
    lock.release()

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
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['lms'][:,0], plots['lms'][:,1], 'r')
    axes.plot(plots['lms'][:,0], plots['lms'][:,2], 'g')
    axes.plot(plots['lms'][:,0], plots['lms'][:,3], 'b')
    axes.axis('normal')
    axes.axis([350, 850, -.05, 1.05])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength [nm]', fontsize=12)
        axes.set_ylabel('Relative energy sensitivities', fontsize=12)
    if options['full_title']:
        axes.set_title('CIE 2006 LMS cone fundamentals\nField size: ' + str(plots['field_size']) +
                            u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                            u' yr,  Domain: %s\u2013%s nm' % (plots['lambda_min'],
                                                              plots['lambda_max']) +
                            ',  Step: %s nm' % plots['lambda_step'], fontsize=12)
    else:
        axes.set_title('CIE 2006 LMS cone fundamentals', fontsize=12)
    lock.release()

def lms_base(axes, plots, options):
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
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['lms'][:,0], plots['lms'][:,1], 'r')
    axes.plot(plots['lms'][:,0], plots['lms'][:,2], 'g')
    axes.plot(plots['lms'][:,0], plots['lms'][:,3], 'b')
    axes.axis('normal')
    axes.axis([350, 850, -.05, 1.05])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength [nm]', fontsize=12)
        axes.set_ylabel('Relative energy sensitivities', fontsize=12)
    if options['full_title']:
        axes.set_title('CIE 2006 LMS cone fundamentals (9 sign. figs. data)\nField size: ' + str(plots['field_size']) +
                       u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                       u' yr,  Domain: %s\u2013%s nm' % (plots['lambda_min'],
                                                         plots['lambda_max']) +
                       ',  Step: %s nm' % plots['lambda_step'], fontsize=12)
    else:
        axes.set_title('CIE 2006 LMS cone fundamentals (9 sign. figs. data)', fontsize=12)
    lock.release()

def bm(axes, plots, options):
    """
    Plot the MacLeod-Boynton diagram onto the given axes
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['bm'][:,1], plots['bm'][:,3], 'k')
    axes.plot(plots['purple_line_bm'][:,1], plots['purple_line_bm'][:,2], 'k')
    lambdavalues = np.concatenate(([plots['bm'][0,0]], np.arange(410, 490, 10),
                                   [500, 550, 575, 600, 700], [plots['bm'][-1,0]]))
    for l in lambdavalues: # add wavelength parameters
        ind = np.nonzero(plots['bm'][:,0] == l)[0]
        axes.plot(plots['bm'][ind,1], plots['bm'][ind,3], 'wo')
        if l > 490:
            align = 'bottom'
        elif l == 830:
            align = 'top'
        else:
            align = 'center'
        if options['labels'] and np.shape(ind)[0] > 0:
            axes.text(plots['bm'][ind,1], plots['bm'][ind,3], '   ' + "%.0f" % l,
                           fontsize=options['label_fontsize'], verticalalignment=align)
    axes.plot(plots['bm_white'][0], plots['bm_white'][2], 'kx')
    if options['labels']:
        axes.text(plots['bm_white'][0], plots['bm_white'][2], '   E',
                       fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['lambda_min']) == 390 and
            float(plots['lambda_max']) == 830 and
            float(plots['lambda_step']) == 1):
            axes.set_xlabel('$l_\mathrm{\,MB,\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) +'}$',
                            fontsize=16)
            axes.set_ylabel('$s_\mathrm{\,MB,\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) + '}$',
                            fontsize=16)
        else:
            axes.set_xlabel('$l_\mathrm{\,MB,\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) + '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                                           plots['lambda_max'],
                                                                           plots['lambda_step']),
                            fontsize=16)
            axes.set_ylabel('$s_\mathrm{\,MB,\,' +
                                str(plots['field_size']) + ',\,' +
                                str(plots['age']) + '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                                          plots['lambda_max'],
                                                                          plots['lambda_step']),
                            fontsize=16)
    if options['full_title']:
        axes.set_title('MacLeod-Boynton ls chromaticity diagram\nField size: ' + str(plots['field_size']) +
                            u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                            u' yr,  Domain: %s\u2013%s nm' % (plots['lambda_min'],
                                                              plots['lambda_max']) +
                            ',  Step: %s nm' % plots['lambda_step'], fontsize=12)
    else:
        axes.set_title('MacLeod-Boynton ls chromaticity diagram', fontsize=12)
    lock.release()

def lm(axes, plots, options):
    """
    Plot the normalised lm diagram onto the given axes.
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['lm'][:,1], plots['lm'][:,2], 'k')
    axes.plot(plots['purple_line_lm'][:,1], plots['purple_line_lm'][:,2], 'k')
    lambdavalues = np.concatenate((np.arange(450, 631, 10), [700], [plots['lm'][0,0]], [plots['lm'][-1,0]]))
    for l in lambdavalues: # add wavelength parameters
        ind = np.nonzero(plots['lm'][:,0] == l)[0]
        axes.plot(plots['lm'][ind,1], plots['lm'][ind,2], 'wo')
        if l == 390:
            align = 'top'
        else:
            align = 'center'
        if options['labels'] and np.shape(ind)[0] > 0:
            axes.text(plots['lm'][ind,1], plots['lm'][ind,2], '   ' + "%.0f" % l,
                           fontsize=options['label_fontsize'], verticalalignment=align)
    axes.plot(plots['lm_white'][0], plots['lm_white'][1], 'kx')
    if options['labels']:
            axes.text(plots['lm_white'][0], plots['lm_white'][1], '   E',
                           fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, .65))
    if options['axis_labels']:
        if (float(plots['lambda_min']) == 390 and
            float(plots['lambda_max']) == 830 and
            float(plots['lambda_step']) == 1):
            axes.set_xlabel('$l_\mathrm{\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) +'}$',
                                 fontsize=16)
            axes.set_ylabel('$m_\mathrm{\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) + '}$',
                                 fontsize=16)
        else:
            axes.set_xlabel('$l_\mathrm{\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) + '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                                           plots['lambda_max'],
                                                                           plots['lambda_step']),
                                 fontsize=16)
            axes.set_ylabel('$m_\mathrm{\,' +
                                 str(plots['field_size']) + ',\,' +
                                 str(plots['age']) + '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                                           plots['lambda_max'],
                                                                           plots['lambda_step']),
                                 fontsize=16)
    if options['full_title']:
        axes.set_title('Maxwellian lm chromaticity diagram\nField size: ' + str(plots['field_size']) +
                            u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                            u' yr,  Domain: %s\u2013%s nm' % (plots['lambda_min'],
                                                              plots['lambda_max']) +
                            ',  Step: %s nm' % plots['lambda_step'], fontsize=12)
    else:
        axes.set_title('Maxwellian lm chromaticity diagram', fontsize=12)
    lock.release()

def xyz31(axes, plots, options):
    """
    Plot the xyz1931 standard CMFs onto the given axes.
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,1], 'r')
    axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,2], 'g')
    axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,3], 'b')
    if options['cie64']:
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,1], 'r:')
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,2], 'g:')
        axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,3], 'b:')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength [nm]', fontsize=12)
        axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
    axes.set_title(u'CIE 1931 XYZ standard 2\N{DEGREE SIGN} CMFs', fontsize=12)
    lock.release()

def xyz64(axes, plots, options):
    """
    Plot the xyz1964 standard CMFs onto the given axes.
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,1], 'r')
    axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,2], 'g')
    axes.plot(plots['xyz64'][:,0], plots['xyz64'][:,3], 'b')
    if options['cie31']:
        axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,1], 'r:')
        axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,2], 'g:')
        axes.plot(plots['xyz31'][:,0], plots['xyz31'][:,3], 'b:')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength [nm]', fontsize=12)
        axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
    axes.set_title(u'CIE 1964 XYZ standard 10\N{DEGREE SIGN}CMFs', fontsize=12)
    lock.release()

def xy31(axes, plots, options):
    """
    Plot the xy1931 chromaticity diagram onto the given axes.
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    lambdavalues = np.concatenate(([390], np.arange(470, 611, 10), [700, 830]))
    if options['cie64']:
        axes.plot(plots['cc64'][:,1], plots['cc64'][:,2], 'k:')
        axes.plot(plots['purple_line_cc64'][:,1], plots['purple_line_cc64'][:,2], 'k:')
        for l in lambdavalues: # add wavelength parameters
            ind = np.nonzero(plots['cc64'][:,0] == l)[0]
            axes.plot(plots['cc64'][ind,1], plots['cc64'][ind,2], 'ks')
    axes.plot(plots['cc31'][:,1], plots['cc31'][:,2], 'k')
    axes.plot(plots['purple_line_cc31'][:,1], plots['purple_line_cc31'][:,2], 'k')
    for l in lambdavalues: # add wavelength parameters
        ind = np.nonzero(plots['cc31'][:,0] == l)[0]
        axes.plot(plots['cc31'][ind,1], plots['cc31'][ind,2], 'ko')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            axes.text(plots['cc31'][ind,1], plots['cc31'][ind,2], '   ' + "%.0f" % l,
                           fontsize=options['label_fontsize'], verticalalignment=align)
    axes.plot(1./3, 1./3, 'kx')
    if options['labels']:
        axes.text(1./3, 1./3, '   E',
                       fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        axes.set_xlabel('$x$', fontsize=16)
        axes.set_ylabel('$y$', fontsize=16)
    axes.set_title(u'CIE 1931 xy standard 2\N{DEGREE SIGN} chromaticity diagram', fontsize=12)
    lock.release()

def xy64(axes, plots, options):
    """
    Plot the xy1964 chromaticity diagram onto the given axes.
    
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc182.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    lambdavalues = np.concatenate(([390], np.arange(470, 611, 10), [700, 830]))
    if options['cie31']:
        axes.plot(plots['cc31'][:,1], plots['cc31'][:,2], 'k--')
        axes.plot(plots['purple_line_cc31'][:,1], plots['purple_line_cc31'][:,2], 'k--')
        for l in lambdavalues: # add wavelength parameters
            ind = np.nonzero(plots['cc31'][:,0] == l)[0]
            axes.plot(plots['cc31'][ind,1], plots['cc31'][ind,2], 'ko')
    axes.plot(plots['cc64'][:,1], plots['cc64'][:,2], 'k')
    axes.plot(plots['purple_line_cc64'][:,1], plots['purple_line_cc64'][:,2], 'k')
    for l in lambdavalues: # add wavelength parameters
        ind = np.nonzero(plots['cc64'][:,0] == l)[0]
        axes.plot(plots['cc64'][ind,1], plots['cc64'][ind,2], 'ks')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            axes.text(plots['cc64'][ind,1], plots['cc64'][ind,2], '   ' + "%.0f" % l,
                           fontsize=options['label_fontsize'], verticalalignment=align)
    axes.plot(1./3, 1./3, 'kx')
    if options['labels']:
        axes.text(1./3, 1./3, '   E',
                       fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        axes.set_xlabel('$x_{10}$', fontsize=16)
        axes.set_ylabel('$y_{10}$', fontsize=16)
    axes.set_title(u'CIE 1964 xy standard 10\N{DEGREE SIGN} chromaticity diagram', fontsize=12)
    lock.release()
