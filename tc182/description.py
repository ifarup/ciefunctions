#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description: Generate html description strings for the tc182 package.

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

def _head():
    return """
    <head>
    <style>
    body {
      font-family: Sans-Serif;
    }
    .matrix {
        position: relative;
        border-spacing: 10px 0;
    }
    .matrix:before {
        content: "";
        position: absolute;
        left: -6px;
        top: 0;
        border: 1px solid #000;
        border-right: 0px;
        width: 6px;
        height: 100%;
    }
    .matrix:after {
        content: "";
        position: absolute;
        right: -6px;
        top: 0;
        border: 1px solid #000;
        border-left: 0px;
        width: 6px;
        height: 100%;
    }
    </style>
    </head>
    """

def _heading(heading):
    return """
    <h2>%s</h2>
    """ % heading

def _sub_heading(sub_heading):
    return """
    <h4>%s</h4>
    """ % sub_heading

def _parameters(data):
    return u"""
    <p>
    <b>Parameters</b>
    <table>
    <tr>
        <td>Field size</td>
        <td>: &nbsp;&nbsp; %.1f\u00b0 </td>
    </tr>
    <tr>
        <td>Age</td>
        <td>: &nbsp;&nbsp; %d yr</td>
    </tr>
    </table>
    </p>
    """ % (data['field_size'], data['age'])

def _functions(par1, par2, par3):
    return """
    <p>
    <b>Function symbols</b><br />
    %s<br />
    %s<br />
    %s<br />
    </p>
    """ % (par1, par2, par3)

def _normalisation(data):
    return u"""
    <em>Normalisation:</em><br />
    Equal tristimulus values for illuminant E for
    <table>
        <tr>
            <td>Wavelength domain:</td>
            <td valign="bottom">&nbsp;%0.1f\u2013%0.1f&nbsp;nm</td>
        </tr>
        <tr>
            <td>Wavelength step:</td>
            <td valign="bottom">&nbsp;%0.1f&nbsp;nm</td>
        </tr>
    </table>
    """  % (data['lambda_min'], data['lambda_max'], data['lambda_step'])

def _normalisation_lms():
    return """
    <b>Normalisation</b><br />
    Peak value of unity at 0.1&nbsp;nm resolution<br />
    """
    
def _lms_to_xyz(data):
    html_string = """
    <b>Transformation equation</b><br />
    """ + _normalisation(data) + """
    <br />
    <table>
    <tr>
    <td>
    <table class="matrix">
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
    </table>
    </td>
    <td>
    &nbsp;&nbsp;=&nbsp;&nbsp;
    </td>
    <td>
    <table class="matrix">
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'])
    for i in range(3):
        html_string = html_string + '<tr>\n'
        for j in range(3):
            if data['trans_mat'][i][j] == 0:
                html_string = html_string + """
                <td align="center">
                0
                </td>
                """
            else:
                html_string = html_string + '<td align="right">\n'
                html_string = html_string + '%0.8f\n' % data['trans_mat'][i][j]
                html_string = html_string + '</td>\n'
        html_string = html_string + '</tr>\n'
    html_string = html_string + """
    </table>
    </td>
    <td>
    &nbsp;&nbsp;&nbsp;
    </td>
    <td>
    <table class="matrix">
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>l</em></font><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>m</em></font><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>s</em></font><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
    </table>
    </td>
    </tr>
    </table>
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'])
    return html_string

def _xyz_to_xy(data):
    return """
    <b>Transformation equation</b><br />
    """ + _normalisation(data) + """
    <br />
    <table>
        <tr>
            <td>
                <em>x</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            </td>
            <td>
                =
            </td>
            <td>
            <font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            / (&nbsp;<font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)&nbsp;)
            </td>
        </tr>
        <tr>
            <td>
                <em>y</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            </td>
            <td>
                =
            </td>
            <td>
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            / (&nbsp;<font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)&nbsp;)
            </td>
        </tr>
        <tr>
            <td>
                <em>z</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            </td>
            <td>
                =
            </td>
            <td>
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            / (&nbsp;<font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(&lambda;)&nbsp;)
            </td>
        </tr>
    </table>
    <br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'])

def _illuminant_E_cc(data):
    return """
    <b>Chromaticity point of illuminant E</b><br />
    (<em>x</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d;&nbsp;E</sub>, 
    <em>y</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d;&nbsp;E</sub>)
    =
    (%.5f, %.5f) <br /><br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['cc_white'][0], data['cc_white'][1])

