# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:32:45 2022

@author: Hongseok
"""

""" Import libraries """
# For Qt layout (GUI)
from PyQt5.QtWidgets import (QTabWidget, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout)

# from pyqtgraph.Qt import QtCore
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime, Qt

# For VISA control
import pyvisa as visa
import pyvisa_py #hidden import for exe file

# General
import sys
import time
import numpy as np
import MeaSSUre_IV_UI_all_v1_61 as ui
import module_fet_output, module_fet_transfer, module_PBSNBS
import module_IV, module_collector, module_memory_endurance
import module_fet_i_t, module_synaptic_epsc_ppf, module_synaptic_pd
import module_reservoir_test
import os

""" Draw Qt GUI """
app = QApplication(sys.argv)

""" Round digit for converting float to int """
ROUNDNUM = 4

""" QTimer interval for refreshing the measurement time"""
TIMER_INTERVAL = 10 # miliseconds

#REF: https://pgh268400.tistory.com/378
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class App(QWidget):       
    def __init__(self):
        super(App, self).__init__()

        """Setup UI"""
        #Grid layout setup
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('MeaSSUre: I-V')
        window_ico = resource_path('icon.ico')
        self.setWindowIcon(QIcon(window_ico))
        self.rm = visa.ResourceManager()

        # self.setFixedSize(1550, 800)
        

        #Setup panels        
        self.ConnectionControlBox = ui.CreateConnectionControlBox(num_equipment = 3)  
        self.ConnectionControlBox.set_item(0, 'SMU1 (Drain):')
        self.ConnectionControlBox.set_item(1, 'SMU2 (Gate):')
        self.ConnectionControlBox.set_item(2, 'SMU3 (Pulse):')
        
        self.DataSettingsBox = ui.CreateDataSettingsBox()
        self.RunBox = ui.CreateRunBox()
        self.LogBox = ui.CreateLogBox()
        self.TimeDisplayBox = ui.TimeDisplayBox()
        
        self.LiveBox = ui.CreateLiveValueBox(num_values = 4)
        title_list = ["SMU1 voltage", "SMU1 current", "SMU2 voltage", "SMU2 current"]
        self.LiveBox.set_titles(title_list)
        value_list = ["- V", "- A", "- V", " - A"]
        self.LiveBox.set_values(value_list)
        self.LiveBox.set_status_idle() 
        self.SWInfoBox = ui.CreateSWInfoBox(sw_text = "MeaSSUre: I-V (v1.61 March 2024)",
                                            date_text = "v1.61 beta March 2024",
                                            name_text = "Created by Prof. Hongseok Oh",
                                            aff_text = "Department of Physics, Soongsil University (SSU), South Korea",
                                            contact_text = "Email: hoh331@gmail.com")
        
        self.setup_tabs()
        TOTAL_WIDTH = 100
        TOTAL_HEIGHT = 100
        # Widget layout
        for i in range (TOTAL_WIDTH):
            grid.setRowStretch(i,1)
        for j in range (TOTAL_HEIGHT):
            grid.setColumnStretch(j,1)

        LEFT_COL_WIDTH = 25
        TOP_ROW_HEIGHT = 8
        BOTTOM_ROW_HEIGHT = 10 
        CONNECTION_BOX_HEIGHT = 20
        DATA_BOX_WIDTH = 40
        TIME_BOX_WIDTH = 20
        INFO_BOX_HEIGHT = 10
        
        grid.addWidget(self.ConnectionControlBox.groupbox, 0,0,CONNECTION_BOX_HEIGHT, LEFT_COL_WIDTH)
        grid.addWidget(self.tabs,TOP_ROW_HEIGHT,LEFT_COL_WIDTH,TOTAL_HEIGHT - TOP_ROW_HEIGHT, TOTAL_WIDTH - LEFT_COL_WIDTH)
        grid.addWidget(self.LogBox.groupbox, CONNECTION_BOX_HEIGHT, 0, TOTAL_HEIGHT - CONNECTION_BOX_HEIGHT - INFO_BOX_HEIGHT - BOTTOM_ROW_HEIGHT, LEFT_COL_WIDTH)
        grid.addWidget(self.DataSettingsBox.groupbox, 0, LEFT_COL_WIDTH, TOP_ROW_HEIGHT, DATA_BOX_WIDTH)   
        grid.addWidget(self.TimeDisplayBox.groupbox, 0,LEFT_COL_WIDTH + DATA_BOX_WIDTH, TOP_ROW_HEIGHT, TIME_BOX_WIDTH)
        grid.addWidget(self.RunBox.groupbox, 0, LEFT_COL_WIDTH + DATA_BOX_WIDTH + TIME_BOX_WIDTH, TOP_ROW_HEIGHT, TOTAL_WIDTH - LEFT_COL_WIDTH - DATA_BOX_WIDTH - TIME_BOX_WIDTH)
        grid.addWidget(self.LiveBox.groupbox, TOTAL_HEIGHT - BOTTOM_ROW_HEIGHT - INFO_BOX_HEIGHT, 0, BOTTOM_ROW_HEIGHT, LEFT_COL_WIDTH)
        grid.addWidget(self.SWInfoBox.groupbox, TOTAL_HEIGHT - INFO_BOX_HEIGHT, 0, INFO_BOX_HEIGHT, LEFT_COL_WIDTH)
        # grid.addWidget(self.LiveBox.groupbox, TOTAL_HEIGHT - BOTTOM_ROW_HEIGHT, LEFT_COL_WIDTH, BOTTOM_ROW_HEIGHT, TOTAL_WIDTH - LEFT_COL_WIDTH)
        # grid.addWidget(self.SWInfoBox.groupbox, TOTAL_HEIGHT - INFO_BOX_HEIGHT, 0, INFO_BOX_HEIGHT, LEFT_COL_WIDTH)
        
        self.scan_index = 0
        # load measurement units
        
        # Startup
        self.RunBox.btn_run.clicked.connect(self.run_measurement)
        self.RunBox.btn_abort.clicked.connect(self.abort_measurement)
        self.tabs.currentChanged.connect(self.tab_change)
        
        self.measurement_done_flag = False
        self.scan_type = "Output"
        self.tab_change(self.tabs.currentIndex())
        self.show()      
        
    def setup_tabs(self):
        # Load modules
        self.module_list = []
        self.module_list.append(module_fet_output.CreateClass(self))
        self.module_list.append(module_fet_transfer.CreateClass(self))
        self.module_list.append(module_PBSNBS.CreateClass(self))
        self.module_list.append(module_IV.CreateClass(self))
        self.module_list.append(module_collector.CreateClass(self))
        self.module_list.append(module_memory_endurance.CreateClass(self))
        self.module_list.append(module_fet_i_t.CreateClass(self))
        self.module_list.append(module_synaptic_epsc_ppf.CreateClass(self))
        self.module_list.append(module_synaptic_pd.CreateClass(self))
        self.module_list.append(module_reservoir_test.CreateClass(self))

        self.tabs = QTabWidget()
        
        for item in self.module_list:
            self.tabs.addTab(item.tab, item.scan_type)             
        
        self.tabtotalnum = len(self.module_list)        
    
    @pyqtSlot(object)
    def update_plot(self, array):
        self.module_list[self.tabs.currentIndex()].update_plot(array)                                
               
    def run_measurement(self):
        print("run_measurement called")
        self.module_list[self.tabs.currentIndex()].run_measurement()
        
    def abort_measurement(self):
        print("abort_measurement called")
        self.module_list[self.tabs.currentIndex()].abort_measurement()
        
    def stop_measurement(self):
        print("stop_measurement called")
        self.module_list[self.tabs.currentIndex()].stop_measurement()
        
    def tab_change(self, i):
        self.scan_type = self.module_list[i].scan_type
        
        if self.scan_type == "Collector":
            self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Collector)")
            self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Base)")
        else:
            self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
            self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        
        
        # if i == 0:
        #     #self.RunBox.btn_run.setText("Run (Output)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        # elif i == 1:
        #     #self.RunBox.btn_run.setText("Run (Transfer)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        # elif i == 2:
        #     #self.RunBox.btn_run.setText("Run (PBS/NBS)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        # elif i == 3:
        #     #self.RunBox.btn_run.setText("Run (I-V)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (N/A)")
        # elif i == 4:
        #     #self.RunBox.btn_run.setText("Run (BJT: Collector C/C)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Collector)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Base)")
        # elif i == 5:
        #     #self.RunBox.btn_run.setText("Run (Endurance)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        # else:
        #     #self.RunBox.btn_run.setText("Run (I-t)")
        #     self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
        #     self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")


if __name__ == '__main__':

    """ Run the program    """

    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())