#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ciefunctions: GUI application for the calculation of the CIE
              cone-fundamental-based colorimetric functions provided
              by CIE TC 1-97.

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

import tc1_97
import tc1_97.description
import tc1_97.plot
import tc1_97.table
from tc1_97.utils import resource_path
import sys
import os
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg \
    import NavigationToolbar2QT \
    as NavigationToolbar
from matplotlib.figure import Figure


class AppForm(QtWidgets.QMainWindow):
    """
    The main application window.
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        QtWidgets.QWidget.move(self, 0, 0)
        self.setWindowTitle(' CIE Functions')
        self.create_menu()
        self.create_main_frame()
        self.on_compute()

    def save_table(self):
        file_choices = "CSV (*.csv)|*.csv"

        pre = ''
        post = ''
        if self.plot_combo.currentIndex() == self.COMBO_LMS:
            pre = 'cie2006_lms'
        elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:
            pre = 'cie2006_lms_9figs'
        elif self.plot_combo.currentIndex() == self.COMBO_MB:
            pre = 'macleod_boynton_cc'
        elif self.plot_combo.currentIndex() == self.COMBO_LM:
            pre = 'maxwellian_cc'
        elif self.plot_combo.currentIndex() == self.COMBO_XYZ:
            pre = 'cie_xyz_F'
        elif self.plot_combo.currentIndex() == self.COMBO_XY:
            pre = 'cie_cc_F'
        elif self.plot_combo.currentIndex() == self.COMBO_PURPLE_XYZ:
            pre = 'purple_xyz_F'
        elif self.plot_combo.currentIndex() == self.COMBO_PURPLE_XY:
            pre = 'purple_cc_F'

        if ((self.plot_combo.currentIndex() in [self.COMBO_LMS,
                                                self.COMBO_LMSBASE]) and
                self.log_check.isChecked()):
            post = '__logarithmic_values'

        elif (self.plot_combo.currentIndex() == self.COMBO_LM or
              ((self.plot_combo.currentIndex() in [self.COMBO_XYZ,
                                                   self.COMBO_XY,
                                                   self.COMBO_PURPLE_XYZ,
                                                   self.COMBO_PURPLE_XY]) and
                self.norm_check.isChecked())):
            post = '__renormalized_values'

        if ((self.plot_combo.currentIndex() == self.COMBO_XYZSTD) and
                (self.field_combo.currentIndex() == self.STD_31)):
            suggest = 'cie_xyz__standard1931__fs_2.csv'
        elif (self.plot_combo.currentIndex() == self.COMBO_XYZSTD and
              self.field_combo.currentIndex() == self.STD_64):
            suggest = 'cie_xyz__standard1964__fs_10.csv'
        elif (self.plot_combo.currentIndex() == self.COMBO_XYSTD and
              self.field_combo.currentIndex() == self.STD_31):
            suggest = 'cie_cc__standard1931__fs_2.csv'
        elif (self.plot_combo.currentIndex() == self.COMBO_XYSTD and
              self.field_combo.currentIndex() == self.STD_64):
            suggest = 'cie_cc__standard1964__fs_10.csv'
        else:
            suggest = (pre + '__fs_' + str(self.field_spin.value()) +
                       '__age_' + str(self.age_spin.value()) +
                       '__domain_' + str(self.lambda_min_spin.value()) +
                       '-' + str(self.lambda_max_spin.value()) +
                       '__step_' + str(self.resolution_spin.value()) +
                       post + '.csv')

        path = QtWidgets.QFileDialog.getSaveFileName(self,
                                                     'Save file', suggest,
                                                     file_choices)[0]

        if path:
            if self.plot_combo.currentIndex() == self.COMBO_LMS:
                if self.log_check.isChecked():
                    np.savetxt(path, self.results['logLMS'],
                               '%.1f, %.5f, %.5f, %.5f')
                else:
                    np.savetxt(path, self.results['LMS'],
                               '%.1f, %.5e, %.5e, %.5e')
            elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:
                if self.log_check.isChecked():
                    np.savetxt(path, self.results['logLMS_base'],
                               '%.1f, %.8f, %.8f, %.8f')
                else:
                    np.savetxt(path, self.results['LMS_base'],
                               '%.1f, %.8e, %.8e, %.8e')
            elif self.plot_combo.currentIndex() == self.COMBO_MB:
                np.savetxt(path, self.results['lms_mb'],
                           '%.1f, %.6f, %.6f, %.6f')
            elif self.plot_combo.currentIndex() == self.COMBO_LM:
                np.savetxt(path, self.results['lms_mw'],
                           '%.1f, %.6f, %.6f, %.6f')
            elif self.plot_combo.currentIndex() == self.COMBO_XYZ:
                if self.norm_check.isChecked():
                    np.savetxt(path, self.results['XYZ_N'],
                               '%.1f, %.6e, %.6e, %.6e')
                else:
                    np.savetxt(path, self.results['XYZ'],
                               '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == self.COMBO_XY:
                if self.norm_check.isChecked():
                    np.savetxt(path, self.results['xyz_N'],
                               '%.1f, %.5f, %.5f, %.5f')
                else:
                    np.savetxt(path, self.results['xyz'],
                               '%.1f, %.5f, %.5f, %.5f')
            elif self.plot_combo.currentIndex() == self.COMBO_PURPLE_XYZ:
                if self.norm_check.isChecked():
                    np.savetxt(path, self.results['XYZ_purples_N'],
                               '%.1f, %.6e, %.6e, %.6e')
                else:
                    np.savetxt(path, self.results['XYZ_purple'],
                               '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == self.COMBO_PURPLE_XY:
                if self.norm_check.isChecked():
                    np.savetxt(path, self.results['xyz_purples_N'],
                               '%.1f, %.5f, %.5f, %.5f')
                else:
                    np.savetxt(path, self.results['xyz_purples'],
                               '%.1f, %.5f, %.5f, %.5f')
            elif self.plot_combo.currentIndex() == self.COMBO_XYZSTD:
                if self.field_combo.currentIndex() == self.STD_31:
                    np.savetxt(path, self.results['XYZ31'],
                               '%.1f, %.6e, %.6e, %.6e')
                else:
                    np.savetxt(path, self.results['XYZ64'],
                               '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == self.COMBO_XYSTD:
                if self.field_combo.currentIndex() == self.STD_31:
                    np.savetxt(path, self.results['xyz31'],
                               '%.1f, %.5f, %.5f, %.5f')
                else:
                    np.savetxt(path, self.results['xyz64'],
                               '%.1f, %.5f, %.5f, %.5f')

    def options(self):
        """
        Return a dict() with the current plot options for the plot module.
        """
        return {'grid': self.grid_check.isChecked(),
                'cie31': self.cie31_check.isChecked(),
                'cie64': self.cie64_check.isChecked(),
                'labels': self.wavelength_check.isChecked(),
                'log10': self.log_check.isChecked(),
                'norm': self.norm_check.isChecked(),
                'label_fontsize': 7,
                'title_fontsize': 10.5,
                'full_title': True,
                'axis_labels': True}

    def on_about(self):
        msg = """
