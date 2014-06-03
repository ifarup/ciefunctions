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
import sys
import numpy as np
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
import PyQt4.QtWebKit as qtweb
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
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
        elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:
            suggest += 'lms_9_'
        elif self.plot_combo.currentIndex() == self.COMBO_XY:
            suggest += 'cc_'
        elif self.plot_combo.currentIndex() == self.COMBO_BM:
            suggest += 'bm_'
        elif self.plot_combo.currentIndex() == self.COBMO_LM:
            suggest += 'lm_'
        suggest += 'fs_' + str(self.field_spin.value()) + '_age_' + \
            str(self.age_spin.value()) + '_res_' + \
            str(self.resolution_spin.value()) + '.csv'
        path = qt.QFileDialog.getSaveFileName(self, 
                        'Save file', suggest, 
                        file_choices)
        if path:
            if self.plot_combo.currentIndex() == self.COMBO_XYZ:
                np.savetxt(path, self.results['xyz'], '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == self.COMBO_LMS:
                np.savetxt(path, self.results['lms_standard'], '%.1f, %.5e, %.5e, %.5e')
            elif self.plot_combo.currentIndex() == self.COMBO_LMSBASE:
                np.savetxt(path, self.results['lms_base'], '%.1f, %.8e, %.8e, %.8e')
            elif self.plot_combo.currentIndex() == self.COMBO_XY:
                np.savetxt(path, self.results['cc'], '%.1f, %.5f, %.5f, %.5f')
            elif self.plot_combo.currentIndex() == self.COMBO_BM:
                np.savetxt(path, self.results['bm'], '%.1f, %.6f, %.6f, %.6f')
            elif self.plot_combo.currentIndex() == self.COMBO_LM:
                np.savetxt(path, self.results['lm'], '%.1f, %.5f, %.5f, %.5f')
    
    def plot_options(self):
        """
        Return a dict() with the current plot options for use as argument to the plot module.
        """
        return { 'grid' : self.grid_check.isChecked(),
                 'cie31' : self.cie31_check.isChecked(),
                 'cie64' : self.cie64_check.isChecked(),
                 'labels' : self.wavelength_check.isChecked(),
                 'label_fontsize' : 7 }
    
    def on_about(self):
        msg = """
CIE Functions: Calculate the CIE functions according to the terms of reference of CIE TC1-82.
        
Copyright (C) 2012-2013 Ivar Farup and Jan Henrik Wold

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
        """
        qt.QMessageBox.about(self, "About the demo", msg.strip())  


    def on_grid(self):
        self.axes.grid(self.grid_check.isChecked())
        self.canvas.draw()

    def on_draw(self):

        # Reset GUI values that have not been computed
        self.field_spin.setValue(self.last_field)
        self.age_spin.setValue(self.last_age)
        self.lambda_min_spin.setValue(self.last_lambda_min)
        self.lambda_max_spin.setValue(self.last_lambda_max)
        self.resolution_spin.setValue(self.last_resolution)

        if self.plot_combo.currentIndex() not in [self.COMBO_XYSTD, self.COMBO_XYZSTD]:
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
            tc182.plot.xyz(self.axes, self.plots, self.plot_options())

            # Create html description
            html_string = tc182.description.xyz(self.results, self.plot_combo.currentText(), True)

            # Create table            
            self.table.setRowCount(np.shape(self.results['xyz'])[0])
            self.table.setColumnCount(np.shape(self.results['xyz'])[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'X', 'Y', 'Z'])
            for i in range(np.shape(self.results['xyz'])[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.results['xyz'][i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.6e' % self.results['xyz'][i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.6e' % self.results['xyz'][i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.6e' % self.results['xyz'][i, 3]))
        
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
            tc182.plot.xy(self.axes, self.plots, self.plot_options())

            # Greate html description
            html_string = tc182.description.xy(self.results, self.plot_combo.currentText(), True)

            # Create table
            self.table.setRowCount(np.shape(self.results['cc'])[0])
            self.table.setColumnCount(np.shape(self.results['cc'])[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'x', 'y', 'z'])
            for i in range(np.shape(self.results['xyz'])[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.results['cc'][i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.5f' % self.results['cc'][i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.5f' % self.results['cc'][i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.5f' % self.results['cc'][i, 3]))
        
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
            tc182.plot.lms(self.axes, self.plots, self.plot_options())

            # Create html description
            html_string = tc182.description.lms(self.results, self.plot_combo.currentText(), True)

            # Create table
            self.table.setRowCount(np.shape(self.results['lms_standard'])[0])
            self.table.setHorizontalHeaderLabels(['lambda', 'L', 'M', 'S'])
            self.table.setColumnCount(np.shape(self.results['lms_standard'])[1])
            for i in range(np.shape(self.results['xyz'])[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.results['lms_standard'][i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.5e' % self.results['lms_standard'][i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.5e' % self.results['lms_standard'][i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.5e' % self.results['lms_standard'][i, 3]))
        
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
            tc182.plot.lms_base(self.axes, self.plots, self.plot_options())
            
            # Create html description
            html_string = tc182.description.lms(self.results, self.plot_combo.currentText(), True)
            
            # Create table
            self.table.setRowCount(np.shape(self.results['lms_base'])[0])
            self.table.setHorizontalHeaderLabels(['lambda', 'L', 'M', 'S'])
            self.table.setColumnCount(np.shape(self.results['lms_base'])[1])
            for i in range(np.shape(self.results['xyz'])[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.results['lms_base'][i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.8e' % self.results['lms_base'][i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.8e' % self.results['lms_base'][i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.8e' % self.results['lms_base'][i, 3]))
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
            tc182.plot.bm(self.axes, self.plots, self.plot_options())

            # Create html description
            html_string = tc182.description.bm(self.results, self.plot_combo.currentText(), True)

            # Create table
            self.table.setRowCount(np.shape(self.results['bm'])[0])
            self.table.setColumnCount(np.shape(self.results['bm'])[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'l', 'm', 's'])
            for i in range(np.shape(self.results['xyz'])[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.results['bm'][i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.6f' % self.results['bm'][i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.6f' % self.results['bm'][i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.6f' % self.results['bm'][i, 3]))
        
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
            html_string = tc182.description.lm(self.results, self.plot_combo.currentText(), True)

            # Create plot
            tc182.plot.lm(self.axes, self.plots, self.plot_options())

            # Create table            
            self.table.setRowCount(np.shape(self.results['lm'])[0])
            self.table.setColumnCount(np.shape(self.results['lm'])[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'lN', 'mN', 'sN'])
            for i in range(np.shape(self.results['xyz'])[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.results['lm'][i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.5f' % self.results['lm'][i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.5f' % self.results['lm'][i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.5f' % self.results['lm'][i, 3]))
        
        #
        # CIE standard XYZ
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYZSTD:
            
            # Setup GUI
            self.wavelength_check.setDisabled(True)
            self.wavelength_label.setDisabled(True)

            if self.field_combo.currentIndex() == 0: # 2 deg
                
                # Setup GUI
                self.compare_label_31.setDisabled(True)
                self.compare_label_64.setEnabled(True)
                self.cie31_check.setDisabled(True)
                self.cie64_check.setEnabled(True)
                
                # Create html descrption
                html_string = tc182.description.standard(self.plot_combo.currentText(), u'CIE 1931 2\u00b0  XYZ CMFs', True)

                # Create plot                
                tc182.plot.xyz31(self.axes, self.plots, self.plot_options())
                
                # Create table
                self.table.setRowCount(np.shape(self.plots['xyz31'])[0])
                self.table.setColumnCount(np.shape(self.plots['xyz31'])[1])
                self.table.setHorizontalHeaderLabels(['lambda', 'X', 'Y', 'Z'])
                for i in range(np.shape(self.plots['xyz31'])[0]):
                    self.table.setItem(i, 0,
                                       qt.QTableWidgetItem('%.1f' % self.plots['xyz31'][i, 0]))
                    self.table.setItem(i, 1,
                                       qt.QTableWidgetItem('%.6e' % self.plots['xyz31'][i, 1]))
                    self.table.setItem(i, 2,
                                       qt.QTableWidgetItem('%.6e' % self.plots['xyz31'][i, 2]))
                    self.table.setItem(i, 3,
                                       qt.QTableWidgetItem('%.6e' % self.plots['xyz31'][i, 3]))

            else: # 10 deg
                
                # Setup GUI
                self.compare_label_31.setEnabled(True)
                self.compare_label_64.setDisabled(True)
                self.cie31_check.setEnabled(True)
                self.cie64_check.setDisabled(True)

                # Create html descption
                html_string = tc182.description.standard(self.plot_combo.currentText(), u'CIE 1964 10\u00b0  XYZ CMFs', True)

                # Create plot
                tc182.plot.xyz64(self.axes, self.plots, self.plot_options())
                
                # Create table
                self.table.setRowCount(np.shape(self.plots['xyz64'])[0])
                self.table.setColumnCount(np.shape(self.plots['xyz64'])[1])
                self.table.setHorizontalHeaderLabels(['lambda', 'X', 'Y', 'Z'])
                for i in range(np.shape(self.plots['xyz64'])[0]):
                    self.table.setItem(i, 0,
                                       qt.QTableWidgetItem('%.1f' % self.plots['xyz64'][i, 0]))
                    self.table.setItem(i, 1,
                                       qt.QTableWidgetItem('%.6e' % self.plots['xyz64'][i, 1]))
                    self.table.setItem(i, 2,
                                       qt.QTableWidgetItem('%.6e' % self.plots['xyz64'][i, 2]))
                    self.table.setItem(i, 3,
                                       qt.QTableWidgetItem('%.6e' % self.plots['xyz64'][i, 3]))
        
        #
        # CIE standard chromaticity diagram
        #
        elif self.plot_combo.currentIndex() == self.COMBO_XYSTD:
            
            # Setup GUI
            self.wavelength_check.setEnabled(True)
            self.wavelength_label.setEnabled(True)
            
            if self.field_combo.currentIndex() == 0: # 2 deg
                
                # Setup GUI
                self.compare_label_31.setDisabled(True)
                self.compare_label_64.setEnabled(True)
                self.cie31_check.setDisabled(True)
                self.cie64_check.setEnabled(True)

                # Create html description
                html_string = tc182.description.standard(self.plot_combo.currentText(), u'CIE 1931 (x, y) chromaticity diagram', True)

                # Create plot
                tc182.plot.xy31(self.axes, self.plots, self.plot_options())

                # Create table
                self.table.setRowCount(np.shape(self.plots['cc31'])[0])
                self.table.setColumnCount(np.shape(self.plots['cc31'])[1])
                self.table.setHorizontalHeaderLabels(['lambda', 'x', 'y', 'z'])
                for i in range(np.shape(self.results['xyz'])[0]):
                    self.table.setItem(i, 0,
                                       qt.QTableWidgetItem('%.1f' % self.plots['cc31'][i, 0]))
                    self.table.setItem(i, 1,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc31'][i, 1]))
                    self.table.setItem(i, 2,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc31'][i, 2]))
                    self.table.setItem(i, 3,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc31'][i, 3]))
            else: # 10 deg

                # Setup GUI
                self.compare_label_31.setEnabled(True)
                self.compare_label_64.setDisabled(True)
                self.cie31_check.setEnabled(True)
                self.cie64_check.setDisabled(True)
                
                # Create html description
                html_string = tc182.description.standard(self.plot_combo.currentText(), u'CIE 1964 (x<sub>10</sub>, y<sub>10</sub>) chromaticity diagram', True)

                # Create plot
                tc182.plot.xy31(self.axes, self.plots, self.plot_options())

                # Create table
                self.table.setRowCount(np.shape(self.plots['cc64'])[0])
                self.table.setColumnCount(np.shape(self.plots['cc64'])[1])
                self.table.setHorizontalHeaderLabels(['lambda', 'x10', 'y10', 'z10'])
                for i in range(np.shape(self.results['xyz'])[0]):
                    self.table.setItem(i, 0,
                                       qt.QTableWidgetItem('%.1f' % self.plots['cc64'][i, 0]))
                    self.table.setItem(i, 1,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc64'][i, 1]))
                    self.table.setItem(i, 2,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc64'][i, 2]))
                    self.table.setItem(i, 3,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc64'][i, 3]))

        # Refresh GUI        
        self.transformation.setHtml(html_string)
        self.canvas.draw()

    def on_compute(self):
        self.last_age = self.age_spin.value()
        self.last_field = self.field_spin.value()
        self.last_resolution = self.resolution_spin.value()
        self.last_lambda_min = self.lambda_min_spin.value()
        self.last_lambda_max = self.lambda_max_spin.value()
        self.results, self.plots = tc182.compute_tabulated(self.last_field, self.last_age,
                                                           self.last_lambda_min, self.last_lambda_max,
                                                           self.last_resolution)
        self.on_draw()

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
        
        save_table_action = self.create_action("&Save table",
            shortcut="Ctrl+S", slot=self.save_table, 
            tip="Save the table")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (save_table_action, None, quit_action))
        
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
                     qtcore.SIGNAL('currentIndexChanged(int)'), self.on_draw)

        self.resolution_spin = qt.QDoubleSpinBox()
        self.resolution_spin.setMinimum(0.1)
        self.resolution_spin.setMaximum(5)
        self.resolution_spin.setDecimals(1)
        self.resolution_spin.setValue(1)
        self.resolution_spin.setSingleStep(0.1)
        
        self.lambda_min_spin = qt.QDoubleSpinBox()
        self.lambda_min_spin.setMinimum(390)
        self.lambda_min_spin.setMaximum(400)
        self.lambda_min_spin.setDecimals(1)
        self.lambda_min_spin.setValue(390)
        self.lambda_min_spin.setSingleStep(0.1)

        self.lambda_max_spin = qt.QDoubleSpinBox()
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
        self.plot_combo.addItem('Equi-power normalised lm diagram')
        self.COMBO_LM = 2
        self.plot_combo.addItem('CIE MacLeod-Boynton ls diagram')
        self.COMBO_BM = 3
        self.plot_combo.addItem('CIE XYZ fundamental CMFs')
        self.COMBO_XYZ = 4
        self.plot_combo.addItem('CIE xy fundamental chromaticity diagram')
        self.COMBO_XY = 5
        self.plot_combo.addItem('CIE XYZ standard CMFs')
        self.COMBO_XYZSTD = 6
        self.plot_combo.addItem('CIE xy standard chromaticity diagram')
        self.COMBO_XYSTD = 7
        self.connect(self.plot_combo,
                     qtcore.SIGNAL('currentIndexChanged(int)'), self.on_draw)

        self.grid_check = qt.QCheckBox()
        self.connect(self.grid_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_grid)

        self.wavelength_check = qt.QCheckBox()
        self.connect(self.wavelength_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw)

        self.cie31_check = qt.QCheckBox()
        self.connect(self.cie31_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw)

        self.cie64_check = qt.QCheckBox()
        self.connect(self.cie64_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw)

        self.compute_button = qt.QPushButton('       &Compute       ')
        self.connect(self.compute_button,
                     qtcore.SIGNAL('clicked(bool)'), self.on_compute)
        
        self.table = qt.QTableWidget()
        self.transformation = qtweb.QWebView()

        # Layout with labels
        # 
        self.compare_label_31 = qt.QLabel(u'Compare with CIE 1931 2\N{DEGREE SIGN}') 
        self.compare_label_64 = qt.QLabel(u'Compare with CIE 1964 10\N{DEGREE SIGN}')
        self.wavelength_label = qt.QLabel('Labels')
        self.age_label = qt.QLabel('Age (yr)')
        self.resolution_label = qt.QLabel('Step (nm)')
        self.lambda_min_max_label = qt.QLabel('Domain (nm)') 
        self.lambda_min_max_dash = qt.QLabel(u'\u2013')
        grid = qt.QGridLayout()
        grid.addWidget(qt.QLabel(u'Field size (\N{DEGREE SIGN})'), 0, 0, qtcore.Qt.AlignRight)
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
        check_bar.addWidget(self.wavelength_label,0, 6, qtcore.Qt.AlignRight)
        check_bar.addWidget(self.wavelength_check,0, 7)
        check_widget = qt.QWidget()
        check_widget.setLayout(check_bar)
        inner_vbox.addWidget(check_widget)
        inner_widget = qt.QWidget()
        inner_widget.setLayout(inner_vbox)

        spectral_tabs = qt.QTabWidget()
        spectral_tabs.addTab(inner_widget, 'Plot')
        spectral_tabs.addTab(self.table, 'Table')

        spectral_vbox = qt.QVBoxLayout()
        spectral_vbox.addWidget(spectral_tabs)
        spectral_vbox.addWidget(self.plot_combo)

        spectral_hbox = qt.QHBoxLayout()
        spectral_innerwidget = qt.QWidget()
        spectral_innerwidget.setLayout(spectral_vbox)
        spectral_splitter = qt.QSplitter()
        spectral_splitter.addWidget(spectral_innerwidget)
        spectral_splitter.addWidget(self.transformation)
#         main_tabs = qt.QTabWidget()
#         main_tabs.addTab(spectral_splitter, 'Spectral')
#         main_tabs.addTab(qt.QTabWidget(), 'Purples')

        vbox = qt.QVBoxLayout()
#         vbox.addWidget(main_tabs)
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

if __name__ == "__main__":
    main()
