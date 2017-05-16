#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot: Generate matplotlib plots for the tc1_97 package.

Copyright (C) 2012-2017 Ivar Farup and Jan Henrik Wold

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
import matplotlib
import threading
from matplotlib.ticker import MaxNLocator

lock = threading.Lock()


def lms(axes, plots, options):
    """
    Plot the lms functions onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(plots['lms'][:, 0], plots['lms'][:, 1], 'r')
    axes.plot(plots['lms'][:, 0], plots['lms'][:, 2], 'g')
    axes.plot(plots['lms'][:, 0], plots['lms'][:, 3], 'b')
    axes.axis('normal')
    axes.axis([350, 850, -.05, 1.05])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Relative energy sensitivities', fontsize=10.5)
    if options['full_title']:
        axes.set_title(
            ('CIE 2006 LMS cone fundamentals\nField size: %s' %
             plots['field_size'] +
             u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
             u' yr,  Domain: %s nm \u2013 %s nm' % (plots['lambda_min'],
                                               plots['lambda_max']) +
             ',  Step: %s nm' % plots['lambda_step']),
            fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE 2006 LMS cone fundamentals',
                       fontsize=options['title_fontsize'])
    lock.release()


def lms_base(axes, plots, options):
    """
    Plot the chromaticity diagram onto the given axes, 9 sign. figs.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(plots['lms'][:, 0], plots['lms'][:, 1], 'r')
    axes.plot(plots['lms'][:, 0], plots['lms'][:, 2], 'g')
    axes.plot(plots['lms'][:, 0], plots['lms'][:, 3], 'b')
    axes.axis('normal')
    axes.axis([350, 850, -.05, 1.05])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Relative energy sensitivities', fontsize=10.5)
    if options['full_title']:
       axes.set_title(('CIE 2006 LMS cone fundamentals ' +
                        '(9 sign. figs. data)\nField size: %s''' %
                       plots['field_size'] +
                        u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                        u' yr,  Domain: %s nm \u2013 %s nm' % (
                            plots['lambda_min'],
                            plots['lambda_max']) +
                        ',  Step: %s nm' % plots['lambda_step']),
                       fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE 2006 LMS cone fundamentals (9 sign. figs. data)',
                       fontsize=options['title_fontsize'])
    lock.release()