CIE Functions:  Calculates the CIE cone-fundamental-based colorimetric \
functions according to CIE TC 1-97.

Copyright (C) 2012-2017 Ivar Farup and Jan Henrik Wold

This program is free software: you can redistribute it and/or modify it \
under the terms of the GNU General Public License as published by the \
Free Software Foundation, either version 3 of the License, or (at your \
option) any later version.

This program is distributed in the hope that it will be useful, but \
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY \
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License \
for more details.

You should have received a copy of the GNU General Public License along \
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
        QtWidgets.QMessageBox.about(self, "About CIE Functions", msg.strip())

    def on_grid(self):
        self.axes.grid(self.grid_check.isChecked())
        self.canvas.draw()

    def on_draw(self, redraw_description=True):

        # Reset GUI values that have not been computed
        self.field_spin.setValue(self.last_field)
        self.age_spin.setValue(self.last_age)
        self.lambda_min_spin.setValue(self.last_lambda_min)
        self.lambda_max_spin.setValue(self.last_lambda_max)
        self.resolution_spin.setValue(self.last_resolution)
        self.mpl_toolbar.update()  # reset the views history (fixes #124)

        if self.plot_combo.currentIndex() not in \
           [self.COMBO_XYSTD, self.COMBO_XYZSTD]:
            self.field_spin.show()
            self.field_combo.hide()
            self.age_label.show()
            self.age_spin.show()
            self.resolution_label.show()
            self.resolution_spin.show()
            self.compute_button.show()
            self.lambda_min_max_label.show()
            self.lambda_min_max_dash.show()
            self.lambda_min_spin.show()
            self.lambda_max_spin.show()
        else:
            self.field_spin.hide()
            self.field_combo.show()
            self.age_label.hide()
            self.age_spin.hide()
            self.resolution_label.hide()
            self.resolution_spin.hide()
            self.compute_button.hide()
            self.lambda_min_max_label.hide()
            self.lambda_min_max_dash.hide()
            self.lambda_min_spin.hide()
            self.lambda_max_spin.hide()

        if self.plot_combo.currentIndex() in [self.COMBO_LMS,
                                              self.COMBO_LMSBASE]:
            self.norm_label.setVisible(False)
            self.norm_check.setVisible(False)
            self.log_label.setVisible(True)
            self.log_check.setVisible(True)
        elif self.plot_combo.currentIndex() == self.COMBO_LM:
            self.log_label.setVisible(False)
            self.log_check.setVisible(False)
            self.norm_check.setVisible(False)
            self.norm_label.setVisible(True)
        elif self.plot_combo.currentIndex() in [self.COMBO_XYZ,
                                                self.COMBO_XY,
                                                self.COMBO_PURPLE_XYZ,
                                                self.COMBO_PURPLE_XY]:
            self.log_label.setVisible(False)
            self.log_check.setVisible(False)
            self.norm_label.setVisible(True)
            self.norm_check.setVisible(True)
        else:
            self.log_label.setVisible(False)
            self.log_check.setVisible(False)
            self.norm_label.setVisible(False)
            self.norm_check.setVisible(False)

        #
        # CIE LMS cone fundamentals
        # (description, plot and table)
        #
        if self.plot_combo.currentIndex() == self.COMBO_LMS:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create html description
            html_string = tc1_97.description.LMS(self.results,
                                                 self.plot_combo.currentText(),
                                                 self.options(), True)
            # Create plot
            tc1_97.plot.LMS(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.LMS(self.results, self.options(), True)

        #
        # CIE LMS cone fundamentals (9 sign. figs.)
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create html description
            html_string = tc1_97.description.LMS_base(
                self.results,
                self.plot_combo.currentText(),
                self.options(), True)

            # Create plot
            tc1_97.plot.LMS_base(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.LMS_base(self.results,
                                               self.options(), True)

        #
        # MacLeod-Boynton ls chromaticity diagram
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_MB:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create html description
            html_string = tc1_97.description.lms_mb(
                    self.results,
                    self.plot_combo.currentText(),
                    self.options(), True)

            # Create plot
            tc1_97.plot.lms_mb(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.lms_mb(self.results,
                                             self.options(), True)

        #
        # Maxwellian lm chromaticity diagram
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_LM:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create html description
            html_string = tc1_97.description.lms_mw(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

            # Create plot
            tc1_97.plot.lm_mw(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.lms_mw(
                    self.results, self.options(), True)

        #
        # CIE XYZ cone-fundamental-based tristimulus functions
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYZ:

            # Setup GUI
            self.compare_label_31.setEnabled(True)
            self.compare_label_64.setEnabled(True)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setEnabled(True)
            self.cie64_check.setEnabled(True)

            # Create html description
            html_string = tc1_97.description.XYZ(self.results,
                                                 self.plot_combo.currentText(),
                                                 self.options(), True)

            # Create plot
            tc1_97.plot.XYZ(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.XYZ(self.results, self.options(), True)

        #
        # CIE xy cone-fundamental-based chromaticity diagram
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XY:
            # Setup GUI
            self.compare_label_31.setEnabled(True)
            self.compare_label_64.setEnabled(True)
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            self.cie31_check.setEnabled(True)
            self.cie64_check.setEnabled(True)

            # Create html description
            html_string = tc1_97.description.xyz(self.results,
                                                 self.plot_combo.currentText(),
                                                 self.options(), True)

            # Create plot
            tc1_97.plot.xy(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.xyz(self.results, self.options(), True)

        #
        # XYZ cone-fundamental-based tristimulus functions for
        # purple-line stimuli (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_PURPLE_XYZ:

            # Setup GUI
            self.compare_label_31.setEnabled(False)
            self.compare_label_64.setEnabled(False)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setEnabled(False)
            self.cie64_check.setEnabled(False)

            # Create html descriptions
            html_string = tc1_97.description.XYZ_purples(
                self.results,
                self.plot_combo.currentText(),
                self.options(), True)

            # Create plot
            tc1_97.plot.XYZ_purples(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.XYZ_purples(self.results,
                                                  self.options(), True)

        #
        # xy cone-fundamental-based chromaticity diagram (purple-line stimuli)
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_PURPLE_XY:

            # Setup GUI
            self.compare_label_31.setEnabled(False)
            self.compare_label_64.setEnabled(False)
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            self.cie31_check.setEnabled(False)
            self.cie64_check.setEnabled(False)

            # Create html description
            html_string = tc1_97.description.xyz_purples(
                self.results,
                self.plot_combo.currentText(),
                self.options(), True)

            # Create plot
            tc1_97.plot.xy_purples(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc1_97.table.xyz_purples(self.results,
                                                  self.options(), True)

        #
        # CIE XYZ standard colour-matching functions
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYZSTD:

            # Setup GUI
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)

            if self.field_combo.currentIndex() == self.STD_31:

                # Setup GUI
                self.compare_label_31.setDisabled(True)
                self.compare_label_64.setEnabled(True)
                self.cie31_check.setDisabled(True)
                self.cie64_check.setEnabled(True)

                # Create html description
                html_string = tc1_97.description.XYZ31(
                    self.results,
                    self.plot_combo.currentText(),
                    self.options(), True)

                # Create plot
                tc1_97.plot.XYZ31(self.axes, self.plots, self.options())

                # Create html table
                html_table = tc1_97.table.XYZ31(self.results,
                                                self.options(), True)

            else:  # STD_64

                # Setup GUI
                self.compare_label_31.setEnabled(True)
                self.compare_label_64.setDisabled(True)
                self.cie31_check.setEnabled(True)
                self.cie64_check.setDisabled(True)

                # Create html description
                html_string = tc1_97.description.XYZ64(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

                # Create plot
                tc1_97.plot.XYZ64(self.axes, self.plots, self.options())

                # Create html table
                html_table = tc1_97.table.XYZ64(self.results,
                                                self.options(), True)

        #
        # CIE xy standard chromaticity diagrams
        # (description, plot and table)
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYSTD:

            # Setup GUI
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)

            if self.field_combo.currentIndex() == self.STD_31:

                # Setup GUI
                self.compare_label_31.setDisabled(True)
                self.compare_label_64.setEnabled(True)
                self.cie31_check.setDisabled(True)
                self.cie64_check.setEnabled(True)

                # Create html description
                html_string = tc1_97.description.xyz31(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

                # Create plot
                tc1_97.plot.xy31(self.axes, self.plots, self.options())

                # Create html table
                html_table = tc1_97.table.xyz31(self.results,
                                                self.options(), True)

            else:   # STD_64

                # Setup GUI
                self.compare_label_31.setEnabled(True)
                self.compare_label_64.setDisabled(True)
                self.cie31_check.setEnabled(True)
                self.cie64_check.setDisabled(True)

                # Create html description
                html_string = tc1_97.description.xyz64(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

                # Create plot
                tc1_97.plot.xy64(self.axes, self.plots, self.options())

                # Create html table
                html_table = tc1_97.table.xyz64(self.results,
                                                self.options(), True)

        #
        # Refresh GUI
        #
        base_url = QtCore.QUrl.fromLocalFile(os.getcwd() + os.sep)
        if redraw_description:
            self.transformation.setHtml(html_string, baseUrl=base_url)
            self.html_table.setHtml(html_table, baseUrl=base_url)
        self.canvas.draw()

    def on_draw_plot_only(self):
        self.on_draw(False)

    def on_draw_all(self):
        self.on_draw(True)

    def on_compute(self):
        if self.lambda_max_spin.value() < 700:
            self.lambda_max_spin.setValue(700)
        self.lambda_max_spin.setMinimum(700)
        self.last_age = self.age_spin.value()
        self.last_field = self.field_spin.value()
        self.last_resolution = tc1_97.my_round(self.resolution_spin.value(), 1)
        self.last_lambda_min = tc1_97.my_round(self.lambda_min_spin.value(), 1)
        self.last_lambda_max = tc1_97.my_round(self.lambda_max_spin.value(), 1)
        self.results, self.plots = tc1_97.compute_tabulated(
            self.last_field,
            self.last_age,
            self.last_lambda_min,
            self.last_lambda_max,
            self.last_resolution)
        if self.results['XYZ'][-1, 0] < 700:
            self.lambda_max_spin.setMinimum(self.results['XYZ'][-1, 0])
        if self.results['XYZ'][-1, 0] != self.last_lambda_max:
            self.last_lambda_max = self.results['XYZ'][-1, 0]
            self.lambda_max_spin.setValue(self.last_lambda_max)
        self.on_draw(True)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")
        quit_action = self.file_menu.addAction("&Quit")
        quit_action.triggered.connect(self.close)

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.help_menu.addAction("&About")
        about_action.triggered.connect(self.on_about)

    def create_main_frame(self):
        self.main_frame = QtWidgets.QWidget()

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((10.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        #
        self.field_spin = QtWidgets.QDoubleSpinBox()
        self.field_spin.setLocale(QtCore.QLocale('C'))
        self.field_spin.setMinimum(1)
        self.field_spin.setMaximum(10)
        self.field_spin.setDecimals(1)
        self.field_spin.setValue(2)
        self.field_spin.setSingleStep(0.1)

        self.field_combo = QtWidgets.QComboBox()
        self.field_combo.addItem(u'2\N{DEGREE SIGN} (1931)')
        self.STD_31 = 0
        self.field_combo.addItem(u'10\N{DEGREE SIGN} (1964)')
        self.STD_64 = 1
        self.field_combo.hide()
        self.field_combo.currentIndexChanged.connect(self.on_draw_all)

        self.age_spin = QtWidgets.QSpinBox()
        self.age_spin.setMinimum(20)
        self.age_spin.setMaximum(70)
        self.age_spin.setValue(32)

        self.lambda_min_spin = QtWidgets.QDoubleSpinBox()
        self.lambda_min_spin.setLocale(QtCore.QLocale('C'))
        self.lambda_min_spin.setMinimum(390)
        self.lambda_min_spin.setMaximum(400)
        self.lambda_min_spin.setDecimals(1)
        self.lambda_min_spin.setValue(390)
        self.lambda_min_spin.setSingleStep(0.1)

        self.lambda_max_spin = QtWidgets.QDoubleSpinBox()
        self.lambda_max_spin.setLocale(QtCore.QLocale('C'))
        self.lambda_max_spin.setMinimum(700)
        self.lambda_max_spin.setMaximum(830)
        self.lambda_max_spin.setDecimals(1)
        self.lambda_max_spin.setValue(830)
        self.lambda_max_spin.setSingleStep(0.1)

        self.resolution_spin = QtWidgets.QDoubleSpinBox()
        self.resolution_spin.setLocale(QtCore.QLocale('C'))
        self.resolution_spin.setMinimum(0.1)
        self.resolution_spin.setMaximum(5)
        self.resolution_spin.setDecimals(1)
        self.resolution_spin.setValue(1)
        self.resolution_spin.setSingleStep(0.1)

        self.plot_combo = QtWidgets.QComboBox()
        self.plot_combo.addItem('CIE LMS cone fundamentals')
        self.COMBO_LMS = 0
        self.plot_combo.addItem('CIE LMS cone fundamentals (9 sign. figs.)')
        self.COMBO_LMSBASE = 1
        self.plot_combo.addItem(
            u'MacLeod\u2013Boynton ls chromaticity diagram')
        self.COMBO_MB = 2
        self.plot_combo.addItem('Maxwellian lm chromaticity diagram')
        self.COMBO_LM = 3
        self.plot_combo.addItem(
            'CIE XYZ cone-fundamental-based tristimulus functions')
        self.COMBO_XYZ = 4
        self.plot_combo.addItem(
            'CIE xy cone-fundamental-based chromaticity diagram')
        self.COMBO_XY = 5
        self.plot_combo.addItem(
            'XYZ cone-fundamental-based tristimulus functions for ' +
            'purple-line stimuli')
        self.COMBO_PURPLE_XYZ = 6
        self.plot_combo.addItem(
            'xy cone-fundamental-based chromaticity diagram ' +
            '(purple-line stimuli)')
        self.COMBO_PURPLE_XY = 7
        self.plot_combo.addItem('CIE XYZ standard colour-matching functions')
        self.COMBO_XYZSTD = 8
        self.plot_combo.addItem('CIE xy standard chromaticity diagram')
        self.COMBO_XYSTD = 9
        self.plot_combo.currentIndexChanged.connect(self.on_draw_all)

        self.grid_check = QtWidgets.QCheckBox()
        self.grid_check.stateChanged.connect(self.on_grid)

        self.wavelength_check = QtWidgets.QCheckBox()
        self.wavelength_check.stateChanged.connect(self.on_draw_plot_only)

        self.cie31_check = QtWidgets.QCheckBox()
        self.cie31_check.stateChanged.connect(self.on_draw_plot_only)

        self.cie64_check = QtWidgets.QCheckBox()
        self.cie64_check.stateChanged.connect(self.on_draw_plot_only)

        self.norm_check = QtWidgets.QCheckBox()
        self.norm_check.stateChanged.connect(self.on_draw_all)

        self.log_check = QtWidgets.QCheckBox()
        self.log_check.stateChanged.connect(self.on_draw_all)

        self.save_table_button = QtWidgets.QPushButton('&Save table')
        self.save_table_button.clicked.connect(self.save_table)

        self.compute_button = QtWidgets.QPushButton('       &Compute       ')
        self.compute_button.clicked.connect(self.on_compute)

        self.transformation = QtWebEngineWidgets.QWebEngineView()
        self.html_table = QtWebEngineWidgets.QWebEngineView()

        # Layout with labels
        #
        self.compare_label_31 = QtWidgets.QLabel(
            u'Compare with CIE 1931 2\N{DEGREE SIGN}')
        self.compare_label_64 = QtWidgets.QLabel(
            u'Compare with CIE 1964 10\N{DEGREE SIGN}')
        self.grid_label = QtWidgets.QLabel('Grid')
        self.wavelength_label = QtWidgets.QLabel('Labels')
        self.norm_label = QtWidgets.QLabel(' Renormalized values  ')
        self.log_label = QtWidgets.QLabel(' Logarithmic values  ')
        self.field_label = QtWidgets.QLabel(u' Field size (\N{DEGREE SIGN})')
        self.age_label = QtWidgets.QLabel(' Age (yr)')
        self.lambda_min_max_label = QtWidgets.QLabel(' Domain (nm)')
        self.lambda_min_max_dash = QtWidgets.QLabel(u'\u2013')
        self.resolution_label = QtWidgets.QLabel(' Step (nm)')

        grid = QtWidgets.QGridLayout()
        grid.setRowMinimumHeight(0, 34)
        grid.addWidget(self.field_label, 0, 0, QtCore.Qt.AlignRight)
        grid.addWidget(self.age_label, 0, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.lambda_min_max_label, 0, 4, QtCore.Qt.AlignRight)
        grid.addWidget(self.lambda_min_max_dash, 0, 6)
        grid.addWidget(self.resolution_label, 0, 8, QtCore.Qt.AlignRight)
        grid.addWidget(QtWidgets.QLabel(''), 0, 10)

        grid.addWidget(self.field_spin, 0, 1)
        grid.addWidget(self.field_combo, 0, 1)
        grid.addWidget(self.age_spin, 0, 3)
        grid.addWidget(self.lambda_min_spin, 0, 5)
        grid.addWidget(self.lambda_max_spin, 0, 7)
        grid.addWidget(self.resolution_spin, 0, 9)
        grid.addWidget(self.compute_button, 0, 11)
        grid.setColumnStretch(2, 11)
        grid.setColumnStretch(4, 16)
        grid.setColumnStretch(8, 13)
        grid.setColumnStretch(10, 8)

        inner_vbox = QtWidgets.QVBoxLayout()
        inner_vbox.addWidget(self.mpl_toolbar)
        inner_vbox.addWidget(self.canvas)
        check_bar = QtWidgets.QGridLayout()
        check_bar.addWidget(self.compare_label_31, 0, 0, QtCore.Qt.AlignRight)
        check_bar.addWidget(self.cie31_check, 0, 1)
        check_bar.addWidget(QtWidgets.QLabel(''), 0, 2)
        check_bar.addWidget(self.compare_label_64, 0, 3, QtCore.Qt.AlignRight)
        check_bar.addWidget(self.cie64_check, 0, 4)
        check_bar.addWidget(self.grid_label, 0, 5, QtCore.Qt.AlignRight)
        check_bar.addWidget(self.grid_check, 0, 6)
        check_bar.addWidget(self.wavelength_label, 0, 7, QtCore.Qt.AlignRight)
        check_bar.addWidget(self.wavelength_check, 0, 8)
        check_bar.setColumnStretch(2, 8)
        check_bar.setColumnStretch(3, 16)
        check_bar.setColumnStretch(5, 14)
        check_bar.setColumnStretch(7, 16)

        check_widget = QtWidgets.QWidget()
        check_widget.setLayout(check_bar)
        inner_vbox.addWidget(check_widget)
        inner_widget = QtWidgets.QWidget()
        inner_widget.setLayout(inner_vbox)

        table_vbox = QtWidgets.QVBoxLayout()
        table_vbox.addWidget(self.html_table)
        table_vbox.addWidget(self.save_table_button)
        table_widget = QtWidgets.QWidget()
        table_widget.setLayout(table_vbox)

        spectral_tabs = QtWidgets.QTabWidget()
        spectral_tabs.addTab(inner_widget, 'Plot')
        spectral_tabs.addTab(table_widget, 'Table')

        combo_grid = QtWidgets.QGridLayout()
        combo_grid.addWidget(self.plot_combo, 0, 0)
        combo_grid.addWidget(QtWidgets.QLabel('   '), 0, 1)
        combo_grid.addWidget(self.norm_label, 0, 2, QtCore.Qt.AlignRight)
        combo_grid.addWidget(self.norm_check, 0, 3)
        combo_grid.addWidget(self.log_label, 0, 2, QtCore.Qt.AlignRight)
        combo_grid.addWidget(self.log_check, 0, 3)
        combo_grid.setColumnMinimumWidth(0, 650)
        combo_grid.setColumnMinimumWidth(2, 150)
        combo_grid.setColumnMinimumWidth(3, 20)
        combo_grid.setColumnStretch(0, 1)
        combo_grid.setSpacing(0)

        spectral_innerwidget = QtWidgets.QWidget()
        spectral_vbox = QtWidgets.QVBoxLayout(spectral_innerwidget)
        spectral_vbox.addWidget(spectral_tabs)
        spectral_vbox.addLayout(combo_grid)
        spectral_vbox.addLayout(grid)

        spectral_splitter = QtWidgets.QSplitter()
        spectral_splitter.addWidget(spectral_innerwidget)
        spectral_splitter.addWidget(self.transformation)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(spectral_splitter)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)


def main():
    """
    Run the CIE Functions application.
    """
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile(resource_path('icons/ciefunctions_icon (16x16) .png'),
                     QtCore.QSize(16, 16))
    app_icon.addFile(resource_path('icons/ciefunctions_icon (24x24) .png'),
                     QtCore.QSize(24, 24))
    app_icon.addFile(resource_path('icons/ciefunctions_icon (32x32) .png'),
                     QtCore.QSize(32, 32))
    app_icon.addFile(resource_path('icons/ciefunctions_icon (48x48) .png'),
                     QtCore.QSize(48, 48))
    app_icon.addFile(resource_path('icons/ciefunctions_icon (256x256) .png'),
                     QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
