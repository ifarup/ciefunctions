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
    <h2 class="description-heading-2">%s</h2>
    """ % heading

def _sub_heading(sub_heading):
    return """
    <h4 class="description-heading-4">%s</h4>
    """ % sub_heading

def _parameters(data):
    return u"""
    <p>
    <b class="description-subtitle">Parameters</b>
    <table>
    <tr>
        <td>Field size</td>
        <td>: &nbsp;&nbsp; %s\u00b0 </td>
    </tr>
    <tr>
        <td>Age</td>
        <td>: &nbsp;&nbsp; %d yr</td>
    </tr>
    </table>
    </p>
    """ % (data['field_size'], data['age'])
    
def _parameters_31():
    return u"""
    <p>
    <b class="description-subtitle">Parameters</b>
    <table>
    <tr>
        <td>Field size</td>
        <td>: &nbsp;&nbsp; 2\u00b0 </td>
    </tr>
    </table>
    </p>
    """

def _parameters_64():
    return u"""
    <p>
    <b class="description-subtitle">Parameters</b>
    <table>
    <tr>
        <td>Field size</td>
        <td>: &nbsp;&nbsp; 10\u00b0 </td>
    </tr>
    </table>
    </p>
    """

def _functions(par1, par2, par3):
    return """
    <p>
    <b class="description-subtitle">Function symbols</b><br />
    %s &nbsp;&nbsp; %s &nbsp;&nbsp; %s
    </p>
    """ % (par1, par2, par3)

def _coordinates(par1, par2, par3):
    return """
    <p>
    <b class="description-subtitle">Coordinate symbols</b><br />
    %s &nbsp;&nbsp; %s &nbsp;&nbsp; %s
    </p>
    """ % (par1, par2, par3)

def _wavelenghts(data):
    return u"""
    <p>
    <b class="description-subtitle">Selected wavelenghts</b>
    <table>
    <tr>
        <td>Domain</td>
        <td>: &nbsp;&nbsp; %.1f &ndash; %.1f nm</td>
    </tr>
    <tr>
        <td>Step</td>
        <td>: &nbsp;&nbsp; %.1f nm</td>
    </tr>
    </table>
    </p>
    """ % (data['lambda_min'], data['lambda_max'], data['lambda_step'])

def _normalisation(data):
    return u"""
    <em class="description-subtitle">Normalisation:</em><br />
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
    <p>
    <b class="description-subtitle">Normalisation</b><br />
    Function values peaking at unity at 0.1&nbsp;nm resolution<br />
    </p>
    """
    
def _normalisation_xyz(data):
    return """
    <p>
    <b class="description-subtitle">Normalisation</b><br />
    <ul>
    <li>Equal tristimulus values for Illuminant E</li>
    <li>Values of <font style="text-decoration: overline;"><em>y</em></font><sub> F, %s, %d</sub> peaking at unity at 0.1 nm resolution</li>
    </ul>
    </p>
    """ % (data['field_size'], data['age'])
    
def _precision_lms():
    return """
    <p>
    <b class="description-subtitle">Precision of tabulated values</b><br />
    6 significant figures<br />
    </p>
    """
    
def _precision_lms_base():
    return """
    <p>
    <b class="description-subtitle">Precision of tabulated values</b><br />
    9 significant figures<br />
    </p>
    """
    
def _precision_bm():
    return """
    <p>
    <b class="description-subtitle">Precision of tabulated values</b><br />
    6 decimal places<br />
    </p>
    """
    
def _precision_lm():
    return """
    <p>
    <b class="description-subtitle">Precision of tabulated values</b><br />
    6 decimal places<br />
    </p>
    """
    
def _precision_xyz():
    return """
    <p>
    <b class="description-subtitle">Precision of tabulated values</b><br />
    7 significant figures<br />
    </p>
    """
    
def _precision_xy():
    return """
    <p>
    <b class="description-subtitle">Precision of tabulated values</b><br />
    5 decimal places<br />
    </p>
    """
    
def _lms_to_xyz(data):
    html_string = """
    <b class="description-subtitle">Transformation equation</b><br />
    <br />
    <table>
    <tr>
    <td>
    <table class="matrix">
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
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
            <td align="center"><font style="text-decoration: overline;"><em>l</em></font><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>m</em></font><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
        <tr>
            <td align="center"><font style="text-decoration: overline;"><em>s</em></font><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)</td>
        </tr>
    </table>
    </td>
    </tr>
    </table>
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'])
    html_string += """
    <p>
    In the above transformation the cone fundamentals 
    <font style="text-decoration: overline;"><em>l</em></font><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;),
    <font style="text-decoration: overline;"><em>m</em></font><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;) and
    <font style="text-decoration: overline;"><em>s</em></font><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;) are given to the precision of 9 significant figures.
    </p>
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['field_size'], data['age'])
    return html_string

def _lms_to_bm(data):
    return """
    <p>
    <b class="description-subtitle">Transformation equations</b><br />
    TODO
    </p>
    """

def _lms_to_lm(data):
    return """
    <p>
    <b class="description-subtitle">Transformation equations</b><br />
    TODO
    </p>
    """

def _xyz_to_xy(data):
    return """
    <b class="description-subtitle">Transformation equations</b><br />
    <br />
    <table>
        <tr>
            <td>
                <em>x</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            </td>
            <td>
                =
            </td>
            <td>
            <font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            / (&nbsp;<font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)&nbsp;)
            </td>
        </tr>
        <tr>
            <td>
                <em>y</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            </td>
            <td>
                =
            </td>
            <td>
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            / (&nbsp;<font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)&nbsp;)
            </td>
        </tr>
        <tr>
            <td>
                <em>z</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            </td>
            <td>
                =
            </td>
            <td>
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            / (&nbsp;<font style="text-decoration: overline;"><em>x</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>y</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)
            +
            <font style="text-decoration: overline;"><em>z</em></font><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(&lambda;)&nbsp;)
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
    <b class="description-subtitle">Chromaticity point of illuminant E</b><br />
    (<em>x</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d;&nbsp;E</sub>, 
    <em>y</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d;&nbsp;E</sub>)
    =
    (%.5f, %.5f) <br /><br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['cc_white'][0], data['cc_white'][1])

