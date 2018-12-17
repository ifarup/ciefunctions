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

# The HTML code is aligned left in order to keep the html_string as
# short as possible This is to stay within the size limit of the
# QWebEngineView that will render the html code.

import numpy as np
import sys
from tc1_97.utils import resource_path

def _head():
    package_path = resource_path(".")
    html_string = """
 <head>
<link type="text/css" rel="stylesheet" href="%s/table.css" />
<script type="text/javascript"
    src="%s/MathJax-2.7.5/MathJax.js?config=TeX-AMS_HTML">
</script>
<script type="text/x-mathjax-config">
   MathJax.Hub.Config({
   displayAlign: "left",
   showProcessingMessages: false,
   messageStyle: "none",
   inlineMath:[["\\(","\\)"]],
   displayMath:[["$$","$$"]],
   tex2jax: { preview: "none" },
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


def LMS(results, options, include_head=False):
    """
    Generate html tables of LMS functions for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representations of the LMS and logLMS tables
    """
    λ_step = float(results['λ_step'])
    λ_min = float(results['λ_min'])
    length_LMS = np.shape(results['LMS'])[0]
    length_logLMS = np.shape(results['logLMS'])[0]
    html_table = ""
    if include_head:
        html_table += _head()
    if options['log10']:
        html_table += """
<table>
<thead>
<tr>
<th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
<th>\\(\mathrm{log_{\,10}}\,(\,\\bar l_{\,%s,\,%d}(\lambda)\,)\, \\)</th>
<th>\\(\mathrm{log_{\,10}}\,(\,\\bar m_{\,%s,\,%d}(\lambda)\,)\, \\)</th>
<th>\\(\mathrm{log_{\,10}}\,(\,\\bar s_{\,%s,\,%d}(\lambda)\,)\, \\)</th>
</tr>
</thead>
<tbody>
        """ % (results['field_size'], results['age'],
               results['field_size'], results['age'],
               results['field_size'], results['age'])
        for i in range(length_logLMS):
            if (np.abs(λ_step-np.round(λ_step)) < 0.05 and
                np.abs(λ_min-np.round(λ_min)) < 0.05):
                html_table += """
<tr>
<td>%.0f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
</tr>
                """ % (results['logLMS'][i, 0],
                       results['logLMS'][i, 1],
                       results['logLMS'][i, 2],
                       results['logLMS'][i, 3])
            else:
                html_table += """
<tr>
<td>%.1f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
</tr>
                """ % (results['logLMS'][i, 0],
                       results['logLMS'][i, 1],
                       results['logLMS'][i, 2],
                       results['logLMS'][i, 3])
        html_table += """
</tbody>
</table>
        """
    else:
        html_table += """
<table>
<thead>
<tr>
<th>\\(\lambda\,\mathsf{\small\,(nm)} \\)</th>
<th>\\(\\bar l_{%s,\,%d}(\lambda) \\)</th>
<th>\\(\\bar m_{\,%s,\,%d}(\lambda) \\)</th>
<th>\\(\\bar s_{\,%s,\,%d}(\lambda) \\)</th>
</tr>
</thead>
<tbody>
        """ % (results['field_size'], results['age'],
               results['field_size'], results['age'],
               results['field_size'], results['age'])
        for i in range(length_LMS):
            if (np.abs(λ_step-np.round(λ_step)) < 0.05 and
                np.abs(λ_min-np.round(λ_min)) < 0.05):
                html_table += """
<tr>
<td>%.0f</td>
<td>%.5e</td>
<td>%.5e</td>
<td>%.5e</td>
</tr>
                """ % (results['LMS'][i, 0],
                       results['LMS'][i, 1],
                       results['LMS'][i, 2],
                       results['LMS'][i, 3])
            else:
                html_table += """
