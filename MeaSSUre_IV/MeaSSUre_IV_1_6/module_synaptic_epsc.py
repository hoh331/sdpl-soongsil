# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):        
    def tab_setup(self):
        self.tab = QWidget()   
        self.scan_type = "EPSC"
        
        """EPSC Tab Setup"""            
        self.EPSC_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain bias setup', 9)
        self.EPSC_Drain_ParamBox.set_item(0, 'Vds', '1', 'V')
        self.EPSC_Drain_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.EPSC_Drain_ParamBox.show_only_name(1)
        self.EPSC_Drain_ParamBox.set_item(2, 'Drain Auto Zero', '0', '0: OFF/1: ON')
        self.EPSC_Drain_ParamBox.set_item(3, 'Drain Voltage source range', '20', 'V')        
        self.EPSC_Drain_ParamBox.set_item(4, 'Drain Current sensing range', '100E-6', 'A')        
        self.EPSC_Drain_ParamBox.set_item(5, 'Drain trigger delay', '0.0', 's')
        self.EPSC_Drain_ParamBox.set_item(6, 'Drain source delay', '0.0', 's')
        self.EPSC_Drain_ParamBox.set_item(7, 'Drain NPLC', '1', 'number')
        self.EPSC_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.EPSC_Gate_ParamBox = ui.CreateParameterSettingsBox('Gate bias setup', 9)
        self.EPSC_Gate_ParamBox.set_item(0, 'Vgs', '0', 'V')
        self.EPSC_Gate_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.EPSC_Gate_ParamBox.show_only_name(1)
        self.EPSC_Gate_ParamBox.set_item(2, 'Gate Auto Zero', '0', '0: OFF/1: ON')
        self.EPSC_Gate_ParamBox.set_item(3, 'Gate Voltage source range', '20', 'V')        
        self.EPSC_Gate_ParamBox.set_item(4, 'Gate Current sensing range', '100E-6', 'A')   
        self.EPSC_Gate_ParamBox.set_item(5, 'Gate trigger delay', '0.0', 's')
        self.EPSC_Gate_ParamBox.set_item(6, 'Gate source delay', '0.0', 's')
        self.EPSC_Gate_ParamBox.set_item(7, 'Gate NPLC', '1', 'number')
        self.EPSC_Gate_ParamBox.set_item(8, 'Current compliance', '100E-3', 'A')
                
        self.EPSC_Pulse_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Pulse setup', 6, 2, layout = "vertical")
        self.EPSC_Pulse_ParamBox.set_toggle_item(0, "Drain (Memristor/Memtransistor)", 1)
        self.EPSC_Pulse_ParamBox.set_toggle_item(1, "Gate (Synaptic Transistor)", 0)
        self.EPSC_Pulse_ParamBox.set_item(0, 'Measurement time', '10', 's')
        self.EPSC_Pulse_ParamBox.set_item(1, 'Pulse amplitude', '1', 'V')
        self.EPSC_Pulse_ParamBox.set_item(2, 'Pulse start point', '3', 's')
        self.EPSC_Pulse_ParamBox.set_item(3, 'Pulse duration', '100', 'ms')
        self.EPSC_Pulse_ParamBox.set_item(4, 'Delay before sweep starts', '1', 's')
        self.EPSC_Pulse_ParamBox.set_item(5, 'Measurement time step', '50', 'ms')
        
        self.EPSC_GraphBox = ui.CreateGraphBox('EPSC characteristics', 2)
        self.EPSC_GraphBox.set_titles(0, 'EPSC curves (Ids-Vds)', 'Time (s)', 'Ids (A)')        
        self.EPSC_GraphBox.set_titles(1, 'EPSC curves (leakage) (Igs-Vds)', 'Time (s)', 'Igs (A)')
        
        
        # tab setup
        self.tab_hbox = QHBoxLayout()  
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox.addWidget(self.EPSC_Drain_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.EPSC_Gate_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.EPSC_Pulse_ParamBox.groupbox)
        self.tab_vbox.addStretch(1)
        self.tab_hbox.addLayout(self.tab_vbox)
        self.tab_hbox.addWidget(self.EPSC_GraphBox.groupbox)
        self.tab_hbox.setStretch(0,1)
        self.tab_hbox.setStretch(1,4)
        self.tab.setLayout(self.tab_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("EPSC module loaded")
      
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.EPSC_GraphBox.addnew_plot(0)
                self.EPSC_GraphBox.addnew_plot(1)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.EPSC_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                self.EPSC_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,4])
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
        vds_start = round(float(self.EPSC_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
        self.vds_list.append(vds_start)          
        vgs_start = round(float(self.EPSC_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
        self.vgs_list.append(vgs_start)        
        
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[]]
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.EPSC_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.EPSC_Gate_ParamBox.le_list[-5].text()), ROUNDNUM))
        print ("Bias parameters:")
        print (self.SMU_init_params[0])
        print (self.SMU_init_params[1])
        
        self.stress_time_list = round(float(self.EPSC_Pulse_ParamBox.le_list[0].text()), ROUNDNUM)
        self.pulse_amp = round(float(self.EPSC_Pulse_ParamBox.le_list[1].text()), ROUNDNUM)
        self.pulse_start = round(float(self.EPSC_Pulse_ParamBox.le_list[2].text()), ROUNDNUM)
        self.pulse_width = int(round(float(self.EPSC_Pulse_ParamBox.le_list[3].text()), ROUNDNUM))
        self.wait_time = round(float(self.EPSC_Pulse_ParamBox.le_list[4].text()), ROUNDNUM)
        self.time_step = round(float(self.EPSC_Pulse_ParamBox.le_list[5].text()), ROUNDNUM)
        
        self.pulse_target = self.EPSC_Pulse_ParamBox.rbtn_list[0].isChecked()
        
        self.tot_num_measure_points = int(self.stress_time_list*1000.0/self.pulse_width)+10000
        
        print ("Prepare measurement...")
        # Prepare data array for save
        self.result_data = np.empty((self.tot_num_measure_points, 5))
        self.result_data[:] = np.NaN
        self.N = 0
        self.start = 0
        
        #Reset graph
        self.EPSC_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   wait_time = self.wait_time,
                                   pulse_width = self.pulse_width,
                                   stress_time_list = self.stress_time_list,
                                   pulse_start = self.pulse_start,
                                   pulse_amp = self.pulse_amp,
                                   pulse_target = self.pulse_target,
                                   time_step = self.time_step)
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()  

