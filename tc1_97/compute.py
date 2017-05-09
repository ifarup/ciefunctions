#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute: Calculate the CIE functions provided by CIE TC 1-97.

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

import os
import inspect
import numpy as np
import scipy.optimize
import scipy.interpolate
import warnings
from scipy.spatial import Delaunay
from scipy.io.matlab.miobase import arr_dtype_number

# The following coding conventions have been applied:
#
# * All functions have a docstring of minimum one line describing the
#   overall purpose of the function as well as the names and types
#   of the parameters and return values.
#
# * In some places, variables have been reused, typically in order to build up
#   arrays sequentially. The typical example is found in, e.g.,
#   absorptance_from_lms10q, where the absorptance array is first initialized
#   as the absorbance, then edited in place. This is in order to achieve
#   a shorter and also more efficient code with less memory allocation, and to
#   avoid namespace pollution in the case of comput_tabulated. Unfortunately,
#   it reduces the readability of the code somewhat. Therefore, all such
#   occurences are marked with comments in the code.


#==============================================================================
# Tabulated and derived visual data
#==============================================================================

def my_round(x, n=0):
    """
    Round array x to n decimal points using round half away from zero.

    This function is needed because the rounding specified in the CIE
    recommendation is different from the standard rounding scheme
    in python (which is following the IEEE recommendation).

    Parameters
    ----------
    x : ndarray
        Array to be rounded
    n : int
        Number of decimal points

    Returns
    -------
    y : ndarray
        Rounded array
    """
    s = np.sign(x)
    return s*np.floor(np.absolute(x)*10**n + 0.5)/10**n


def significant_figures(x, n=0):
    """
    Round x to n significant figures (not decimal points).

    This function is needed because the rounding specified in the CIE
    recommendation is different from the standard rounding scheme
    in python (which is following the IEEE recommendation). Uses
    my_round (above).

    Parameters
    ----------
    x : int, float or ndarray
        Number or array to be rounded.

    Returns
    -------
    t : float or ndarray
        Rounded number or array.
    """
    if type(x) == float or type(x) == int:
        if x == 0.:
            return 0
        else:
            exponent = np.ceil(np.log10(x))
            return 10**exponent * my_round(x / 10**exponent, n)
    exponent = x.copy()
    exponent[x == 0] = 0
    exponent[x != 0] = np.ceil(np.log10(abs(x[x != 0])))
    return 10**exponent * my_round(x / 10**exponent, n)


def chop(arr, epsilon=1e-14):
    """
    Chop values smaller than epsilon in absolute value to zero.

    Similar to Mathematica function.

    Parameters
    ----------
    arr : float or ndarray
        Array or number to be chopped.
    epsilon : float
        Minimum number.

    Returns
    -------
    chopped : float or ndarray
        Chopped numbers.
    """
    if (type(arr) == type(float())) or (type(arr) == type(int())):
        chopped = arr
        if np.abs(chopped) < epsilon:
            chopped = 0
        return chopped
    chopped = arr.copy()                    # initialise to arr values
    chopped[np.abs(chopped) < epsilon] = 0  # set too low values to zero
    return chopped

# def resource_path(relative):
#     """
#     Extend relative path to full path (mainly for PyInstaller integration).
#     """
#     return os.path.join(
#         os.environ.get(
#             '_MEIPASS2',
#             os.path.abspath('.')
#         ),
#         relative
#     )


def resource_path(relative):
    """
    Extend relative path to full path (mainly for PyInstaller integration).

    Parameters
    ----------
    relative : string
        The relative path name.

    Returns
    -------
    absolute : string
        The absolute path name.
    """
    return os.path.dirname(
        os.path.abspath(
            inspect.getsourcefile(resource_path))) + '/' + relative


def read_csv_file(filename, pad=-np.inf):
    """
    Read a CSV file and return pylab array.

    Parameters
    ----------
    filename : string
        Name of the CSV file to read
    pad : float
        Value to pad for missing values.

    Returns
    -------
    csv_array : ndarray
        The content of the file plus padding.
    """
    f = open(resource_path(filename))
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i].split(',')
        for j in range(len(data[i])):
            if data[i][j].strip() == '':
                data[i][j] = pad
            else:
                data[i][j] = float(data[i][j])
    return np.array(data)


def chromaticities_from_XYZ(xyz31, xyz64):
    """
    Compute chromaticities and knots (for interpolation) from XYZ functions.

    Parameters
    ----------
    xyz31 : ndarray
        CIE 1931 colour matching functions
    xyz64 : ndarray
        CIE 1964 colour matching functions

    Returns
    -------
    cc31 : ndarray
        Chromaticities for the 1931 colour matching functions.
    cc64 : ndarray
        Chromaticities for the 1964 colour matching functions.
    cc31knots : ndarray
        Knots for interpolating the chromaticities.
    cc64knots : ndarray
        Knots for interpolating the chromaticities.
    """
    cc31 = xyz31.copy()
    cc31sum = np.sum(cc31[:, 1:], axis=1)
    cc64 = xyz64.copy()
    cc64sum = np.sum(cc64[:, 1:], axis=1)
    for i in range(1, 4):
        cc31[:, i] = cc31[:, i] / cc31sum
        cc64[:, i] = cc64[:, i] / cc64sum

    cc31knots = np.array([cc31[0, 0],
                          cc31[np.argmin(cc31[:, 1]), 0],
                          cc31[np.argmax(cc31[:, 2]), 0],
                          700,
                          cc31[-1, 0]])

    cc64knots = np.array([cc64[0, 0],
                          cc64[np.argmin(cc64[:, 1]), 0],
                          cc64[np.argmax(cc64[:, 2]), 0],
                          700,
                          cc64[-1, 0]])
    return cc31, cc64, cc31knots, cc64knots


def docul_fine(ocular_sum_32, docul2):
    """
    Calculate the two parts of docul.

    Parameters
    ----------
    ocular_sum_32 : ndarray
        Sum of two ocular functions
    docul2 : ndarray

    Returns
    -------
    docul1_fine : ndarray
        Tabulated docul1 with high resolution
    docul2_fine : ndarray
        Tabulated docul2 with high resolution
    """
    docul2_pad = np.zeros((75, 2))             # initialize
    docul2_pad[:, 0] = np.arange(460, 835, 5)  # fill
    docul2_pad[:, 1] = 0                       # fill
    docul2 = np.concatenate((docul2, docul2_pad))
    spl = scipy.interpolate.InterpolatedUnivariateSpline(docul2[:, 0],
                                                         docul2[:, 1])
    docul2_fine = ocular_sum_32.copy()
    docul2_fine[:, 1] = spl(ocular_sum_32[:, 0])
    docul1_fine = ocular_sum_32.copy()
    docul1_fine[:, 1] = ocular_sum_32[:, 1] - docul2_fine[:, 1]
    return docul1_fine, docul2_fine