<tr>
<td>%.1f</td>
<td>%.5e</td>
<td>%.5e</td>
<td>%.5e</td>
</tr>
                """ % (results['LMS'][i, 0],
                       results['LMS'][i, 1],
                       results['LMS'][i, 2],
                       results['LMS'][i, 3])
        html_table += """
          </tbody>
        </table>
        """
    return html_table


def LMS_base(results, options, include_head=False):
    """
    Generate html tables of LMS functions for GUI and web apps.

    Parameters
    ----------
    results : dict
        as returned by tc1_97.compute.compute_tabulated()

    Returns
    -------
    html_table : string
        HTML representations of the LMS and logLMS tables
    """
    λ_step = float(results['λ_step'])
    λ_min = float(results['λ_min'])
    length_LMS_base = np.shape(results['LMS_base'])[0]
    length_logLMS_base = np.shape(results['logLMS_base'])[0]
    html_table = ""
    if include_head:
        html_table += _head()
    if options['log10']:
        html_table += """
<table>
<thead>
<tr>
<th>\\(\lambda\,\mathsf{\small\,(nm)}\\)</th>
<th>\\(\mathrm{log_{\,10}}\,(\,\\bar l_{\,%s,\,%d}(\lambda)\,)\, \\)</th>
<th>\\(\mathrm{log_{\,10}}\,(\,\\bar m_{\,%s,\,%d}(\lambda)\,)\, \\)</th>
<th>\\(\mathrm{log_{\,10}}\,(\,\\bar s_{\,%s,\,%d}(\lambda)\,)\, \\)</th>
</tr>
</thead>
<tbody>
        """ % (results['field_size'], results['age'],
               results['field_size'], results['age'],
               results['field_size'], results['age'])
        for i in range(length_logLMS_base):
            if (np.abs(λ_step-np.round(λ_step)) < 0.05 and
                np.abs(λ_min-np.round(λ_min)) < 0.05):
                html_table += """
<tr>
<td>%.0f</td>
<td>%.8f</td>
<td>%.8f</td>
<td>%.8f</td>
</tr>
                """ % (results['logLMS_base'][i, 0],
                       results['logLMS_base'][i, 1],
                       results['logLMS_base'][i, 2],
                       results['logLMS_base'][i, 3])
            else:
                html_table += """
<tr>
<td>%.1f</td>
<td>%.8f</td>
<td>%.8f</td>
<td>%.8f</td>
</tr>
                """ % (results['logLMS_base'][i, 0],
                       results['logLMS_base'][i, 1],
                       results['logLMS_base'][i, 2],
                       results['logLMS_base'][i, 3])
        html_table += """
</tbody>
</table>
        """
    else:
        html_table += """
<table>
<thead>
<tr>
<th>\\(\lambda\,\mathsf{\small\,(nm)} \\)</th>
<th>\\(\\bar l_{%s,\,%d}(\lambda) \\)</th>
<th>\\(\\bar m_{\,%s,\,%d}(\lambda) \\)</th>
<th>\\(\\bar s_{\,%s,\,%d}(\lambda) \\)</th>
</tr>
</thead>
<tbody>
        """ % (results['field_size'], results['age'],
               results['field_size'], results['age'],
               results['field_size'], results['age'])
        for i in range(length_LMS_base):
            if (np.abs(λ_step-np.round(λ_step)) < 0.05 and
                np.abs(λ_min-np.round(λ_min)) < 0.05):
                html_table += """
<tr>
<td>%.0f</td>
<td>%.8e</td>
<td>%.8e</td>
<td>%.8e</td>
</tr>
                """ % (results['LMS_base'][i, 0],
                       results['LMS_base'][i, 1],
                       results['LMS_base'][i, 2],
                       results['LMS_base'][i, 3])
            else:
                html_table += """
<tr>
<td>%.1f</td>
<td>%.8e</td>
<td>%.8e</td>
<td>%.8e</td>
</tr>
                """ % (results['LMS_base'][i, 0],
                       results['LMS_base'][i, 1],
                       results['LMS_base'][i, 2],
                       results['LMS_base'][i, 3])
        html_table += """
