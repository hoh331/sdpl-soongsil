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

# For VISA control
import pyvisa as visa
import pyvisa_py #hidden import for exe file

# General
import sys
import time
import numpy as np
import MeaSSUre_IV_UI_all as ui

""" Draw Qt GUI """
app = QApplication(sys.argv)

""" Round digit for converting float to int """
ROUNDNUM = 4

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
        
        self.ConnectionControlBox = ui.CreateConnectionControlBox(num_equipment = 2)  
        self.ConnectionControlBox.set_item(0, 'SMU1 (Drain):')
        self.ConnectionControlBox.set_item(1, 'SMU2 (Gate):')
        
        self.DataSettingsBox = ui.CreateDataSettingsBox()
        self.RunBox = ui.CreateRunBox()
        self.LogBox = ui.CreateLogBox()
        
        self.LiveBox = ui.CreateLiveValueBox(num_values = 4)
        title_list = ["SMU1 voltage", "SMU1 current", "SMU2 voltage", "SMU2 current"]
        self.LiveBox.set_titles(title_list)
        value_list = ["- V", "- A", "- V", " - A"]
        self.LiveBox.set_values(value_list)
        self.LiveBox.set_status_idle() 
        self.SWInfoBox = ui.CreateSWInfoBox(sw_text = "MeaSSUre: I-V",
                                            date_text = "v1.2 May 2023",
                                            name_text = "Created by Prof. Hongseok Oh",
                                            aff_text = "Department of Physics, Soongsil University (SSU), South Korea",
                                            contact_text = "Email: hoh331@gmail.com")
        
        self.setup_tabs()
        
        # Widget layout
        for i in range (22):
            grid.setRowStretch(i,1)
        for j in range (15):
            grid.setColumnStretch(j,1)
        
        grid.addWidget(self.ConnectionControlBox.groupbox, 0,0,3,3)
        grid.addWidget(self.tabs,1,3,19,14)
        grid.addWidget(self.LogBox.groupbox, 3,0,16,3)
        grid.addWidget(self.DataSettingsBox.groupbox, 0,3,1,10)    
        grid.addWidget(self.RunBox.groupbox, 0,13,1,2)
        grid.addWidget(self.LiveBox.groupbox, 20,3,2,13)
        grid.addWidget(self.SWInfoBox.groupbox, 19,0,3,3)
        
        
        
        # Startup
        self.RunBox.btn_run.clicked.connect(self.run_measurement)
        self.RunBox.btn_abort.clicked.connect(self.abort_measurement)
        self.tabs.currentChanged.connect(self.tab_change)
        
        self.measurement_done_flag = False
        self.scan_type = "Output"
        self.tab_change(self.tabs.currentIndex())
        self.show()      
        
    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabOutput = QWidget()
        self.tabTransfer = QWidget()
        self.tabIV = QWidget()
        self.tabCollector = QWidget()
        
        self.tabs.addTab(self.tabOutput, 'FET: Output')
        self.tabs.addTab(self.tabTransfer, 'FET: Transfer')
        self.tabs.addTab(self.tabIV, 'I-V')
        self.tabs.addTab(self.tabCollector, 'BJT: Collector C/C')
        self.tabtotalnum = 4
        
        """Output Tab Setup"""
        self.Output_Drain_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Drain bias setup', 9, 2)
        self.Output_Drain_ParamBox.set_toggle_item(0, 'Single sweep', True)
        self.Output_Drain_ParamBox.set_toggle_item(1, 'Double sweep', False)
        self.Output_Drain_ParamBox.set_item(0, 'Vds start', '0', 'V')
        self.Output_Drain_ParamBox.set_item(1, 'Vds stop', '10', 'V')
        self.Output_Drain_ParamBox.set_item(2, 'Vds step', '0.1', 'V')
        self.Output_Drain_ParamBox.set_item(3, 'Delay before sweep', '1', 's')
        self.Output_Drain_ParamBox.set_item(4, 'Measurement settings', '0', '0')
        self.Output_Drain_ParamBox.show_only_name(4)
        self.Output_Drain_ParamBox.set_item(5, 'Drain trigger delay', '0.1', 's')
        self.Output_Drain_ParamBox.set_item(6, 'Drain source delay', '0.1', 's')
        self.Output_Drain_ParamBox.set_item(7, 'Drain NPLC', '1', 'number')
        self.Output_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.Output_Gate_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Gate bias setup', 8, 2)
        self.Output_Gate_ParamBox.set_toggle_item(0, 'Linear steps', False)
        self.Output_Gate_ParamBox.set_toggle_item(1, 'Custom steps', True)
        self.Output_Gate_ParamBox.set_item(0, 'Vgs (start)', '5, 10, 20, 30', 'V')
        self.Output_Gate_ParamBox.set_item(1, 'Vgs stop', '10', 'V')
        self.Output_Gate_ParamBox.set_item(2, 'Vgs step', '10', 'V')
        self.Output_Gate_ParamBox.set_item(3, 'Measurement settings', '0', '0')
        self.Output_Gate_ParamBox.show_only_name(3)
        self.Output_Gate_ParamBox.set_item(4, 'Gate trigger delay', '0.1', 's')
        self.Output_Gate_ParamBox.set_item(5, 'Gate source delay', '0.1', 's')
        self.Output_Gate_ParamBox.set_item(6, 'Gate NPLC', '1', 'number')
        self.Output_Gate_ParamBox.set_item(7, 'Current compliance', '100E-3', 'A')
        
        self.Output_GraphBox = ui.CreateGraphBox('Output characteristics', 2)
        self.Output_GraphBox.set_titles(0, 'Output curves (Ids-Vds)', 'Vds (V)', 'Ids (A)')
        self.Output_GraphBox.set_titles(1, 'Gate leakage curves (Igs-Vds)', 'Vds (V)', 'Igs (A)')
        

        # Output tab setup
        self.tabOutput_hbox = QHBoxLayout()  
        self.tabOutput_vbox = QVBoxLayout()
        self.tabOutput_vbox.addWidget(self.Output_Drain_ParamBox.groupbox)
        self.tabOutput_vbox.addWidget(self.Output_Gate_ParamBox.groupbox)
        self.tabOutput_hbox.addLayout(self.tabOutput_vbox)
        self.tabOutput_hbox.addWidget(self.Output_GraphBox.groupbox)
        self.tabOutput_hbox.setStretch(0,1)
        self.tabOutput_hbox.setStretch(1,4)
        self.tabOutput.setLayout(self.tabOutput_hbox)

        """Transfer Tab Setup"""
       
        self.Transfer_Gate_ParamBox =  ui.CreateParameterSettingsBoxWithToggle('Gate bias setup', 9, 2)
        self.Transfer_Gate_ParamBox.set_toggle_item(0, 'Single sweep', False)
        self.Transfer_Gate_ParamBox.set_toggle_item(1, 'Double sweep', True)
        self.Transfer_Gate_ParamBox.set_item(0, 'Vgs start', '0', 'V')
        self.Transfer_Gate_ParamBox.set_item(1, 'Vgs stop', '20', 'V')
        self.Transfer_Gate_ParamBox.set_item(2, 'Vgs step', '0.2', 'V')
        self.Transfer_Gate_ParamBox.set_item(3, 'Delay before sweep', '1', 's')
        self.Transfer_Gate_ParamBox.set_item(4, 'Measurement settings', '0', '0')
        self.Transfer_Gate_ParamBox.show_only_name(4)
        self.Transfer_Gate_ParamBox.set_item(5, 'Gate trigger delay', '0.1', 's')
        self.Transfer_Gate_ParamBox.set_item(6, 'Gate source delay', '0.1', 's')
        self.Transfer_Gate_ParamBox.set_item(7, 'Gate NPLC', '1', 'number')
        self.Transfer_Gate_ParamBox.set_item(8, 'Current compliance', '100E-3', 'A')
        
        self.Transfer_Drain_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Drain bias setup', 8, 2)
        self.Transfer_Drain_ParamBox.set_toggle_item(0, 'Linear steps', False)
        self.Transfer_Drain_ParamBox.set_toggle_item(1, 'Custom steps', True)
        self.Transfer_Drain_ParamBox.set_item(0, 'Vds (start)', '5, 10, 20, 30', 'V')
        self.Transfer_Drain_ParamBox.set_item(1, 'Vds stop', '10', 'V')
        self.Transfer_Drain_ParamBox.set_item(2, 'Vds step', '10', 'V')
        self.Transfer_Drain_ParamBox.set_item(3, 'Measurement settings', '0', '0')
        self.Transfer_Drain_ParamBox.show_only_name(3)
        self.Transfer_Drain_ParamBox.set_item(4, 'Drain trigger delay', '0.1', 's')
        self.Transfer_Drain_ParamBox.set_item(5, 'Drain source delay', '0.1', 's')
        self.Transfer_Drain_ParamBox.set_item(6, 'Drain NPLC', '1', 'number')
        self.Transfer_Drain_ParamBox.set_item(7, 'Current compliance', '10E-3', 'A')
        
        
        self.Transfer_GraphBox = ui.CreateGraphBox('Transfer characteristics', 2)
        self.Transfer_GraphBox.set_titles(0, 'Transfer curves (Ids-Vgs)', 'Vgs (V)', 'Ids (A)')
        self.Transfer_GraphBox.set_titles(1, 'Gate leakage curves (Igs-Vgs)', 'Vgs (V)', 'Igs (A)')
        

        # Transfer tab setup
        self.tabTransfer_hbox = QHBoxLayout()  
        self.tabTransfer_vbox = QVBoxLayout()
        self.tabTransfer_vbox.addWidget(self.Transfer_Gate_ParamBox.groupbox)
        self.tabTransfer_vbox.addWidget(self.Transfer_Drain_ParamBox.groupbox)
        self.tabTransfer_hbox.addLayout(self.tabTransfer_vbox)
        self.tabTransfer_hbox.addWidget(self.Transfer_GraphBox.groupbox)
        self.tabTransfer_hbox.setStretch(0,1)
        self.tabTransfer_hbox.setStretch(1,4)
        self.tabTransfer.setLayout(self.tabTransfer_hbox)
        
        """I-V Tab Setup"""
       
        self.IV_Drain_ParamBox =  ui.CreateParameterSettingsBoxWithToggle('Drain bias setup', 10, 2)
        self.IV_Drain_ParamBox.set_toggle_item(0, 'Single sweep', True)
        self.IV_Drain_ParamBox.set_toggle_item(1, 'Double sweep', False)
        self.IV_Drain_ParamBox.set_item(0, 'Vds start', '0', 'V')
        self.IV_Drain_ParamBox.set_item(1, 'Vds stop', '1', 'V')
        self.IV_Drain_ParamBox.set_item(2, 'Vds step', '0.1', 'V')
        self.IV_Drain_ParamBox.set_item(3, 'Number of sweeps', '1', 'cycle(s)')
        self.IV_Drain_ParamBox.set_item(4, 'Delay before sweep', '1', 's')
        self.IV_Drain_ParamBox.set_item(5, 'Measurement settings', '0', '0')
        self.IV_Drain_ParamBox.show_only_name(5)
        self.IV_Drain_ParamBox.set_item(6, 'Drain trigger delay', '0.1', 's')
        self.IV_Drain_ParamBox.set_item(7, 'Drain source delay', '0.1', 's')
        self.IV_Drain_ParamBox.set_item(8, 'Drain NPLC', '1', 'number')
        self.IV_Drain_ParamBox.set_item(9, 'Current compliance', '10E-3', 'A')
        
        self.IV_GraphBox = ui.CreateGraphBox('I-V characteristics', 2)
        self.IV_GraphBox.set_titles(0, 'I-V curves (Linear)', 'Vds (V)', 'Ids (A)')
        self.IV_GraphBox.set_titles(1, 'I-V curves (Semi-Log)', 'Vds (V)', 'Log(Ids(A))')
        

        # I-V tab setup
        self.tabIV_hbox = QHBoxLayout()  
        self.tabIV_vbox = QVBoxLayout()
        self.tabIV_vbox.addWidget(self.IV_Drain_ParamBox.groupbox)
        self.tabIV_vbox.addStretch(1)
        self.tabIV_hbox.addLayout(self.tabIV_vbox)
        self.tabIV_hbox.addWidget(self.IV_GraphBox.groupbox)
        self.tabIV_hbox.setStretch(0,1)
        self.tabIV_hbox.setStretch(1,4)
        self.tabIV.setLayout(self.tabIV_hbox)
        
        
        """Collector Tab Setup"""
        self.Collector_Drain_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Collector bias setup', 9, 2)
        self.Collector_Drain_ParamBox.set_toggle_item(0, 'Single sweep', True)
        self.Collector_Drain_ParamBox.set_toggle_item(1, 'Double sweep', False)
        self.Collector_Drain_ParamBox.set_item(0, 'Vc start', '0', 'V')
        self.Collector_Drain_ParamBox.set_item(1, 'Vc stop', '1', 'V')
        self.Collector_Drain_ParamBox.set_item(2, 'Vc step', '0.01', 'V')
        self.Collector_Drain_ParamBox.set_item(3, 'Delay before sweep', '1', 's')
        self.Collector_Drain_ParamBox.set_item(4, 'Measurement settings', '0', '0')
        self.Collector_Drain_ParamBox.show_only_name(4)
        self.Collector_Drain_ParamBox.set_item(5, 'Collector trigger delay', '0.1', 's')
        self.Collector_Drain_ParamBox.set_item(6, 'Collector source delay', '0.1', 's')
        self.Collector_Drain_ParamBox.set_item(7, 'Collector NPLC', '1', 'number')
        self.Collector_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.Collector_Gate_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Base current setup', 8, 2)
        self.Collector_Gate_ParamBox.set_toggle_item(0, 'Linear steps', False)
        self.Collector_Gate_ParamBox.set_toggle_item(1, 'Custom steps', True)
        self.Collector_Gate_ParamBox.set_item(0, 'Ib (start)', '5, 10, 20, 30', 'uA')
        self.Collector_Gate_ParamBox.set_item(1, 'Ib stop', '10', 'uA')
        self.Collector_Gate_ParamBox.set_item(2, 'Ib step', '10', 'uA')
        self.Collector_Gate_ParamBox.set_item(3, 'Measurement settings', '0', '0')
        self.Collector_Gate_ParamBox.show_only_name(3)
        self.Collector_Gate_ParamBox.set_item(4, 'Base trigger delay', '0.1', 's')
        self.Collector_Gate_ParamBox.set_item(5, 'Base source delay', '0.1', 's')
        self.Collector_Gate_ParamBox.set_item(6, 'Base NPLC', '1', 'number')
        self.Collector_Gate_ParamBox.set_item(7, 'Voltage compliance', '25', 'V')
        
        self.Collector_GraphBox = ui.CreateGraphBox('Collector characteristics', 1)
        self.Collector_GraphBox.set_titles(0, 'Collector characteristic curves (Ic-Vc)', 'Vc (V)', 'Ic (A)')
        

        # Output tab setup
        self.tabCollector_hbox = QHBoxLayout()  
        self.tabCollector_vbox = QVBoxLayout()
        self.tabCollector_vbox.addWidget(self.Collector_Drain_ParamBox.groupbox)
        self.tabCollector_vbox.addWidget(self.Collector_Gate_ParamBox.groupbox)
        self.tabCollector_hbox.addLayout(self.tabCollector_vbox)
        self.tabCollector_hbox.addWidget(self.Collector_GraphBox.groupbox)
        self.tabCollector_hbox.setStretch(0,1)
        self.tabCollector_hbox.setStretch(1,4)
        self.tabCollector.setLayout(self.tabCollector_hbox)
    
    @pyqtSlot(object)
    def update_plot(self, array):
        print("signal received!")
        
        if self.scan_type == "Output":
            print(array)
            if array[0] == 9999:
                self.measurement_done_flag = True
                self.stop_measurement()
            else:
                if np.isnan(array)[0] == True:
                    self.Output_GraphBox.addnew_plot(0)
                    self.Output_GraphBox.addnew_plot(1)
                    self.count = 1
                    self.start = self.N
        
                else:
                    self.result_data[self.N] = array
                    self.Output_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,1], self.result_data[self.start:self.start+self.count,3])
                    self.Output_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,1], self.result_data[self.start:self.start+self.count,2])
                    # Update the plot
        
                    self.N = self.N+1
                    self.count = self.count + 1
                    
                    self.LiveBox.set_status_run()
                    self.LiveBox.set_values(['%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'A'), '%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A')])
        
        elif self.scan_type == "Transfer":
            print(array)
            if array[0] == 9999:
                self.measurement_done_flag = True
                self.stop_measurement()
            else:
                if np.isnan(array)[0] == True:
                    self.Transfer_GraphBox.addnew_plot(0)
                    self.Transfer_GraphBox.addnew_plot(1)
                    self.count = 1
                    self.start = self.N
        
                else:
                    self.result_data[self.N] = array
                    self.Transfer_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,5])
                    self.Transfer_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,4])
                    # Update the plot
        
                    self.N = self.N+1
                    self.count = self.count + 1
                    
                    self.LiveBox.set_status_run()
                    self.LiveBox.set_values(['%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'A'), '%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A')])
            
        elif self.scan_type == "I-V":
            print(array)
            if array[0] == 9999:
                self.measurement_done_flag = True
                self.stop_measurement()
            else:
                if np.isnan(array)[0] == True:
                    self.IV_GraphBox.addnew_plot(0)
                    self.IV_GraphBox.addnew_plot(1)
                    self.count = 1
                    self.start = self.N
        
                else:
                    self.result_data[self.N] = array
                    self.IV_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,1])
                    self.IV_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                    # Update the plot
        
                    self.N = self.N+1
                    self.count = self.count + 1
                    
                    self.LiveBox.set_status_run()
                    self.LiveBox.set_values(['- V', ' -A', '%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A')])
        
        elif self.scan_type == "Collector":          
            print(array)
            if array[0] == 9999:
                self.measurement_done_flag = True
                self.stop_measurement()
            else:
                if np.isnan(array)[0] == True:
                    self.Collector_GraphBox.addnew_plot(0)
                    self.count = 1
                    self.start = self.N
        
                else:
                    self.result_data[self.N] = array
                    self.Collector_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,1], self.result_data[self.start:self.start+self.count,3])
                     # Update the plot
        
                    self.N = self.N+1
                    self.count = self.count + 1
                    
                    self.LiveBox.set_status_run()
                    self.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[3], 'A'), '%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[0], 'uA')])

            
            
               
    def run_measurement(self):
        self.SMU_list = self.ConnectionControlBox.get_SMU_list()
        print("Run Measurement: %s" %(self.scan_type))
        self.LogBox.update_log("Run Measurement: %s" %(self.scan_type))
        
        for i in range(self.tabtotalnum):
            if i != self.tabs.currentIndex():
                self.tabs.setTabEnabled(i, False)
                
        print("Preparing tables of biasing values...")
               
        if self.scan_type == "Output":
            # Calculate sweep points
            self.vds_list = []
            self.vgs_list = []
            self.wait_time = round(float(self.Output_Drain_ParamBox.le_list[3].text()), ROUNDNUM)
            
            # Calculate list for drain biases
            vds_start = round(float(self.Output_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
            vds_stop =  round(float(self.Output_Drain_ParamBox.le_list[1].text()), ROUNDNUM)
            vds_step =  round(float(self.Output_Drain_ParamBox.le_list[2].text()), ROUNDNUM)
            
            temp = vds_start
            while (temp <= vds_stop):
                self.vds_list.append(temp)
                temp = round((temp + vds_step), ROUNDNUM)
                
            if self.Output_Drain_ParamBox.rbtn_list[1].isChecked():
                self.vds_list = np.concatenate([self.vds_list, np.flip(self.vds_list)])
                
            # calculate list for gate biases
            if self.Output_Gate_ParamBox.rbtn_list[1].isChecked():
                text = self.Output_Gate_ParamBox.le_list[0].text()
                self.vgs_list = [float(x) for x in text.split(',')]
                
            else:                
                vgs_start = round(float(self.Output_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
                vgs_stop =  round(float(self.Output_Gate_ParamBox.le_list[1].text()), ROUNDNUM)
                vgs_step =  round(float(self.Output_Gate_ParamBox.le_list[2].text()), ROUNDNUM)     
                
                temp = vgs_start
                while (temp <= vgs_stop):
                    self.vgs_list.append(temp)
                    temp = round((temp + vgs_step), ROUNDNUM)   

            self.tot_num_measure_points = len(self.vds_list)*len(self.vgs_list)
            
            print ("Table prepared")
            
            print ("Preparing bias parameters")
            self.SMU_init_params = [[],[]]
            self.SMU_init_params[0].append(round(float(self.Output_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Output_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Output_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Output_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
            
            self.SMU_init_params[1].append(round(float(self.Output_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Output_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Output_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Output_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
            print ("Bias parameters:")
            print (self.SMU_init_params[0])
            print (self.SMU_init_params[1])
            
            
            
            
            print ("Prepare measurement...")
            # Prepare data array for save
            self.result_data = np.empty((self.tot_num_measure_points, 6))
            self.result_data[:] = np.NaN
            self.N = 0
            self.start = 0
            
            #Reset graph
            self.Output_GraphBox.reset_plot()   
            
            # Initiate IO_Thread thread
            self.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
            self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                       scan_type = self.scan_type, 
                                       vds_list = self.vds_list, 
                                       vgs_list = self.vgs_list,
                                       wait_time = self.wait_time)
            self.IO_Thread.signal.connect(self.update_plot)
            self.LogBox.update_log("Measurement start!")
            self.IO_Thread.start()  
            
            
        elif self.scan_type == "Transfer":
            # Calculate sweep points
            self.vds_list = []
            self.vgs_list = []
            self.wait_time = round(float(self.Transfer_Gate_ParamBox.le_list[3].text()), ROUNDNUM)
            
            # Calculate list for drain biases
            vgs_start = round(float(self.Transfer_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
            vgs_stop =  round(float(self.Transfer_Gate_ParamBox.le_list[1].text()), ROUNDNUM)
            vgs_step =  round(float(self.Transfer_Gate_ParamBox.le_list[2].text()), ROUNDNUM)
            
            temp = vgs_start
            while (temp <= vgs_stop):
                self.vgs_list.append(temp)
                temp = round((temp + vgs_step), ROUNDNUM)
                
            if self.Transfer_Gate_ParamBox.rbtn_list[1].isChecked():
                self.vgs_list = np.concatenate([self.vgs_list, np.flip(self.vgs_list)])
                
            # calculate list for gate biases
            if self.Transfer_Drain_ParamBox.rbtn_list[1].isChecked():
                text = self.Transfer_Drain_ParamBox.le_list[0].text()
                self.vds_list = [float(x) for x in text.split(',')]
                
            else:                
                vds_start = round(float(self.Transfer_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
                vds_stop =  round(float(self.Transfer_Drain_ParamBox.le_list[1].text()), ROUNDNUM)
                vds_step =  round(float(self.Transfer_Drain_ParamBox.le_list[2].text()), ROUNDNUM)     
                
                temp = vds_start
                while (temp <= vds_stop):
                    self.vds_list.append(temp)
                    temp = round((temp + vds_step), ROUNDNUM)   
                    
            self.tot_num_measure_points = len(self.vds_list)*len(self.vgs_list)
                    
            print ("Table prepared")
            
            print ("Preparing bias parameters")
            self.SMU_init_params = [[],[]]
            self.SMU_init_params[0].append(round(float(self.Transfer_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Transfer_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Transfer_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Transfer_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
            
            self.SMU_init_params[1].append(round(float(self.Transfer_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Transfer_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Transfer_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Transfer_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
            print ("Bias parameters:")
            print (self.SMU_init_params[0])
            print (self.SMU_init_params[1])
            
            print ("Prepare measurement...")
            
            # Prepare data array for save
            self.result_data = np.empty((self.tot_num_measure_points, 6))
            self.result_data[:] = np.NaN
            self.N = 0
            self.start = 0
            
            #Reset graph
            self.Transfer_GraphBox.reset_plot()   
            
            # Initiate IO_Thread thread
            self.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
            self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                       scan_type = self.scan_type, 
                                       vds_list = self.vds_list, 
                                       vgs_list = self.vgs_list,
                                       wait_time = self.wait_time)
            self.IO_Thread.signal.connect(self.update_plot)
            self.LogBox.update_log("Measurement start!")
            self.IO_Thread.start()      
            
        elif self.scan_type == "I-V":
            # Calculate sweep points
            self.vds_list = []
            self.wait_time = round(float(self.IV_Drain_ParamBox.le_list[4].text()), ROUNDNUM)
            
            # Calculate list for drain biases
            vds_start = round(float(self.IV_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
            vds_stop =  round(float(self.IV_Drain_ParamBox.le_list[1].text()), ROUNDNUM)
            vds_step =  round(float(self.IV_Drain_ParamBox.le_list[2].text()), ROUNDNUM)
            self.repeat_num = int(self.IV_Drain_ParamBox.le_list[3].text())
            
            temp = vds_start
            while (temp <= vds_stop):
                self.vds_list.append(temp)
                temp = round((temp + vds_step), ROUNDNUM)
                
            if self.IV_Drain_ParamBox.rbtn_list[1].isChecked():
                self.vds_list = np.concatenate([self.vds_list, np.flip(self.vds_list)])  
                
            self.tot_num_measure_points = len(self.vds_list)*self.repeat_num
                
            print ("Table prepared")
            
            print ("Preparing bias parameters")
            self.SMU_init_params = [[]]
            self.SMU_init_params[0].append(round(float(self.IV_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.IV_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.IV_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.IV_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
            
            print ("Bias parameters:")
            print (self.SMU_init_params[0])
            
            print ("Prepare measurement...")
            
            # Prepare data array for save
            self.result_data = np.empty((self.tot_num_measure_points, 3))
            self.result_data[:] = np.NaN
            self.N = 0
            self.start = 0
            
            #Reset graph
            self.IV_GraphBox.reset_plot()   
            
            # Initiate IO_Thread thread
            self.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
            self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                       scan_type = self.scan_type, 
                                       vds_list = self.vds_list, 
                                       repeat_num = self.repeat_num,
                                       wait_time = self.wait_time)
            self.IO_Thread.signal.connect(self.update_plot)
            self.LogBox.update_log("Measurement start!")
            self.IO_Thread.start()      
            
            
        elif self.scan_type == "Collector":
            # Calculate sweep points
            self.vds_list = []
            self.vgs_list = []
            self.wait_time = round(float(self.Collector_Drain_ParamBox.le_list[3].text()), ROUNDNUM)
            
            # Calculate list for drain biases
            vds_start = round(float(self.Collector_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
            vds_stop =  round(float(self.Collector_Drain_ParamBox.le_list[1].text()), ROUNDNUM)
            vds_step =  round(float(self.Collector_Drain_ParamBox.le_list[2].text()), ROUNDNUM)
            
            temp = vds_start
            while (temp <= vds_stop):
                self.vds_list.append(temp)
                temp = round((temp + vds_step), ROUNDNUM)
                
            if self.Collector_Drain_ParamBox.rbtn_list[1].isChecked():
                self.vds_list = np.concatenate([self.vds_list, np.flip(self.vds_list)])
                
            # calculate list for gate biases
            if self.Collector_Gate_ParamBox.rbtn_list[1].isChecked():
                text = self.Collector_Gate_ParamBox.le_list[0].text()
                self.vgs_list = [float(x) for x in text.split(',')]
                
            else:                
                vgs_start = round(float(self.Collector_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
                vgs_stop =  round(float(self.Collector_Gate_ParamBox.le_list[1].text()), ROUNDNUM)
                vgs_step =  round(float(self.Collector_Gate_ParamBox.le_list[2].text()), ROUNDNUM)     
                
                temp = vgs_start
                while (temp <= vgs_stop):
                    self.vgs_list.append(temp)
                    temp = round((temp + vgs_step), ROUNDNUM)   

            self.tot_num_measure_points = len(self.vds_list)*len(self.vgs_list)
            
            print ("Table prepared")
            
            print ("Preparing bias parameters")
            self.SMU_init_params = [[],[]]
            self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
            
            self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
            print ("Bias parameters:")
            print (self.SMU_init_params[0])
            print (self.SMU_init_params[1])
            
            
            
            
            print ("Prepare measurement...")
            # Prepare data array for save
            self.result_data = np.empty((self.tot_num_measure_points, 6))
            self.result_data[:] = np.NaN
            self.N = 0
            self.start = 0
            
            #Reset graph
            self.Collector_GraphBox.reset_plot()   
            
            # Initiate IO_Thread thread
            self.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
            self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                       scan_type = self.scan_type, 
                                       vds_list = self.vds_list, 
                                       vgs_list = self.vgs_list,
                                       wait_time = self.wait_time)
            self.IO_Thread.signal.connect(self.update_plot)
            self.LogBox.update_log("Measurement start!")
            self.IO_Thread.start()  
        
    def abort_measurement(self):
        self.IO_Thread.abort()
        
    def stop_measurement(self):
        self.LogBox.update_log("Measurement done!")
        self.result_data = self.result_data[0:self.N,:]
        print(self.result_data)
        if self.measurement_done_flag == True:
            self.LiveBox.set_status_idle()
        else:
            self.LiveBox.set_status_abort()
        
        self.LiveBox.set_values(['- V',' - A', '- V', '- A'])
        self.measurement_done_flag = False
        
        self.DataSettingsBox.save_recording(self.result_data)
                
        outputpath_jpg = '%s%s%s%s' %(self.DataSettingsBox.root.dirName, '/', self.DataSettingsBox.newfilename, '.jpg')
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        screenshot.save(outputpath_jpg, 'jpg')
        self.LogBox.update_log("Data saved to: %s%s%s%s" %(self.DataSettingsBox.root.dirName, '/', self.DataSettingsBox.newfilename, '.dat'))
        
        for i in range(self.tabtotalnum):
            self.tabs.setTabEnabled(i, True)
        
    def tab_change(self, i):
        if i == 0:
            self.scan_type = "Output"
            self.RunBox.btn_run.setText("Run (FET: Output)")
            self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
            self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        elif i == 1:
            self.scan_type = "Transfer"
            self.RunBox.btn_run.setText("Run (FET: Transfer)")
            self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Drain)")
            self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Gate)")
        elif i == 2:
            self.scan_type = "I-V"
            self.RunBox.btn_run.setText("Run (I-V)")
            self.ConnectionControlBox.lbl_list[0].setText("SMU1")
            self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Not used)")
        else:
            self.scan_type = "Collector"
            self.RunBox.btn_run.setText("Run (BJT: Collector C/C)")
            self.ConnectionControlBox.lbl_list[0].setText("SMU1 (Collector)")
            self.ConnectionControlBox.lbl_list[1].setText("SMU2 (Base)")
            
            
class IO_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(object)
    def __init__(self, SMU_list, SMU_init_params, scan_type = None, wait_time = None, vds_list = None, vgs_list = None, repeat_num = None, parent = None):
        QtCore.QThread.__init__(self, parent)
        print("IO Thread start")
        
        self.SMU_list = SMU_list
        self.SMU_init_params = SMU_init_params
        self.scan_type = scan_type
        self.vds_list = vds_list
        self.vgs_list = vgs_list
        self.repeat_num = repeat_num
        self.wait_time = wait_time
        
        self.flag = 1
        
    def init_SMU(self, SMU, Param_list):
        SMU.write("*RST")
        SMU.write(":SOUR:FUNC VOLT")
        SMU.write(":SOUR:VOLT:MODE FIXED")
        SMU.write(":SOUR:VOLT:RANG:AUTO ON") # auto source range
        SMU.write(":SENS:FUNC \"CURR\"")
        SMU.write(":SENS:CURR:RANG:AUTO ON") # auto current range     
        SMU.write(":TRIG:DEL ", str(Param_list[0]))
        SMU.write(":SOUR:DEL ", str(Param_list[1]))
        SMU.write(":SENS:CURR:NPLC ", str(Param_list[2]))
        SMU.write(":SENS:CURR:PROT ", str(Param_list[3]))   
        print("Setup SMU: %s as a voltage source is complete." %(SMU))
        
    def init_SMU_Curr(self, SMU, Param_list):
        SMU.write("*RST")
        SMU.write(":SOUR:FUNC CURR")
        SMU.write(":SOUR:CURR:MODE FIXED")
        SMU.write(":SOUR:CURR:RANG:AUTO ON") # auto source range
        SMU.write(":SENS:FUNC \"VOLT\"")
        SMU.write(":SENS:VOLT:RANG:AUTO ON")
        SMU.write(":TRIG:DEL ", str(Param_list[0]))
        SMU.write(":SOUR:DEL ", str(Param_list[1]))
        SMU.write(":SENS:VOLT:NPLC ", str(Param_list[2]))
        SMU.write(":SENS:VOLT:PROT ", str(Param_list[3]))  
        print("Setup SMU: %s as a current source is complete." %(SMU))
        
    def run(self):
        if self.scan_type == "Output":
            print("Scan type: %s" %(self.scan_type))
            self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
            self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
            
            self.SMU_DRAIN = self.SMU_list[0]
            self.SMU_GATE = self.SMU_list[1]
            
            new_curve = np.empty(6)
            new_curve[:] = np.NaN
            
            for vgs in self.vgs_list:
                if self.flag == 1:
                    self.signal.emit(new_curve) #Notify main function to draw a new curve
                    self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
                    self.SMU_GATE.write(":OUTP ON")
                else:
                    break;
                for vds in self.vds_list:
                    if self.flag == 1:
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                        self.SMU_DRAIN.write(":OUTP ON")
                        if vds == self.vds_list[0]:
                            time.sleep(self.wait_time)
                        CURRENT_GATE = self.SMU_GATE.query_ascii_values(":READ?")
                        CURRENT_DRAIN = self.SMU_DRAIN.query_ascii_values(":READ?")
                        CURRENT_GATE = CURRENT_GATE[1]
                        CURRENT_DRAIN = CURRENT_DRAIN[1]
    
                        temp = np.array([vgs, vds, CURRENT_GATE, CURRENT_DRAIN, np.log10(np.abs(CURRENT_GATE)), np.log10(np.abs(CURRENT_DRAIN))])

                        self.signal.emit(temp)
                    else:
                        break;
        
        elif self.scan_type == "Transfer":
            print("Scan type: %s" %(self.scan_type))
            self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
            self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
            
            self.SMU_DRAIN = self.SMU_list[0]
            self.SMU_GATE = self.SMU_list[1]
            
            new_curve = np.empty(6)
            new_curve[:] = np.NaN
            self.signal.emit(new_curve)
            
            for vds in self.vds_list:
                if self.flag == 1:
                    self.signal.emit(new_curve) #Notify main function to draw a new curve
                    self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                    self.SMU_DRAIN.write(":OUTP ON")
                else:
                    break;
                for vgs in self.vgs_list:
                    if self.flag == 1:
                        if vgs == self.vgs_list[0]:
                            time.sleep(self.wait_time)
                        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
                        self.SMU_GATE.write(":OUTP ON")
                        CURRENT_GATE = self.SMU_GATE.query_ascii_values(":READ?")
                        CURRENT_DRAIN = self.SMU_DRAIN.query_ascii_values(":READ?")
                        CURRENT_GATE = CURRENT_GATE[1]
                        CURRENT_DRAIN = CURRENT_DRAIN[1]
    
                        temp = np.array([vgs, vds, CURRENT_GATE, CURRENT_DRAIN, np.log10(np.abs(CURRENT_GATE)), np.log10(np.abs(CURRENT_DRAIN))])

                        self.signal.emit(temp)
                    else:
                        break;
                        
            
        elif self.scan_type == "I-V":
            print("Scan type: %s" %(self.scan_type))
            self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
            
            self.SMU_DRAIN = self.SMU_list[0]
            
            new_curve = np.empty(3)
            new_curve[:] = np.NaN
            self.signal.emit(new_curve)
            
            for i in range(self.repeat_num):
                if self.flag == 1:
                    self.signal.emit(new_curve) #Notify main function to draw a new curve
                else:
                    break;
                for vds in self.vds_list:
                    if self.flag == 1:
                        if vds == self.vds_list[0]:
                            time.sleep(self.wait_time)
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                        self.SMU_DRAIN.write(":OUTP ON")
                        CURRENT_DRAIN = self.SMU_DRAIN.query_ascii_values(":READ?")
                        CURRENT_DRAIN = CURRENT_DRAIN[1]
    
                        temp = np.array([vds, CURRENT_DRAIN, np.log10(np.abs(CURRENT_DRAIN))])

                        self.signal.emit(temp)
                    else:
                        break;
                        
        elif self.scan_type == "Collector":
            print("Scan type: %s" %(self.scan_type))
            self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
            self.init_SMU_Curr(self.SMU_list[1], self.SMU_init_params[1])
            
            self.SMU_COLLECTOR = self.SMU_list[0]
            self.SMU_BASE = self.SMU_list[1]
            
            new_curve = np.empty(6)
            new_curve[:] = np.NaN
            self.signal.emit(new_curve)
            
            # self.vgs_list = np.multiply(self.vgs_list, 1.0E-6)
            
            for vgs in self.vgs_list:
                if self.flag == 1:
                    vgs_str = str(vgs)+str("E-6")
                    print("Vgs value:")
                    print(vgs_str)
                    self.SMU_BASE.write(":SOUR:CURR:LEV ", vgs_str)
                    self.SMU_BASE.write(":OUTP ON")
                    self.signal.emit(new_curve) #Notify main function to draw a new curve
                else:
                    break;
                for vds in self.vds_list:
                    if self.flag == 1:
                        if vds == self.vds_list:
                            time.sleep(self.wait_time)
                        self.SMU_COLLECTOR.write(":SOUR:VOLT:LEV ", str(vds))
                        self.SMU_COLLECTOR.write(":OUTP ON")
                        CURRENT_GATE = self.SMU_BASE.query_ascii_values(":READ?")
                        CURRENT_DRAIN = self.SMU_COLLECTOR.query_ascii_values(":READ?")
                        print("gate reading")
                        print(CURRENT_GATE)
                        VOLTAGE_GATE = CURRENT_GATE[0]
                        CURRENT_GATE = CURRENT_GATE[1]
                        CURRENT_DRAIN = CURRENT_DRAIN[1]
    
                        temp = np.array([vgs, vds, VOLTAGE_GATE, CURRENT_DRAIN, np.log10(np.abs(CURRENT_GATE)), np.log10(np.abs(CURRENT_DRAIN))])

                        self.signal.emit(temp)
                    else:
                        break;
        self.stop()


    def stop(self):  
        self.signal.emit([9999,9999,9999,9999,9999,9999])  

        print("IO_Thread stop called") 
        if self.scan_type == "I-V":
            self.SMU_DRAIN.write("OUTP OFF")    
        elif self.scan_type == "Collector":
            self.SMU_BASE.write("OUTP OFF")
            self.SMU_COLLECTOR.write("OUTP OFF")
        else:
            self.SMU_DRAIN.write("OUTP OFF")
            self.SMU_GATE.write("OUTP OFF")
            
        self.quit()
        
    def abort(self):
        self.flag = 0
        


if __name__ == '__main__':

    """ Run the program    """

    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())