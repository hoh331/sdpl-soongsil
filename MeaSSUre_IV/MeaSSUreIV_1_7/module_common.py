# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""
import MeaSSUre_IV_UI_all_v1_7 as ui
# For Qt layout (GUI)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea)

# from pyqtgraph.Qt import QtCore
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

# General
import time
import numpy as np

# General

""" Round digit for converting float to int """
ROUNDNUM = 4
TIMER_INTERVAL = 10

class CreateClass_Super:
    def __init__(self, main_ui):
        self.main = main_ui
        self.tab_setup()
        
    def tab_setup(self):        
        print("tab_setup called, override this method")
        """ Override this method"""
    
    def update_plot(self, array):
        print("update_plot called, override this method")
        """ Override this method"""
        
    def run_measurement(self):        
        self.measurement_timer = QTimer()
        self.measurement_timer.setInterval(TIMER_INTERVAL)
        self.main.TimeDisplayBox.check_start_time()
        self.measurement_timer.timeout.connect(self.main.TimeDisplayBox.update_time_elapsed)
        self.measurement_timer.start(TIMER_INTERVAL)
        
        self.SMU_list = self.main.ConnectionControlBox.get_SMU_list()
        print("Run Measurement: %s" %(self.scan_type))
        self.main.LogBox.update_log("Run Measurement: %s" %(self.scan_type))
        
        for i in range(self.main.tabtotalnum):
            if i != self.main.tabs.currentIndex():
                self.main.tabs.setTabEnabled(i, False)
                
        print("Preparing tables of biasing values...")
        
        self.run_measurement_start()
        
    def run_measurement_start(self):     
        print("run_measurement_start called, override this method")
        """ Override this method"""

    def stop_measurement(self):
        self.main.LogBox.update_log("Measurement done!")
        self.measurement_timer.stop()
        self.result_data = self.result_data[0:self.N,:]
        print(self.result_data)
        if self.measurement_done_flag == True:
            self.main.LiveBox.set_status_idle()
        else:
            self.main.LiveBox.set_status_abort()
        
        self.main.LiveBox.set_values(['- V',' - A', '- V', '- A'])
        self.measurement_done_flag = False
        
        self.main.DataSettingsBox.save_recording(self.result_data)
                
        outputpath_jpg = '%s%s%s%s' %(self.main.DataSettingsBox.root.dirName, '/', self.main.DataSettingsBox.newfilename, '.jpg')
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.main.winId())
        screenshot.save(outputpath_jpg, 'jpg')
        self.main.LogBox.update_log("Data saved to: %s%s%s%s" %(self.main.DataSettingsBox.root.dirName, '/', self.main.DataSettingsBox.newfilename, '.dat'))
        
        self.enable_tab_all()

    def abort_measurement(self):
        self.IO_Thread.abort()
        self.enable_tab_all()
            
    def enable_tab_all(self):
        for i in range(self.main.tabtotalnum):
            self.main.tabs.setTabEnabled(i, True)

class IO_Thread_Super(QtCore.QThread):
    signal = QtCore.pyqtSignal(object)
    def __init__(self, SMU_list, SMU_init_params, scan_type = None,
                 wait_time = None, vds_list = None, vgs_list = None, 
                 repeat_num = None, pulse_width = None, stress_time_list = None,
                 stress_vgs = None, stress_vds = None, parent = None, 
                 pulse_width_program = None, pulse_width_erase = None,
                 pulse_width_read = None, pulse_start = None, pulse_amp = None,
                 pulse_target = None, time_step = None, pulse_to_pulse_delay = None,
                 num_pulses = None, **kwargs):
        
        QtCore.QThread.__init__(self, parent)
        print("IO Thread start")
        
        self.SMU_list = SMU_list
        self.SMU_init_params = SMU_init_params
        self.scan_type = scan_type
        self.vds_list = vds_list
        self.vgs_list = vgs_list
        self.repeat_num = repeat_num
        self.wait_time = wait_time
        self.pulse_width = pulse_width
        self.stress_time_list = stress_time_list
        self.stress_vgs = stress_vgs
        self.stress_vds = stress_vds
        self.pulse_width_program = pulse_width_program
        self.pulse_width_erase = pulse_width_erase
        self.pulse_width_read = pulse_width_read
        self.pulse_start = pulse_start
        self.pulse_amp = pulse_amp
        self.pulse_target = pulse_target
        self.time_step = time_step
        self.pulse_to_pulse_delay = pulse_to_pulse_delay
        self.num_pulses = num_pulses
        
        self.flag = 1
        self.kwargs = kwargs
        
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
        print("run(IO thread) called, override this method")
        """ Override this method"""

    def stop(self):  
        self.signal.emit([99999999,99999999,99999999,99999999,99999999,99999999])  

        print("IO_Thread stop called") 
        self.SMU_DRAIN.write("OUTP OFF")
        self.SMU_GATE.write("OUTP OFF")
            
        self.quit()
        
    def abort(self):
        self.flag = 0
        
    def take_positive(self, value):
        if value > 0:
            return value
        else:
            return 0