</tbody>
</table>
        """
    return html_table


def lms_mb(results, options, include_head=False):
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
    for i in range(np.shape(results['lms_mb'])[0]):
        if (float(results['λ_step']) ==
                np.round(float(results['λ_step'])) and
                float(results['λ_min']) ==
                np.round(float(results['λ_min']))):
            html_table += """
<tr>
<td>%.0f</td>
<td>%.6f</td>
<td>%.6f</td>
<td>%.6f</td>
</tr>
            """ % (results['lms_mb'][i, 0],
                   results['lms_mb'][i, 1],
                   results['lms_mb'][i, 2],
                   results['lms_mb'][i, 3])
        else:
            html_table += """
<tr>
<td>%.1f</td>
<td>%.6f</td>
<td>%.6f</td>
<td>%.6f</td>
</tr>
            """ % (results['lms_mb'][i, 0],
                   results['lms_mb'][i, 1],
                   results['lms_mb'][i, 2],
                   results['lms_mb'][i, 3])
    html_table += """
</tbody>
</table>
    """
    return html_table


def lms_mw(results, options, include_head=False):
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
    for i in range(np.shape(results['lms_mw'])[0]):
        if (float(results['λ_step']) ==
                np.round(float(results['λ_step'])) and
                float(results['λ_min']) ==
                np.round(float(results['λ_min']))):
            html_table += """
<tr>
<td>%.0f</td>
<td>%.6f</td>
<td>%.6f</td>
<td>%.6f</td>
</tr>
            """ % (results['lms_mw'][i, 0],
                   results['lms_mw'][i, 1],
                   results['lms_mw'][i, 2],
                   results['lms_mw'][i, 3])
        else:
            html_table += """
<tr>
<td>%.1f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
</tr>
            """ % (results['lms_mw'][i, 0],
                   results['lms_mw'][i, 1],
                   results['lms_mw'][i, 2],
                   results['lms_mw'][i, 3])

    html_table += """
</tbody>
</table>
    """
    return html_table


def XYZ(results, options, include_head=False):
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
        XYZ = results['XYZ_N']
    else:
        XYZ = results['XYZ']
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
    for i in range(np.shape(XYZ)[0]):
        if (float(results['λ_step']) ==
                np.round(float(results['λ_step'])) and
                float(results['λ_min']) ==
                np.round(float(results['λ_min']))):
            html_table += """
<tr>
<td>%.0f</td>
<td>%.6e</td>
<td>%.6e</td>
<td>%.6e</td>
</tr>
            """ % (XYZ[i, 0],
                   XYZ[i, 1],
                   XYZ[i, 2],
                   XYZ[i, 3])
        else:
            html_table += """
<tr>
<td>%.1f</td>
<td>%.6e</td>
<td>%.6e</td>
<td>%.6e</td>
</tr>
            """ % (XYZ[i, 0],
                   XYZ[i, 1],
                   XYZ[i, 2],
                   XYZ[i, 3])
    html_table += """
</tbody>
</table>
    """
    return html_table


def xyz(results, options, include_head=False):
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
<th>\\(x_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
<th>\\(y_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
<th>\\(z_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda}} \\)</th>
</tr>
</thead>
<tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(xyz)[0]):
        if (float(results['λ_step']) ==
                np.round(float(results['λ_step'])) and
                float(results['λ_min']) ==
                np.round(float(results['λ_min']))):
            html_table += """
<tr>
<td>%.0f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
</tr>
            """ % (xyz[i, 0],
                   xyz[i, 1],
                   xyz[i, 2],
                   xyz[i, 3])
        else:
            html_table += """
<tr>
<td>%.1f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
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


