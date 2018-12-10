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

def LMS(axes, plots, options):
    """
    Plot the CIE 2006 LMS cone fundamentals (6 sign.figs.) onto the given axes.

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
    if options['log10']: 
        axes.plot(plots['logLMS'][:, 0], plots['logLMS'][:, 1], 'r')
        axes.plot(plots['logLMS'][:, 0], plots['logLMS'][:, 2], 'g')
        axes.plot(plots['logLMS'][:, 0], plots['logLMS'][:, 3], 'b')
        axes.axis('normal')
        axes.set_xlim((350, 850))
        axes.set_ylim((-7.4, 0.4))
        axes.yaxis.set_major_locator(MaxNLocator(nbins = 7, min_n_ticks = 6))
    else:
        axes.plot(plots['LMS'][:, 0], plots['LMS'][:, 1], 'r')
        axes.plot(plots['LMS'][:, 0], plots['LMS'][:, 2], 'g')
        axes.plot(plots['LMS'][:, 0], plots['LMS'][:, 3], 'b')
        axes.axis('normal')
        axes.axis([350, 850, -.05, 1.05]) 
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        if options['log10']:
            axes.set_ylabel('$\mathrm{Log}\,_{10}\,\mathrm{(relativ\,\,energy\,\,sensitivity)}$',
                            fontsize=10.5)   
        else:    
            axes.set_ylabel('Relative energy sensitivities', fontsize=10.5)
        
    if options['full_title']:
        title = ('CIE 2006 LMS cone fundamentals\n' + 
                'Field size: %s''' % plots['field_size'] + 
                u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + 
                u' yr,  Domain: %s nm \u2013 %s nm' % 
                (plots['λ_min'], plots['λ_max']) + 
                ',  Step: %s nm' % plots['λ_step'])
        if options['log10']:
            title += ',  Logarithmic values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE 2006 LMS cone fundamentals',
                       fontsize=options['title_fontsize'])   
    lock.release()


def LMS_base(axes, plots, options):
    """
    Plot the CIE 2006 LMS cone fundamentals (9 sign. figs) onto the given axes.

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
    if options['log10']:
        axes.plot(plots['logLMS_base'][:, 0], plots['logLMS_base'][:, 1], 'r')
        axes.plot(plots['logLMS_base'][:, 0], plots['logLMS_base'][:, 2], 'g')
        axes.plot(plots['logLMS_base'][:, 0], plots['logLMS_base'][:, 3], 'b')
        axes.axis('normal')
        axes.set_xlim((350, 850))
        axes.set_ylim((-7.4, 0.4))
        axes.yaxis.set_major_locator(MaxNLocator(nbins = 7, min_n_ticks = 6))
    else:
        axes.plot(plots['LMS_base'][:, 0], plots['LMS_base'][:, 1], 'r')
        axes.plot(plots['LMS_base'][:, 0], plots['LMS_base'][:, 2], 'g')
        axes.plot(plots['LMS_base'][:, 0], plots['LMS_base'][:, 3], 'b')
        axes.axis('normal')
        axes.axis([350, 850, -.05, 1.05])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        if options['log10']:
            axes.set_ylabel('$\mathrm{Log}\,_{10}\,\mathrm{(relativ\,\,energy\,\,sensitivity)}$',
                            fontsize=10.5)   
        else:    
            axes.set_ylabel('Relative energy sensitivities', fontsize=10.5)
        
    if options['full_title']:
        title = ('CIE 2006 LMS cone fundamentals ' +
                 '(9 sign. figs. data)\nField size: %s''' %
                 plots['field_size'] + u'\N{DEGREE SIGN},  Age: ' +
                 str(plots['age']) + 
                 u' yr,  Domain: %s nm \u2013 %s nm' %
                 ( plots['λ_min'], plots['λ_max']) +
                 ',  Step: %s nm' % plots['λ_step'])
        if options['log10']:
            title += ',  Logarithmic values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE 2006 LMS cone fundamentals (9 sign. figs. data)',
                       fontsize=options['title_fontsize'])
    lock.release()