class IO_Thread(IO_Thread_Super):                
    def run(self):
        def repeating_measurement():
            if self.flag == 1:
                CURRENT_TIME = time.time()-self.start_time
                if CURRENT_TIME > self.stress_time_list:
                    self.flag = 0
                else:
                    if CURRENT_TIME < self.pulse_start:
                        print("before pulse")
                        CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                        CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                        temp = np.array([CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                        self.signal.emit(temp)
                    elif CURRENT_TIME >= self.pulse_start and CURRENT_TIME <self.pulse_finish:
                        print("during pulse")
                        if self.pulse_target == 1:
                            self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vdsamp))
                            self.SMU_DRAIN.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            temp = np.array([CURRENT_TIME, vdsamp, CURRENT_DRAIN, vgs, CURRENT_GATE])
                            self.signal.emit(temp)
                        else:
                            self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgsamp))
                            self.SMU_GATE.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            temp = np.array([CURRENT_TIME, vds, CURRENT_DRAIN, vgsamp, CURRENT_GATE])
                            self.signal.emit(temp)
                    else:
                        print("after pulse")
                        if self.pulse_target == 1:
                            self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                            self.SMU_DRAIN.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            temp = np.array([CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                            self.signal.emit(temp)
                        else:
                            self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
                            self.SMU_GATE.write(":OUTP ON")
                            CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                            CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1] 
                            temp = np.array([CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                            self.signal.emit(temp)                                 
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
    
        
        vds = self.vds_list[0]
        vgs = self.vgs_list[0]
        self.pulse_finish = self.pulse_start + self.pulse_width/1000.0
        
        print("Pulse start time: %.2f" %(self.pulse_start))
        print("Pulse finish time: %.2f" %(self.pulse_finish))
        vgsamp = vgs
        vdsamp = vds
        if self.pulse_target == 1:
            vdsamp = vds + self.pulse_amp
        else:
            vgsamp = vgs + self.pulse_amp
        
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

        time.sleep(self.wait_time)
        self.start_time = time.time()
        timer.start(self.time_step)
        self.exec_()
            
   
        