# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):        
    def tab_setup(self):
        self.tab = QWidget()   
        self.scan_type = "2T0C DRAM operation"
        
        """EPSC_PPF Tab Setup"""    
        self.TTZC_RT_Drain_ParamBox = ui.CreateParameterSettingsBox('2T0C Write Transistor Drain bias setup', 7)
        self.TTZC_RT_Drain_ParamBox.set_item(0, 'Write Tr Drain Auto Zero', '0', '0: OFF/1: ON')
        self.TTZC_RT_Drain_ParamBox.set_item(1, 'Write Tr Drain Voltage source range', '20', 'V')        
        self.TTZC_RT_Drain_ParamBox.set_item(2, 'Write Tr Drain Current sensing range', '100E-6', 'A')        
        self.TTZC_RT_Drain_ParamBox.set_item(3, 'Write Tr Drain trigger delay', '0.0', 's')
        self.TTZC_RT_Drain_ParamBox.set_item(4, 'Write Tr Drain source delay', '0.0', 's')
        self.TTZC_RT_Drain_ParamBox.set_item(5, 'Write Tr Drain NPLC', '1', 'number')
        self.TTZC_RT_Drain_ParamBox.set_item(6, 'Write Tr Current compliance', '10E-3', 'A')
        
        self.TTZC_WT_Drain_ParamBox = ui.CreateParameterSettingsBox('2T0C Read Transistor Drain SMU setup', 7)
        self.TTZC_WT_Drain_ParamBox.set_item(0, 'Read Tr Drain Auto Zero', '0', '0: OFF/1: ON')
        self.TTZC_WT_Drain_ParamBox.set_item(1, 'Read Tr Drain Voltage source range', '20', 'V')        
        self.TTZC_WT_Drain_ParamBox.set_item(2, 'Read Tr Drain Current sensing range', '100E-6', 'A')   
        self.TTZC_WT_Drain_ParamBox.set_item(3, 'Read Tr Drain trigger delay', '0.0', 's')
        self.TTZC_WT_Drain_ParamBox.set_item(4, 'Read Tr Drain source delay', '0.0', 's')
        self.TTZC_WT_Drain_ParamBox.set_item(5, 'Read Tr Drain NPLC', '1', 'number')
        self.TTZC_WT_Drain_ParamBox.set_item(6, 'Read Tr DrainCurrent compliance', '10E-3', 'A')
        
        self.TTZC_WT_Gate_ParamBox = ui.CreateParameterSettingsBox('2T0C Write Transistor Gate SMU setup', 7)
        self.TTZC_WT_Gate_ParamBox.set_item(0, 'Write Tr Gate Auto Zero', '0', '0: OFF/1: ON')
        self.TTZC_WT_Gate_ParamBox.set_item(1, 'Write Tr Gate Voltage source range', '20', 'V')        
        self.TTZC_WT_Gate_ParamBox.set_item(2, 'Write Tr Gate Current sensing range', '100E-6', 'A')   
        self.TTZC_WT_Gate_ParamBox.set_item(3, 'Write Tr Gate trigger delay', '0.0', 's')
        self.TTZC_WT_Gate_ParamBox.set_item(4, 'Write Tr Gate source delay', '0.0', 's')
        self.TTZC_WT_Gate_ParamBox.set_item(5, 'Write Tr Gate NPLC', '1', 'number')
        self.TTZC_WT_Gate_ParamBox.set_item(6, 'Write Tr Gate Current compliance', '10E-3', 'A')   
                
        self.TTZC_Operation_Pulse_ParamBox = ui.CreateParameterSettingsBox('Pulse setup', 11)   
        self.TTZC_Operation_Pulse_ParamBox.set_item(0, 'Write Tr Drain (WBL) Bias', '5', 'V')
        self.TTZC_Operation_Pulse_ParamBox.set_item(1, 'Read Tr Drain (RWL) Bias', '1', 'V')
        self.TTZC_Operation_Pulse_ParamBox.set_item(2, 'Write Tr Gate (WWL) Bias', '0', 'V')
        self.TTZC_Operation_Pulse_ParamBox.set_item(3, 'Measurement time', '10', 's')
        self.TTZC_Operation_Pulse_ParamBox.set_item(4, 'Pulse amplitude', '5', 'V')
        self.TTZC_Operation_Pulse_ParamBox.set_item(5, 'Pulse start point', '3', 's')
        self.TTZC_Operation_Pulse_ParamBox.set_item(6, 'Pulse duration', '100', 'ms')
        self.TTZC_Operation_Pulse_ParamBox.set_item(7, 'Pre-pulse biasing time', '100', 'ms')
        self.TTZC_Operation_Pulse_ParamBox.set_item(8, 'Post-pulse biasing time', '100', 'ms')        
        self.TTZC_Operation_Pulse_ParamBox.set_item(9, 'Delay before sweep starts', '1', 's')
        self.TTZC_Operation_Pulse_ParamBox.set_item(10, 'Measurement time step', '50', 'ms')
        
        self.TTZC_GraphBox = ui.CreateGraphBox('2T0C characteristics', 4, placement_orientation = 'vertical')
        self.TTZC_GraphBox.set_titles(0, '2T0C WBL Voltage-Time curve', 'Time (s)', 'V_WBL (V)')        
        self.TTZC_GraphBox.set_titles(1, '2T0C_WWL Voltage-Time curve', 'Time (s)', 'V_WWL (V)')   
        self.TTZC_GraphBox.set_titles(2, '2T0C_RWL Voltage-Time curve', 'Time (s)', 'V_RWL (V)')
        self.TTZC_GraphBox.set_titles(3, '2T0C_RTr Current-Time curve', 'Time (s)', 'I_RWL (A)')
        
        
        # tab setup
        self.tab_hbox = QHBoxLayout()  
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox2 = QVBoxLayout()
        self.tab_vbox.addWidget(self.TTZC_RT_Drain_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.TTZC_WT_Drain_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.TTZC_WT_Gate_ParamBox.groupbox)
        self.tab_vbox.addStretch(1)
        
        self.tab_vbox2.addWidget(self.TTZC_Operation_Pulse_ParamBox.groupbox)
        self.tab_vbox2.addStretch(1)
                
        
        self.tab_hbox.addLayout(self.tab_vbox)
        self.tab_hbox.addLayout(self.tab_vbox2)
        self.tab_hbox.addWidget(self.TTZC_GraphBox.groupbox)
        self.tab_hbox.setStretch(0,1)
        self.tab_hbox.setStretch(1,1)
        self.tab_hbox.setStretch(2,3)
        self.tab.setLayout(self.tab_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("EPSC_PPF module loaded")
      
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.TTZC_GraphBox.addnew_plot(0)
                self.TTZC_GraphBox.addnew_plot(1)
                self.TTZC_GraphBox.addnew_plot(2)
                self.TTZC_GraphBox.addnew_plot(3)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.TTZC_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,3])
                self.TTZC_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,5])
                self.TTZC_GraphBox.update_plot(2, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,1])
                self.TTZC_GraphBox.update_plot(3, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                # self.main.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[2], 'A'), '%.4e%s' %(array[3], 'V'), '%.4e%s' %(array[4], 'A')])

    def run_measurement_start(self):      
        # Calculate sweep points
        self.wt_drain_bias_list = []
        self.rt_drain_bias_list = []
        self.wt_gate_bias_list = []
        
        # Calculate list for drain biases       
        wt_drain_bias_start = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[0].text()), ROUNDNUM)
        self.wt_drain_bias_list.append(wt_drain_bias_start)    
        rt_drain_bias_start = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[1].text()), ROUNDNUM)
        self.rt_drain_bias_list.append(rt_drain_bias_start) 
        wt_gate_bias_start = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[2].text()), ROUNDNUM)
        self.wt_gate_bias_list.append(wt_gate_bias_start)        
        
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[],[]]
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.TTZC_RT_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.TTZC_WT_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.TTZC_WT_Gate_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        print ("Bias parameters:")
        print (self.SMU_init_params[0])
        print (self.SMU_init_params[1])
        print (self.SMU_init_params[2])
        
        self.stress_time_list = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[3].text()), ROUNDNUM)
        self.pulse_amp = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[4].text()), ROUNDNUM)
        self.pulse_start = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[5].text()), ROUNDNUM)
        self.pulse_width = int(round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[6].text()), ROUNDNUM))
        self.pre_pulse_bias_time = int(round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[7].text()), ROUNDNUM))
        self.post_pulse_bias_time = int(round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[8].text()), ROUNDNUM))        
        self.wait_time = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[9].text()), ROUNDNUM)
        self.time_step = round(float(self.TTZC_Operation_Pulse_ParamBox.le_list[10].text()), ROUNDNUM)
                
        self.tot_num_measure_points = int(self.stress_time_list*1000.0/self.time_step)+10
        
        print ("Prepare measurement...")
        # Prepare data array for save
        self.result_data = np.empty((self.tot_num_measure_points, 7)) # Save V, I data from 3 SMUs
            
        self.result_data[:] = np.NaN
        self.N = 0
        self.start = 0
        
        #Reset graph
        self.TTZC_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   rt_drain_bias_list = self.rt_drain_bias_list, 
                                   wt_drain_bias_list = self.wt_drain_bias_list,
                                   wt_gate_bias_list = self.wt_gate_bias_list,                                   
                                   wait_time = self.wait_time,
                                   pulse_width = self.pulse_width,
                                   stress_time_list = self.stress_time_list,
                                   pulse_start = self.pulse_start,
                                   pulse_amp = self.pulse_amp,
                                   time_step = self.time_step,
                                   pre_pulse_bias_time = self.pre_pulse_bias_time,
                                   post_pulse_bias_time = self.post_pulse_bias_time) 
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()  

