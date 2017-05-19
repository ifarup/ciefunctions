#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
table: Generate html tables for the tc1_97 package.

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
import sys
import inspect
import os.path


def _head():
    package_path = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))
    html_string = """
    <head>
    <link type="text/css" rel="stylesheet" href="%s/table.css" />
    <script type="text/javascript"
    src="%s/../web/static/web/MathJax-2.4-latest/MathJax.js?config=TeX-AMS_HTML">
    </script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            displayAlign: "left",
            showProcessingMessages: false,
            messageStyle: "none",
            inlineMath:[["\\(","\\)"]],
            displayMath:[["$$","$$"]],
            "HTML-CSS": {
    """ % (package_path, package_path)
    if sys.platform.startswith('win'):
        html_string += """
                scale: 95
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


def lms(results, options, include_head=False):
    """
    Generate html table of LMS functions for inclusion in GUI app and web app.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
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
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
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


def mb(results, options, include_head=False):
    """
    Generate html table of MacLeod-Boynton diagram for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(l_{\,\mathrm{MB},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
        <th>\\(m_{\,\mathrm{MB},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
        <th>\\(s_{\,\mathrm{MB},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    results['mb'][results['mb'] <= 0] = 0
    for i in range(np.shape(results['mb'])[0]):
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
            """ % (results['mb'][i, 0],
                   results['mb'][i, 1],
                   results['mb'][i, 2],
                   results['mb'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.6f</td>
               <td>%.6f</td>
               <td>%.6f</td>
            </tr>
            """ % (results['mb'][i, 0],
                   results['mb'][i, 1],
                   results['mb'][i, 2],
                   results['mb'][i, 3])

    html_table += """
      </tbody>
    </table>
    """
    return html_table


def lm(results, options, include_head=False):
    """
    Generate html table of normalized lm diagram for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the tablulated normalized lm diagram
    """
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(l_{\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
        <th>\\(m_{\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
        <th>\\(s_{\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
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


def xyz(results, options, include_head=False):
    """
    Generate html table of XYZ values for inclusion in GUI app and web app.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
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


def xyz_purples(results, options, include_head=False):
    """
    Generate html table of XYZ values (purples) for inclusion apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the XYZ table (purples)
    """
    if options['norm']:
        purple = results['purple_xyz_N']
    else:
        purple = results['purple_xyz']
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\\lambda_{\\,\\mathrm{c}}\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(\\bar x_{\,\mathrm{Fp},\,%s,\,%d}(\lambda_{\\,\\mathrm{c}})
            \\)</th>
        <th>\\(\\bar y_{\,\mathrm{Fp},\,%s,\,%d}(\lambda_{\\,\\mathrm{c}})
            \\)</th>
        <th>\\(\\bar z_{\,\mathrm{Fp},\,%s,\,%d}(\lambda_{\\,\\mathrm{c}})
            \\)</th>
      </tr>
      </thead>
      <tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(purple)[0]):
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
            """ % (purple[i, 0],
                   purple[i, 1],
                   purple[i, 2],
                   purple[i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.6e</td>
               <td>%.6e</td>
               <td>%.6e</td>
            </tr>
            """ % (purple[i, 0],
                   purple[i, 1],
                   purple[i, 2],
                   purple[i, 3])
    html_table += """
      </tbody>
    </table>
    """
    return html_table


def xy(results, options, include_head=False):
    """
    Generate html table of chromaticity values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(x_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
        <th>\\(y_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
        <th>\\(z_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
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


def xy_purples(results, options, include_head=False):
    """
    Generate html table of chromaticity values (purples) for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representation of the chromatictiy table (purples)
    """
    if options['norm']:
        xy = results['purple_cc_N']
    else:
        xy = results['purple_cc']
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <thead>
      <tr>
        <th>\\(\\lambda_{\\,\\mathrm{c}}\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(x_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda_{\\mathrm{c}}}}
            \\)</th>
        <th>\\(y_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda_{\\mathrm{c}}}}
            \\)</th>
        <th>\\(z_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda_{\\mathrm{c}}}}
            \\)</th>
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


def xyz_31(results, options, include_head=False):
    """
    Generate html table of CIE 1931 XYZ values for GUI app and web app.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
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


def xyz_64(results, options, include_head=False):
    """
    Generate html table of CIE 1964 XYZ values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
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


def xy_31(results, options, include_head=False):
    """
    Generate html table of CIE 1931 chromaticity values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(x_{\mathrm{\\lambda}} \\)</th>
        <th>\\(y_{\mathrm{\\lambda}} \\)</th>
        <th>\\(z_{\mathrm{\\lambda}} \\)</th>
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


def xy_64(results, options, include_head=False):
    """
    Generate html table of CIE 1964 chromaticity values for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

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
        <th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
        <th>\\(x_{10;\,\mathrm{\\lambda}} \\)</th>
        <th>\\(x_{10;\,\mathrm{\\lambda}} \\)</th>
        <th>\\(x_{10;\,\mathrm{\\lambda}} \\)</th>
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