def XYZ_purples(results, options, include_head=False):
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
        XYZ_p = results['XYZ_purples_N']
    else:
        XYZ_p = results['XYZ_purples']
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
<table>
<thead>
<tr>
<th>\\(\\lambda_{\\,\\mathrm{c}}\,\mathsf{\small\,(nm)}\\)</th>
<th>\\(\\bar x_{\,\mathrm{Fp},\,%s,\,%d}(\lambda_{\\,\\mathrm{c}})\\)</th>
<th>\\(\\bar y_{\,\mathrm{Fp},\,%s,\,%d}(\lambda_{\\,\\mathrm{c}})\\)</th>
<th>\\(\\bar z_{\,\mathrm{Fp},\,%s,\,%d}(\lambda_{\\,\\mathrm{c}})\\)</th>
</tr>
</thead>
<tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(XYZ_p)[0]):
        if (float(results['λ_step']) ==
                np.round(float(results['λ_step'])) and
                float(results['λ_min']) ==
                np.round(float(results['λ_min']))):
            html_table += """
<tr>
<td>%.0f</td>
<td>%.6e</td>
<td>%.6e</td>
<td>%.6e</td>
</tr>
            """ % (XYZ_p[i, 0],
                   XYZ_p[i, 1],
                   XYZ_p[i, 2],
                   XYZ_p[i, 3])
        else:
            html_table += """
<tr>
<td>%.1f</td>
<td>%.6e</td>
<td>%.6e</td>
<td>%.6e</td>
</tr>
            """ % (XYZ_p[i, 0],
                   XYZ_p[i, 1],
                   XYZ_p[i, 2],
                   XYZ_p[i, 3])
    html_table += """
</tbody>
</table>
    """
    return html_table


def xyz_purples(results, options, include_head=False):
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
        xyz_purples = results['xyz_purples_N']
    else:
        xyz_purples = results['xyz_purples']
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
<table>
<thead>
<tr>
<th>\\(\\lambda_{\\,\\mathrm{c}}\,\mathsf{\small\,(nm)}\\)</th>
<th>\\(x_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda_{\\mathrm{c}}}}\\)</th>
<th>\\(y_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda_{\\mathrm{c}}}}\\)</th>
<th>\\(z_{\,\mathrm{F},\,%s,\,%d\\mathrm{;\\,\\lambda_{\\mathrm{c}}}}\\)</th>
</tr>
</thead>
<tbody>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(xyz_purples)[0]):
        if (float(results['λ_step']) ==
                np.round(float(results['λ_step'])) and
                float(results['λ_min']) ==
                np.round(float(results['λ_min']))):
            html_table += """
<tr>
<td>%.0f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
</tr>
            """ % (xyz_purples[i, 0],
                   xyz_purples[i, 1],
                   xyz_purples[i, 2],
                   xyz_purples[i, 3])
        else:
            html_table += """
<tr>
<td>%.1f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
</tr>
            """ % (xyz_purples[i, 0],
                   xyz_purples[i, 1],
                   xyz_purples[i, 2],
                   xyz_purples[i, 3])
    html_table += """
</tbody>
</table>
    """
    return html_table


def XYZ31(results, options, include_head=False):
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
    for i in range(np.shape(results['XYZ31'])[0]):
        html_table += """
<tr>
<td>%.0f</td>
<td>%.6e</td>
<td>%.6e</td>
<td>%.6e</td>
</tr>
        """ % (results['XYZ31'][i, 0],
               results['XYZ31'][i, 1],
               results['XYZ31'][i, 2],
               results['XYZ31'][i, 3])
    html_table += """
</tbody>
</table>
    """
    return html_table


def XYZ64(results, options, include_head=False):
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
    for i in range(np.shape(results['XYZ64'])[0]):
        html_table += """
<tr>
<td>%.0f</td>
<td>%.6e</td>
<td>%.6e</td>
<td>%.6e</td>
</tr>
        """ % (results['XYZ64'][i, 0],
               results['XYZ64'][i, 1],
               results['XYZ64'][i, 2],
               results['XYZ64'][i, 3])
    html_table += """
</tbody>
</table>
    """
    return html_table


def xyz31(results, options, include_head=False):
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
    for i in range(np.shape(results['xyz31'])[0]):
        html_table += """
<tr>
<td>%.0f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
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
    for i in range(np.shape(results['xyz64'])[0]):
        html_table += """
<tr>
<td>%.0f</td>
<td>%.5f</td>
<td>%.5f</td>
<td>%.5f</td>
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
