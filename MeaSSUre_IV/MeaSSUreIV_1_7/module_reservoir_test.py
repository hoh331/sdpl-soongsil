# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):        
    def tab_setup(self):
        self.tab = QWidget()   
        self.scan_type = "Reservoir_Test"
        
        """EPSC_PPF Tab Setup"""            
        self.RC_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain bias setup', 9)
        self.RC_Drain_ParamBox.set_item(0, 'Vds', '1', 'V')
        self.RC_Drain_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.RC_Drain_ParamBox.show_only_name(1)
        self.RC_Drain_ParamBox.set_item(2, 'Drain Auto Zero', '0', '0: OFF/1: ON')
        self.RC_Drain_ParamBox.set_item(3, 'Drain Voltage source range', '20', 'V')        
        self.RC_Drain_ParamBox.set_item(4, 'Drain Current sensing range', '100E-6', 'A')        
        self.RC_Drain_ParamBox.set_item(5, 'Drain trigger delay', '0.0', 's')
        self.RC_Drain_ParamBox.set_item(6, 'Drain source delay', '0.0', 's')
        self.RC_Drain_ParamBox.set_item(7, 'Drain NPLC', '1', 'number')
        self.RC_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.RC_Gate_ParamBox = ui.CreateParameterSettingsBox('Gate bias setup', 9)
        self.RC_Gate_ParamBox.set_item(0, 'Vgs', '0', 'V')
        self.RC_Gate_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.RC_Gate_ParamBox.show_only_name(1)
        self.RC_Gate_ParamBox.set_item(2, 'Gate Auto Zero', '0', '0: OFF/1: ON')
        self.RC_Gate_ParamBox.set_item(3, 'Gate Voltage source range', '20', 'V')        
        self.RC_Gate_ParamBox.set_item(4, 'Gate Current sensing range', '100E-6', 'A')   
        self.RC_Gate_ParamBox.set_item(5, 'Gate trigger delay', '0.0', 's')
        self.RC_Gate_ParamBox.set_item(6, 'Gate source delay', '0.0', 's')
        self.RC_Gate_ParamBox.set_item(7, 'Gate NPLC', '1', 'number')
        self.RC_Gate_ParamBox.set_item(8, 'Current compliance', '100E-3', 'A')
        
        self.RC_External_ParamBox = ui.CreateParameterSettingsBox('External SMU setup', 7)
        self.RC_External_ParamBox.set_item(0, 'External Auto Zero', '0', '0: OFF/1: ON')
        self.RC_External_ParamBox.set_item(1, 'External Voltage source range', '20', 'V')        
        self.RC_External_ParamBox.set_item(2, 'External Current sensing range', '100E-6', 'A')   
        self.RC_External_ParamBox.set_item(3, 'External trigger delay', '0.0', 's')
        self.RC_External_ParamBox.set_item(4, 'External source delay', '0.0', 's')
        self.RC_External_ParamBox.set_item(5, 'External NPLC', '1', 'number')
        self.RC_External_ParamBox.set_item(6, 'Current compliance', '100E-3', 'A')   
                
        self.RC_Pulse_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Pulse setup', 7, 3, layout = "vertical")
        self.RC_Pulse_ParamBox.set_toggle_item(0, "Gate (Synaptic Transistor)", 1)
        self.RC_Pulse_ParamBox.set_toggle_item(1, "Drain (Memristor/Memtransistor)", 0)
        self.RC_Pulse_ParamBox.set_toggle_item(2, "External (Photonic Synaptic Transistor)", 0)        
        self.RC_Pulse_ParamBox.set_item(0, 'Number of pixels', '4', '#')
        self.RC_Pulse_ParamBox.set_item(1, 'Pulse amplitude', '1', 'V')
        self.RC_Pulse_ParamBox.set_item(2, 'Pulse duration', '100', 'ms')
        self.RC_Pulse_ParamBox.set_item(3, 'Delay between pulses', '100', 'ms')
        self.RC_Pulse_ParamBox.set_item(4, 'Pre-recording before sweep', '1', 's')
        self.RC_Pulse_ParamBox.set_item(5, 'Post-recording after sweep', '1', 's')
        self.RC_Pulse_ParamBox.set_item(6, 'Time step', '50', 'ms')
        
        self.RC_GraphBox = ui.CreateGraphBox('EPSC_PPF characteristics', 3, placement_orientation = 'vertical')
        self.RC_GraphBox.set_titles(0, 'RC profile', 'Time (s)', 'Bias (V)')
        self.RC_GraphBox.set_titles(1, 'RC response', 'Time (s)', 'Ids (A)')        
        self.RC_GraphBox.set_titles(2, 'Gate leakage', 'Time (s)', 'Igs (A)')
        
        
        # tab setup
        self.tab_hbox = QHBoxLayout()  
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox2 = QVBoxLayout()
        self.tab_vbox.addWidget(self.RC_Drain_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.RC_Gate_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.RC_External_ParamBox.groupbox)
        self.tab_vbox.addStretch(1)
        
        self.tab_vbox2.addWidget(self.RC_Pulse_ParamBox.groupbox)
        self.tab_vbox2.addStretch(1)
                
        
        self.tab_hbox.addLayout(self.tab_vbox)
        self.tab_hbox.addLayout(self.tab_vbox2)
        self.tab_hbox.addWidget(self.RC_GraphBox.groupbox)
        self.tab_hbox.setStretch(0,1)
        self.tab_hbox.setStretch(1,1)
        self.tab_hbox.setStretch(2,3)
        self.tab.setLayout(self.tab_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("Reservoir test module loaded")
      
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.RC_GraphBox.addnew_plot(0)
                self.RC_GraphBox.addnew_plot(1)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.RC_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                self.RC_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,4])
                # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[2], 'A'), '%.4e%s' %(array[3], 'V'), '%.4e%s' %(array[4], 'A')])

    def run_measurement_start(self):      
        # Calculate sweep points
        self.vds_list = []
        self.vgs_list = []
        
        
        # Calculate list for drain biases
        vds_start = round(float(self.RC_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
        self.vds_list.append(vds_start)          
        vgs_start = round(float(self.RC_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
        self.vgs_list.append(vgs_start)        
        
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[],[]]
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.RC_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.RC_Gate_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.RC_External_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        print ("Bias parameters:")
        print (self.SMU_init_params[0])
        print (self.SMU_init_params[1])
        print (self.SMU_init_params[2])
        
        self.num_pixel = round(float(self.RC_Pulse_ParamBox.le_list[0].text()), ROUNDNUM)
        self.pulse_amp = round(float(self.RC_Pulse_ParamBox.le_list[1].text()), ROUNDNUM)
        self.pulse_width = int(round(float(self.RC_Pulse_ParamBox.le_list[2].text()), ROUNDNUM))
        self.pulse_to_pulse_delay = round(float(self.RC_Pulse_ParamBox.le_list[3].text()), ROUNDNUM)        
        self.pre_record_time = round(float(self.RC_Pulse_ParamBox.le_list[4].text()), ROUNDNUM)
        self.post_record_time = round(float(self.RC_Pulse_ParamBox.le_list[5].text()), ROUNDNUM)
        self.time_step = round(float(self.RC_Pulse_ParamBox.le_list[5].text()), ROUNDNUM)
                
        # Calculate list for drain biases
        for i in range (3):
            if self.RC_Pulse_ParamBox.rbtn_list[i].isChecked():
                self.pulse_target = i
        
        print("Pulse SMU index = %d" %(self.pulse_target))
        
        self.total_stress_time = self.pre_record_time + self.post_record_time + self.num_pixel*(self.pulse_width+self.pulse_to_pulse_delay)
        self.tot_num_measure_points = int(self.total_stress_time*1000.0/self.time_step)+10000
        
        print ("Prepare measurement...")
        # Prepare data array for save
        if self.pulse_target == 0 or self.pulse_target == 1:
            self.result_data = np.empty((self.tot_num_measure_points, 6)) # Save V, I data of SMU_SOURCE, SMU_GATE
        else:
            self.result_data = np.empty((self.tot_num_measure_points, 8)) # Save V, I data from SMU_EXT
            
        self.result_data[:] = np.NaN
        self.N = 0
        self.start = 0
        
        #Reset graph
        self.RC_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   num_pixel = self.num_pixel,
                                   pulse_amp = self.pulse_amp,
                                   pulse_width = self.pulse_width,
                                   pulse_to_pulse_delay = self.pulse_to_pulse_delay,
                                   pre_record_time = self.pre_record_time,
                                   post_record_time = self.post_record_time,
                                   time_step = self.time_step,                         
                                   pulse_target = self.pulse_target
                                   ) 
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()  


class IO_Thread(IO_Thread_Super):  
    def __init__(self, SMU_list, SMU_init_params, scan_type = None,
                 vds_list = None, vgs_list = None, num_pixel = None,
                 pulse_amp = None, pulse_width = None, pulse_to_pulse_delay = None,
                 pre_record_time = None, post_record_time = None, time_step = None,
                 pulse_target = None, **kwargs):
        
        QtCore.QThread.__init__(self)
        print("IO Thread start")
        
        self.SMU_list = SMU_list
        self.SMU_init_params = SMU_init_params
        self.scan_type = scan_type

        self.vds_list = vds_list
        self.vgs_list = vgs_list
        self.num_pixel = int(num_pixel)
        
        self.pulse_amp = pulse_amp
        self.pulse_width = pulse_width
        self.pulse_to_pulse_delay = pulse_to_pulse_delay
        self.pre_record_time = pre_record_time
        self.post_record_time = post_record_time
        self.time_step = time_step
        self.pulse_target = pulse_target

        self.flag = 1 # If measurment is done (or aborted) 0: aborted, 1: running
        self.series_num = 0 # current cycle (0 ~ 2**num_pixel)
        
    def is_pulse_rightnow(self, current_time, pulse_time_list, pulse_width):
        pulse_width = pulse_width/1000.0
        for pulse_time in pulse_time_list:
            if current_time >= pulse_time and current_time < pulse_time + pulse_width:
                return True
                break            
        return False    
                
    def run(self):          
        def repeating_measurement():
            if self.flag == 1:
                CURRENT_TIME = time.time() - self.start_time
                
                if CURRENT_TIME > self.stress_time_list:
                    self.series_num = self.series_num + 1                        
                    self.start_time = time.time()
                    CURRENT_TIME = time.time() - self.start_time
                    
                if self.series_num < 2**self.num_pixel:
                    if bool(self.pulse_time_list_full[self.series_num]):
                        if self.is_pulse_rightnow(CURRENT_TIME, self.pulse_time_list_full[self.series_num], self.pulse_width):
                            if self.pulse_target == 0: # Pulse to gate                       
                                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgsamp))
                                self.SMU_GATE.write(":OUTP ON")
                                CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                                CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                                temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgsamp, CURRENT_GATE])
                                self.signal.emit(temp)
                            
                            elif self.pulse_target == 1: # Pulse to drain
                                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vdsamp))
                                self.SMU_DRAIN.write(":OUTP ON")
                                CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                                CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                                temp = np.array([self.series_num, CURRENT_TIME, vdsamp, CURRENT_DRAIN, vgs, CURRENT_GATE])
                                self.signal.emit(temp)
                                
                            else: # Pulse from external source
                                self.SMU_EXT.write(":SOUR:VOLT:LEV ", str(extamp))
                                self.SMU_EXT.write(":OUTP ON")
                                CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                                CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1]
                                CURRENT_EXT = (self.SMU_EXT.query_ascii_values(":READ?"))[1]
                                temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE, extamp, CURRENT_EXT])
                                self.signal.emit(temp)
    
                        else:
                            if self.pulse_target == 0: # Pulse to gate 
                                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
                                self.SMU_GATE.write(":OUTP ON")
                                CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                                CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                                temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                                self.signal.emit(temp)  
                            
                            elif self.pulse_target == 1: # Pulse to drain
                                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                                self.SMU_DRAIN.write(":OUTP ON")
                                CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                                CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                                temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                                self.signal.emit(temp)
                                
                            else: # Pulse from external source
                                self.SMU_EXT.write(":SOUR:VOLT:LEV ", str(ext))
                                self.SMU_EXT.write(":OUTP ON")
                                CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                                CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                                CURRENT_EXT = (self.SMU_EXT.query_ascii_values(":READ?"))[1]
                                temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE, ext, CURRENT_EXT])
                                self.signal.emit(temp)   
                                
                    else:
                        if self.pulse_target == 0: # Pulse to gate 
                            self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
                            self.SMU_GATE.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                            self.signal.emit(temp)  
                        
                        elif self.pulse_target == 1: # Pulse to drain
                            self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                            self.SMU_DRAIN.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                            self.signal.emit(temp)
                            
                        else: # Pulse from external source
                            self.SMU_EXT.write(":SOUR:VOLT:LEV ", str(ext))
                            self.SMU_EXT.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            CURRENT_EXT = (self.SMU_EXT.query_ascii_values(":READ?"))[1]
                            temp = np.array([self.series_num, CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE, ext, CURRENT_EXT])
                            self.signal.emit(temp)   
                        
                else:
                    self.flag = 0                                
            else:
                timer.stop()
                self.stop()  
            
        print("Scan type: %s" %(self.scan_type))
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
        
        self.SMU_DRAIN = self.SMU_list[0]
        self.SMU_GATE = self.SMU_list[1]
    
        self.SMU_DRAIN.write(":SYST:AZER:STAT ", str(self.SMU_init_params[0][4])) #Disable autozero
        self.SMU_GATE.write(":SYST:AZER:STAT ", str(self.SMU_init_params[1][4])) #Disable autozero
        
        # Fix source & measure range
        self.SMU_DRAIN.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[0][5]))
        self.SMU_DRAIN.write(":SENS:CURR:RANG ", str(self.SMU_init_params[0][6]))     
        self.SMU_GATE.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[1][5]))
        self.SMU_GATE.write(":SENS:CURR:RANG ", str(self.SMU_init_params[1][6]))    
        
        if self.pulse_target == 2:
            self.init_SMU(self.SMU_list[2], self.SMU_init_params[2])
            self.SMU_EXT = self.SMU_list[2]
            self.SMU_EXT.write(":SYST:AZER:STAT ", str(self.SMU_init_params[2][4])) #Disable autozero 
            self.SMU_EXT.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[2][5]))
            self.SMU_EXT.write(":SENS:CURR:RANG ", str(self.SMU_init_params[2][6])) 
    
        
        self.pulse_list = np.zeros((int(round(2**self.num_pixel)), self.num_pixel))
        pulse_unit_time = round(self.pulse_width/1000.0+self.pulse_to_pulse_delay/1000.0, 4)
        
        for i in range (int(2**self.num_pixel)):
            temp = i
            for j in range (self.num_pixel):
                digit, remainder = np.divmod(temp, 2**(self.num_pixel-j-1))
                self.pulse_list[i][j] = digit
                temp = remainder
        
        self.pulse_time_list = np.zeros(self.num_pixel)
        
        for i in range (self.num_pixel):
                self.pulse_time_list[i] = self.pre_record_time + i*pulse_unit_time
        
        self.pulse_time_list_full = []
        for i in range (int(2**self.num_pixel)):
            self.pulse_time_list_full.append([])
            for j in range (self.num_pixel):
                if self.pulse_list[i][j] == 1:
                    self.pulse_time_list_full[i].append(self.pulse_time_list[j])
        
        print("Pulse time list")
        print(self.pulse_time_list_full)
        
        self.stress_time_list = self.pre_record_time + self.post_record_time + self.num_pixel*pulse_unit_time
        print(f'Total measurement time per sequence: {self.stress_time_list}')
        
        vds = self.vds_list[0]
        vgs = self.vgs_list[0]
        ext = 0.0

        vgsamp = vgs
        vdsamp = vds
        extamp = ext        

        if self.pulse_target == 0:
            vgsamp = vgs + self.pulse_amp
        elif self.pulse_target == 1:
            vdsamp = vds + self.pulse_amp
        else:
            extamp = ext + self.pulse_amp
        
        timer = QTimer()
        timer.setTimerType(QtCore.Qt.PreciseTimer)
        timer.timeout.connect(repeating_measurement)
        
        new_curve = np.empty(5)
        new_curve[:] = np.NaN
        self.time_step = int(self.time_step)
        self.signal.emit(new_curve)
        
        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
        self.SMU_GATE.write(":OUTP ON")
        
        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
        self.SMU_DRAIN.write(":OUTP ON")        
        
        if self.pulse_target == 2:
            self.SMU_EXT.write(":SOUR:VOLT:LEV ", str(ext))
            self.SMU_EXT.write(":OUTP ON")  
            
        self.start_time = time.time()
        timer.start(self.time_step)
        print(f'Timer started with time step of {self.time_step}')
        self.exec_()
            
    def stop(self):  
        self.signal.emit([99999999,99999999,99999999,99999999,99999999,99999999])  

        print("IO_Thread stop called") 
        self.SMU_DRAIN.write("OUTP OFF")
        self.SMU_GATE.write("OUTP OFF")
        if self.pulse_target == 2:
            self.SMU_EXT.write("OUTP OFF")
            
        self.quit()
   
        