def _illuminant_E_lm(data):
    return """
    <b class="description-subtitle">Chromaticity point of illuminant E</b><br />
    (<em>l</em><sub>&nbsp;%s,&nbsp;%d;&nbsp;E</sub>, 
    <em>m</em><sub>,&nbsp;%s,&nbsp;%d;&nbsp;E</sub>)
    =
    (%.6f, %.6f) <br /><br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['lm_white'][0], data['lm_white'][1])

def _illuminant_E_bm(data):
    return """
    <b class="description-subtitle">Chromaticity point of illuminant E</b><br />
    (<em>l</em><sub>&nbsp;MB,&nbsp;%s,&nbsp;%d;&nbsp;E</sub>, 
    <em>s</em><sub>&nbsp;MB,&nbsp;%s,&nbsp;%d;&nbsp;E</sub>)
    =
    (%.5f, %.5f) <br /><br />
    """ % (data['field_size'], data['age'],
           data['field_size'], data['age'],
           data['bm_white'][0], data['bm_white'][2])

def _purple_cc(data):
    return """
    <b class="description-subtitle">Tangent points of the purple line</b><br />
    (<em>x</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>y</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f) <br />
    (<em>x</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>y</em><sub>&nbsp;F,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm))
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
    <b class="description-subtitle">Tangent points of the purple line</b><br />
    (<em>l</em><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>m</em><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.6f, %.6f) <br />
    (<em>l</em><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>m</em><sub>&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.6f, %.6f)
    """ % (data['field_size'], data['age'], data['purple_line_lm'][0,0],
           data['field_size'], data['age'], data['purple_line_lm'][0,0],
           data['purple_line_lm'][0,1], data['purple_line_lm'][0,2],
           data['field_size'], data['age'], data['purple_line_lm'][1,0],
           data['field_size'], data['age'], data['purple_line_lm'][1,0],
           data['purple_line_lm'][1,1], data['purple_line_lm'][1,2])

def _purple_bm(data):
    return """
    <b class="description-subtitle">Tangent points of the purple line</b><br />
    (<em>l</em><sub>&nbsp;MB,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>s</em><sub>&nbsp;MB,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm))
    &nbsp;=&nbsp;
    (%.5f, %.5f) <br />
    (<em>l</em><sub>&nbsp;MB,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm), 
    <em>s</em><sub>&nbsp;MB,&nbsp;%s,&nbsp;%d&nbsp;</sub>(%.1f nm))
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
                    _functions('<font style="text-decoration: overline;"><em>x</em></font><sub> F, %s, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>y</em></font><sub> F, %s, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>z</em></font><sub> F, %s, %d</sub>' % (data['field_size'], data['age'])) +
                    _wavelenghts(data) +
                    _normalisation_xyz(data) +
                    _lms_to_xyz(data) +
                    _precision_xyz())
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
                    _coordinates('<em>x</em><sub> F, %s, %d</sub>' % (data['field_size'], data['age']),
                               '<em>y</em><sub> F, %s, %d</sub>' % (data['field_size'], data['age']),
                               '<em>z</em><sub> F, %s, %d</sub>' % (data['field_size'], data['age'])) +
                    _wavelenghts(data) +
                    _xyz_to_xy(data) +
                    _precision_xy() +
                    _illuminant_E_cc(data) +
                    _purple_cc(data))
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
                    _functions('<font style="text-decoration: overline;"><em>l</em></font><sub> %s, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>m</em></font><sub> %s, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>s</em></font><sub> %s, %d</sub>' % (data['field_size'], data['age'])) +
                    _wavelenghts(data) +
                    _normalisation_lms() +
                    _precision_lms())
    return html_string

def lms_base(data, heading, include_head=False):
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
                    _functions('<font style="text-decoration: overline;"><em>l</em></font><sub> %s, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>m</em></font><sub> %s, %d</sub>' % (data['field_size'], data['age']),
                               '<font style="text-decoration: overline;"><em>s</em></font><sub> %s, %d</sub>' % (data['field_size'], data['age'])) +
                    _wavelenghts(data) +
                    _normalisation_lms() +
                    _precision_lms_base())
    return html_string

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
                    _coordinates('TODO', 'TODO', 'TODO') +
                    _wavelenghts(data) +
                    _lms_to_bm(data) +
                    _precision_bm() +
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
                    _coordinates('TODO', 'TODO', 'TODO') +
                    _wavelenghts(data) +
                    _lms_to_lm(data) +
                    _precision_lm() +
                    _illuminant_E_lm(data) +
                    _purple_lm(data))
    return html_string

def xyz31(heading, include_head=False):
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
                    _parameters_31())
    return html_string

def xyz64(heading, include_head=False):

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
                    _parameters_64())
    return html_string

def xy31(heading, include_head=False):
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
                    _parameters_31())
    return html_string

def xy64(heading, include_head=False):
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
                    _parameters_64())
    return html_string