class VisualData:
    """
    Class containing all visual data input to the computations.

    All data are read from files in the 'data' folder.
    """
    absorbance = read_csv_file('data/absorbances0_1nm.csv')[:, [0, 2, 3, 4]]
    macula_2 = read_csv_file('data/absorbances0_1nm.csv')[:, [0, 6]]
    macula_rel = macula_2 / .35  # since macula at 2 degrees has a
                                 # maximum of 0.35 at 460 (at 5nm step)
    ocular_sum_32 = read_csv_file(
        'data/absorbances0_1nm.csv')[:, [0, 5]]  # 32 years only!!!

    lms10_log_quant = read_csv_file('data/ss10q_fine_8dp.csv')
    lms10_lin_energ = read_csv_file('data/linss10e_fine_8dp.csv', 0)
    lms10_lin_energ_n_signfig = read_csv_file('data/linss10e_fine.csv', 0)
    lms2_log_quant = read_csv_file('data/ss2_10q_fine_8dp.csv')
    lms2_lin_energ = read_csv_file('data/linss2_10e_fine_8dp.csv', 0)
    lms2_lin_energ_n_signfig = read_csv_file('data/linss2_10e_fine.csv', 0)
    vlambdaLM_10_lin_energ = read_csv_file('data/linCIE2015v10e_fine_8dp.csv')
    vlambdaLM_2_lin_energ = read_csv_file('data/linCIE2015v2e_fine_8dp.csv')
    vlambdaLM_10_log_quant = read_csv_file('data/logCIE2015v10q_fine_8dp.csv')
    vlambdaLM_2_log_quant = read_csv_file('data/logCIE2015v2q_fine_8dp.csv')
    xyz31 = read_csv_file('data/ciexyz31_1.csv')
    xyz64 = read_csv_file('data/ciexyz64_1.csv')
    docul2 = read_csv_file('data/docul2.csv')

    cc31, cc64, cc31knots, cc64knots = chromaticities_from_XYZ(xyz31, xyz64)
    docul1_fine, docul2_fine = docul_fine(ocular_sum_32, docul2)


#==============================================================================
# Compute absorptance data from tabulated cone fundamentals; do we need these?
#==============================================================================


def absorptance_from_lms10q():
    """
    Compute the absorptance from quantal lms 10 for reference.
    """
    absorptance = VisualData.lms10_log_quant.copy()  # initialize
    absorptance[:, 1:] = 10**(absorptance[:, 1:])    # convert in-place
    for i in range(1, 4):                            # ditto
        absorptance[:, i] = (absorptance[:, i] /
                             10**(-d_mac_max(10)*VisualData.macula_rel[:, 1] -
                                  VisualData.ocular_sum_32[:, 1]))
        absorptance[:, i] = absorptance[:, i]/absorptance[:, i].max()
    return absorptance


def absorbance_from_lms10q():
    """
    Compute the absorbance from quantal lms 10 for reference.
    """
    absorbance = absorptance_from_lms10q(
        VisualData.lms10_log_quant)  # for in-place editing
    absorbance[:, 1] = (np.log10(1 - absorbance[:, 1] *
                                 (1 - 10**-d_LM_max(10))) /
                        -d_LM_max(10))
    absorbance[:, 2] = (np.log10(1 - absorbance[:, 2] *
                                 (1 - 10**-d_LM_max(10))) /
                        -d_LM_max(10))
    absorbance[:, 3] = (np.log10(1 - absorbance[:, 3] *
                                 (1 - 10**-d_S_max(10))) /
                        -d_S_max(10))
    return absorbance


#==============================================================================
# Functions of age and field size
#==============================================================================


def chromaticity_interpolated(field_size):
    """
    Compute the spectral chromaticity coordinates by interpolation for
    reference.

    Parameters
    ----------
    field_size : float
        The field size in degrees.

    Returns
    -------
    chromaticity : ndarray
        The xyz chromaticities, with wavelenghts in first column.
    """
    alpha = (field_size - 2)/8.
    knots = (1 - alpha)*VisualData.cc31knots + alpha*VisualData.cc64knots
    knots[0] = 360.
    knots[-1] = 830.
    lambd = np.arange(360., 831.)

    lambda31_func = scipy.interpolate.interp1d(
        knots, VisualData.cc31knots, kind='linear')
    lambda64_func = scipy.interpolate.interp1d(
        knots, VisualData.cc64knots, kind='linear')
    lambda31 = lambda31_func(lambd)
    lambda64 = lambda64_func(lambd)

    # x values
    cc31x_func = scipy.interpolate.interp1d(VisualData.cc31[:, 0],
                                            VisualData.cc31[:, 1],
                                            kind='cubic')
    cc64x_func = scipy.interpolate.interp1d(VisualData.cc64[:, 0],
                                            VisualData.cc64[:, 1],
                                            kind='cubic')
    cc31x = cc31x_func(lambda31)
    cc64x = cc64x_func(lambda64)
    xvalues = (1-alpha)*cc31x + alpha*cc64x
    # y values
    cc31y_func = scipy.interpolate.interp1d(VisualData.cc31[:, 0],
                                            VisualData.cc31[:, 2],
                                            kind='cubic')
    cc64y_func = scipy.interpolate.interp1d(VisualData.cc64[:, 0],
                                            VisualData.cc64[:, 2],
                                            kind='cubic')
    cc31y = cc31y_func(lambda31)
    cc64y = cc64y_func(lambda64)
    yvalues = (1-alpha)*cc31y + alpha*cc64y
    zvalues = 1 - xvalues - yvalues
    return np.concatenate((np.reshape(lambd, (471, 1)),
                           np.reshape(xvalues, (471, 1)),
                           np.reshape(yvalues, (471, 1)),
                           np.reshape(zvalues, (471, 1))), 1)


def ocular(age):
    """
    The optical density of the ocular media as a function of age.

    Computes a weighted average of docul1 and docul2.

    Parameters
    ----------
    age : float
        Age in years.

    Returns
    -------
    ocular : ndarray
        The optical density of the ocular media; wavelength in first column.
    """
    ocul = VisualData.docul2_fine.copy()  # initialise for in-place editing
    if age < 60:
        ocul[:, 1] = ((1 + 0.02*(age - 32)) * VisualData.docul1_fine[:, 1] +
                      VisualData.docul2_fine[:, 1])
    else:
        ocul[:, 1] = ((1.56 + 0.0667*(age - 60)) *
                      VisualData.docul1_fine[:, 1] +
                      VisualData.docul2_fine[:, 1])
    return ocul


def d_mac_max(field_size):
    """
    Maximum optical density of the macular pigment (function of field size).

    Parameters
    ----------
    field_size : float
        Field size in degrees.

    Returns
    -------
    d_mac_max : float
        Maximum optical density of the macular pigment.
    """
    return my_round(0.485*np.exp(-field_size/6.132), 3)


def d_LM_max(field_size):
    """
    Maximum optical density of the visual pigment (function of field size).

    Parameters
    ----------
    field_size : float
        Field size in degrees.

    Returns
    -------
    d_LM_max : float
        Maximum optical density of the visual pigment.
    """
    return my_round(0.38 + 0.54*np.exp(-field_size/1.333), 3)


def d_S_max(field_size):
    """
    Maximum optical density of the visual pigment (function of field size).

    Parameters
    ----------
    field_size : float
        Field size in degrees.

    Returns
    -------
    d_S_max : float
        Maximum optical density of the visual pigment.
    """
    return my_round(0.30 + 0.45*np.exp(-field_size/1.333), 3)


def absorpt(field_size):
    """
    Compute quantal absorptance as a function of field size.

    Parameters
    ----------
    field_size : float
        Field size in degrees.

    Returns
    -------
    absorpt : ndarray
        The computed lms functions, with wavelengths in first column.
    """
    abt = VisualData.absorbance.copy()  # initialize for in-place editing
    abt[:, 1] = 1 - 10**(-d_LM_max(field_size) *
                         10**(VisualData.absorbance[:, 1]))  # L
    abt[:, 2] = 1 - 10**(-d_LM_max(field_size) *
                         10**(VisualData.absorbance[:, 2]))  # M
    abt[:, 3] = 1 - 10**(-d_S_max(field_size) *
                         10**(VisualData.absorbance[:, 3]))  # S
    return abt


