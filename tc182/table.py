#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
table: Generate html tables for the tc182 package.

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

import numpy as np
import sys


def _head():
    html_string = """
    <head>
    <link type="text/css" rel="stylesheet" href="table.css" />
    <script type="text/javascript"
    src="web/static/web/MathJax-2.4-latest/MathJax.js?config=TeX-AMS_HTML">
    </script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            displayAlign: "left",
            showProcessingMessages: false,
            messageStyle: "none",
            inlineMath:[["\\(","\\)"]],
            displayMath:[["$$","$$"]],
            "HTML-CSS": {
    """
    if sys.platform.startswith('win'):
        html_string += """
                scale: 190
        """
    elif sys.platform.startswith('linux'):
        html_string += """
                scale: 95
        """
    else:
        html_string += """
                scale: 100
        """
    html_string += """
            }
        });
    </script>
    </head>
    """
    return html_string


def xyz(results, options, include_head=False):
    """
    Generate html table of XYZ values for inclusion in GUI app and web app.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the XYZ table
    """
    if options['norm']:
        xyz = results['xyz_N']
    else:
        xyz = results['xyz']
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(\\bar x_{\,\mathrm{F},\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(\\bar y_{\,\mathrm{F},\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(\\bar z_{\,\mathrm{F},\,%s,\,%d}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(xyz)[0]):
        if (float(results['lambda_step']) ==
                np.round(float(results['lambda_step'])) and
                float(results['lambda_min']) ==
                np.round(float(results['lambda_min']))):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.6e</td>
               <td>%.6e</td>
               <td>%.6e</td>
            </tr>
            """ % (xyz[i, 0],
                   xyz[i, 1],
                   xyz[i, 2],
                   xyz[i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.6e</td>
               <td>%.6e</td>
               <td>%.6e</td>
            </tr>
            """ % (xyz[i, 0],
                   xyz[i, 1],
                   xyz[i, 2],
                   xyz[i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def xy(results, options, include_head=False):
    """
    Generate html table of chromaticity values for GUI and web apps.
o
    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the chromatictiy table
    """
    if options['norm']:
        xy = results['xy_N']
    else:
        xy = results['xy']
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(x_{\,\mathrm{F},\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(y_{\,\mathrm{F},\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(z_{\,\mathrm{F},\,%s,\,%d}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(xy)[0]):
        if (float(results['lambda_step']) ==
                np.round(float(results['lambda_step'])) and
                float(results['lambda_min']) ==
                np.round(float(results['lambda_min']))):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.5f</td>
               <td>%.5f</td>
               <td>%.5f</td>
            </tr>
            """ % (xy[i, 0],
                   xy[i, 1],
                   xy[i, 2],
                   xy[i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.5f</td>
               <td>%.5f</td>
               <td>%.5f</td>
            </tr>
            """ % (xy[i, 0],
                   xy[i, 1],
                   xy[i, 2],
                   xy[i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def lms(results, options, include_head=False):
    """
    Generate html table of LMS functions for inclusion in GUI app and web app.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the LMS table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(\\bar l_{%s,\,%d}(\lambda) \\)</th>
        <th>\\(\\bar m_{\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(\\bar s_{\,%s,\,%d}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['lms'])[0]):
        if (float(results['lambda_step']) ==
                np.round(float(results['lambda_step'])) and
                float(results['lambda_min']) ==
                np.round(float(results['lambda_min']))):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.5e</td>
               <td>%.5e</td>
               <td>%.5e</td>
            </tr>
            """ % (results['lms'][i, 0],
                   results['lms'][i, 1],
                   results['lms'][i, 2],
                   results['lms'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.5e</td>
               <td>%.5e</td>
               <td>%.5e</td>
            </tr>
            """ % (results['lms'][i, 0],
                   results['lms'][i, 1],
                   results['lms'][i, 2],
                   results['lms'][i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def lms_base(results, options, include_head=False):
    """
    Generate html table of LMS base functions for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the LMS base table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(\\bar l_{%s,\,%d}(\lambda) \\)</th>
        <th>\\(\\bar m_{\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(\\bar s_{\,%s,\,%d}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['lms_base'])[0]):
        if (float(results['lambda_step']) ==
                np.round(float(results['lambda_step'])) and
                float(results['lambda_min']) ==
                np.round(float(results['lambda_min']))):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.8e</td>
               <td>%.8e</td>
               <td>%.8e</td>
            </tr>
            """ % (results['lms_base'][i, 0],
                   results['lms_base'][i, 1],
                   results['lms_base'][i, 2],
                   results['lms_base'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.8e</td>
               <td>%.8e</td>
               <td>%.8e</td>
            </tr>
            """ % (results['lms_base'][i, 0],
                   results['lms_base'][i, 1],
                   results['lms_base'][i, 2],
                   results['lms_base'][i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def bm(results, options, include_head=False):
    """
    Generate html table of MacLeod-Boynton diagram for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the MacLeod-Boynton table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(l_{\,\mathrm{MB},\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(m_{\,\mathrm{MB},\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(s_{\,\mathrm{MB},\,%s,\,%d}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    results['bm'][results['bm'] <= 0] = 0
    for i in range(np.shape(results['bm'])[0]):
        if (float(results['lambda_step']) ==
                np.round(float(results['lambda_step'])) and
                float(results['lambda_min']) ==
                np.round(float(results['lambda_min']))):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.6f</td>
               <td>%.6f</td>
               <td>%.6f</td>
            </tr>
            """ % (results['bm'][i, 0],
                   results['bm'][i, 1],
                   results['bm'][i, 2],
                   results['bm'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.6f</td>
               <td>%.6f</td>
               <td>%.6f</td>
            </tr>
            """ % (results['bm'][i, 0],
                   results['bm'][i, 1],
                   results['bm'][i, 2],
                   results['bm'][i, 3])

    html_table += """
      </tbody>
    </table>
    """
    return html_table


def lm(results, options, include_head=False):
    """
    Generate html table of normalised lm diagram for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the tablulated normalised lm diagram
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(l_{\,\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(m_{\,\,%s,\,%d}(\lambda) \\)</th>
        <th>\\(s_{\,\,%s,\,%d}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['lm'])[0]):
        if (float(results['lambda_step']) ==
                np.round(float(results['lambda_step'])) and
                float(results['lambda_min']) ==
                np.round(float(results['lambda_min']))):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.6f</td>
               <td>%.6f</td>
               <td>%.6f</td>
            </tr>
            """ % (results['lm'][i, 0],
                   results['lm'][i, 1],
                   results['lm'][i, 2],
                   results['lm'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.5f</td>
               <td>%.5f</td>
               <td>%.5f</td>
            </tr>
            """ % (results['lm'][i, 0],
                   results['lm'][i, 1],
                   results['lm'][i, 2],
                   results['lm'][i, 3])

    html_table += """
      </tbody>
    </table>
    """
    return html_table


def xyz31(results, options, include_head=False):
    """
    Generate html table of CIE 1931 XYZ values for GUI app and web app.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the XYZ table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(\\bar x(\lambda) \\)</th>
        <th>\\(\\bar y(\lambda) \\)</th>
        <th>\\(\\bar z(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """
    for i in range(np.shape(results['xyz31'])[0]):
        html_table += """
        <tr>
           <td>%.0f</td>
           <td>%.6e</td>
           <td>%.6e</td>
           <td>%.6e</td>
        </tr>
        """ % (results['xyz31'][i, 0],
               results['xyz31'][i, 1],
               results['xyz31'][i, 2],
               results['xyz31'][i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def xyz64(results, options, include_head=False):
    """
    Generate html table of CIE 1964 XYZ values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the XYZ table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(\\bar x_{10}(\lambda) \\)</th>
        <th>\\(\\bar y_{10}(\lambda) \\)</th>
        <th>\\(\\bar z_{10}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """
    for i in range(np.shape(results['xyz64'])[0]):
        html_table += """
        <tr>
           <td>%.0f</td>
           <td>%.6e</td>
           <td>%.6e</td>
           <td>%.6e</td>
        </tr>
        """ % (results['xyz64'][i, 0],
               results['xyz64'][i, 1],
               results['xyz64'][i, 2],
               results['xyz64'][i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def xy31(results, options, include_head=False):
    """
    Generate html table of CIE 1931 chromaticity values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the chromatictiy table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(x(\lambda) \\)</th>
        <th>\\(y(\lambda) \\)</th>
        <th>\\(z(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """
    for i in range(np.shape(results['xy31'])[0]):
        html_table += """
        <tr>
           <td>%.0f</td>
           <td>%.5f</td>
           <td>%.5f</td>
           <td>%.5f</td>
        </tr>
        """ % (results['xy31'][i, 0],
               results['xy31'][i, 1],
               results['xy31'][i, 2],
               results['xy31'][i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def xy64(results, options, include_head=False):
    """
    Generate html table of CIE 1964 chromaticity values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the chromatictiy table
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\\)</th>
        <th>\\(x_{10}(\lambda) \\)</th>
        <th>\\(y_{10}(\lambda) \\)</th>
        <th>\\(z_{10}(\lambda) \\)</th>
      </tr>
      </thead>
      <tbody>
    """
    for i in range(np.shape(results['xy64'])[0]):
        html_table += """
        <tr>
           <td>%.0f</td>
           <td>%.5f</td>
           <td>%.5f</td>
           <td>%.5f</td>
        </tr>
        """ % (results['xy64'][i, 0],
               results['xy64'][i, 1],
               results['xy64'][i, 2],
               results['xy64'][i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table
