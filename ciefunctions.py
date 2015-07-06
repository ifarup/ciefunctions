#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ciefunctions: GUI application for the calculation of CIE functions.

Copyright (C) 2012-2014 Ivar Farup and Jan Henrik Wold

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

import tc182
import tc182.description
import tc182.plot
import tc182.table
import sys
import os
import numpy as np
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
import PyQt4.QtWebKit as qtweb
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg \
    import NavigationToolbar2QTAgg \
    as NavigationToolbar
from matplotlib.figure import Figure


class AppForm(qt.QMainWindow):
    """
    The main application window.
    """
    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowTitle('CIE Functions')
        self.create_menu()
        self.create_main_frame()
        self.on_compute()

    def save_table(self):
        file_choices = "CSV (*.csv)|*.csv"

        suggest = ''
        if self.plot_combo.currentIndex() == self.COMBO_XYZ:
            suggest += 'xyz_'
        elif self.plot_combo.currentIndex() == self.COMBO_LMS:
            suggest += 'lms_'
        elif self.plot_combo.currentIndex() == self.COMBO_PURPLE:
            suggest += 'purple_'
        elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:
            suggest += 'lms_9_'
        elif self.plot_combo.currentIndex() == self.COMBO_XY:
            suggest += 'xy_'
        elif self.plot_combo.currentIndex() == self.COMBO_BM:
            suggest += 'bm_'
        elif self.plot_combo.currentIndex() == self.COMBO_LM:
            suggest += 'lm_'
        suggest += 'fs_' + str(self.field_spin.value()) + '_age_' + \
                   str(self.age_spin.value()) + '_res_' + \
                   str(self.resolution_spin.value()) + '.csv'
        path = str(qt.QFileDialog.getSaveFileName(self,
                                                  'Save file', suggest,
                                                  file_choices))
        if path:
            if self.plot_combo.currentIndex() == self.COMBO_XYZ:
                np.savetxt(path, self.results['xyz'], '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == self.COMBO_PURPLE:
                np.savetxt(path, self.results['purple_xyz'],
                           '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == self.COMBO_LMS:
                np.savetxt(path, self.results['lms'], '%.1f, %.5e, %.5e, %.5e')
            elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:
                np.savetxt(path, self.results['lms_base'],
                           '%.1f, %.8e, %.8e, %.8e')
            elif self.plot_combo.currentIndex() == self.COMBO_XY:
                np.savetxt(path, self.results['xy'], '%.1f, %.5f, %.5f, %.5f')
            elif self.plot_combo.currentIndex() == self.COMBO_BM:
                np.savetxt(path, self.results['bm'], '%.1f, %.6f, %.6f, %.6f')
            elif self.plot_combo.currentIndex() == self.COMBO_LM:
                np.savetxt(path, self.results['lm'], '%.1f, %.6f, %.6f, %.6f')

    def options(self):
        """
        Return a dict() with the current plot options for the plot module.
        """
        return {'grid': self.grid_check.isChecked(),
                'cie31': self.cie31_check.isChecked(),
                'cie64': self.cie64_check.isChecked(),
                'labels': self.wavelength_check.isChecked(),
                'label_fontsize': 7,
                'title_fontsize': 11,
                'full_title': True,
                'axis_labels': True,
                'norm': self.norm_check.isChecked()}

    def on_about(self):
        msg = """
CIE Functions: Calculate the CIE functions according to CIE TC1-82.

Copyright (C) 2012-2013 Ivar Farup and Jan Henrik Wold

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
        qt.QMessageBox.about(self, "About the demo", msg.strip())

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

        if self.plot_combo.currentIndex() in [self.COMBO_XY,
                                              self.COMBO_XYZ,
                                              self.COMBO_PURPLE]:
            self.norm_label.setVisible(True)
            self.norm_check.setVisible(True)
        else:
            self.norm_label.setVisible(False)
            self.norm_check.setVisible(False)

        #
        # XYZ plot and table
        #
        if self.plot_combo.currentIndex() == self.COMBO_XYZ:

            # Setup GUI
            self.compare_label_31.setEnabled(True)
            self.compare_label_64.setEnabled(True)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setEnabled(True)
            self.cie64_check.setEnabled(True)

            # Create plot
            tc182.plot.xyz(self.axes, self.plots, self.options())

            # Create html description
            html_string = tc182.description.xyz(self.results,
                                                self.plot_combo.currentText(),
                                                self.options(), True)

            # Create html table
            html_table = tc182.table.xyz(self.results, self.options(), True)

        #
        # chromaticity diagram
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XY:
            # Setup GUI
            self.compare_label_31.setEnabled(True)
            self.compare_label_64.setEnabled(True)
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            self.cie31_check.setEnabled(True)
            self.cie64_check.setEnabled(True)

            # Create plot
            tc182.plot.xy(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc182.table.xy(self.results, self.options(), True)

            # Greate html description
            html_string = tc182.description.xy(self.results,
                                               self.plot_combo.currentText(),
                                               self.options(), True)

        #
        # Purple plot and table
        #
        if self.plot_combo.currentIndex() == self.COMBO_PURPLE:

            # Setup GUI
            self.compare_label_31.setEnabled(False)
            self.compare_label_64.setEnabled(False)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setEnabled(False)
            self.cie64_check.setEnabled(False)

            # Create plot
            tc182.plot.purple(self.axes, self.plots, self.options())

            # Create html description
            html_string = tc182.description.purple(
                self.results,
                self.plot_combo.currentText(),
                self.options(), True)

            # Create html table
            html_table = tc182.table.purple(self.results, self.options(), True)

        #
        # LMS standard
        #
        elif self.plot_combo.currentIndex() == self.COMBO_LMS:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create plot
            tc182.plot.lms(self.axes, self.plots, self.options())

            # Create html description
            html_string = tc182.description.lms(self.results,
                                                self.plot_combo.currentText(),
                                                self.options(), True)

            # Create html table
            html_table = tc182.table.lms(self.results, self.options(), True)

        #
        # LMS base
        #
        elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create plot
            tc182.plot.lms_base(self.axes, self.plots, self.options())

            # Create html description
            html_string = tc182.description.lms_base(
                self.results,
                self.plot_combo.currentText(),
                self.options(), True)

            # Create html table
            html_table = tc182.table.lms_base(self.results,
                                              self.options(), True)

        #
        # MacLeod-Boynton
        #
        elif self.plot_combo.currentIndex() == self.COMBO_BM:

            # Setup GUI
            self.compare_label_31.setDisabled(True)
            self.compare_label_64.setDisabled(True)
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            self.cie31_check.setDisabled(True)
            self.cie64_check.setDisabled(True)

            # Create plot
            tc182.plot.bm(self.axes, self.plots, self.options())

            # Create html description
            html_string = tc182.description.bm(self.results,
                                               self.plot_combo.currentText(),
                                               self.options(), True)

            # Create html table
            html_table = tc182.table.bm(self.results, self.options(), True)

        #
        # Normalised lm-diagram
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
            html_string = tc182.description.lm(self.results,
                                               self.plot_combo.currentText(),
                                               self.options(), True)

            # Create plot
            tc182.plot.lm(self.axes, self.plots, self.options())

            # Create html table
            html_table = tc182.table.lm(self.results, self.options(), True)

        #
        # CIE standard XYZ
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYZSTD:

            # Setup GUI
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)

            if self.field_combo.currentIndex() == 0:  # 2 deg

                # Setup GUI
                self.compare_label_31.setDisabled(True)
                self.compare_label_64.setEnabled(True)
                self.cie31_check.setDisabled(True)
                self.cie64_check.setEnabled(True)

                # Create html descrption
                html_string = tc182.description.xyz31(
                    self.results,
                    self.plot_combo.currentText(),
                    self.options(), True)

                # Create html table
                html_table = tc182.table.xyz31(self.results,
                                               self.options(), True)

                # Create plot
                tc182.plot.xyz31(self.axes, self.plots, self.options())

            else:               # 10 deg

                # Setup GUI
                self.compare_label_31.setEnabled(True)
                self.compare_label_64.setDisabled(True)
                self.cie31_check.setEnabled(True)
                self.cie64_check.setDisabled(True)

                # Create html descption
                html_string = tc182.description.xyz64(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

                # Create html table
                html_table = tc182.table.xyz64(self.results,
                                               self.options(), True)

                # Create plot
                tc182.plot.xyz64(self.axes, self.plots, self.options())

        #
        # CIE standard chromaticity diagram
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYSTD:

            # Setup GUI
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)

            if self.field_combo.currentIndex() == 0:  # 2 deg

                # Setup GUI
                self.compare_label_31.setDisabled(True)
                self.compare_label_64.setEnabled(True)
                self.cie31_check.setDisabled(True)
                self.cie64_check.setEnabled(True)

                # Create html description
                html_string = tc182.description.xy31(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

                # Create html table
                html_table = tc182.table.xy31(self.results,
                                              self.options(), True)

                # Create plot
                tc182.plot.xy31(self.axes, self.plots, self.options())

            else:               # 10 deg

                # Setup GUI
                self.compare_label_31.setEnabled(True)
                self.compare_label_64.setDisabled(True)
                self.cie31_check.setEnabled(True)
                self.cie64_check.setDisabled(True)

                # Create html description
                html_string = tc182.description.xy64(
                    self.results, self.plot_combo.currentText(),
                    self.options(), True)

                # Create html table
                html_table = tc182.table.xy64(self.results,
                                              self.options(), True)

                # Create plot
                tc182.plot.xy64(self.axes, self.plots, self.options())

        # Refresh GUI

        base_url = qtcore.QUrl.fromLocalFile(os.getcwd() + os.sep)
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
        self.last_resolution = tc182.my_round(self.resolution_spin.value(), 1)
        self.last_lambda_min = tc182.my_round(self.lambda_min_spin.value(), 1)
        self.last_lambda_max = tc182.my_round(self.lambda_max_spin.value(), 1)
        self.results, self.plots = tc182.compute_tabulated(
            self.last_field,
            self.last_age,
            self.last_lambda_min,
            self.last_lambda_max,
            self.last_resolution)
        if self.results['xyz'][-1, 0] < 700:
            self.lambda_max_spin.setMinimum(self.results['xyz'][-1, 0])
        if self.results['xyz'][-1, 0] != self.last_lambda_max:
            self.last_lambda_max = self.results['xyz'][-1, 0]
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
        action = qt.QAction(text, self)
        if icon is not None:
            action.setIcon(qt.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, qtcore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        quit_action = self.create_action("&Quit", slot=self.close,
                                         shortcut="Ctrl+Q",
                                         tip="Close the application")

        self.add_actions(self.file_menu, (quit_action,))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
                                          shortcut='F1', slot=self.on_about,
                                          tip='About CIE Functions')

        self.add_actions(self.help_menu, (about_action,))

    def create_main_frame(self):
        self.main_frame = qt.QWidget()

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
        self.age_spin = qt.QSpinBox()
        self.age_spin.setMinimum(20)
        self.age_spin.setMaximum(70)
        self.age_spin.setValue(32)

        self.field_spin = qt.QDoubleSpinBox()
        self.field_spin.setLocale(qtcore.QLocale('C'))
        self.field_spin.setMinimum(1)
        self.field_spin.setMaximum(10)
        self.field_spin.setDecimals(1)
        self.field_spin.setValue(2)
        self.field_spin.setSingleStep(0.1)

        self.field_combo = qt.QComboBox()
        self.field_combo.addItem(u'2\N{DEGREE SIGN} (1931)')
        self.field_combo.addItem(u'10\N{DEGREE SIGN} (1964)')
        self.field_combo.hide()
        self.connect(self.field_combo,
                     qtcore.SIGNAL('currentIndexChanged(int)'),
                     self.on_draw_all)

        self.resolution_spin = qt.QDoubleSpinBox()
        self.resolution_spin.setLocale(qtcore.QLocale('C'))
        self.resolution_spin.setMinimum(0.1)
        self.resolution_spin.setMaximum(5)
        self.resolution_spin.setDecimals(1)
        self.resolution_spin.setValue(1)
        self.resolution_spin.setSingleStep(0.1)

        self.lambda_min_spin = qt.QDoubleSpinBox()
        self.lambda_min_spin.setLocale(qtcore.QLocale('C'))
        self.lambda_min_spin.setMinimum(390)
        self.lambda_min_spin.setMaximum(400)
        self.lambda_min_spin.setDecimals(1)
        self.lambda_min_spin.setValue(390)
        self.lambda_min_spin.setSingleStep(0.1)

        self.lambda_max_spin = qt.QDoubleSpinBox()
        self.lambda_max_spin.setLocale(qtcore.QLocale('C'))
        self.lambda_max_spin.setMinimum(700)
        self.lambda_max_spin.setMaximum(830)
        self.lambda_max_spin.setDecimals(1)
        self.lambda_max_spin.setValue(830)
        self.lambda_max_spin.setSingleStep(0.1)

        self.plot_combo = qt.QComboBox()
        self.plot_combo.addItem('CIE LMS cone fundamentals')
        self.COMBO_LMS = 0
        self.plot_combo.addItem('CIE LMS cone fundamentals (9 sign. figs.)')
        self.COMBO_LMSBASE = 1
        self.plot_combo.addItem(
            u'MacLeod\u2013Boynton ls chromaticity diagram')
        self.COMBO_BM = 2
        self.plot_combo.addItem('Maxwellian lm chromaticity diagram')
        self.COMBO_LM = 3
        self.plot_combo.addItem(
            'CIE XYZ cone-fundamental-based spectral tristimulus values')
        self.COMBO_XYZ = 4
        self.plot_combo.addItem(
            'XYZ cone-fundamental-based tristimulus values for ' +
            'purple-line stimuli')
        self.COMBO_PURPLE = 5
        self.plot_combo.addItem(
            'CIE xy cone-fundamental-based chromaticity diagram')
        self.COMBO_XY = 6
        self.plot_combo.addItem('CIE XYZ standard colour-matching functions')
        self.COMBO_XYZSTD = 7
        self.plot_combo.addItem('CIE xy standard chromaticity diagram')
        self.COMBO_XYSTD = 8
        self.connect(self.plot_combo,
                     qtcore.SIGNAL('currentIndexChanged(int)'),
                     self.on_draw_all)

        self.grid_check = qt.QCheckBox()
        self.connect(self.grid_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_grid)

        self.wavelength_check = qt.QCheckBox()
        self.connect(self.wavelength_check,
                     qtcore.SIGNAL('stateChanged(int)'),
                     self.on_draw_plot_only)

        self.cie31_check = qt.QCheckBox()
        self.connect(self.cie31_check,
                     qtcore.SIGNAL('stateChanged(int)'),
                     self.on_draw_plot_only)

        self.cie64_check = qt.QCheckBox()
        self.connect(self.cie64_check,
                     qtcore.SIGNAL('stateChanged(int)'),
                     self.on_draw_plot_only)

        self.norm_check = qt.QCheckBox()
        self.connect(self.norm_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw_all)

        self.save_table_button = qt.QPushButton('&Save table')
        self.connect(self.save_table_button,
                     qtcore.SIGNAL('clicked(bool)'),
                     self.save_table)

        self.compute_button = qt.QPushButton('       &Compute       ')
        self.connect(self.compute_button,
                     qtcore.SIGNAL('clicked(bool)'), self.on_compute)

        self.transformation = qtweb.QWebView()
        self.html_table = qtweb.QWebView()

        # Layout with labels
        #
        self.compare_label_31 = qt.QLabel(
            u'Compare with CIE 1931 2\N{DEGREE SIGN}')
        self.compare_label_64 = qt.QLabel(
            u'Compare with CIE 1964 10\N{DEGREE SIGN}')
        self.norm_label = qt.QLabel('Renormalised values ')
        self.wavelength_label = qt.QLabel('Labels')
        self.age_label = qt.QLabel('Age (yr)')
        self.resolution_label = qt.QLabel('Step (nm)')
        self.lambda_min_max_label = qt.QLabel('Domain (nm)')
        self.lambda_min_max_dash = qt.QLabel(u'\u2013')
        grid = qt.QGridLayout()
        grid.addWidget(qt.QLabel(u'Field size (\N{DEGREE SIGN})'), 0,
                       0, qtcore.Qt.AlignRight)
        grid.addWidget(self.age_label, 0, 2, qtcore.Qt.AlignRight)
        grid.addWidget(self.lambda_min_max_label, 0, 4, qtcore.Qt.AlignRight)
        grid.addWidget(self.lambda_min_max_dash, 0, 6)
        grid.addWidget(self.resolution_label, 0, 8, qtcore.Qt.AlignRight)

        grid.addWidget(self.field_spin, 0, 1)
        grid.addWidget(self.field_combo, 0, 1)
        grid.addWidget(self.age_spin, 0, 3)
        grid.addWidget(self.lambda_min_spin, 0, 5)
        grid.addWidget(self.lambda_max_spin, 0, 7)
        grid.addWidget(self.resolution_spin, 0, 9)
        grid.addWidget(self.compute_button, 0, 11)
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(4, 1)
        grid.setColumnStretch(8, 1)
        grid.setColumnStretch(10, 3)

        inner_vbox = qt.QVBoxLayout()
        inner_vbox.addWidget(self.mpl_toolbar)
        inner_vbox.addWidget(self.canvas)
        check_bar = qt.QGridLayout()
        check_bar.addWidget(self.compare_label_31, 0, 0, qtcore.Qt.AlignRight)
        check_bar.addWidget(self.cie31_check, 0, 1)
        check_bar.addWidget(self.compare_label_64, 0, 2, qtcore.Qt.AlignRight)
        check_bar.addWidget(self.cie64_check, 0, 3)
        check_bar.addWidget(qt.QLabel('Grid'), 0, 4, qtcore.Qt.AlignRight)
        check_bar.addWidget(self.grid_check, 0, 5)
        check_bar.addWidget(self.wavelength_label, 0, 6, qtcore.Qt.AlignRight)
        check_bar.addWidget(self.wavelength_check, 0, 7)
        check_widget = qt.QWidget()
        check_widget.setLayout(check_bar)
        inner_vbox.addWidget(check_widget)
        inner_widget = qt.QWidget()
        inner_widget.setLayout(inner_vbox)

        table_vbox = qt.QVBoxLayout()
        table_vbox.addWidget(self.html_table)
        table_vbox.addWidget(self.save_table_button)
        table_widget = qt.QWidget()
        table_widget.setLayout(table_vbox)

        spectral_tabs = qt.QTabWidget()
        spectral_tabs.addTab(inner_widget, 'Plot')
        spectral_tabs.addTab(table_widget, 'Table')

        combo_widget = qt.QWidget()
        combo_grid = qt.QGridLayout(combo_widget)
        combo_grid.addWidget(self.plot_combo, 0, 0)
        combo_grid.addWidget(qt.QLabel('   '), 0, 1)
        combo_grid.addWidget(self.norm_label, 0, 2, qtcore.Qt.AlignRight)
        combo_grid.addWidget(self.norm_check, 0, 3)
        combo_grid.setColumnMinimumWidth(2, 150)
        combo_grid.setColumnMinimumWidth(3, 20)
        combo_grid.setColumnStretch(0, 1)
        combo_grid.setSpacing(0)

        spectral_innerwidget = qt.QWidget()
        spectral_vbox = qt.QVBoxLayout(spectral_innerwidget)
        spectral_vbox.addWidget(spectral_tabs)
        spectral_vbox.addWidget(combo_widget)

        spectral_splitter = qt.QSplitter()
        spectral_splitter.addWidget(spectral_innerwidget)
        spectral_splitter.addWidget(self.transformation)

        vbox = qt.QVBoxLayout()
        vbox.addWidget(spectral_splitter)
        vbox.addLayout(grid)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)


def main():
    """
    Run the CIE Functions application.
    """
    app = qt.QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