def lms_mb(axes, plots, options):
    """
    Plot the MacLeod-Boynton ls diagram onto the given axes

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
    axes.plot(plots['lms_mb'][:, 1], plots['lms_mb'][:, 3], 'k')
    axes.plot(plots['lms_mb_tg_purple'][:, 1],
              plots['lms_mb_tg_purple'][:, 2], 'k')
    λ_values = np.concatenate(
        ([plots['lms_mb'][0, 0]], np.arange(410, 490, 10),
         [500, 550, 575, 600, 700], [plots['lms_mb'][-1, 0]]))
    for λ in λ_values:  # add wavelength parameters
        ind = np.nonzero(plots['lms_mb'][:, 0] == λ)[0]
        axes.plot(plots['lms_mb'][ind, 1], plots['lms_mb'][ind, 3],
                  'o', markeredgecolor='k', markerfacecolor='w')
        if λ > 490:
            align = 'bottom'
        elif λ == 830:
            align = 'top'
        else:
            align = 'center'
        if options['labels'] and np.shape(ind)[0] > 0:
            axes.text(plots['lms_mb'][ind, 1], plots['lms_mb'][ind, 3],
                      '   ' + '%.0f' %
                      λ, fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(plots['lms_mb_white'][0], plots['lms_mb_white'][2], 'kx')
    if options['labels']:
        axes.text(plots['lms_mb_white'][0], plots['lms_mb_white'][2], '   E',
                  fontsize=options['label_fontsize'],
                  verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['λ_min']) == 390 and
                float(plots['λ_max']) == 830 and
                float(plots['λ_step']) == 1):
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
                            (plots['λ_min'],
                             plots['λ_max'],
                             plots['λ_step']),
                            fontsize=11)
            axes.set_ylabel('$s_\mathrm{\,MB,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '\,(%s-%s,\,%s)}$' %
                            (plots['λ_min'],
                             plots['λ_max'],
                             plots['λ_step']),
                            fontsize=11)
    if options['full_title']:
        axes.set_title((u'MacLeod\u2013Boynton ls chromaticity ' +
                        u'diagram\nField size: %s''' % plots['field_size'] +
                        u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
                        u' yr,  Domain: %s nm \u2013 %s nm' %
                        (plots['λ_min'], plots['λ_max']) +
                        ',  Step: %s nm' % plots['λ_step']),
                       fontsize=options['title_fontsize'])
    else:
        axes.set_title(u'MacLeod\u2013Boynton ls chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()


def lm_mw(axes, plots, options):
    """
    Plot the Maxwellian lm diagram onto the given axes.

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
    axes.plot(plots['lms_mw'][:, 1], plots['lms_mw'][:, 2], 'k')
    axes.plot(plots['lms_mw_tg_purple'][:, 1],
              plots['lms_mw_tg_purple'][:, 2], 'k')
    λ_values = np.concatenate(
        (np.arange(450, 631, 10), [700], [plots['lms_mw'][0, 0]],
         [plots['lms_mw'][-1, 0]]))
    for λ in λ_values:  # add wavelength parameters
        ind = np.nonzero(plots['lms_mw'][:, 0] == λ)[0]
        axes.plot(plots['lms_mw'][ind, 1], plots['lms_mw'][ind, 2],
                  'o', markeredgecolor='k', markerfacecolor='w')
        if λ == 390:
            align = 'top'
        else:
            align = 'center'
        if options['labels'] and np.shape(ind)[0] > 0:
            axes.text(plots['lms_mw'][ind, 1], plots['lms_mw'][ind, 2],
                      '   ' + '%.0f' % λ,
                      fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(plots['lms_mw_white'][0], plots['lms_mw_white'][1], 'kx')
    if options['labels']:
            axes.text(plots['lms_mw_white'][0], plots['lms_mw_white'][1],
                      '   E', fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.xaxis.set_major_locator( MaxNLocator(nbins = 6, min_n_ticks = 3) )
    axes.set_ylim((-.05, .65))
    axes.yaxis.set_major_locator( MaxNLocator(nbins = 4, min_n_ticks = 3) )
    if options['axis_labels']:
        if (float(plots['λ_min']) == 390 and
                float(plots['λ_max']) == 830 and
                float(plots['λ_step']) == 1):
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
                            (plots['λ_min'],
                             plots['λ_max'],
                             plots['λ_step']),
                            fontsize=11)
            axes.set_ylabel('$m_\mathrm{\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) + '\,(%s-%s,\,%s)}$' %
                            (plots['λ_min'],
                             plots['λ_max'],
                             plots['λ_step']),
                            fontsize=11)
    if options['full_title']:
        axes.set_title(
            ('Maxwellian lm chromaticity diagram\nField size: %s' %
             plots['field_size'] +
             u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) +
             u' yr,  Domain: %s nm \u2013 %s nm' % (plots['λ_min'],
                                               plots['λ_max']) +
             ',  Step: %s nm' % plots['λ_step'] + ',  Renormalized values'),
            fontsize=options['title_fontsize'])
    else:
        axes.set_title('Maxwellian lm chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()
    
    
def XYZ(axes, plots, options):
    """
    Plot the CIE XYZ cone-fundamental-based tristimulus functions onto the 
    given axes.
    
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
        XYZ = plots['XYZ_N']
    else:
        XYZ = plots['XYZ']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(XYZ[:, 0], XYZ[:, 1], 'r')
    axes.plot(XYZ[:, 0], XYZ[:, 2], 'g')
    axes.plot(XYZ[:, 0], XYZ[:, 3], 'b')
    if options['cie31']:
        axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 1], 'r--')
        axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 2], 'g--')
        axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 3], 'b--')
    if options['cie64']:
        axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 1], 'r:')
        axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 2], 'g:')
        axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 3], 'b:')
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
                (plots['λ_min'], plots['λ_max']) + \
                ',  Step: %s nm' % plots['λ_step']
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE XYZ cone-fundamental-based ' +
                       'tristimulus functions',
                       fontsize=options['title_fontsize'])
    lock.release()


def xy(axes, plots, options):
    """
    Plot the CIE xy cone-fundamental-based chromaticity diagram onto the given
    axes.

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
        xyz_white = plots['xyz_white_N']
        xyz_tg_purple = plots['xyz_tg_purple_N']
    else:
        xyz = plots['xyz']
        xyz_white = plots['xyz_white']
        xyz_tg_purple = plots['xyz_tg_purple']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    λ_values = np.concatenate(
        ([xyz[0, 0]], np.arange(470, 611, 10), [700], [xyz[-1, 0]]))
    if options['cie31']:
        axes.plot(plots['xyz31'][:, 1], plots['xyz31'][:, 2], 'k--')
        axes.plot(plots['xyz31_tg_purple'][:, 1],
                  plots['xyz31_tg_purple'][:, 2], 'k--')
        for l in λ_values:  # add wavelength parameters
            ind = np.nonzero(plots['xyz31'][:, 0] == l)[0]
            axes.plot(plots['xyz31'][ind, 1], plots['xyz31'][ind, 2], 'ko')
    if options['cie64']:
        axes.plot(plots['xyz64'][:, 1], plots['xyz64'][:, 2], 'k:')
        axes.plot(plots['xyz64_tg_purple'][:, 1],
                  plots['xyz64_tg_purple'][:, 2], 'k:')
        for l in λ_values:  # add wavelength parameters
            ind = np.nonzero(plots['xyz64'][:, 0] == l)[0]
            axes.plot(plots['xyz64'][ind, 1], plots['xyz64'][ind, 2], 'ks')
    axes.plot(xyz[:, 1], xyz[:, 2], 'k')
    axes.plot(xyz_tg_purple[:, 1], xyz_tg_purple[:, 2], 'k')
    for l in λ_values:  # add wavelength parameters
        ind = np.nonzero(xyz[:, 0] == l)[0]
        axes.plot(xyz[ind, 1], xyz[ind, 2],
                  'o', markeredgecolor='k', markerfacecolor='w')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            if np.shape(ind)[0] > 0:
                axes.text(xyz[ind, 1], xyz[ind, 2], '   ' + '%.0f' %
                          l, fontsize=options['label_fontsize'],
                          verticalalignment=align)
    axes.plot(xyz_white[0], xyz_white[1], 'kx')
    if options['labels']:
        axes.text(xyz_white[0], xyz_white[1], '   E',
                  fontsize=options['label_fontsize'], verticalalignment=align)
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['λ_min']) == 390 and
                float(plots['λ_max']) == 830 and
                float(plots['λ_step']) == 1):
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
                            '\,(%s-%s,\,%s)}$' % (plots['λ_min'],
                                                  plots['λ_max'],
                                                  plots['λ_step']),
                            fontsize=11)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) +
                            '\,(%s-%s,\,%s)}$' % (plots['λ_min'],
                                                  plots['λ_max'],
                                                  plots['λ_step']),
                            fontsize=11)
    if options['full_title']:
        title = 'CIE xy cone-fundamental-based chromaticity diagram\n' +\
                'Field size: %s' % plots['field_size'] + \
                u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + \
                u' yr,  Domain: %s nm \u2013 %s nm' % (plots['λ_min'],
                                                  plots['λ_max']) + \
                ',  Step: %s nm' % plots['λ_step']
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE xy cone-fundamental-based chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()
    
    
def XYZ_purples(axes, plots, options):
    """
    Plot the XYZ cone-fundamental-based  tristimulus functions for purple-
    line stimuli, as parameterized by complementary wavelength, onto the 
    given axes.
    
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
        XYZ_p = plots['XYZ_purples_N']
    else:
        XYZ_p = plots['XYZ_purples']  
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(XYZ_p[:, 0], XYZ_p[:, 1], 'r')
    axes.plot(XYZ_p[:, 0], XYZ_p[:, 2], 'g')
    axes.plot(XYZ_p[:, 0], XYZ_p[:, 3], 'b')
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
                (plots['λ_min'], plots['λ_max']) + \
                ',  Step: %s nm' % plots['λ_step'] 
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])    
    else:
        axes.set_title('CIE XYZ cone-fundamental-based ' +
                       'tristimulus functions',
                       fontsize=options['title_fontsize'])
    lock.release()    
    
    
def xy_purples(axes, plots, options):
    """
    Plot the CIE xy chromaticity diagram, with marking of purple-line stimuli, 
    onto the given axes.

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
        xyz_purples = plots['xyz_purples_N']
        xyz_white = plots['xyz_white_N']
        xyz_tg_purple = plots['xyz_tg_purple_N']
    else:
        xyz = plots['xyz']
        xyz_purples = plots['xyz_purples']        
        xyz_white = plots['xyz_white']
        xyz_tg_purple = plots['xyz_tg_purple']
    axes.clear()
    axes.grid(options['grid'])
    axes.tick_params(labelsize=10)
    axes.plot(xyz_purples[:, 1], xyz_purples[:, 2], 'k')
    λ_values = np.arange(400, 700, 10)
    axes.plot(xyz[:, 1], xyz[:, 2], 'k')
    axes.plot(xyz_tg_purple[:, 1], xyz_tg_purple[:, 2], 'k')
    axes.plot(xyz_white[0], xyz_white[1], 'kx')
    axes.plot(xyz_tg_purple[0, 1], xyz_tg_purple[0, 2],
              'o', markeredgecolor='k', markerfacecolor='w')
    axes.plot(xyz_tg_purple[1, 1], xyz_tg_purple[1, 2],
              'o', markeredgecolor='k', markerfacecolor='w')
    if options['labels']:
        axes.text(xyz_tg_purple[0, 1], xyz_tg_purple[0, 2], '   ' + '%.1f' %
                  xyz_tg_purple[0, 0], fontsize=options['label_fontsize'],
                  verticalalignment='center')
        axes.text(xyz_tg_purple[1, 1], xyz_tg_purple[1, 2], '   ' + '%.1f' %
                  xyz_tg_purple[1, 0], fontsize=options['label_fontsize'],
                  verticalalignment='center')
    for l in λ_values:  # add complementary-wavelength parameters
        ind = np.nonzero(xyz_purples[:, 0] == l)[0]
        axes.plot(xyz_purples[ind, 1], xyz_purples[ind, 2],
                  'o', markeredgecolor='k', markerfacecolor='w')
        if options['labels']:
            if np.shape(ind)[0] > 0:
                axes.text(xyz_purples[ind, 1], xyz_purples[ind, 2],
                          '   ' + '%.0fc' %
                          l, fontsize=options['label_fontsize'],
                          verticalalignment='center')
    if options['labels']:
        axes.text(xyz_white[0], xyz_white[1], '   E',
                  fontsize=options['label_fontsize'],
                  verticalalignment='center')
    axes.axis('scaled')
    axes.set_xlim((-.05, 1.05))
    axes.set_ylim((-.05, 1.05))
    if options['axis_labels']:
        if (float(plots['λ_min']) == 390 and
                float(plots['λ_max']) == 830 and
                float(plots['λ_step']) == 1):
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
                            '\,(%s-%s,\,%s)}$' % (plots['λ_min'],
                                                  plots['λ_max'],
                                                  plots['λ_step']),
                            fontsize=11)
            axes.set_ylabel('$y_\mathrm{\,F,\,' +
                            str(plots['field_size']) + ',\,' +
                            str(plots['age']) +
                            '\,(%s-%s,\,%s)}$' % (plots['λ_min'],
                                                  plots['λ_max'],
                                                  plots['λ_step']),
                            fontsize=11)
    if options['full_title']:
        title = 'xy cone-fundamental-based chromaticity diagram (purple-line stimuli)\n' + \
                'Field size: %s' % plots['field_size'] + \
                u'\N{DEGREE SIGN},  Age: ' + str(plots['age']) + \
                u' yr,  Domain: %s nm \u2013 %s nm' % (plots['λ_min'], \
                                                  plots['λ_max']) + \
                ',  Step: %s nm' % plots['λ_step']
        if options['norm']:
            title += ',  Renormalized values'
        axes.set_title(title, fontsize=options['title_fontsize'])
    else:
        axes.set_title('CIE xy cone-fundamental-based chromaticity diagram',
                       fontsize=options['title_fontsize'])
    lock.release()