def _illuminant_E_lm(data):
    return """
    <b>Chromaticity point of illuminant E</b><br />
    (<em>l</em><sub>&nbsp;%.1f,&nbsp;%d;&nbsp;E</sub>, 
    <em>m</em><sub>,&nbsp;%.1f,&nbsp;%d;&nbsp;E</sub>)
    =
    (%.5f, %.5f) <br /><br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['lm_white'][0], data['lm_white'][1])

def _illuminant_E_bm(data):
    return """
    <b>Chromaticity point of illuminant E</b><br />
    (<em>l</em><sub>&nbsp;MB,&nbsp;%.1f,&nbsp;%d;&nbsp;E</sub>, 
    <em>s</em><sub>&nbsp;MB,&nbsp;%.1f,&nbsp;%d;&nbsp;E</sub>)
    =
    (%.5f, %.5f) <br /><br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['bm_white'][0], data['bm_white'][2])

def _purple_cc(data):
    return """
    <b>Tangent points of the purple line</b><br />
    (<em>x</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>y</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f) <br />
    (<em>x</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>y</em><sub>&nbsp;F,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f)
    """ % (data['field_size'], data['age'], data['purple_line_cc'][0,0],
           data['field_size'], data['age'], data['purple_line_cc'][0,0],
           data['purple_line_cc'][0,1], data['purple_line_cc'][0,2],
           data['field_size'], data['age'], data['purple_line_cc'][1,0],
           data['field_size'], data['age'], data['purple_line_cc'][1,0],
           data['purple_line_cc'][1,1], data['purple_line_cc'][1,2])

def _purple_lm(data):
    return """
    <b>Tangent points of the purple line</b><br />
    (<em>l</em><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>m</em><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f) <br />
    (<em>l</em><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>m</em><sub>&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f)
    """ % (data['field_size'], data['age'], data['purple_line_lm'][0,0],
           data['field_size'], data['age'], data['purple_line_lm'][0,0],
           data['purple_line_lm'][0,1], data['purple_line_lm'][0,2],
           data['field_size'], data['age'], data['purple_line_lm'][1,0],
           data['field_size'], data['age'], data['purple_line_lm'][1,0],
           data['purple_line_lm'][1,1], data['purple_line_lm'][1,2])

def _purple_bm(data):
    return """
    <b>Tangent points of the purple line</b><br />
    (<em>l</em><sub>&nbsp;MB,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>s</em><sub>&nbsp;MB,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f) <br />
    (<em>l</em><sub>&nbsp;MB,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>s</em><sub>&nbsp;MB,&nbsp;%.1f,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f)
    """ % (data['field_size'], data['age'], data['purple_line_bm'][0,0],
           data['field_size'], data['age'], data['purple_line_bm'][0,0],
           data['purple_line_bm'][0,1], data['purple_line_bm'][0,2],
           data['field_size'], data['age'], data['purple_line_bm'][1,0],
           data['field_size'], data['age'], data['purple_line_bm'][1,0],
           data['purple_line_bm'][1,1], data['purple_line_bm'][1,2])

