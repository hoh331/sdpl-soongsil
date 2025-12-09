# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):
    def tab_setup(self):
        self.pbit_memristor = QWidget()
        self.tab = self.pbit_memristor
        self.scan_type = "P-bit (Memristor)"
        
        """Pbit_Memristor Tab Setup"""
        
        self.Pbit_Memristor_Program_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Program setup', 7, 2)
        self.Pbit_Memristor_Program_ParamBox.set_toggle_item(0, 'Linear steps', True)
        self.Pbit_Memristor_Program_ParamBox.set_toggle_item(1, 'Custom steps', False)        
        self.Pbit_Memristor_Program_ParamBox.set_item(0, 'Vread start', '2', 'V')
        self.Pbit_Memristor_Program_ParamBox.set_item(1, 'Vread stop', '4', 'V')
        self.Pbit_Memristor_Program_ParamBox.set_item(2, 'Vread step', '0.1', 'V')
        self.Pbit_Memristor_Program_ParamBox.set_item(3, 'Read pulse duration', '50', 'ms')
        self.Pbit_Memristor_Program_ParamBox.set_item(4, '# of reads per voltage', '100', 'times')
        self.Pbit_Memristor_Program_ParamBox.set_item(5, 'Pre read delay', '50', 'ms')
        self.Pbit_Memristor_Program_ParamBox.set_item(6, 'Post read delay', '50', 'ms')        
        
        self.Pbit_Memristor_Erase_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Erase setup', 2, 2)
        self.Pbit_Memristor_Erase_ParamBox.set_toggle_item(0, 'Erase after read', True)
        self.Pbit_Memristor_Erase_ParamBox.set_toggle_item(1, 'No erase', False)           
        self.Pbit_Memristor_Erase_ParamBox.set_item(0, 'Erase pulse bias', '-3', 'V')
        self.Pbit_Memristor_Erase_ParamBox.set_item(1, 'Erase pulse width', '100', 'ms')
        
        self.Pbit_Memristor_Ref_ParamBox = ui.CreateParameterSettingsBox('Reference setup', 1)
        self.Pbit_Memristor_Ref_ParamBox.set_item(0, 'Reference bias', '2.5', 'V')
        
        self.Pbit_Memristor_General_ParamBox = ui.CreateParameterSettingsBox('Reference setup', 1)
        self.Pbit_Memristor_General_ParamBox.set_item(0, 'Refresh time', '50', 'ms')
                        
        self.Pbit_Memristor_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain SMU setup', 7)
        self.Pbit_Memristor_Drain_ParamBox.set_item(0, 'External Auto Zero', '0', '0: OFF/1: ON')
        self.Pbit_Memristor_Drain_ParamBox.set_item(1, 'External Voltage source range', '20', 'V')  
        self.Pbit_Memristor_Drain_ParamBox.set_item(2, 'External Current sensing range', '100E-6', 'A') 
        self.Pbit_Memristor_Drain_ParamBox.set_item(3, 'Drain Trigger delay', '0', 'ms')
        self.Pbit_Memristor_Drain_ParamBox.set_item(4, 'Drain Source delay', '0', 'ms')
        self.Pbit_Memristor_Drain_ParamBox.set_item(5, 'Drain NPLC', '0.1', 'number')
        self.Pbit_Memristor_Drain_ParamBox.set_item(6, 'Current compliance', '1E-3', 'A')
        
        self.Pbit_Memristor_RefSMU_ParamBox = ui.CreateParameterSettingsBox('Reference SMU setup', 7)
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(0, 'External Auto Zero', '0', '0: OFF/1: ON')
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(1, 'External Voltage source range', '20', 'V')  
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(2, 'External Current sensing range', '100E-6', 'A') 
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(3, 'Ref Trigger delay', '0', 'ms')
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(4, 'Ref Source delay', '0', 'ms')
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(5, 'Ref NPLC', '0.1', 'number')
        self.Pbit_Memristor_RefSMU_ParamBox.set_item(6, 'Ref compliance', '1E-3', 'A')       
        
        self.Pbit_Memristor_Read_ParamBox = ui.CreateParameterSettingsBox('Read SMU setup', 7)
        self.Pbit_Memristor_Read_ParamBox.set_item(0, 'External Auto Zero', '0', '0: OFF/1: ON')
        self.Pbit_Memristor_Read_ParamBox.set_item(1, 'External Voltage source range', '20', 'V')  
        self.Pbit_Memristor_Read_ParamBox.set_item(2, 'External Current sensing range', '100E-6', 'A') 
        self.Pbit_Memristor_Read_ParamBox.set_item(3, 'Read Trigger delay', '0', 'ms')
        self.Pbit_Memristor_Read_ParamBox.set_item(4, 'Read Source delay', '0', 'ms')
        self.Pbit_Memristor_Read_ParamBox.set_item(5, 'Read NPLC', '0.1', 'number')
        self.Pbit_Memristor_Read_ParamBox.set_item(6, 'Read compliance', '1E-3', 'A')     
      
        self.Pbit_Memristor_GraphBox = ui.CreateGraphBox('P-bit (Memristor)', 3, placement_orientation = 'vertical')
        self.Pbit_Memristor_GraphBox.set_titles(0, 'Device response', 'Cycle (#)', 'Ids (A)')  
        self.Pbit_Memristor_GraphBox.set_titles(1, 'Output response', 'Cycle (#)', 'Voutput (V)')  
        self.Pbit_Memristor_GraphBox.set_titles(2, 'Probability vs Input voltage', 'Voltage (V)', 'Probability')  

        # Pbit_Memristor tab setup
        self.tabPbit_Memristor_hbox = QHBoxLayout()  
        self.tabPbit_Memristor_vbox = QVBoxLayout()
        self.tabPbit_Memristor_vbox2 = QVBoxLayout()
        
        self.tabPbit_Memristor_vbox.addWidget(self.Pbit_Memristor_Program_ParamBox.groupbox)
        self.tabPbit_Memristor_vbox.addWidget(self.Pbit_Memristor_Erase_ParamBox.groupbox)
        self.tabPbit_Memristor_vbox.addWidget(self.Pbit_Memristor_Ref_ParamBox.groupbox)
        self.tabPbit_Memristor_vbox.addWidget(self.Pbit_Memristor_General_ParamBox.groupbox)
        self.tabPbit_Memristor_vbox.addStretch(1)
        
        self.tabPbit_Memristor_vbox2.addWidget(self.Pbit_Memristor_Drain_ParamBox.groupbox)
        self.tabPbit_Memristor_vbox2.addWidget(self.Pbit_Memristor_RefSMU_ParamBox.groupbox)
        self.tabPbit_Memristor_vbox2.addWidget(self.Pbit_Memristor_Read_ParamBox.groupbox)        
        self.tabPbit_Memristor_vbox2.addStretch(1)
        
        self.tabPbit_Memristor_hbox.addLayout(self.tabPbit_Memristor_vbox)
        self.tabPbit_Memristor_hbox.addLayout(self.tabPbit_Memristor_vbox2)
        self.tabPbit_Memristor_hbox.addWidget(self.Pbit_Memristor_GraphBox.groupbox)
        self.tabPbit_Memristor_hbox.setStretch(0,1)
        self.tabPbit_Memristor_hbox.setStretch(1,1)
        self.tabPbit_Memristor_hbox.setStretch(2,3)
        self.tab.setLayout(self.tabPbit_Memristor_hbox)        
        
        #main ui communication test
        self.main.LogBox.update_log("P-bit (memristor) module loaded")
                    
    def run_measurement_start(self): 
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[], []]
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Pbit_Memristor_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Pbit_Memristor_RefSMU_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[2].append(round(float(self.Pbit_Memristor_Read_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        print ("Bias parameters:")
        print (self.SMU_init_params[0])
        print (self.SMU_init_params[1])
        print (self.SMU_init_params[2])
        
        # Calculate sweep points
        self.vread_list = []
                
        # Calculate list for read biases
        vread_start = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[0].text()), ROUNDNUM)
        vread_stop = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[1].text()), ROUNDNUM)
        vread_step = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[2].text()), ROUNDNUM)
        
        if self.Pbit_Memristor_Program_ParamBox.rbtn_list[1].isChecked():
            text = self.Pbit_Memristor_Program_ParamBox.le_list[0].text()
            self.vread_list = [float(x) for x in text.split(',')]
            
        else:                
            vread_start = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[0].text()), ROUNDNUM)
            vread_stop = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[1].text()), ROUNDNUM)
            vread_step = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[2].text()), ROUNDNUM) 
            
            temp = vread_start
            while (temp <= vds_stop):
                self.vread_list.append(temp)
                temp = round((temp + vread_step), ROUNDNUM)                 
        
        self.pulse_width_read = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[3].text())/1000.0, ROUNDNUM)
        
        self.read_num = int(self.Pbit_Memristor_Sequence_ParamBox.le_list[4].text())
        
        self.pulse_width_pre = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[5].text())/1000.0, ROUNDNUM)      
        self.pulse_width_post = round(float(self.Pbit_Memristor_Program_ParamBox.le_list[6].text())/1000.0, ROUNDNUM)      
        
        self.erase_flag = self.Pbit_Memristor_Erase_ParamBox.rbtn_list[0].isChecked()
        self.erase_pulse_bias = round(float(self.Pbit_Memristor_Erase_ParamBox.le_list[0].text()), ROUNDNUM)
        self.erase_pulse_width = round(float(self.Pbit_Memristor_Erase_ParamBox.le_list[1].text()), ROUNDNUM)
        
        self.vref = round(float(self.Pbit_Memristor_Ref_ParamBox.le_list[0].text())/1000.0, ROUNDNUM)    
        
        self.refresh_time = round(float(self.Pbit_Memristor_General_ParamBox.le_list[0].text())/1000.0, ROUNDNUM)       
        
        print ("Prepare measurement...")
        
        # Prepare data array for save
        self.result_data = np.empty((1000000, 6))
        self.result_data[:] = np.NaN
        self.vout_data = np.empty((100000,3))
        self.vout_data[:] = np.NaN
        self.summary_data = np.empty((np.shape(self.vread_list)[0], 3))
        self.summary_data[:] = np.NaN
        self.N = 0
        self.count = 0
        self.start = 0
        self.N_read = 0
        self.N_start = 0
        self.cycle_count = 0

        
        #Reset graph
        self.Pbit_Memristor_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vread_list = self.vread_list,
                                   pulse_width_read = self.pulse_width_read,
                                   read_num = self.read_num,
                                   pulse_width_pre = self.pulse_width_pre,
                                   pulse_width_post = self.pulse_width_post,
                                   erase_flag = self.erase_flag,
                                   erase_pulse_bias = self.erase_pulse_bias,
                                   erase_pulse_width = self.erase_pulse_width,
                                   vref = self.vref,
                                   refresh_time = self.refresh_time)
        
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()            

    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.Pbit_Memristor_GraphBox.addnew_plot(0)
                self.Pbit_Memristor_GraphBox.addnew_plot(1)
                self.Pbit_Memristor_GraphBox.addnew_plot(2, type = "symbol")
                
                if self.cycle_count >= 0:
                    self.summary_data[self.cycle_count][0] = self.vread_list[self.cycle_count]
                    self.summary_data[self.cycle_count][1] = np.average(self.vout_data[self.N_start:self.N_start+self.N_read][2])
                    self.Pbit_Memristor_GraphBox.update_plot(2, self.vout_data[0:self.cycle_count][0], self.vout_data[0:self.cycle_count][1])
                
                self.cycle_count = self.cycle_count + 1                   
                self.count = 1
                self.N_start = self.N_start + self.N_read
                self.N_read = 0                
                self.start = self.N    
    
            else:
                self.result_data[self.N] = array
                self.Pbit_Memristor_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,1], self.result_data[self.start:self.start+self.count,3])
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A'), '%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'uA')])
                
                if array[-1]==1:
                    self.vout_data[self.N_start + self.N_read][0] = array[0]
                    self.vout_data[self.N_start + self.N_read][1] = array[2]
                    self.vout_data[self.N_start + self.N_read][2] = array[4]
                    self.Pbit_Memristor_GraphBox.update_plot(1, self.vout_data[self.N_start:self.N_start+self.N_read+1,0], self.vout_data[self.N_start:self.N_start+self.N_read+1,2])
                    self.N_read = self.N_read + 1
                    # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                