def XYZ31(axes, plots, options):
    """
    Plot the CIE 1931 XYZ CMFs onto the given axes.

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
    axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 1], 'r')
    axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 2], 'g')
    axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 3], 'b')
    if options['cie64']:
        axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 1], 'r:')
        axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 2], 'g:')
        axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 3], 'b:')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Tristimulus values', fontsize=10.5)
    axes.set_title(
        u'CIE 1931 XYZ standard 2\N{DEGREE SIGN} colour-matching functions',
        fontsize=options['title_fontsize'])
    lock.release()


def XYZ64(axes, plots, options):
    """
    Plot the CIE 1964 XYZ CMFs onto the given axes.

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
    axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 1], 'r')
    axes.plot(plots['XYZ64'][:, 0], plots['XYZ64'][:, 2], 'g')
    axes.plot(plots['xyz64'][:, 0], plots['XYZ64'][:, 3], 'b')
    if options['cie31']:
        axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 1], 'r--')
        axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 2], 'g--')
        axes.plot(plots['XYZ31'][:, 0], plots['XYZ31'][:, 3], 'b--')
    axes.axis('normal')
    axes.axis([350, 850, -.2, 2.3])
    if options['axis_labels']:
        axes.set_xlabel('Wavelength (nm)', fontsize=10.5)
        axes.set_ylabel('Tristimulus values', fontsize=10.5)
    axes.set_title(
        u'CIE 1964 XYZ standard 10\N{DEGREE SIGN} colour-matching functions',
        fontsize=options['title_fontsize'])
    lock.release()


