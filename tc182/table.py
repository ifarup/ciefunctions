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

def _head():
    return """
    <head>
    <style>
    body {
      font-family: Sans-Serif;
    }
    table {
    	margin-left: auto;
		margin-right: auto;
		width: 100%;
    }
    tr:nth-child(even){
        background-color: #ddd;
    }
    td {
        padding: 0px 10px 0px 10px;
        text-align: center;
    }
    </style>
    </head>
    """

def xyz(results, include_head=False):
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
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <tr>
        <th>&lambda;</th>
        <th><font style="text-decoration: overline;"><em>x</em></font><sub> F, %s, %d</sub></th>
        <th><font style="text-decoration: overline;"><em>y</em></font><sub> F, %s, %d</sub></th>
        <th><font style="text-decoration: overline;"><em>z</em></font><sub> F, %s, %d</sub></th>
      <tr>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['xyz'])[0]):
        if float(results['lambda_step']) == np.round(float(results['lambda_step'])):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.6e</td>
               <td>%.6e</td>
               <td>%.6e</td>
            </tr>
            """ % (results['xyz'][i, 0],
                   results['xyz'][i, 1],
                   results['xyz'][i, 2],
                   results['xyz'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.6e</td>
               <td>%.6e</td>
               <td>%.6e</td>
            </tr>
            """ % (results['xyz'][i, 0],
                   results['xyz'][i, 1],
                   results['xyz'][i, 2],
                   results['xyz'][i, 3])
    html_table += """
    </table>
    """
    return html_table

def xy(results, include_head=False):
    """
    Generate html table of chromaticity values for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><em>x</em><sub> F, %s, %d</sub></th>
        <th><em>y</em><sub> F, %s, %d</sub></th>
        <th><em>z</em><sub> F, %s, %d</sub></th>
      <tr>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['xy'])[0]):
        if float(results['lambda_step']) == np.round(float(results['lambda_step'])):
            html_table += """
            <tr>
               <td>%.0f</td>
               <td>%.5f</td>
               <td>%.5f</td>
               <td>%.5f</td>
            </tr>
            """ % (results['xy'][i, 0],
                   results['xy'][i, 1],
                   results['xy'][i, 2],
                   results['xy'][i, 3])
        else:
            html_table += """
            <tr>
               <td>%.1f</td>
               <td>%.5f</td>
               <td>%.5f</td>
               <td>%.5f</td>
            </tr>
            """ % (results['xy'][i, 0],
                   results['xy'][i, 1],
                   results['xy'][i, 2],
                   results['xy'][i, 3])
    html_table += """
    </table>
    """
    return html_table

def lms(results, include_head=False):
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
    results['lms'][results['lms'][:,0] > 615, 3] = 0
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <tr>
        <th>&lambda;</th>
        <th><font style="text-decoration: overline;"><em>l</em></font><sub> %s, %d</sub></th>
        <th><font style="text-decoration: overline;"><em>m</em></font><sub> %s, %d</sub></th>
        <th><font style="text-decoration: overline;"><em>s</em></font><sub> %s, %d</sub></th>
      <tr>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['lms'])[0]):
        if float(results['lambda_step']) == np.round(float(results['lambda_step'])):
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
    </table>
    """
    return html_table

def lms_base(results, include_head=False):
    """
    Generate html table of LMS base functions for inclusion in GUI app and web app.
    
    Parameters
    ----------
    results : dict
        as returned by tc182.compute.compute_tabulated()
        
    Returns
    -------
    html_table : string
        HTML representation of the LMS base table
    """
    results['lms_base'][results['lms_base'][:,0] > 615, 3] = 0
    html_table = ""
    if include_head:
        html_table += _head()
    html_table += """
    <table>
      <tr>
        <th>&lambda;</th>
        <th><font style="text-decoration: overline;"><em>l</em></font><sub> %s, %d</sub></th>
        <th><font style="text-decoration: overline;"><em>m</em></font><sub> %s, %d</sub></th>
        <th><font style="text-decoration: overline;"><em>s</em></font><sub> %s, %d</sub></th>
      <tr>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['lms_base'])[0]):
        if float(results['lambda_step']) == np.round(float(results['lambda_step'])):
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
    </table>
    """
    return html_table

def bm(results, include_head=False):
    """
    Generate html table of MacLeod-Boynton diagram for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><em>l</em><sub> MB, %s, %d</sub></th>
        <th><em>m</em><sub> MB, %s, %d</sub></th>
        <th><em>s</em><sub> MB, %s, %d</sub></th>
      <tr>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    results['bm'][results['bm'] <= 0] = 0
    for i in range(np.shape(results['bm'])[0]):
        if float(results['lambda_step']) == np.round(float(results['lambda_step'])):
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
    </table>
    """
    return html_table

def lm(results, include_head=False):
    """
    Generate html table of normalised lm diagram for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><em>l</em><sub> %s, %d</sub></th>
        <th><em>m</em><sub> %s, %d</sub></th>
        <th><em>s</em><sub> %s, %d</sub></th>
      <tr>
    """ % (results['field_size'], results['age'],
           results['field_size'], results['age'],
           results['field_size'], results['age'])
    for i in range(np.shape(results['lm'])[0]):
        if float(results['lambda_step']) == np.round(float(results['lambda_step'])):
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
    </table>
    """
    return html_table

def xyz31(results, include_head=False):
    """
    Generate html table of CIE 1931 XYZ values for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><font style="text-decoration: overline;"><em>x</em></font></th>
        <th><font style="text-decoration: overline;"><em>y</em></font></th>
        <th><font style="text-decoration: overline;"><em>z</em></font></th>
      <tr>
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
    </table>
    """
    return html_table

def xyz64(results, include_head=False):
    """
    Generate html table of CIE 1964 XYZ values for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><font style="text-decoration: overline;"><em>x</em></font><sub>10</sub></th>
        <th><font style="text-decoration: overline;"><em>y</em></font><sub>10</sub></th>
        <th><font style="text-decoration: overline;"><em>z</em></font><sub>10</sub></th>
      <tr>
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
    </table>
    """
    return html_table

def xy31(results, include_head=False):
    """
    Generate html table of CIE 1931 chromaticity values for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><em>x</em></th>
        <th><em>y</em></th>
        <th><em>z</em></th>
      <tr>
    """
    for i in range(np.shape(results['cc31'])[0]):
        html_table += """
        <tr>
           <td>%.0f</td>
           <td>%.5f</td>
           <td>%.5f</td>
           <td>%.5f</td>
        </tr>
        """ % (results['cc31'][i, 0],
               results['cc31'][i, 1],
               results['cc31'][i, 2],
               results['cc31'][i, 3])
    html_table += """
    </table>
    """
    return html_table

def xy64(results, include_head=False):
    """
    Generate html table of CIE 1964 chromaticity values for inclusion in GUI app and web app.
    
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
      <tr>
        <th>&lambda;</th>
        <th><em>x</em><sub>10</sub></th>
        <th><em>y</em><sub>10</sub></th>
        <th><em>z</em><sub>10</sub></th>
      <tr>
    """
    for i in range(np.shape(results['cc64'])[0]):
        html_table += """
        <tr>
           <td>%.0f</td>
           <td>%.5f</td>
           <td>%.5f</td>
           <td>%.5f</td>
        </tr>
        """ % (results['cc64'][i, 0],
               results['cc64'][i, 1],
               results['cc64'][i, 2],
               results['cc64'][i, 3])
    html_table += """
    </table>
    """
    return html_table