def lms_quantal(field_size, age):
    """
    Compute quantal cone fundamentals as a function of field size and age.

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.

    Returns
    -------
    lms : ndarray
        The computed lms functions, with wavelengths in first column.
    """
    abt = absorpt(field_size)
    lmsq = abt.copy()           # initialise for in-place editing
    ocul = ocular(age)
    for i in range(1, 4):
        lmsq[:, i] = (abt[:, i] *
                      10**(-d_mac_max(field_size) *
                           VisualData.macula_rel[:, 1] - ocul[:, 1]))
        lmsq[:, i] = lmsq[:, i] / (lmsq[:, i].max())
    return lmsq


def lms_energy_base(field_size, age):
    """
    Compute energy cone fundamentals as a function of field size and age.

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.

    Returns
    -------
    lms : ndarray
        The computed lms functions, with wavelengths in first column.
    lms_max : ndarray
        Max values of the lms functions before renormalization.
    """
    if age == 32:
        if field_size == 2:
            return VisualData.lms2_lin_energ.copy(), 0   # dummy max value
        elif field_size == 10:
            return VisualData.lms10_lin_energ.copy(), 0  # dummy max value
    lms = lms_quantal(field_size, age)  # initialize for in-place editing
    lms_max = []
    for i in range(1, 4):
        lms[:, i] = lms[:, i] * lms[:, 0]
        lms_max.append(lms[:, i].max())
        lms[:, i] = lms[:, i] / lms[:, i].max()
    return significant_figures(lms, 9), np.array(lms_max)


def lms_energy(field_size, age, signfig=6):
    """
    Compute energy cone fundamentals as a function of field size and age.

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.
    signfig : int
        Number of significant figures in returned lms.

    Returns
    -------
    lms : ndarray
        The computed lms functions, with wavelengths in first column.
    lms_max : ndarray
        Max values of the lms functions before renormalization.
    """
    if signfig == 6 and age == 32:
        if field_size == 2:
            return (VisualData.lms2_lin_energ_n_signfig.copy(),
                    0)  # dummy max value
        elif field_size == 10:
            return (VisualData.lms10_lin_energ_n_signfig.copy(),
                    0)  # dummy max value
    lms, lms_max = lms_energy_base(field_size, age)
    if signfig < 6 and age == 32:  # conditionally use preloaded versions
        if field_size == 2:
            lms, lms_max = (VisualData.lms2_lin_energ_n_signfig.copy(),
                            0)  # dummy max value
        elif field_size == 10:
            lms, lms_max = (VisualData.lms10_lin_energ_n_signfig.copy(),
                            0)  # dummy max value
    return significant_figures(lms, signfig), lms_max


def v_lambda_l_cone_weight(field_size, age):
    """
    Compute weighting factor of l_bar(lambda) in V(lambda) synthesis.

    The weighting factors are given on quantal scale.

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.

    Returns
    -------
    weight : float
        The computed weighting factor.
    """
    field_size = 2.  # For strategy 2 in github issue 121. Comment line
                     # for strategy 3
    abt_fs = absorpt(field_size)
    abt_2 = absorpt(2.)
    lmsq_fs_age = lms_quantal(field_size, age)
    lmsq_2_32 = lms_quantal(2, 32)
    const_fs_age = (abt_fs[0, 1] * lmsq_fs_age[0, 2] /
                    (abt_fs[0, 2] * lmsq_fs_age[0, 1]))
    const_2_32 = abt_2[0, 1] * lmsq_2_32[0, 2] / (abt_2[0, 2] *
                                                  lmsq_2_32[0, 1])
    return 1.89 * const_fs_age / const_2_32


def v_lambda_quantal(field_size, age):
    """
    Compute the V(lambda) function as a function of field size and age.

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.

    Returns
    -------
    v_lambda : ndarray
        The computed v_lambda function, with wavelengths in first column.
    """
    lms = lms_quantal(field_size, age)
    v_lambda = np.zeros((np.shape(lms)[0], 2))  # initialize for
                                                # in-place editing
    v_lambda[:, 0] = lms[:, 0]
    v_lambda[:, 1] = (v_lambda_l_cone_weight(field_size, age) * lms[:, 1] +
                      lms[:, 2])
    v_lambda[:, 1] = v_lambda[:, 1] / v_lambda[:, 1].max()
    return v_lambda


def v_lambda_energy_from_quantal(field_size, age):
    """
    Compute the V(lambda) function as a function of field size and age.

    Starting from quantal V(lambda).

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.

    Returns
    -------
    v_lambda : ndarray
        The computed v_lambda function, with wavelengths in first column.
    """
    if age == 32:
        if field_size == 2:
            return VisualData.vlambdaLM_2_log_quant.copy()
        elif field_size == 10:
            return VisualData.vlambdaLM_10_log_quant.copy()
    v_lambda = v_lambda_quantal(field_size, age)  # initialise for
                                                  # in-place editing
    v_lambda[:, 1] = v_lambda[:, 1] * v_lambda[:, 0]
    v_lambda[:, 1] = v_lambda[:, 1] / v_lambda[:, 1].max()
    return v_lambda


def v_lambda_energy_from_lms(field_size, age, v_lambda_signfig=7, mat_dp=8):
    """
    Compute the V(lambda) function as a function of field size and age.

    Starting from engergy scale LMS.

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.
    v_lambda_signfig : int
        Number of significant figures in v_lambda.
    mat_dp : int
        Number of decimal places in transformation matrix.

    Returns
    -------
    v_lambda : ndarray
        The computed v_lambda function, with wavelengths in first column.
    weights : ndarray
        The two weighting factors in V(lambda) = a21*L(lambda) + \
                                                 a22*M(lambda)
    """
    if age == 32:
        if field_size == 2:
            return (VisualData.vlambdaLM_2_lin_energ.copy(),
                    np.array([0.68990272, 0.34832189]))
        elif field_size == 10:
            return (VisualData.vlambdaLM_10_lin_energ.copy(),
                    np.array([0.69283932, 0.34967567]))
    lms, lms_max = lms_energy_base(field_size, age)
    v_lambda = np.zeros((np.shape(lms)[0], 2))  # initialize for in-place
                                                # editing
    v_lambda[:, 0] = lms[:, 0]
    l_weight = v_lambda_l_cone_weight(field_size, age)
    v_lambda[:, 1] = l_weight * lms_max[0]*lms[:, 1] + lms_max[1]*lms[:, 2]
    m = v_lambda[:, 1].max()
    a21 = my_round(l_weight * lms_max[0] / m, mat_dp)
    a22 = my_round(lms_max[1]/m, mat_dp)
    v_lambda[:, 1] = significant_figures(a21 * lms[:, 1] + a22*lms[:, 2],
                                         v_lambda_signfig)
    return v_lambda, np.array([a21, a22])


def projective_lms_to_cc_matrix(trans_mat):
    """
    Compute the coefficients of the projective transformation from lms to cc.

    Compute the matrix for the coefficients of the projective
    transformation from lms to cc.

    Parameters
    ----------
    trans_mat : ndarray
        Transformation matrix from lms to xyz.

    Returns
    -------
    mat : ndarray
        Coefficient matrix for the transformation directly from lms to cc.
    """
    mat = trans_mat.copy()      # initialise for in-place editing
    mat[2, 0] = trans_mat[0, 0] + trans_mat[1, 0] + trans_mat[2, 0]
    mat[2, 1] = trans_mat[0, 1] + trans_mat[1, 1] + trans_mat[2, 1]
    mat[2, 2] = trans_mat[0, 2] + trans_mat[1, 2] + trans_mat[2, 2]
    return mat