def xyz(data, heading, include_head=False):
    """
    Generate html page with information about the XYZ system.
    
    Parameters
    ----------
    data : dict
        Computed CIE functions as returned from the tc182 module.
    heading : string
        The heading of the page.
    include_head : bool
        Indlue html head with css (for matrix etc.)
        
    Returns
    -------
    html_string : string
        The generated page.
    """
    html_string = ""
    if include_head:
        html_string += _head()
    html_string += (_heading(heading) +
                    _parameters(data) +
                    _functions('<font style="text-decoration: overline;"><em>x</em></font><sub> F, %.1f, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>y</em></font><sub> F, %.1f, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>z</em></font><sub> F, %.1f, %d</sub>' % (data['field_size'], data['age'])) +
                    _lms_to_xyz(data))
    return html_string

def xy(data, heading, include_head=False):
    """
    Generate html page with information about the xy system.
    
    Parameters
    ----------
    data : dict
        Computed CIE functions as returned from the tc182 module.
    heading : string
        The heading of the page.
    include_head : bool
        Indlue html head with css (for matrix etc.)
        
    Returns
    -------
    html_string : string
        The generated page.
    """
    html_string = ""
    if include_head:
        html_string += _head()
    html_string += (_heading(heading) +
                    _parameters(data) +
                    _functions('<em>x</em><sub> F, %.1f, %d</sub>' % (data['field_size'], data['age']),
                               '<em>y</em><sub> F, %.1f, %d</sub>' % (data['field_size'], data['age']),
                               '<em>z</em><sub> F, %.1f, %d</sub>' % (data['field_size'], data['age'])) +
                    _xyz_to_xy(data) + _illuminant_E_cc(data) + _purple_cc(data))
    return html_string

def lms(data, heading, include_head=False):
    """
    Generate html page with information about the LMS system.
    
    Parameters
    ----------
    data : dict
        Computed CIE functions as returned from the tc182 module.
    heading : string
        The heading of the page.
    include_head : bool
        Indlue html head with css (for matrix etc.)
        
    Returns
    -------
    html_string : string
        The generated page.
    """
    html_string = ""
    if include_head:
        html_string += _head()
    html_string += (_heading(heading) +
                    _parameters(data) +
                    _functions('<font style="text-decoration: overline;"><em>l</em></font><sub> %.1f, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>m</em></font><sub> %.1f, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>s</em></font><sub> %.1f, %d</sub>' % (data['field_size'], data['age'])) +
                    _normalisation_lms())
    return html_string

def lms_base(data, heading, include_head=False):
    """
    Wrapper for consistency.
    """
    return lms(data, heading, include_head)

def bm(data, heading, include_head=False):
    """
    Generate html page with information about the BM system.
    
    Parameters
    ----------
    data : dict
        Computed CIE functions as returned from the tc182 module.
    heading : string
        The heading of the page.
    include_head : bool
        Indlue html head with css (for matrix etc.)
        
    Returns
    -------
    html_string : string
        The generated page.
    """
    html_string = ""
    if include_head:
        html_string += _head()
    html_string += (_heading(heading) +
                    _parameters(data) +
                    _illuminant_E_bm(data) +
                    _purple_bm(data))
    return html_string


def lm(data, heading, include_head=False):
    """
    Generate html page with information about the lm system.
    
    Parameters
    ----------
    data : dict
        Computed CIE functions as returned from the tc182 module.
    heading : string
        The heading of the page.
    include_head : bool
        Indlue html head with css (for matrix etc.)
        
    Returns
    -------
    html_string : string
        The generated page.
    """
    html_string = ""
    if include_head:
        html_string += _head()
    html_string += (_heading(heading) +
                    _parameters(data) +
                    _illuminant_E_lm(data) +
                    _purple_lm(data))
    return html_string

def standard(heading, sub_heading, include_head=False):
    """
    Generate html page with information about the standard
    
    Parameters
    ----------
    heading : string
        The heading of the page.
    sub_heading : string
        The sub-heading of the page.
    include_head : bool
        Indlue html head with css (for matrix etc.)
        
    Returns
    -------
    html_string : string
        The generated page.
    """
    html_string = ""
    if include_head:
        html_string += _head()
    html_string += (_heading(heading) +
                    _sub_heading(sub_heading))
    return html_string