class IO_Thread(IO_Thread_Super):  
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
                CURRENT_TIME = time.time()-self.start_time
                if CURRENT_TIME > self.stress_time_list:
                    self.flag = 0
                else:
                    if self.is_pulse_rightnow(CURRENT_TIME, np.subtract(self.pulse_time_list, self.pre_pulse_bias_time/1000.0),
                                              self.pulse_width + self.pre_pulse_bias_time + 
                                              self.post_pulse_bias_time):  
                        wt_drain_bias = wt_drain_bias_amp
                    else:
                        wt_drain_bias = wt_drain_bias_rest
                    
                    if self.is_pulse_rightnow(CURRENT_TIME, self.pulse_time_list, self.pulse_width):     
                        wt_gate_bias = wt_gate_bias_amp
                    else:
                        wt_gate_bias = wt_gate_bias_rest
  
                    self.SMU_WT_DRAIN.write(":SOUR:VOLT:LEV ", str(wt_drain_bias))
                    self.SMU_WT_GATE.write(":SOUR:VOLT:LEV ", str(wt_gate_bias))
                    self.SMU_RT_DRAIN.write(":SOUR:VOLT:LEV ", str(rt_drain_bias))
                    self.SMU_WT_GATE.write(":OUTP ON")
                    self.SMU_RT_DRAIN.write(":OUTP ON")
                    self.SMU_WT_DRAIN.write(":OUTP ON")
                    
                    CURRENT_RT_DRAIN = (self.SMU_RT_DRAIN.query_ascii_values(":READ?"))[1]
                    CURRENT_WT_DRAIN = (self.SMU_WT_DRAIN.query_ascii_values(":READ?"))[1]
                    CURRENT_WT_GATE = (self.SMU_WT_GATE.query_ascii_values(":READ?"))[1]
                    temp = np.array([CURRENT_TIME, rt_drain_bias, CURRENT_RT_DRAIN, 
                                      wt_drain_bias, CURRENT_WT_DRAIN,
                                      wt_gate_bias, CURRENT_WT_GATE])
                    self.signal.emit(temp)  
                        
            else:
                timer.stop()
                self.stop()  
            
            
        rt_drain_bias = 0
        wt_drain_bias = 0
        wt_gate_bias = 0    
        
        print("Scan type: %s" %(self.scan_type))
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
        self.init_SMU(self.SMU_list[2], self.SMU_init_params[2])
                
        self.SMU_WT_DRAIN = self.SMU_list[0]
        self.SMU_RT_DRAIN = self.SMU_list[1]        
        self.SMU_WT_GATE = self.SMU_list[2]
        
        self.rt_drain_bias_list = self.kwargs.get('rt_drain_bias_list')
        self.wt_drain_bias_list = self.kwargs.get('wt_drain_bias_list')
        self.wt_gate_bias_list = self.kwargs.get('wt_gate_bias_list')   
        self.pre_pulse_bias_time = self.kwargs.get('pre_pulse_bias_time')
        self.post_pulse_bias_time = self.kwargs.get('post_pulse_bias_time')
    
        for i in range (3):
            self.SMU_list[i].write(":SYST:AZER:STAT ", str(self.SMU_init_params[i][4]))
            self.SMU_list[i].write(":SYST:AZER:STAT ", str(self.SMU_init_params[i][5]))
            self.SMU_list[i].write(":SYST:AZER:STAT ", str(self.SMU_init_params[i][6]))
                        
    
        self.pulse_time_list = []
        self.pulse_time_list.append(self.pulse_start)
        print("Pulse time list")
        print(self.pulse_time_list)
        
        rt_drain_bias_rest = 0
        
        wt_drain_bias_rest = 0
        wt_drain_bias_amp = self.wt_drain_bias_list[0]  
        rt_drain_bias = self.rt_drain_bias_list[0]  

        wt_gate_bias_rest = self.wt_gate_bias_list[0]        
        wt_gate_bias_amp = wt_gate_bias + self.pulse_amp
        
        timer = QTimer()
        timer.setTimerType(QtCore.Qt.PreciseTimer)
        timer.timeout.connect(repeating_measurement)
        
        new_curve = np.empty(7)
        new_curve[:] = np.NaN
        self.time_step = int(self.time_step)
        self.signal.emit(new_curve)
        
        self.SMU_RT_DRAIN.write(":SOUR:VOLT:LEV ", str(rt_drain_bias))
        self.SMU_WT_DRAIN.write(":SOUR:VOLT:LEV ", str(wt_drain_bias))
        self.SMU_WT_GATE.write(":SOUR:VOLT:LEV ", str(wt_gate_bias))
        self.SMU_RT_DRAIN.write(":OUTP ON")
        self.SMU_WT_DRAIN.write(":OUTP ON")
        self.SMU_WT_GATE.write(":OUTP ON")

        time.sleep(self.wait_time)
        self.start_time = time.time()
        timer.start(self.time_step)
        self.exec_()
            
    def stop(self):  
        self.signal.emit([99999999,99999999,99999999,99999999,99999999,99999999,99999999])  

        print("IO_Thread stop called") 
        self.SMU_RT_DRAIN.write(":OUTP OFF")
        self.SMU_WT_DRAIN.write(":OUTP OFF")
        self.SMU_WT_GATE.write(":OUTP OFF")
            
        self.quit()
   
        