def xy31(axes, plots, options):
    """
    Plot the CIE 1931 xy chromaticity diagram onto the given axes.

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
    λ_values = np.concatenate(([390], np.arange(470, 611, 10), [700, 830]))
    if options['cie64']:
        axes.plot(plots['xyz64'][:, 1], plots['xyz64'][:, 2], 'k:')
        axes.plot(plots['xyz64_tg_purple'][:, 1],
                  plots['xyz64_tg_purple'][:, 2], 'k:')
        for l in λ_values:  # add wavelength parameters
            ind = np.nonzero(plots['xyz64'][:, 0] == l)[0]
            axes.plot(plots['xyz64'][ind, 1], plots['xyz64'][ind, 2], 'ks')
    axes.plot(plots['xyz31'][:, 1], plots['xyz31'][:, 2], 'k')
    axes.plot(plots['xyz31_tg_purple'][:, 1],
              plots['xyz31_tg_purple'][:, 2], 'k')
    for l in λ_values:      # add wavelength parameters
        ind = np.nonzero(plots['xyz31'][:, 0] == l)[0]
        axes.plot(plots['xyz31'][ind, 1], plots['xyz31'][ind, 2], 'ko')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            axes.text(plots['xyz31'][ind, 1],
                      plots['xyz31'][ind, 2], '   ' + '%.0f' %
                      l, fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(0.33331,0.33329, 'kx')
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


def xy64(axes, plots, options):
    """
    Plot the CIE 1964 xy chromaticity diagram onto the given axes.

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
    λ_values = np.concatenate(([390], np.arange(470, 611, 10), [700, 830]))
    if options['cie31']:
        axes.plot(plots['xyz31'][:, 1], plots['xyz31'][:, 2], 'k--')
        axes.plot(plots['xyz31_tg_purple'][:, 1],
                  plots['xyz31_tg_purple'][:, 2], 'k--')
        for l in λ_values:  # add wavelength parameters
            ind = np.nonzero(plots['xyz31'][:, 0] == l)[0]
            axes.plot(plots['xyz31'][ind, 1], plots['xyz31'][ind, 2], 'ko')
    axes.plot(plots['xyz64'][:, 1], plots['xyz64'][:, 2], 'k')
    axes.plot(plots['xyz64_tg_purple'][:, 1],
              plots['xyz64_tg_purple'][:, 2], 'k')
    for l in λ_values:      # add wavelength parameters
        ind = np.nonzero(plots['xyz64'][:, 0] == l)[0]
        axes.plot(plots['xyz64'][ind, 1], plots['xyz64'][ind, 2], 'ks')
        if l == 700 or l == 390:
            align = 'top'
        elif l == 830:
            align = 'bottom'
        else:
            align = 'center'
        if options['labels']:
            axes.text(plots['xyz64'][ind, 1],
                      plots['xyz64'][ind, 2], '   ' + '%.0f' %
                      l, fontsize=options['label_fontsize'],
                      verticalalignment=align)
    axes.plot(0.33330, 0.33333, 'kx')
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
