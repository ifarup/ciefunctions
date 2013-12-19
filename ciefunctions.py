#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ciefunctions: GUI application for the calculation of CIE functions.

Copyright (C) 2012-2013 Ivar Farup and Jan Henrik Wold

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

import tc
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
        self.create_status_bar()
        self.on_compute()
    
    def save_table(self):
        file_choices = "CSV (*.csv)|*.csv"
        
        suggest = ''
        if self.plot_combo.currentIndex() == 0:
            suggest += 'xyz_'
        elif self.plot_combo.currentIndex() == 1:
            suggest += 'lms_'
        elif self.plot_combo.currentIndex() == 2:
            suggest += 'lms_9_'
        elif self.plot_combo.currentIndex() == 3:
            suggest += 'cc_'
        elif self.plot_combo.currentIndex() == 4:
            suggest += 'bm_'
        elif self.plot_combo.currentIndex() == 5:
            suggest += 'lm_'
        suggest += 'fs_' + str(self.field_spin.value()) + '_age_' + \
            str(self.age_spin.value()) + '_res_' + \
            str(self.resolution_spin.value()) + '.csv'
        path = unicode(qt.QFileDialog.getSaveFileName(self, 
                        'Save file', suggest, 
                        file_choices))
        if path:
            self.statusBar().showMessage('Saved to %s' % path, 2000)
            if self.plot_combo.currentIndex() == 0:
                np.savetxt(path, self.xyz, '%.1f, %.6e, %.6e, %.6e')
            elif self.plot_combo.currentIndex() == 1:
                np.savetxt(path, self.lms_standard, '%.1f, %.5e, %.5e, %.5e')
            elif self.plot_combo.currentIndex() == 2:
                np.savetxt(path, self.lms_base, '%.1f, %.8e, %.8e, %.8e')
            elif self.plot_combo.currentIndex() == 3:
                np.savetxt(path, self.cc, '%.1f, %.5f, %.5f, %.5f')
            elif self.plot_combo.currentIndex() == 4:
                np.savetxt(path, self.bm, '%.1f, %.6f, %.6f, %.6f')
            elif self.plot_combo.currentIndex() == 5:
                np.savetxt(path, self.lm, '%.1f, %.5f, %.5f, %.5f')

    def on_about(self):
        msg = """
CIE Functions: Calculate the CIE functions according to the terms of reference of CIE TC1-82.
        
Copyright (C) 2012-2013 Ivar Farup and Jan Henrik Wold

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
        """
        qt.QMessageBox.about(self, "About the demo", msg.strip())        

    def on_draw(self):
        self.axes.clear()
        self.axes.grid(self.grid_check.isChecked())
        self.field_spin.setValue(self.last_field)
        self.age_spin.setValue(self.last_age)
        self.resolution_spin.setValue(self.last_resolution)
        
        if self.plot_combo.currentIndex() <= 5:
            self.field_spin.show()
            self.field_combo.hide()
            self.age_label.show()
            self.age_spin.show()
            self.resolution_label.show()
            self.resolution_spin.show()
            self.compute_button.show()
        else:
            self.field_spin.hide()
            self.field_combo.show()
            self.age_label.hide()
            self.age_spin.hide()
            self.resolution_label.hide()
            self.resolution_spin.hide()
            self.compute_button.hide()

        if self.plot_combo.currentIndex() == 0: # XYZ
            self.superpose_label_1.show()
            self.superpose_label_2.show()
            self.cie31_check.show()
            self.cie64_check.show()
            self.axes.plot(self.plots['xyz'][:,0], self.plots['xyz'][:,1], 'r')
            self.axes.plot(self.plots['xyz'][:,0], self.plots['xyz'][:,2], 'g')
            self.axes.plot(self.plots['xyz'][:,0], self.plots['xyz'][:,3], 'b')
            if self.cie31_check.isChecked():
                self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,1], 'r--')
                self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,2], 'g--')
                self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,3], 'b--')
            if self.cie64_check.isChecked():
                self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,1], 'r-.')
                self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,2], 'g-.')
                self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,3], 'b-.')
            self.axes.axis('normal')
            self.axes.axis([350, 850, -.2, 2.3])
            self.axes.set_xlabel('Wavelength [nm]', fontsize=12)
            self.axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
            self.axes.set_title('CIE XYZ fundamental CMFs for field size ' + str(self.field_spin.value()) +
                                u'\N{DEGREE SIGN}, and age ' + str(self.age_spin.value()), fontsize=12)
            self.table.setRowCount(np.shape(self.xyz)[0])
            self.table.setColumnCount(np.shape(self.xyz)[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'X', 'Y', 'Z'])
            for i in range(np.shape(self.xyz)[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.xyz[i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.6e' % self.xyz[i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.6e' % self.xyz[i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.6e' % self.xyz[i, 3]))
        elif self.plot_combo.currentIndex() == 1: #xy
            self.superpose_label_1.show()
            self.superpose_label_2.show()
            self.cie31_check.show()
            self.cie64_check.show()
            self.axes.plot(self.plots['cc'][:,1], self.plots['cc'][:,2], 'k')
            self.axes.plot(self.plots['purple_line_cc'][:,1], self.plots['purple_line_cc'][:,2], 'k')
            self.axes.plot(self.cc_white[0], self.cc_white[1], 'kx')
            if self.cie31_check.isChecked():
                self.axes.plot(self.plots['cc31'][:,1], self.plots['cc31'][:,2], 'k--')
                self.axes.plot(self.plots['purple_line_cc31'][:,1], self.plots['purple_line_cc31'][:,2], 'k--')
            if self.cie64_check.isChecked():
                self.axes.plot(self.plots['cc64'][:,1], self.plots['cc64'][:,2], 'k-.')
                self.axes.plot(self.plots['purple_line_cc64'][:,1], self.plots['purple_line_cc64'][:,2], 'k-.')
            self.axes.axis('scaled')
            self.axes.set_xlim((-.05, 1.05))
            self.axes.set_ylim((-.05, 1.05))
            self.axes.set_xlabel('$x_\mathrm{\,F,\,' +
                                 str(self.field_spin.value()) + ',\,' +
                                 str(self.age_spin.value()) +'}$',
                                 fontsize=16)
            self.axes.set_ylabel('$y_\mathrm{\,F,\,' +
                                 str(self.field_spin.value()) + ',\,' +
                                 str(self.age_spin.value()) +'}$',
                                 fontsize=16)
            self.axes.set_title('CIE xy fundamental chromaticity diagram for field size ' + str(self.field_spin.value()) +
                                u'\N{DEGREE SIGN}, and age ' + str(self.age_spin.value()), fontsize=12)
            self.table.setRowCount(np.shape(self.cc)[0])
            self.table.setColumnCount(np.shape(self.cc)[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'x', 'y', 'z'])
            for i in range(np.shape(self.xyz)[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.cc[i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.5f' % self.cc[i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.5f' % self.cc[i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.5f' % self.cc[i, 3]))
        elif self.plot_combo.currentIndex() == 2: # LMS standard
            self.superpose_label_1.hide()
            self.superpose_label_2.hide()
            self.cie31_check.hide()
            self.cie64_check.hide()
            self.axes.plot(self.plots['lms'][:,0], self.plots['lms'][:,1], 'r')
            self.axes.plot(self.plots['lms'][:,0], self.plots['lms'][:,2], 'g')
            self.axes.plot(self.plots['lms'][:,0], self.plots['lms'][:,3], 'b')
            self.axes.axis('normal')
            self.axes.axis([350, 850, -.05, 1.05])
            self.axes.set_xlabel('Wavelength [nm]', fontsize=12)
            self.axes.set_ylabel('Relative energy sensitivities', fontsize=12)
            self.axes.set_title('CIE 2006 LMS cone fundamentals for field size ' + str(self.field_spin.value()) +
                                u'\N{DEGREE SIGN}, and age ' + str(self.age_spin.value()), fontsize=12)
            self.table.setRowCount(np.shape(self.lms_standard)[0])
            self.table.setHorizontalHeaderLabels(['lambda', 'L', 'M', 'S'])
            self.table.setColumnCount(np.shape(self.lms_standard)[1])
            for i in range(np.shape(self.xyz)[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.lms_standard[i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.5e' % self.lms_standard[i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.5e' % self.lms_standard[i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.5e' % self.lms_standard[i, 3]))
        elif self.plot_combo.currentIndex() == 3: # LMS base
            self.superpose_label_1.hide()
            self.superpose_label_2.hide()
            self.cie31_check.hide()
            self.cie64_check.hide()
            self.axes.plot(self.plots['lms'][:,0], self.plots['lms'][:,1], 'r')
            self.axes.plot(self.plots['lms'][:,0], self.plots['lms'][:,2], 'g')
            self.axes.plot(self.plots['lms'][:,0], self.plots['lms'][:,3], 'b')
            self.axes.axis('normal')
            self.axes.axis([350, 850, -.05, 1.05])
            self.axes.set_xlabel('Wavelength [nm]', fontsize=12)
            self.axes.set_ylabel('Relative energy sensitivities', fontsize=12)
            self.axes.set_title('CIE 2006 LMS cone fundamentals for field size ' + str(self.field_spin.value()) +
                                u'\N{DEGREE SIGN}, and age ' + str(self.age_spin.value()) + ' (9 sign. figs. data)', fontsize=12)
            self.table.setRowCount(np.shape(self.lms_base)[0])
            self.table.setHorizontalHeaderLabels(['lambda', 'L', 'M', 'S'])
            self.table.setColumnCount(np.shape(self.lms_base)[1])
            for i in range(np.shape(self.xyz)[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.lms_base[i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.8e' % self.lms_base[i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.8e' % self.lms_base[i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.8e' % self.lms_base[i, 3]))
        elif self.plot_combo.currentIndex() == 4: # BM
            self.superpose_label_1.hide()
            self.superpose_label_2.hide()
            self.cie31_check.hide()
            self.cie64_check.hide()
            self.axes.plot(self.plots['bm'][:,1], self.plots['bm'][:,3], 'k')
            self.axes.plot(self.plots['purple_line_bm'][:,1], self.plots['purple_line_bm'][:,2], 'k')
            self.axes.plot(self.bm_white[0], self.bm_white[2], 'kx')
            self.axes.axis('scaled')
            self.axes.set_xlim((-.05, 1.05))
            self.axes.set_ylim((-.05, 1.05))
            self.axes.set_xlabel('$l_\mathrm{\,MB,\,' +
                                 str(self.field_spin.value()) + ',\,' +
                                 str(self.age_spin.value()) +'}$',
                                 fontsize=16)
            self.axes.set_ylabel('$s_\mathrm{\,MB,\,' +
                                 str(self.field_spin.value()) + ',\,' +
                                 str(self.age_spin.value()) +'}$',
                                 fontsize=16)
            self.axes.set_title('CIE MacLeod-Boynton chromaticity diagram for field size ' + str(self.field_spin.value()) +
                                u'\N{DEGREE SIGN}, and age ' + str(self.age_spin.value()), fontsize=12)
            self.table.setRowCount(np.shape(self.bm)[0])
            self.table.setColumnCount(np.shape(self.bm)[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'l', 'm', 's'])
            for i in range(np.shape(self.xyz)[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.bm[i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.6f' % self.bm[i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.6f' % self.bm[i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.6f' % self.bm[i, 3]))
        elif self.plot_combo.currentIndex() == 5: # lm
            self.superpose_label_1.hide()
            self.superpose_label_2.hide()
            self.cie31_check.hide()
            self.cie64_check.hide()
            self.axes.plot(self.plots['lm'][:,1], self.plots['lm'][:,2], 'k')
            self.axes.plot(self.plots['purple_line_lm'][:,1], self.plots['purple_line_lm'][:,2], 'k')
            self.axes.plot(self.lm_white[0], self.lm_white[1], 'kx')
            self.axes.axis('scaled')
            self.axes.set_xlim((-.05, 1.05))
            self.axes.set_ylim((-.05, .65))
            self.axes.set_xlabel('$l_\mathrm{\,' +
                                 str(self.field_spin.value()) + ',\,' +
                                 str(self.age_spin.value()) +'}$',
                                 fontsize=16)
            self.axes.set_ylabel('$m_\mathrm{\,' +
                                 str(self.field_spin.value()) + ',\,' +
                                 str(self.age_spin.value()) +'}$',
                                 fontsize=16)
            self.axes.set_title('Equi-power normalised $lm$ chromaticity diagram for field size ' + str(self.field_spin.value()) +
                                u'\N{DEGREE SIGN}, and age ' + str(self.age_spin.value()), fontsize=12)
            self.table.setRowCount(np.shape(self.lm)[0])
            self.table.setColumnCount(np.shape(self.lm)[1])
            self.table.setHorizontalHeaderLabels(['lambda', 'lN', 'mN', 'sN'])
            for i in range(np.shape(self.xyz)[0]):
                self.table.setItem(i, 0,
                                   qt.QTableWidgetItem('%.1f' % self.lm[i, 0]))
                self.table.setItem(i, 1,
                                   qt.QTableWidgetItem('%.5f' % self.lm[i, 1]))
                self.table.setItem(i, 2,
                                   qt.QTableWidgetItem('%.5f' % self.lm[i, 2]))
                self.table.setItem(i, 3,
                                   qt.QTableWidgetItem('%.5f' % self.lm[i, 3]))
        elif self.plot_combo.currentIndex() == 6: # CIE std XYZ
            if self.field_combo.currentIndex() == 0: # 2 deg
                self.superpose_label_1.hide()
                self.superpose_label_2.show()
                self.cie31_check.hide()
                self.cie64_check.show()
                self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,1], 'r')
                self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,2], 'g')
                self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,3], 'b')
                if self.cie64_check.isChecked():
                    self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,1], 'r-.')
                    self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,2], 'g-.')
                    self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,3], 'b-.')
                self.axes.axis('normal')
                self.axes.axis([350, 850, -.2, 2.3])
                self.axes.set_xlabel('Wavelength [nm]', fontsize=12)
                self.axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
                self.axes.set_title(u'CIE 1931 XYZ standard 2\N{DEGREE SIGN} CMFs', fontsize=12)
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
                self.superpose_label_1.show()
                self.superpose_label_2.hide()
                self.cie31_check.show()
                self.cie64_check.hide()
                self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,1], 'r')
                self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,2], 'g')
                self.axes.plot(self.plots['xyz64'][:,0], self.plots['xyz64'][:,3], 'b')
                if self.cie31_check.isChecked():
                    self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,1], 'r--')
                    self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,2], 'g--')
                    self.axes.plot(self.plots['xyz31'][:,0], self.plots['xyz31'][:,3], 'b--')
                self.axes.axis('normal')
                self.axes.axis([350, 850, -.2, 2.3])
                self.axes.set_xlabel('Wavelength [nm]', fontsize=12)
                self.axes.set_ylabel('Fundamental tristimulus values', fontsize=12)
                self.axes.set_title(u'CIE 1964 XYZ standard 10\N{DEGREE SIGN}CMFs', fontsize=12)
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
        elif self.plot_combo.currentIndex() == 7: # CIE std xy
            if self.field_combo.currentIndex() == 0: # 2 deg
                self.superpose_label_1.hide()
                self.superpose_label_2.show()
                self.cie31_check.hide()
                self.cie64_check.show()
                self.axes.plot(self.plots['cc31'][:,1], self.plots['cc31'][:,2], 'k')
                self.axes.plot(self.plots['purple_line_cc31'][:,1], self.plots['purple_line_cc31'][:,2], 'k')
                if self.cie64_check.isChecked():
                    self.axes.plot(self.plots['cc64'][:,1], self.plots['cc64'][:,2], 'k-.')
                    self.axes.plot(self.plots['purple_line_cc64'][:,1], self.plots['purple_line_cc64'][:,2], 'k-.')
                self.axes.axis('scaled')
                self.axes.set_xlim((-.05, 1.05))
                self.axes.set_ylim((-.05, 1.05))
                self.axes.set_xlabel('$x$', fontsize=16)
                self.axes.set_ylabel('$y$', fontsize=16)
                self.axes.set_title(u'CIE 1931 xy standard 2\N{DEGREE SIGN} chromaticity diagram', fontsize=12)
                self.table.setRowCount(np.shape(self.plots['cc31'])[0])
                self.table.setColumnCount(np.shape(self.plots['cc31'])[1])
                self.table.setHorizontalHeaderLabels(['lambda', 'x', 'y', 'z'])
                for i in range(np.shape(self.xyz)[0]):
                    self.table.setItem(i, 0,
                                       qt.QTableWidgetItem('%.1f' % self.plots['cc31'][i, 0]))
                    self.table.setItem(i, 1,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc31'][i, 1]))
                    self.table.setItem(i, 2,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc31'][i, 2]))
                    self.table.setItem(i, 3,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc31'][i, 3]))
            else: # 10 deg
                self.superpose_label_1.show()
                self.superpose_label_2.hide()
                self.cie31_check.show()
                self.cie64_check.hide()
                self.axes.plot(self.plots['cc64'][:,1], self.plots['cc64'][:,2], 'k')
                self.axes.plot(self.plots['purple_line_cc64'][:,1], self.plots['purple_line_cc64'][:,2], 'k')
                if self.cie31_check.isChecked():
                    self.axes.plot(self.plots['cc31'][:,1], self.plots['cc31'][:,2], 'k--')
                    self.axes.plot(self.plots['purple_line_cc31'][:,1], self.plots['purple_line_cc31'][:,2], 'k--')
                self.axes.axis('scaled')
                self.axes.set_xlim((-.05, 1.05))
                self.axes.set_ylim((-.05, 1.05))
                self.axes.set_xlabel('$x_{10}$', fontsize=16)
                self.axes.set_ylabel('$y_{10}$', fontsize=16)
                self.axes.set_title(u'CIE 1964 xy standard 10\N{DEGREE SIGN} chromaticity diagram', fontsize=12)
                self.table.setRowCount(np.shape(self.plots['cc64'])[0])
                self.table.setColumnCount(np.shape(self.plots['cc64'])[1])
                self.table.setHorizontalHeaderLabels(['lambda', 'x10', 'y10', 'z10'])
                for i in range(np.shape(self.xyz)[0]):
                    self.table.setItem(i, 0,
                                       qt.QTableWidgetItem('%.1f' % self.plots['cc64'][i, 0]))
                    self.table.setItem(i, 1,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc64'][i, 1]))
                    self.table.setItem(i, 2,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc64'][i, 2]))
                    self.table.setItem(i, 3,
                                       qt.QTableWidgetItem('%.5f' % self.plots['cc64'][i, 3]))
        self.canvas.draw()

    def on_compute(self):
        self.statusBar().showMessage('Computing')
        self.last_age = self.age_spin.value()
        self.last_field = self.field_spin.value()
        self.last_resolution = self.resolution_spin.value()
        self.xyz, self.cc, self.cc_white, self.trans_mat, self.lms_standard, self.lms_base, \
        self.bm, self.bm_white, self.lm, self.lm_white, self.lambda_min, \
        self.purple_line_cc, self.purple_line_bm, self.purple_line_lm, self.plots = \
            tc.compute_tabulated(self.last_field, self.last_age,
                                 self.last_resolution)
        self.statusBar().clearMessage()
        html_string = """
        The transformation from <em>L, M, S</em> to <em>X, Y, Z</em> is<p>
        <center>
            <img src="https://chart.googleapis.com/chart?cht=tx&chl=%5Cbegin%7Bpmatrix%7DX%5C%5CY%5C%5CZ%5Cend%7Bpmatrix%7D%3D%5Cbegin%7Bpmatrix%7D"""
        for i in range(3):
            for j in range(3):
                html_string += str(self.trans_mat[i,j])
                if j < 2:
                    html_string += '%26'
                else:
                    html_string += '%5C%5C'
        html_string += """%5Cend%7Bpmatrix%7D%5Cbegin%7Bpmatrix%7DL%5C%5CM%5C%5CS%5Cend%7Bpmatrix%7D" alt="Transformation equation">
        </center>
        """
        print html_string
        self.transformation.setHtml(html_string)
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
        
        load_file_action = self.create_action("&Save table",
            shortcut="Ctrl+S", slot=self.save_table, 
            tip="Save the table")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (load_file_action, None, quit_action))
        
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
        self.fig = Figure((7.0, 5.0), dpi=self.dpi)
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
        self.age_spin.setMinimum(0)
        self.age_spin.setMaximum(100)
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
        self.resolution_spin.setMaximum(20)
        self.resolution_spin.setDecimals(1)
        self.resolution_spin.setValue(1)
        self.resolution_spin.setSingleStep(0.1)
        
        self.plot_combo = qt.QComboBox()
        self.plot_combo.addItem('CIE XYZ fundamental CMFs')
        self.plot_combo.addItem('CIE xy fundamental chromaticity diagram')
        self.plot_combo.addItem('CIE LMS fundamentals')
        self.plot_combo.addItem('CIE LMS fundamentals (9 sign. figs.)')
        self.plot_combo.addItem('CIE MacLeod-Boynton ls diagram')
        self.plot_combo.addItem('Equi-power normalised lm diagram')
        self.plot_combo.addItem('CIE XYZ standard CMFs')
        self.plot_combo.addItem('CIE xy standard chromaticity diagram')
        self.connect(self.plot_combo,
                     qtcore.SIGNAL('currentIndexChanged(int)'), self.on_draw)

        self.grid_check = qt.QCheckBox()
        self.connect(self.grid_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw)

        self.cie31_check = qt.QCheckBox()
        self.connect(self.cie31_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw)

        self.cie64_check = qt.QCheckBox()
        self.connect(self.cie64_check,
                     qtcore.SIGNAL('stateChanged(int)'), self.on_draw)

        self.compute_button = qt.QPushButton('&Compute')
        self.connect(self.compute_button,
                     qtcore.SIGNAL('clicked(bool)'), self.on_compute)
        
        self.table = qt.QTableWidget()
        self.transformation = qtweb.QWebView()

        # Layout with labels
        # 
        self.superpose_label_1 = qt.QLabel(u'Superpose CIE 1931 2\N{DEGREE SIGN}') 
        self.superpose_label_2 = qt.QLabel(u'Superpose CIE 1964 10\N{DEGREE SIGN}')
        self.age_label = qt.QLabel('Age (year)')
        self.resolution_label = qt.QLabel('    Wavelength step size (nm)')
        grid = qt.QGridLayout()
        grid.addWidget(qt.QLabel('Field size (degree)'), 0, 0, qtcore.Qt.AlignRight)
        grid.addWidget(self.age_label, 1, 0, qtcore.Qt.AlignRight)
        grid.addWidget(self.resolution_label, 2, 0, qtcore.Qt.AlignRight)
        grid.addWidget(qt.QLabel('          Plot'), 0, 2, qtcore.Qt.AlignRight)
        grid.addWidget(qt.QLabel('Grid'), 1, 3, qtcore.Qt.AlignLeft)
        grid.addWidget(self.superpose_label_1, 2, 3, qtcore.Qt.AlignLeft)
        grid.addWidget(self.superpose_label_2, 3, 3, qtcore.Qt.AlignLeft)
        
        grid.addWidget(self.field_spin, 0, 1)
        grid.addWidget(self.field_combo, 0, 1)
        grid.addWidget(self.age_spin, 1, 1)
        grid.addWidget(self.resolution_spin, 2, 1)
        grid.addWidget(self.plot_combo, 0, 3)
        grid.addWidget(self.grid_check, 1, 2, qtcore.Qt.AlignRight)
        grid.addWidget(self.cie31_check, 2, 2, qtcore.Qt.AlignRight)
        grid.addWidget(self.cie64_check, 3, 2, qtcore.Qt.AlignRight)
        grid.addWidget(self.compute_button, 3, 1)
        grid.setColumnStretch(4, 1)
        
        inner_vbox = qt.QVBoxLayout()
        inner_vbox.addWidget(self.canvas)
        inner_vbox.addWidget(self.mpl_toolbar)
        inner_widget = qt.QWidget()
        inner_widget.setLayout(inner_vbox)      

        tabs = qt.QTabWidget()
        tabs.addTab(inner_widget, 'Plot')
        tabs.addTab(self.table, 'Table')
        tabs.addTab(self.transformation, 'Transformation')

        vbox = qt.QVBoxLayout()
        vbox.addWidget(tabs)
        vbox.addLayout(grid)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = qt.QLabel("Ready")
        self.statusBar().addWidget(self.status_text, 1)

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