def compute_xyz_purples(xy, purple_line, white):
    """
    XYZ cone-fundamental-based tristimulus values for purple-line stimuli.

    Parameters
    ----------
    xy : ndarray
        The chromaticity coordinates.
    purple_line : ndarray
        Wavelenghts and tristimulus values of the termini of the
        purple line.
    white : ndarray
        The white point.
    """
    wx = white[0]
    wy = white[1]
    XB = purple_line[0, 1]
    YB = purple_line[0, 2]
    ZB = purple_line[0, 3]
    XR = purple_line[1, 1]
    YR = purple_line[1, 2]
    ZR = purple_line[1, 3]

    purple_xyz = []
    inside = False
    for i in range(len(xy[:, 0])):
        lbd = my_round(xy[i, 0], 1)
        if (lbd > my_round(purple_line[0, 0], 1) and
                lbd < my_round(purple_line[1, 0], 1)):
            cx = xy[i, 1]
            cy = xy[i, 2]

            # Equations for parameter for convex linear combination of
            # tristimulus values of purple-line termini, determined by
            # Mathematica:
            a = (1 /
                 (1 - ((cy - wy) * XB - (cx - wx) * YB +
                       (cx * wy - cy * wx) * (XB + YB + ZB))
                  / ((cy - wy) * XR - (cx - wx) * YR +
                     (cx * wy - cy * wx) * (XR + YR + ZR))))
            if a >= 0 and a <= 1:
                inside = True
                X = a * XB + (1 - a) * XR
                Y = a * YB + (1 - a) * YR
                Z = a * ZB + (1 - a) * ZR
                purple_xyz.append([lbd, X, Y, Z])
            elif inside:
                break
    return np.array(purple_xyz)


def compute_cc_purples(purple_xyz):
    """
    Cone-fundamental-based chromaticity coordinates of purple-line stimuli.

    Parameters
    ----------
    purple_xyz : ndarray
        The tristimulus values of the the purple-line stimuli.
    """
    purple_cc = purple_xyz.copy() # initialize and copy wavelenghts
    purple_cc[:, 1] = purple_xyz[:, 1] / (purple_xyz[:, 1] + purple_xyz[:, 2] + purple_xyz[:, 3])
    purple_cc[:, 2] = purple_xyz[:, 2] / (purple_xyz[:, 1] + purple_xyz[:, 2] + purple_xyz[:, 3])
    purple_cc[:, 3] = purple_xyz[:, 3] / (purple_xyz[:, 1] + purple_xyz[:, 2] + purple_xyz[:, 3])
    return purple_cc


def square_sum(a13, a21, a22, a33, l_spline, m_spline, s_spline, v_spline,
               lambdas, lambda_ref_min, cc_ref, full_results=False,
               xyz_signfig=7, mat_dp=8):
    """
    Function to be optimised for a13.

    Parameters
    ----------
    a13 : ndarray
        1x1 array with parameter to optimise.
    a21, a22, a33 : float
        Parameters in matrix for LMS to XYZ conversion.
    l_spline, m_spline, s_spline, v_spline: InterPolatedUnivariateSpline
        LMS and V(lambda)
    lambdas : ndarray
        Tabulated lambda values according to chosen resolution.
    lambda_ref_min : float
        Lambda value that gives a minimum for the x-coordinate in the
        corresponding reference diagram, i.e. x(lambda_ref_min) = x_ref_min.
    cc_ref : ndarray
        Tabulated reference chromaticity coordinates at 1 nm steps.
    full_results : bool
        Return all or just the computed error.
    xyz_signfig : int
        Number of significant figures in XYZ.
    mat_dp : int
        Number of decimal places in transformation matrix.

    Returns
    -------
    err : float
        Computed error.
    trans_mat : ndarray
        Transformation matrix.
    lambda_test_min : float
        argmin(x(lambda)).
    ok : bool
        Hit the correct minimum wavelength.
    """
    # Stripping reference values according to Stockman-Sharpe
    cc_ref_trunk = cc_ref[30:, 1:].T.copy()
    x_ref_min = cc_ref_trunk[0, :].min()
    # Computed by Mathematica:
    a11 = (-m_spline(lambda_ref_min) * v_spline(lambdas).sum() + a13 *
           (s_spline(lambda_ref_min)*m_spline(lambdas).sum() -
            m_spline(lambda_ref_min)*s_spline(lambdas).sum()) *
           (-1 + x_ref_min) + (a21*l_spline(lambda_ref_min) +
                               a33*s_spline(lambda_ref_min)) *
           m_spline(lambdas).sum() * x_ref_min +
           m_spline(lambda_ref_min) * (
               a22*m_spline(lambdas).sum() +
               v_spline(lambdas).sum()) *
           x_ref_min) / ((m_spline(lambda_ref_min) *
                          l_spline(lambdas).sum() - l_spline(lambda_ref_min) *
                          m_spline(lambdas).sum()) * (-1 + x_ref_min))
    a12 = (l_spline(lambda_ref_min) * v_spline(lambdas).sum() -
           a13 * (s_spline(lambda_ref_min)*l_spline(lambdas).sum() -
                  l_spline(lambda_ref_min)*s_spline(lambdas).sum()) *
           (-1 + x_ref_min) - ((a21 * l_spline(lambda_ref_min) +
                                a22 * m_spline(lambda_ref_min) +
                                a33 * s_spline(lambda_ref_min)) *
                               l_spline(lambdas).sum() +
                               l_spline(lambda_ref_min) *
                               v_spline(lambdas).sum()) * x_ref_min) / \
        ((m_spline(lambda_ref_min) *
          l_spline(lambdas).sum() - l_spline(lambda_ref_min) *
          m_spline(lambdas).sum()) * (-1 + x_ref_min))
    a11 = my_round(a11[0], mat_dp)
    a12 = my_round(a12[0], mat_dp)
    a13 = my_round(a13[0], mat_dp)
    trans_mat = np.array([[a11, a12, a13], [a21, a22, 0], [0, 0, a33]])
    lms = np.array([l_spline(np.arange(390, 831)),
                    m_spline(np.arange(390, 831)),
                    s_spline(np.arange(390, 831))])
    xyz_exact = np.dot(trans_mat, lms)
    xyz = significant_figures(xyz_exact, xyz_signfig)
    cc = np.array([xyz[0, :] / (xyz[0, :] + xyz[1, :] + xyz[2, :]),
                   xyz[1, :] / (xyz[0, :] + xyz[1, :] + xyz[2, :]),
                   xyz[2, :] / (xyz[0, :] + xyz[1, :] + xyz[2, :])])
    err = ((cc - cc_ref_trunk)**2).sum()
    lambda_test_min = np.arange(390, 831)[cc[0, :].argmin()]
    ok = (lambda_test_min == lambda_ref_min)
    if not ok:
        err = err + np.inf
    if full_results:
        return err, trans_mat, lambda_test_min, ok
    else:
        return err