def mb(axes, plots, options):
    """
    Plot the MacLeod-Boynton diagram onto the given axes

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(plots['mb'][:, 1], plots['mb'][:, 3], 'k')
    axes.plot(plots['purple_line_mb'][:, 1],
              plots['purple_line_mb'][:, 2], 'k')
    lambdavalues = np.concatenate(
        ([plots['mb'][0, 0]], np.arange(410, 490, 10),
         [500, 550, 575, 600, 700], [plots['mb'][-1, 0]]))
    for l in lambdavalues:  # add wavelength parameters
        ind = np.nonzero(plots['mb'][:, 0] == l)[0]
        axes.plot(plots['mb'][ind, 1], plots['mb'][ind, 3], 'o', markeredgecolor='k', markerfacecolor='w')
        if l > 490:
            align = 'bottom'
        elif l == 830:
            align = 'top'
        else:
            align = 'center'
        if options['labels'] and np.shape(ind)[0] > 0:
            axes.text(plots['mb'][ind, 1], plots['mb'][ind, 3],
                      '   ' + '%.0f' %
                      l, fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(plots['mb_white'][0], plots['mb_white'][2], 'kx')
    if options['labels']:
        axes.text(plots['mb_white'][0], plots['mb_white'][2], '   E',
                  fontsize=options['label_fontsize'],
                  verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['lambda_min']) == 390 and
                float(plots['lambda_max']) == 830 and
                float(plots['lambda_step']) == 1):
            axes.set_xlabel('$l_\mathrm{\,MB,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
            axes.set_ylabel('$s_\mathrm{\,MB,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
        else:
            axes.set_xlabel('$l_\mathrm{\,MB,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '\,(%s-%s,\,%s)}$' %
                            (plots['lambda_min'],
                             plots['lambda_max'],
                             plots['lambda_step']),
                            fontsize=11)
            axes.set_ylabel('$s_\mathrm{\,MB,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '\,(%s-%s,\,%s)}$' %
                            (plots['lambda_min'],
                             plots['lambda_max'],
                             plots['lambda_step']),
                            fontsize=11)
    if options['full_title']:
        axes.set_title((u'MacLeod\u2013Boynton ls chromaticity ' +
                        u'diagram\nField size: %s''' % plots['field_size'] +
                        u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                        u' yr,  Domain: %s nm \u2013 %s nm' %
                        (plots['lambda_min'], plots['lambda_max']) +
                        ',  Step: %s nm' % plots['lambda_step']),
                       fontsize=options['title_fontsize'])
    else:
        axes.set_title(u'MacLeod\u2013Boynton ls chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()


def lm(axes, plots, options):
    """
    Plot the normalized lm diagram onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(plots['lm'][:, 1], plots['lm'][:, 2], 'k')
    axes.plot(plots['purple_line_lm'][:, 1],
              plots['purple_line_lm'][:, 2], 'k')
    lambdavalues = np.concatenate(
        (np.arange(450, 631, 10), [700], [plots['lm'][0, 0]],
         [plots['lm'][-1, 0]]))
    for l in lambdavalues:  # add wavelength parameters
        ind = np.nonzero(plots['lm'][:, 0] == l)[0]
        axes.plot(plots['lm'][ind, 1], plots['lm'][ind, 2], 'o', markeredgecolor='k', markerfacecolor='w')
        if l == 390:
            align = 'top'
        else:
            align = 'center'
        if options['labels'] and np.shape(ind)[0] > 0:
            axes.text(plots['lm'][ind, 1], plots['lm'][ind, 2],
                      '   ' + '%.0f' % l,
                      fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(plots['lm_white'][0], plots['lm_white'][1], 'kx')
    if options['labels']:
            axes.text(plots['lm_white'][0], plots['lm_white'][1], '   E',
                      fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.xaxis.set_major_locator( MaxNLocator(nbins = 6, min_n_ticks = 3) )
    axes.set_ylim((-.05, .65))
    axes.yaxis.set_major_locator( MaxNLocator(nbins = 4, min_n_ticks = 3) )
    if options['axis_labels']:
        if (float(plots['lambda_min']) == 390 and
                float(plots['lambda_max']) == 830 and
                float(plots['lambda_step']) == 1):
            axes.set_xlabel('$l_\mathrm{\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
            axes.set_ylabel('$m_\mathrm{\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
        else:
            axes.set_xlabel('$l_\mathrm{\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '\,(%s-%s,\,%s)}$' %
                            (plots['lambda_min'],
                             plots['lambda_max'],
                             plots['lambda_step']),
                            fontsize=11)
            axes.set_ylabel('$m_\mathrm{\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '\,(%s-%s,\,%s)}$' %
                            (plots['lambda_min'],
                             plots['lambda_max'],
                             plots['lambda_step']),
                            fontsize=11)
    if options['full_title']:
        axes.set_title(
            ('Maxwellian lm chromaticity diagram\nField size: %s' %
             plots['field_size'] +
             u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
             u' yr,  Domain: %s nm \u2013 %s nm' % (plots['lambda_min'],
                                               plots['lambda_max']) +
             ',  Step: %s nm' % plots['lambda_step'] + ',  Renormalized values'),
            fontsize=options['title_fontsize'])
    else:
        axes.set_title('Maxwellian lm chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()
    
    
def xyz(axes, plots, options):
    """
    Plot the XYZ functions onto the given axes.
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    if options['norm']:
        xyz = plots['xyz_N']
    else:
        xyz = plots['xyz']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(xyz[:, 0], xyz[:, 1], 'r')
    axes.plot(xyz[:, 0], xyz[:, 2], 'g')
    axes.plot(xyz[:, 0], xyz[:, 3], 'b')
    if options['cie31']:
        axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 1], 'r--')
        axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 2], 'g--')
        axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 3], 'b--')
    if options['cie64']:
        axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 1], 'r:')
        axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 2], 'g:')
        axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 3], 'b:')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Cone-fundamental-based tristimulus values',
                        fontsize=10.5)
    if options['full_title']:
        title = 'CIE XYZ cone-fundamental-based tristimulus functions\n' + \
                'Field size: %s''' % plots['field_size'] + \
                u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + \
                u' yr,  Domain: %s nm \u2013 %s nm' % \
                (plots['lambda_min'], plots['lambda_max']) + \
                ',  Step: %s nm' % plots['lambda_step']
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE XYZ cone-fundamental-based ' +
                       'tristimulus functions',
                       fontsize=options['title_fontsize'])
    lock.release()


def xyz_purples(axes, plots, options):
    """
    Plot the XYZ purple functions onto the given axes.
    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    if options['norm']:
        purple = plots['purple_xyz_N']
    else:
        purple = plots['purple_xyz']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(purple[:, 0], purple[:, 1], 'r')
    axes.plot(purple[:, 0], purple[:, 2], 'g')
    axes.plot(purple[:, 0], purple[:, 3], 'b')
    axes.axis('normal')
    axes.axis([480, 580, -.04, .54])
    if options['axis_labels']:
        axes.set_xlabel('Complementary wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Cone-fundamental-based tristimulus values',
                        fontsize=10.5)
    if options['full_title']:
        title = 'XYZ cone-fundamental-based tristimulus functions for ' + \
                'purple-line stimuli\n' + \
                'Field size: %s''' % plots['field_size'] + \
               u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + \
                u' yr,  Domain: %s nm \u2013 %s nm' % \
                (plots['lambda_min'], plots['lambda_max']) + \
                ',  Step: %s nm' % plots['lambda_step']    
        axes.set_title(title, fontsize=options['title_fontsize'])
        if options['norm']:
            title += ',  Renormalized values'
    else:
        axes.set_title('CIE XYZ cone-fundamental-based ' +
                       'tristimulus functions',
                       fontsize=options['title_fontsize'])
    lock.release()


def xy(axes, plots, options):
    """
    Plot the chromaticity diagram onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    if options['norm']:
        xy = plots['xy_N']
        xy_white = plots['xy_white_N']
        purple_line_cc = plots['purple_line_cc_N']
    else:
        xy = plots['xy']
        xy_white = plots['xy_white']
        purple_line_cc = plots['purple_line_cc']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    lambdavalues = np.concatenate(
        ([xy[0, 0]], np.arange(470, 611, 10), [700], [xy[-1, 0]]))
    if options['cie31']:
        axes.plot(plots['xy31'][:, 1], plots['xy31'][:, 2], 'k--')
        axes.plot(plots['purple_line_cc31'][:, 1],
                  plots['purple_line_cc31'][:, 2], 'k--')
        for l in lambdavalues:  # add wavelength parameters
            ind = np.nonzero(plots['xy31'][:, 0] == l)[0]
            axes.plot(plots['xy31'][ind, 1], plots['xy31'][ind, 2], 'ko')
    if options['cie64']:
        axes.plot(plots['xy64'][:, 1], plots['xy64'][:, 2], 'k:')
        axes.plot(plots['purple_line_cc64'][:, 1],
                  plots['purple_line_cc64'][:, 2], 'k:')
        for l in lambdavalues:  # add wavelength parameters
            ind = np.nonzero(plots['xy64'][:, 0] == l)[0]
            axes.plot(plots['xy64'][ind, 1], plots['xy64'][ind, 2], 'ks')
    axes.plot(xy[:, 1], xy[:, 2], 'k')
    axes.plot(purple_line_cc[:, 1], purple_line_cc[:, 2], 'k')
    for l in lambdavalues:  # add wavelength parameters
        ind = np.nonzero(xy[:, 0] == l)[0]
        axes.plot(xy[ind, 1], xy[ind, 2], 'o', markeredgecolor='k', markerfacecolor='w')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            if np.shape(ind)[0] > 0:
                axes.text(xy[ind, 1], xy[ind, 2], '   ' + '%.0f' %
                          l, fontsize=options['label_fontsize'],
                          verticalalignment=align)
    axes.plot(xy_white[0], xy_white[1], 'kx')
    if options['labels']:
        axes.text(xy_white[0], xy_white[1], '   E',
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
                            str(plots['age']) + '}$',
                            fontsize=11)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
        else:
            axes.set_xlabel('$x_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) +
                            '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                  plots['lambda_max'],
                                                  plots['lambda_step']),
                            fontsize=11)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) +
                            '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                  plots['lambda_max'],
                                                  plots['lambda_step']),
                            fontsize=11)
    if options['full_title']:
        title = 'CIE xy cone-fundamental-based chromaticity diagram\n' +\
                'Field size: %s' % plots['field_size'] + \
                u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + \
                u' yr,  Domain: %s nm \u2013 %s nm' % (plots['lambda_min'],
                                                  plots['lambda_max']) + \
                ',  Step: %s nm' % plots['lambda_step']
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])

    else:
        axes.set_title('CIE xy cone-fundamental-based chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()
    
    
def xy_purples(axes, plots, options):
    """
    Plot the chromaticity diagram (purples) onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    if options['norm']:
        xy = plots['purple_cc_N']
        xy_white = plots['xy_white_N']
        locus = plots['xy_N']
        purpleline = plots['purple_line_cc_N']
    else:
        xy = plots['purple_cc']
        xy_white = plots['xy_white']
        locus = plots['xy']
        purpleline = plots['purple_line_cc']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(xy[:, 1], xy[:, 2], 'k')
    lambdavalues = np.arange(400, 700, 10)
    axes.plot(locus[:, 1], locus[:, 2], 'k')
    axes.plot(purpleline[:, 1], purpleline[:, 2], 'k')
    axes.plot(xy_white[0], xy_white[1], 'kx')
    axes.plot(purpleline[0, 1], purpleline[0, 2], 'o', markeredgecolor='k', markerfacecolor='w')
    axes.plot(purpleline[1, 1], purpleline[1, 2], 'o', markeredgecolor='k', markerfacecolor='w')
    if options['labels']:
        axes.text(purpleline[0, 1], purpleline[0, 2], '   ' + '%.1f' %
                  purpleline[0, 0], fontsize=options['label_fontsize'],
                  verticalalignment='center')
        axes.text(purpleline[1, 1], purpleline[1, 2], '   ' + '%.1f' %
                  purpleline[1, 0], fontsize=options['label_fontsize'],
                  verticalalignment='center')
    for l in lambdavalues:  # add wavelength parameters
        ind = np.nonzero(xy[:, 0] == l)[0]
        axes.plot(xy[ind, 1], xy[ind, 2], 'o', markeredgecolor='k', markerfacecolor='w')
        if options['labels']:
            if np.shape(ind)[0] > 0:
                axes.text(xy[ind, 1], xy[ind, 2], '   ' + '%.0fc' %
                          l, fontsize=options['label_fontsize'],
                          verticalalignment='center')
    if options['labels']:
        axes.text(xy_white[0], xy_white[1], '   E',
                  fontsize=options['label_fontsize'], verticalalignment='center')
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['lambda_min']) == 390 and
                float(plots['lambda_max']) == 830 and
                float(plots['lambda_step']) == 1):
            axes.set_xlabel('$x_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '}$',
                            fontsize=11)
        else:
            axes.set_xlabel('$x_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) +
                            '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                  plots['lambda_max'],
                                                  plots['lambda_step']),
                            fontsize=11)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) +
                            '\,(%s-%s,\,%s)}$' % (plots['lambda_min'],
                                                  plots['lambda_max'],
                                                  plots['lambda_step']),
                            fontsize=11)
    if options['full_title']:
        title = 'xy cone-fundamental-based chromaticity diagram (purple-line stimuli)\n' + \
                'Field size: %s' % plots['field_size'] + \
                u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + \
                u' yr,  Domain: %s nm \u2013 %s nm' % (plots['lambda_min'], \
                                                  plots['lambda_max']) + \
                ',  Step: %s nm' % plots['lambda_step']
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE xy cone-fundamental-based chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()