class IO_Thread(IO_Thread_Super):  
    def __init__(self, SMU_list, SMU_init_params, scan_type = None,
                 vread_list = None, pulse_width_read = None,
                 read_num = None, pulse_width_pre = None,
                 pulse_width_post = None, erase_flag = None,
                 erase_pulse_bias = None, erase_pulse_width = None,
                 vref = None, refresh_time = None, **kwargs):
        
        QtCore.QThread.__init__(self, parent)
        print("IO Thread start")
        
        self.SMU_list = SMU_list
        self.SMU_init_params = SMU_init_params
        self.scan_type = scan_type

        self.vread_list = vread_list
        self.pulse_width_read = pulse_width_read
        self.read_num = read_num
        self.pulse_width_pre = pulse_width_pre
        self.pulse_width_post = pulse_width_post
        self.erase_flag = erase_flag
        self.erase_pulse_bias = erase_pulse_bias
        self.erase_pulse_width = erase_pulse_width
        self.vref = vref
        self.refresh_time = refresh_time
    
    def is_pulse_rightnow(self, current_time, pulse_time, pulse_width):
        if current_time >= pulse_time and current_time < pulse_time + pulse_width:
            return True    
        else:
            return False    
    
    def run(self):
        def repeating_measurement():
            print("repeating measurement") 
            if self.flag == 1:
                if self.counter_i < self.counter_i_max:
                    if self.counter_j < self.counter_j_max:
                        CURRENT_TIME = time.time()-self.start.time
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vread_list[self.counter_i][self.counter_j]))
                        CURRENT_SMU_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1]
                        VOLTAGE_SMU_READ = (self.SMU_READ.query_ascii_values(":READ?"))[1] 
                        temp = np.array([self.counter_j, CURRENT_TIME, self.vds_list[self.counter_i][self.counter_j], 
                                         CURRENT_SMU_DRAIN, VOLTAGE_SMU_READ, self.record_index[self.counter_i][self.counter_j]])
                        self.signal.emit(temp)
                    else:
                        self.counter_i = self.counter_i+1
                        self.counter_j = 0
                        self.signal.emit(new_curve)
                        self.start_time = time.time()
                else:
                    self.flag = 0
            else:
                timer.stop()
                self.stop()
        
        print("Scan type: %s" %(self.scan_type))
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
        self.init_SMU(self.SMU_list[2], self.SMU_init_params[2])
        
        self.SMU_DRAIN = self.SMU_list[0]
        self.SMU_REF = self.SMU_list[1]
        self.SMU_READ = self.SMU_list[2]
    
        self.SMU_DRAIN.write(":SYST:AZER:STAT ", str(self.SMU_init_params[0][4])) #Disable autozero
        self.SMU_REF.write(":SYST:AZER:STAT ", str(self.SMU_init_params[1][4])) #Disable autozero
        self.SMU_READ.write(":SYST:AZER:STAT ", str(self.SMU_init_params[2][4])) #Disable autozero
        
        # Fix source & measure range
        self.SMU_DRAIN.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[0][5]))
        self.SMU_DRAIN.write(":SENS:CURR:RANG ", str(self.SMU_init_params[0][6]))     
        self.SMU_REF.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[1][5]))
        self.SMU_REF.write(":SENS:CURR:RANG ", str(self.SMU_init_params[1][6]))     
        self.SMU_READ.write(":SENS:VOLT:DC:RANG ", str(self.SMU_init_params[2][6])) 


        time_per_cycle = self.pulse_width_pre + self.pulse_width_read + self.pulse_width_post
        if erase_flag:
            time_per_cycle = time_per_cycle + self.erase_pulse_width
            
        points_per_cycle = round(time_per_cycle/self.refresh_time)    
        self.drain_bias_list = np.zeros((np.shape(self.vread_list)[0], points_per_cycle))
        self.record_index = np.zeros((np.shape(self.vread_list)[0], points_per_cycle))
        
        # read_pulse_moment = []
        # read_pulse.append(self.pulse_width_pre)
        # erase_pulse_moment = []
        # erase_pulse.append(self.pulse_width_pre + self.pulse_width_read + self.pulse_width_post)
        
        for i in range(np.shape(self.vread_list)[0]):
            for j in range(points_per_cycle):
                if is_pulse_rightnow(self.refresh_time*j, self.pulse_width_pre, self.pulse_width_read):
                    self.drain_bias_list[i][j] = self.vread_list[i]
                    
                if is_pulse_rightnow(self.refresh_time*j, self.pulse_width_pre + self.pulse_width_read + self.pulse_width_post, self.erase_pulse_width):
                    self.drain_bias_list[i][j] = self.erase_pulse_bias
                    
                if self.refresh_time*j < self.pulse_width_pre + self.pulse_width_read and self.refresh_time*j >= self.pulse_width_pre + self.pulse_width_read - self.refresh_time:
                    self.record_index[i][j] = 1
        
        print(f'Drain_bias_list = {self.drain_bias_list}')
        print(f'Record_index = {self.record_index}')
        
        timer = QTimer()
        timer.setTimerType(QtCore.Qt.PreciseTimer)
        timer.timeout.connect(repeating_measurement)
        
        new_curve = np.empty(5)
        new_curve[:] = np.NaN
        self.time_step = int(self.time_step)
        self.signal.emit(new_curve)
        
        self.SMU_REF.write(":SOUR:VOLT:LEV ", str(self.vref))
        self.SMU_REF.write(":OUTP ON")
        
        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
        self.SMU_DRAIN.write(":OUTP ON")        
                
        self.counter_i = 0
        self.counter_j = 0
        self.counter_i_max = np.shape(self.drain_bias_list)[0]
        self.counter_j_max = np.shape(self.drain_bias_list)[1]
        
        self.start_time = time.time()
        timer.start(self.time_step)
        self.exec_()
            
def stop(self):  
    self.signal.emit([99999999,99999999,99999999,99999999,99999999,99999999])  

    print("IO_Thread stop called") 
    self.SMU_DRAIN.write("OUTP OFF")
    self.SMU_REF.write("OUTP OFF")
        
    self.quit()