def compute_tabulated(field_size, age,
                      lambda_min=390, lambda_max=830, lambda_step=1,
                      xyz_signfig=7, cc_dp=5, mat_dp=8,
                      lms_signfig=6, mb_dp=6, lm_dp=6):
    """
    Compute tabulated quantities as a function of field size and age.

    All functions are tabulated at given wavelength lambda_step. The
    functions are tabulated on four different wavelength lambda_steps:
    390-830, 0.1 nm (_base), 390-830, 1 nm (_std), and lambda_min -
    lambda_max, lambda_step (_spec), and lambda_min - lambda_max, 0.1
    nm (_plot).

    Parameters
    ----------
    field_size : float
        Field size in degrees.
    age : float
        Age in years.
    lambda_min : float
        Lower limit of wavelength domain
    lambda_min : float
        Upper limit of wavelength domain
    lambda_step : float
        Resolution of tabulated results in nm.
    xyz_signfig : int
        Number of significant figures in XYZ.
    cc_dp : int
        Number of decimal places in chromaticity coordinates.
    mat_dp : int
        Number of decimal places in transformation matrix.
    lms_signfig : int
        Number of significant figures in LMS standard
    mb_dp : int
        Number of decimal places in Boynton-MacLeod chromaticity coordinates.
    lm_dp : int
        Number of decimal places in the normalized lm coordinates.

    Returns
    -------
    results : dict
        All results: xyz, cc, cc_white, mat, lms_standard, lms_base,
        mb, mb_white, lm, lm_white, lambda_test_min, purple_line_cc,
        purple_line_mb, purple_line_lm
    plots : dict
        Versions of xyz, cc, lms, mb, lm at 0.1 nm for
        plotting. Includes also CIE1964 and CIE1931 data.
    """
    plots = dict()
    lms_base = lms_energy_base(field_size, age)[0]
    lms_standard_base = lms_energy(field_size, age, lms_signfig)[0]
    v_lambda_base, weights = v_lambda_energy_from_lms(field_size, age,
                                                      xyz_signfig, mat_dp)
    # For normalization of Boynton-MacLeod, see below:
    mb_s_max = np.max(lms_base[:, 3] / v_lambda_base[:, 1])

    # Spline functions
    l_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        lms_base[:, 0], lms_base[:, 1])
    m_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        lms_base[:, 0], lms_base[:, 2])
    s_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        lms_base[:, 0], lms_base[:, 3])
    ls_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        lms_standard_base[:, 0], lms_standard_base[:, 1])
    ms_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        lms_standard_base[:, 0], lms_standard_base[:, 2])
    ss_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        lms_standard_base[:, 0], lms_standard_base[:, 3])
    v_spline = scipy.interpolate.InterpolatedUnivariateSpline(
        v_lambda_base[:, 0], v_lambda_base[:, 1])

    # Lambda values
    lambdas_spec = np.arange(lambda_min, lambda_max + .01, lambda_step)
    lambda_max = lambdas_spec[-1]
    lambdas_std = np.arange(390, 830 + 1, 1)
    lambdas_plot = my_round(np.arange(lambda_min, lambda_max + .1, .1), 1)

    plots['lms'] = np.array([lambdas_plot,
                             l_spline(lambdas_plot),
                             m_spline(lambdas_plot),
                             s_spline(lambdas_plot)]).T

    lms_spec = np.array([l_spline(lambdas_spec),
                         m_spline(lambdas_spec),
                         s_spline(lambdas_spec)])

    lms_standard_spec = np.array([ls_spline(lambdas_spec),
                                  ms_spline(lambdas_spec),
                                  ss_spline(lambdas_spec)])

    s_std = s_spline(lambdas_std)
    v_std = v_spline(lambdas_std)
    v_spec = v_spline(lambdas_spec)

    # Compute XYZ and chromaticity diagram
    a21 = weights[0]
    a22 = weights[1]
    a33 = my_round(v_std.sum() / s_std.sum(), mat_dp)

    cc_ref = chromaticity_interpolated(field_size)

    # Optimise
    lambda_x_min_ref = 502
    ok = False
    while not ok:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            a13 = scipy.optimize.fmin(
                square_sum, 0.39, (a21, a22, a33, l_spline, m_spline, s_spline,
                                   v_spline, lambdas_std, lambda_x_min_ref,
                                   cc_ref, False, xyz_signfig, mat_dp),
                xtol=10**(-(mat_dp + 2)), disp=False)
        trans_mat, lambda_x_min_ref, ok = (
            square_sum(a13, a21, a22, a33, l_spline, m_spline,
                       s_spline, v_spline, lambdas_std,
                       lambda_x_min_ref, cc_ref, True,
                       xyz_signfig, mat_dp)[1:])

    # Compute xyz (not normalized)
    xyz_spec = np.dot(trans_mat, lms_spec)  # initialise for in-place editing
    xyz_spec = significant_figures(xyz_spec, xyz_signfig)
    cc_spec = np.array([xyz_spec[0, :] /
                        (xyz_spec[0, :] + xyz_spec[1, :] + xyz_spec[2, :]),
                        xyz_spec[1, :] /
                        (xyz_spec[0, :] + xyz_spec[1, :] + xyz_spec[2, :]),
                        xyz_spec[2, :] /
                        (xyz_spec[0, :] + xyz_spec[1, :] +
                         xyz_spec[2, :])])  # ditto
    cc_spec = my_round(cc_spec, cc_dp)
    cc_white = np.sum(xyz_spec, 1)  # ditto
    cc_white = cc_white / np.sum(cc_white)
    cc_white = my_round(cc_white, cc_dp)

    # Normalized version
    trans_mat_N = trans_mat.copy()  # initialise for in-place editing
    if lambda_min != 390 or lambda_max != 830 or lambda_step != 1:
        xyz_spec_N = np.dot(trans_mat, lms_spec)
        trans_mat_N[0, :] = (trans_mat_N[0, :] * xyz_spec_N[1, :].sum() /
                             xyz_spec_N[0, :].sum())
        trans_mat_N[2, :] = (trans_mat_N[2, :] * xyz_spec_N[1, :].sum() /
                             xyz_spec_N[2, :].sum())
        trans_mat_N = my_round(trans_mat_N, mat_dp)
    xyz_spec_N = np.dot(trans_mat_N, lms_spec)  # ditto
    xyz_spec_N = significant_figures(xyz_spec_N, xyz_signfig)
    cc_spec_N = np.array([xyz_spec_N[0, :] /
                          (xyz_spec_N[0, :] + xyz_spec_N[1, :] +
                           xyz_spec_N[2, :]),
                          xyz_spec_N[1, :] /
                          (xyz_spec_N[0, :] + xyz_spec_N[1, :] +
                           xyz_spec_N[2, :]),
                          xyz_spec_N[2, :] /
                          (xyz_spec_N[0, :] + xyz_spec_N[1, :] +
                           xyz_spec_N[2, :])])  # ditto
    cc_spec_N = my_round(cc_spec_N, cc_dp)
    cc_white_N = np.sum(xyz_spec_N, 1)  # ditto
    cc_white_N = cc_white_N / np.sum(cc_white_N)
    cc_white_N = my_round(cc_white_N, cc_dp)

    # Reshape -- heavy reuse of variables, see comment on code
    # conventions on the top
    lms_spec = np.concatenate(
        (lambdas_spec.reshape((1, len(lambdas_spec))), lms_spec)).T
    lms_standard_spec = np.concatenate(
        (lambdas_spec.reshape((1, len(lambdas_spec))),
         lms_standard_spec)).T
    xyz_spec = np.concatenate(
        (lambdas_spec.reshape((1, len(lambdas_spec))), xyz_spec)).T
    xyz_spec_N = np.concatenate(
        (lambdas_spec.reshape((1, len(lambdas_spec))), xyz_spec_N)).T
    cc_spec = np.concatenate(
        (lambdas_spec.reshape((1, len(lambdas_spec))), cc_spec)).T
    cc_spec_N = np.concatenate(
        (lambdas_spec.reshape((1, len(lambdas_spec))), cc_spec_N)).T
    cc_spec[cc_spec <= 0] = 0
    cc_spec_N[cc_spec_N <= 0] = 0
    Vl = np.concatenate((lambdas_spec.reshape((1, len(lambdas_spec))),
                         v_spec.reshape((1, len(v_spec))))).T

    # Versions for plotting and purple line
    plots['xyz'] = np.dot(trans_mat, plots['lms'][:, 1:].T)
    plots['xyz'] = significant_figures(plots['xyz'], xyz_signfig)
    plots['xy'] = np.array([plots['xyz'][0, :] /
                            (plots['xyz'][0, :] +
                             plots['xyz'][1, :] +
                             plots['xyz'][2, :]),
                            plots['xyz'][1, :] /
                            (plots['xyz'][0, :] +
                             plots['xyz'][1, :] +
                             plots['xyz'][2, :]),
                            plots['xyz'][2, :] /
                            (plots['xyz'][0, :] +
                             plots['xyz'][1, :] +
                             plots['xyz'][2, :])])
    plots['xyz'] = np.concatenate(
        (np.array([plots['lms'][:, 0]]).T, plots['xyz'].T), axis=1)
    plots['xy'] = np.concatenate(
        (np.array([plots['lms'][:, 0]]).T, plots['xy'].T), axis=1)

    # Normalized versions for plotting and purple line
    plots['xyz_N'] = np.dot(trans_mat_N, plots['lms'][:, 1:].T)
    plots['xyz_N'] = significant_figures(plots['xyz_N'], xyz_signfig)
    plots['xy_N'] = np.array([plots['xyz_N'][0, :] /
                              (plots['xyz_N'][0, :] +
                               plots['xyz_N'][1, :] +
                               plots['xyz_N'][2, :]),
                              plots['xyz_N'][1, :] /
                              (plots['xyz_N'][0, :] +
                               plots['xyz_N'][1, :] +
                               plots['xyz_N'][2, :]),
                              plots['xyz_N'][2, :] /
                              (plots['xyz_N'][0, :] +
                               plots['xyz_N'][1, :] +
                               plots['xyz_N'][2, :])])
    plots['xyz_N'] = np.concatenate(
        (np.array([plots['lms'][:, 0]]).T, plots['xyz_N'].T), axis=1)
    plots['xy_N'] = np.concatenate(
        (np.array([plots['lms'][:, 0]]).T, plots['xy_N'].T), axis=1)

    # MacLeod-Boynton -- heavy reuse of variables, see comment on code
    # conventions on the top
    mb_spec = lms_spec.copy()
    mb_spec[:, 1] = trans_mat[1, 0] * lms_spec[:, 1] / Vl[:, 1]
    mb_spec[:, 2] = trans_mat[1, 1] * lms_spec[:, 2] / Vl[:, 1]
    mb_spec[:, 3] = lms_spec[:, 3] / Vl[:, 1]
    mb_spec[:, 3] = mb_spec[:, 3] / mb_s_max
    mb_spec[:, 1:] = my_round(mb_spec[:, 1:], mb_dp)
    mb_spec[mb_spec <= 0] = 0

    # Version for plotting and purple line
    plots['mb'] = plots['lms'].copy()
    plots['mb'][:, 1] = (trans_mat[1, 0] * plots['lms'][:, 1] /
                         plots['xyz'][:, 2])
    plots['mb'][:, 2] = (trans_mat[1, 1] * plots['lms'][:, 2] /
                         plots['xyz'][:, 2])
    plots['mb'][:, 3] = plots['lms'][:, 3] / plots['xyz'][:, 2]
    plots['mb'][:, 3] = plots['mb'][:, 3] / mb_s_max

    L_E = trans_mat[1, 0] * np.sum(lms_spec[:, 1])
    M_E = trans_mat[1, 1] * np.sum(lms_spec[:, 2])
    S_E = np.sum(lms_spec[:, 3]) / mb_s_max

    mb_white = np.array([L_E / (L_E + M_E),
                         M_E / (L_E + M_E),
                         S_E / (L_E + M_E)])
    mb_white = my_round(mb_white, mb_dp)

    # Maxwellian lm diagram
    if lm_dp > 5:
        lms_N = lms_spec.copy()
    else:
        lms_N = lms_standard_spec.copy()
    lms_N_inv = 1. / np.sum(lms_N[:, 1:], 0)
    lms_N[:, 1:] = lms_N[:, 1:] * lms_N_inv
    lm_spec = lms_N.copy()
    lm_spec[:, 1] = lms_N[:, 1] / (lms_N[:, 1] + lms_N[:, 2] + lms_N[:, 3])
    lm_spec[:, 2] = lms_N[:, 2] / (lms_N[:, 1] + lms_N[:, 2] + lms_N[:, 3])
    lm_spec[:, 3] = lms_N[:, 3] / (lms_N[:, 1] + lms_N[:, 2] + lms_N[:, 3])
    lm_spec[:, 1:] = my_round(lm_spec[:, 1:], lm_dp)
    lm_spec[lm_spec <= 0] = 0
    lm_white = np.sum(lms_N[:, 1:], 0)
    lm_white = lm_white / np.sum(lm_white)
    lm_white = my_round(lm_white, lm_dp)

    # Version for plotting and purple line
    plots['lm'] = plots['lms'].copy()
    lms_N_fine = plots['lms'].copy()
    if lm_dp <= 5:
        lms_N_fine[:, 1:] = significant_figures(lms_N_fine[:, 1:], lms_signfig)
    lms_N_fine[:, 1:] = lms_N_fine[:, 1:] / np.sum(lms_N[:, 1:], 0)
    plots['lm'][:, 1] = lms_N_fine[:, 1] / (lms_N_fine[:, 1] +
                                            lms_N_fine[:, 2] +
                                            lms_N_fine[:, 3])
    plots['lm'][:, 2] = lms_N_fine[:, 2] / (lms_N_fine[:, 1] +
                                            lms_N_fine[:, 2] +
                                            lms_N_fine[:, 3])
    plots['lm'][:, 3] = lms_N_fine[:, 3] / (lms_N_fine[:, 1] +
                                            lms_N_fine[:, 2] +
                                            lms_N_fine[:, 3])

    # Compute purple line for cc
    delaunay = Delaunay(plots['xy'][:, 1:3])
    ind = np.argmax(np.abs(
        delaunay.convex_hull[:, 0] - delaunay.convex_hull[:, 1]))
    purple_line_cc = np.zeros((2, 3))  # initialise for in-place editing
    purple_line_cc[0, 0] = plots['xy'][delaunay.convex_hull[ind, 0], 0]
    purple_line_cc[0, 1] = plots['xy'][delaunay.convex_hull[ind, 0], 1]
    purple_line_cc[0, 2] = plots['xy'][delaunay.convex_hull[ind, 0], 2]
    purple_line_cc[1, 0] = plots['xy'][delaunay.convex_hull[ind, 1], 0]
    purple_line_cc[1, 1] = plots['xy'][delaunay.convex_hull[ind, 1], 1]
    purple_line_cc[1, 2] = plots['xy'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_cc'] = purple_line_cc.copy()
    purple_line_cc[:, 1:] = my_round(purple_line_cc[:, 1:], cc_dp)

    purple_line_xyz = np.zeros((2, 4))  # initialise for in-place editing
    purple_line_xyz[0, 0] = plots['xyz'][delaunay.convex_hull[ind, 0], 0]
    purple_line_xyz[0, 1] = plots['xyz'][delaunay.convex_hull[ind, 0], 1]
    purple_line_xyz[0, 2] = plots['xyz'][delaunay.convex_hull[ind, 0], 2]
    purple_line_xyz[0, 3] = plots['xyz'][delaunay.convex_hull[ind, 0], 3]
    purple_line_xyz[1, 0] = plots['xyz'][delaunay.convex_hull[ind, 1], 0]
    purple_line_xyz[1, 1] = plots['xyz'][delaunay.convex_hull[ind, 1], 1]
    purple_line_xyz[1, 2] = plots['xyz'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_xyz'] = purple_line_xyz.copy()
    purple_line_xyz[:, 1:] = significant_figures(purple_line_xyz[:, 1:],
                                                 xyz_signfig)
    purple_line_xyz[:, 0] = my_round(purple_line_xyz[:, 0], 1)

    # Compute purple line for normalized cc
    delaunay = Delaunay(plots['xy_N'][:, 1:3])
    ind = np.argmax(np.abs(
        delaunay.convex_hull[:, 0] - delaunay.convex_hull[:, 1]))
    purple_line_cc_N = np.zeros((2, 3))  # initialise for in-place editing
    purple_line_cc_N[0, 0] = plots['xy_N'][delaunay.convex_hull[ind, 0], 0]
    purple_line_cc_N[0, 1] = plots['xy_N'][delaunay.convex_hull[ind, 0], 1]
    purple_line_cc_N[0, 2] = plots['xy_N'][delaunay.convex_hull[ind, 0], 2]
    purple_line_cc_N[1, 0] = plots['xy_N'][delaunay.convex_hull[ind, 1], 0]
    purple_line_cc_N[1, 1] = plots['xy_N'][delaunay.convex_hull[ind, 1], 1]
    purple_line_cc_N[1, 2] = plots['xy_N'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_cc_N'] = purple_line_cc_N.copy()
    purple_line_cc_N[:, 1:] = my_round(purple_line_cc_N[:, 1:], cc_dp)

    purple_line_xyz_N = np.zeros((2, 4))  # initialise for in-place editing
    purple_line_xyz_N[0, 0] = plots['xyz_N'][delaunay.convex_hull[ind, 0], 0]
    purple_line_xyz_N[0, 1] = plots['xyz_N'][delaunay.convex_hull[ind, 0], 1]
    purple_line_xyz_N[0, 2] = plots['xyz_N'][delaunay.convex_hull[ind, 0], 2]
    purple_line_xyz_N[0, 3] = plots['xyz_N'][delaunay.convex_hull[ind, 0], 3]
    purple_line_xyz_N[1, 0] = plots['xyz_N'][delaunay.convex_hull[ind, 1], 0]
    purple_line_xyz_N[1, 1] = plots['xyz_N'][delaunay.convex_hull[ind, 1], 1]
    purple_line_xyz_N[1, 2] = plots['xyz_N'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_xyz_N'] = purple_line_xyz_N.copy()
    purple_line_xyz_N[:, 1:] = significant_figures(purple_line_xyz_N[:, 1:],
                                                   xyz_signfig)
    purple_line_xyz_N[:, 0] = my_round(purple_line_xyz_N[:, 0], 1)

    # Compute purple line for mb
    delaunay = Delaunay(plots['mb'][:, 1:4:2])
    ind = np.argmax(np.abs(
        delaunay.convex_hull[:, 0] - delaunay.convex_hull[:, 1]))
    purple_line_mb = np.zeros((2, 3))  # initialise for in-place editing
    purple_line_mb[0, 0] = plots['mb'][delaunay.convex_hull[ind, 0], 0]
    purple_line_mb[0, 1] = plots['mb'][delaunay.convex_hull[ind, 0], 1]
    purple_line_mb[0, 2] = plots['mb'][delaunay.convex_hull[ind, 0], 3]
    purple_line_mb[1, 0] = plots['mb'][delaunay.convex_hull[ind, 1], 0]
    purple_line_mb[1, 1] = plots['mb'][delaunay.convex_hull[ind, 1], 1]
    purple_line_mb[1, 2] = plots['mb'][delaunay.convex_hull[ind, 1], 3]
    plots['purple_line_mb'] = purple_line_mb.copy()
    purple_line_mb[:, 1:] = my_round(purple_line_mb[:, 1:], mb_dp)

    # Hack to report correct wavelength also for the chromaticity diagram
    # (they give the same value anyway)
    # Could (should?) be removed at a later stage

    # Edit: they don't always give the same value proved by example:
    # fs: 10 degrees, age: 60 years, step = 1nm

    # if ( purple_line_cc[1,0] != purple_line_mb[1,0] ):
    #     print('Wavelengths differ!')
    #     purple_line_cc[1,0] = purple_line_mb[1,0]

    # Compute purple line for lm
    delaunay = Delaunay(plots['lm'][:, 1:3])
    ind = np.argmax(np.abs(
        delaunay.convex_hull[:, 0] - delaunay.convex_hull[:, 1]))
    purple_line_lm = np.zeros((2, 3))
    purple_line_lm[0, 0] = plots['lm'][delaunay.convex_hull[ind, 0], 0]
    purple_line_lm[0, 1] = plots['lm'][delaunay.convex_hull[ind, 0], 1]
    purple_line_lm[0, 2] = plots['lm'][delaunay.convex_hull[ind, 0], 2]
    purple_line_lm[1, 0] = plots['lm'][delaunay.convex_hull[ind, 1], 0]
    purple_line_lm[1, 1] = plots['lm'][delaunay.convex_hull[ind, 1], 1]
    purple_line_lm[1, 2] = plots['lm'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_lm'] = purple_line_lm.copy()
    purple_line_lm[:, 1:] = my_round(purple_line_lm[:, 1:], lm_dp)

    # Add CIE standards to plot data structure
    plots['xyz31'] = VisualData.xyz31.copy()
    plots['xyz64'] = VisualData.xyz64.copy()
    plots['xy31'] = my_round(VisualData.cc31, 5)
    plots['xy64'] = my_round(VisualData.cc64, 5)

    # Compute purple line for CIE standard cc
    delaunay = Delaunay(plots['xy31'][:, 1:3])
    ind = np.argmax(np.abs(
        delaunay.convex_hull[:, 0] - delaunay.convex_hull[:, 1]))
    purple_line_cc31 = np.zeros((2, 3))  # initialise for in-place editing
    purple_line_cc31[0, 0] = plots['xy31'][delaunay.convex_hull[ind, 0], 0]
    purple_line_cc31[0, 1] = plots['xy31'][delaunay.convex_hull[ind, 0], 1]
    purple_line_cc31[0, 2] = plots['xy31'][delaunay.convex_hull[ind, 0], 2]
    purple_line_cc31[1, 0] = plots['xy31'][delaunay.convex_hull[ind, 1], 0]
    purple_line_cc31[1, 1] = plots['xy31'][delaunay.convex_hull[ind, 1], 1]
    purple_line_cc31[1, 2] = plots['xy31'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_cc31'] = purple_line_cc31.copy()

    delaunay = Delaunay(plots['xy64'][:, 1:3])
    ind = np.argmax(np.abs(
        delaunay.convex_hull[:, 0] - delaunay.convex_hull[:, 1]))
    purple_line_cc64 = np.zeros((2, 3))  # initialise for in-place editing
    purple_line_cc64[0, 0] = plots['xy64'][delaunay.convex_hull[ind, 0], 0]
    purple_line_cc64[0, 1] = plots['xy64'][delaunay.convex_hull[ind, 0], 1]
    purple_line_cc64[0, 2] = plots['xy64'][delaunay.convex_hull[ind, 0], 2]
    purple_line_cc64[1, 0] = plots['xy64'][delaunay.convex_hull[ind, 1], 0]
    purple_line_cc64[1, 1] = plots['xy64'][delaunay.convex_hull[ind, 1], 1]
    purple_line_cc64[1, 2] = plots['xy64'][delaunay.convex_hull[ind, 1], 2]
    plots['purple_line_cc64'] = purple_line_cc64.copy()

    if field_size == np.round(field_size):
        plots['field_size'] = '%.0f' % field_size
    else:
        plots['field_size'] = '%.1f' % field_size
    plots['age'] = age
    plots['lambda_min'] = lambda_min
    plots['lambda_max'] = lambda_max
    plots['lambda_step'] = lambda_step
    plots['xy_white'] = cc_white
    plots['xy_white_N'] = cc_white_N
    plots['mb_white'] = mb_white
    plots['lm_white'] = lm_white

    # Stack all the results in a dict() for return
    results = dict()
    results['xyz'] = chop(xyz_spec)
    results['xyz_N'] = chop(xyz_spec_N)
    results['xy'] = chop(cc_spec)
    results['xy_N'] = chop(cc_spec_N)
    results['xy_white'] = chop(cc_white)
    results['xy_white_N'] = chop(cc_white_N)
    results['trans_mat'] = chop(trans_mat)
    results['trans_mat_N'] = chop(trans_mat_N)
    results['lms'] = chop(lms_standard_spec)
    results['lms_base'] = chop(lms_spec)
    results['mb'] = chop(mb_spec)
    results['mb_white'] = chop(mb_white)
    results['lm'] = chop(lm_spec)
    results['lm_white'] = chop(lm_white)
    results['lambda_ref_min'] = lambda_x_min_ref
    results['purple_line_cc'] = chop(purple_line_cc)
    results['purple_line_cc_N'] = chop(purple_line_cc_N)
    results['purple_line_xyz'] = chop(purple_line_xyz)
    results['purple_line_xyz_N'] = chop(purple_line_xyz_N)
    results['purple_line_cc31'] = chop(plots['purple_line_cc31'])
    results['purple_line_cc64'] = chop(plots['purple_line_cc64'])
    results['purple_line_lm'] = chop(purple_line_lm)
    results['purple_line_mb'] = chop(purple_line_mb)
    results['age'] = chop(age)
    results['xyz31'] = chop(VisualData.xyz31.copy())
    results['xyz64'] = chop(VisualData.xyz64.copy())
    results['xy31'] = chop(my_round(VisualData.cc31, 5))
    results['xy64'] = chop(my_round(VisualData.cc64, 5))
    results['mb_s_max'] = mb_s_max
    results['lms_N_inv'] = lms_N_inv

    # Add tristimulus values for purple-line stimuli
    results['purple_xyz'] = compute_xyz_purples(results['xy'],
                                               results['purple_line_xyz'],
                                               results['xy_white'])
    results['purple_xyz_N'] = compute_xyz_purples(results['xy_N'],
                                                 results['purple_line_xyz_N'],
                                                 results['xy_white_N'])
    plots['purple_xyz'] = compute_xyz_purples(plots['xy'],
                                             plots['purple_line_xyz'],
                                             plots['xy_white'])
    plots['purple_xyz_N'] = compute_xyz_purples(plots['xy_N'],
                                               plots['purple_line_xyz_N'],
                                               plots['xy_white_N'])

    # Add chromaticity coordinates for purple-line stimuli
    results['purple_cc'] = compute_cc_purples(results['purple_xyz'])
    results['purple_cc_N'] = compute_cc_purples(results['purple_xyz_N'])
    plots['purple_cc'] = compute_cc_purples(plots['purple_xyz'])
    plots['purple_cc_N'] = compute_cc_purples(plots['purple_xyz_N'])

    # Format string representations
    if np.round(field_size, 5) == np.round(field_size):
        results['field_size'] = '%.0f' % field_size
    else:
        results['field_size'] = '%.1f' % field_size
    if (np.round(lambda_step, 5) == np.round(lambda_step) and
            np.round(lambda_min, 5) == np.round(lambda_min) and
            np.round(lambda_max, 5) == np.round(lambda_max)):
        results['lambda_min'] = '%.0f' % lambda_min
        results['lambda_max'] = '%.0f' % lambda_max
        results['lambda_purple_min'] = '%.0f' % results['purple_xyz'][0, 0]
        results['lambda_purple_max'] = '%.0f' % results['purple_xyz'][-1, 0]
        results['lambda_step'] = '%.0f' % lambda_step
        results['lambda_purple_min_N'] = '%.0f' % results['purple_xyz_N'][0, 0]
        results['lambda_purple_max_N'] = ('%.0f' %
                                          results['purple_xyz_N'][-1, 0])
        plots['lambda_min'] = '%.0f' % lambda_min
        plots['lambda_max'] = '%.0f' % lambda_max
        plots['lambda_purple_min'] = '%.0f' % plots['purple_xyz'][0, 0]
        plots['lambda_purple_max'] = '%.0f' % plots['purple_xyz'][-1, 0]
        plots['lambda_purple_min_N'] = '%.0f' % plots['purple_xyz_N'][0, 0]
        plots['lambda_purple_max_N'] = '%.0f' % plots['purple_xyz_N'][-1, 0]
        plots['lambda_step'] = '%.0f' % lambda_step
    else:
        results['lambda_min'] = '%.1f' % lambda_min
        results['lambda_max'] = '%.1f' % lambda_max
        results['lambda_step'] = '%.1f' % lambda_step
        results['lambda_purple_min'] = '%.1f' % results['purple_xyz'][0, 0]
        results['lambda_purple_max'] = '%.1f' % results['purple_xyz'][-1, 0]
        results['lambda_purple_min_N'] = '%.1f' % results['purple_xyz_N'][0, 0]
        results['lambda_purple_max_N'] = ('%.1f' %
                                          results['purple_xyz_N'][-1, 0])
        plots['lambda_min'] = '%.1f' % lambda_min
        plots['lambda_max'] = '%.1f' % lambda_max
        plots['lambda_purple_min'] = '%.1f' % plots['purple_xyz'][0, 0]
        plots['lambda_purple_max'] = '%.1f' % plots['purple_xyz'][-1, 0]
        plots['lambda_purple_min_N'] = '%.1f' % plots['purple_xyz_N'][0, 0]
        plots['lambda_purple_max_N'] = '%.1f' % plots['purple_xyz_N'][-1, 0]
        plots['lambda_step'] = '%.1f' % lambda_step

    return results, plots


#==============================================================================
# For testing purposes only
#==============================================================================

if __name__ == '__main__':
    res, plots = compute_tabulated(2, 32, 390, 830, .1)
    print(res['purple_xyz_N'])