def xyz_31(axes, plots, options):
    """
    Plot the xyz1931 standard CMFs onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 1], 'r')
    axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 2], 'g')
    axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 3], 'b')
    if options['cie64']:
        axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 1], 'r:')
        axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 2], 'g:')
        axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 3], 'b:')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Tristimulus values', fontsize=10.5)
    axes.set_title(
        u'CIE 1931 XYZ standard 2\N{DEGREE SIGN} colour-matching functions',
        fontsize=options['title_fontsize'])
    lock.release()


def xyz_64(axes, plots, options):
    """
    Plot the xyz1964 standard CMFs onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 1], 'r')
    axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 2], 'g')
    axes.plot(plots['xyz64'][:, 0], plots['xyz64'][:, 3], 'b')
    if options['cie31']:
        axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 1], 'r--')
        axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 2], 'g--')
        axes.plot(plots['xyz31'][:, 0], plots['xyz31'][:, 3], 'b--')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Tristimulus values', fontsize=10.5)
    axes.set_title(
        u'CIE 1964 XYZ standard 10\N{DEGREE SIGN} colour-matching functions',
        fontsize=options['title_fontsize'])
    lock.release()


def xy_31(axes, plots, options):
    """
    Plot the xy1931 chromaticity diagram onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    lambdavalues = np.concatenate(([390], np.arange(470, 611, 10), [700, 830]))
    if options['cie64']:
        axes.plot(plots['xy64'][:, 1], plots['xy64'][:, 2], 'k:')
        axes.plot(plots['purple_line_cc64'][:, 1],
                  plots['purple_line_cc64'][:, 2], 'k:')
        for l in lambdavalues:  # add wavelength parameters
            ind = np.nonzero(plots['xy64'][:, 0] == l)[0]
            axes.plot(plots['xy64'][ind, 1], plots['xy64'][ind, 2], 'ks')
    axes.plot(plots['xy31'][:, 1], plots['xy31'][:, 2], 'k')
    axes.plot(plots['purple_line_cc31'][:, 1],
              plots['purple_line_cc31'][:, 2], 'k')
    for l in lambdavalues:      # add wavelength parameters
        ind = np.nonzero(plots['xy31'][:, 0] == l)[0]
        axes.plot(plots['xy31'][ind, 1], plots['xy31'][ind, 2], 'ko')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            axes.text(plots['xy31'][ind, 1],
                      plots['xy31'][ind, 2], '   ' + '%.0f' %
                      l, fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(1./3, 1./3, 'kx')
    if options['labels']:
        axes.text(1./3, 1./3, '   E',
                  fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        axes.set_xlabel('$x$', fontsize=11)
        axes.set_ylabel('$y$', fontsize=11)
    axes.set_title(
        u'CIE 1931 xy standard 2\N{DEGREE SIGN} chromaticity diagram',
        fontsize=options['title_fontsize'])
    lock.release()


def xy_64(axes, plots, options):
    """
    Plot the xy1964 chromaticity diagram onto the given axes.

    Parameters
    ----------
    axes : Axes
        Matplotlib axes on which to plot.
    plots : dict
        Data for plotting as returned by tc1_97.
    options : dict
        Plotting options (see code for use).
    """
    lock.acquire()
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    lambdavalues = np.concatenate(([390], np.arange(470, 611, 10), [700, 830]))
    if options['cie31']:
        axes.plot(plots['xy31'][:, 1], plots['xy31'][:, 2], 'k--')
        axes.plot(plots['purple_line_cc31'][:, 1],
                  plots['purple_line_cc31'][:, 2], 'k--')
        for l in lambdavalues:  # add wavelength parameters
            ind = np.nonzero(plots['xy31'][:, 0] == l)[0]
            axes.plot(plots['xy31'][ind, 1], plots['xy31'][ind, 2], 'ko')
    axes.plot(plots['xy64'][:, 1], plots['xy64'][:, 2], 'k')
    axes.plot(plots['purple_line_cc64'][:, 1],
              plots['purple_line_cc64'][:, 2], 'k')
    for l in lambdavalues:      # add wavelength parameters
        ind = np.nonzero(plots['xy64'][:, 0] == l)[0]
        axes.plot(plots['xy64'][ind, 1], plots['xy64'][ind, 2], 'ks')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            axes.text(plots['xy64'][ind, 1],
                      plots['xy64'][ind, 2], '   ' + '%.0f' %
                      l, fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(1./3, 1./3, 'kx')
    if options['labels']:
        axes.text(1./3, 1./3, '   E',
                  fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        axes.set_xlabel('$x_{10}$', fontsize=11)
        axes.set_ylabel('$y_{10}$', fontsize=11)
    axes.set_title(
        u'CIE 1964 xy standard 10\N{DEGREE SIGN} chromaticity diagram',
        fontsize=options['title_fontsize'])
    lock.release()
