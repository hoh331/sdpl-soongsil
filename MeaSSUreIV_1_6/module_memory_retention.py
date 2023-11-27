# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):
    def tab_setup(self):
        self.tabMemory_Retention = QWidget()
        self.tab = self.tabMemory_Retention
        self.scan_type = "Memory retention"
        
        """Memory_Retention Tab Setup"""
        self.Memory_Retention_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Memory Retention setup', 10, 2)
        self.Memory_Retention_ParamBox.set_toggle_item(0, 'Program Retention', True)
        self.Memory_Retention_ParamBox.set_toggle_item(1, 'Erase Retention', False)
        self.Memory_Retention_ParamBox.set_item(0, 'Program gate bias', '-10', 'V')
        self.Memory_Retention_ParamBox.set_item(1, 'Erase gate bias', '10', 'V')
        self.Memory_Retention_ParamBox.set_item(2, 'Read gate bias', '0', 'V')
        self.Memory_Retention_ParamBox.set_item(3, 'Read drain bias', '0.1', 'V')
        self.Memory_Retention_ParamBox.set_item(4, 'Program/Erase Pulse width', '100', 'ms')
        self.Memory_Retention_ParamBox.set_item(5, 'Delay beween squences', '100', 's')
        self.Memory_Retention_ParamBox.set_item(6, 'Total number of cycles', '100', '#')
        self.Memory_Retention_ParamBox.set_item(7, '<Measurement settings>', '0', '0')
        self.Memory_Retention_ParamBox.show_only_name(7)
        self.Memory_Retention_ParamBox.set_item(8, 'Drain NPLC', '1', 'number')
        self.Memory_Retention_ParamBox.set_item(9, 'Current compliance', '10E-3', 'A')
        
        self.Memory_Retention_GraphBox = ui.CreateGraphBox('Memory Retention', 1)
        self.Memory_Retention_GraphBox.set_titles(0, 'Memory Retention recording', 'Time (s)', 'Ids (A)')        

        # Memory_retention tab setup
        self.tabMemory_Retention_hbox = QHBoxLayout()  
        self.tabMemory_Retention_vbox = QVBoxLayout()
        self.tabMemory_Retention_vbox.addWidget(self.Memory_Retention_ParamBox.groupbox)
        self.tabMemory_Retention_vbox.addStretch(1)
        self.tabMemory_Retention_hbox.addLayout(self.tabMemory_Retention_vbox)
        self.tabMemory_Retention_hbox.addWidget(self.Memory_Retention_GraphBox.groupbox)
        self.tabMemory_Retention_hbox.setStretch(0,1)
        self.tabMemory_Retention_hbox.setStretch(1,4)
        self.tabMemory_Retention.setLayout(self.tabMemory_Retention_hbox)
        
        
        #main ui communication test
        self.main.LogBox.update_log("Memory retention module loaded")
    
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.Memory_Retention_GraphBox.addnew_plot(0)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.Memory_Endurance_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,1], self.result_data[self.start:self.start+self.count,4])
                 # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A'), '%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'uA')])

                    
    def run_measurement_start(self):
        TIMER_INTERVAL = 10
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
               
        # Calculate sweep points
        self.vds_list = []
        self.vgs_list = []
        
        # Calculate list for gate and drain biases
        vgs_program = round(float(self.Memory_Retention_ParamBox.le_list[0].text()), ROUNDNUM)
        vgs_erase =  round(float(self.Memory_Retention_ParamBox.le_list[1].text()), ROUNDNUM)
        vgs_read =  round(float(self.Memory_Retention_ParamBox.le_list[2].text()), ROUNDNUM)
        vds_read =  round(float(self.Memory_Retention_ParamBox.le_list[3].text()), ROUNDNUM)
        pulse_width_temp = float(self.Memory_Retention_ParamBox.le_list[4].text())
        pulse_width = round(float(pulse_width_temp/1000), ROUNDNUM)
        wait_time = round(float(self.Memory_Retention_ParamBox.le_list[5].text()), ROUNDNUM)
        repeat_num = round(int(self.Memory_Retention_ParamBox.le_list[6].text()), ROUNDNUM)
        
        if self.Memory_Retention_ParamBox.rbtn_list[0].isChecked():
            self.vgs_list.append(vgs_program)
            self.vgs_list.append(0)
        else:
            self.vgs_list.append(vgs_erase)
            self.vgs_list.append(0)
        
        self.vgs_list.append(vgs_read)
        self.vds_list.append(vds_read)
        self.pulse_width = pulse_width
        self.wait_time = wait_time
        self.repeat_num = repeat_num
                           
        self.tot_num_measure_points = repeat_num
                
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[]]
        self.SMU_init_params[0].append(0) # Drain trigger delay should be 0 for fast pulsation
        self.SMU_init_params[0].append(0) # Drain source delay should be 0 for fast pulsation
        self.SMU_init_params[0].append(round(float(self.Memory_Retention_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Memory_Retention_ParamBox.le_list[-1].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(0) # Gate trigger delay should be 0 for fast pulsation
        self.SMU_init_params[1].append(0) # Gate source delay should be 0 for fast pulsation
        self.SMU_init_params[1].append(0.01) # Gate NPLC should be minimized
        self.SMU_init_params[1].append(round(float(self.Memory_Retention_ParamBox.le_list[-1].text()), ROUNDNUM))
        
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
        self.Memory_Retention_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   wait_time = self.wait_time,
                                   pulse_width = self.pulse_width,
                                   repeat_num = self.tot_num_measure_points)
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()  

class IO_Thread(IO_Thread_Super):        
    def run(self):
        self.OFFSET_TIME = 0.005
        print("Scan type: %s" %(self.scan_type))
        print("Vgs values:")
        print(str(self.vgs_list[0]))
        print(str(self.vgs_list[1]))
        print(str(self.vgs_list[2]))
        print("Vds value:")
        print(self.vds_list)
        time.sleep(0.5)
        print("Initiallized SMUs")
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
        
        self.SMU_DRAIN = self.SMU_list[0]
        self.SMU_GATE = self.SMU_list[1]
        
        new_curve = np.empty(6)
        new_curve[:] = np.NaN
        time.sleep(0.5)
        print("Go to initial biasing points")
        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
        self.SMU_GATE.write(":OUTP ON")
        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
        self.SMU_DRAIN.write(":OUTP ON")
        
        self.signal.emit(new_curve)
        print("Memory_retention measurement start") 
        print("Repeat number: %d" %(self.repeat_num))
        print("Wait time: %.2f" %(self.wait_time))
        print("Pulse width: %.2f" %(self.pulse_width))
        
        self.wait_time = self.take_positive(self.wait_time - self.OFFSET_TIME)
        self.pulse_width = self.take_positive(self.pulse_width - self.OFFSET_TIME)
        
        # Programming
        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs_list[0]))
        time.sleep(self.pulse_width)
        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
        time.sleep(0.01)
        
        for i in range(self.repeat_num):
            if self.flag == 1:                                       
                # Reading after the set time period
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs_list[2]))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds_list[0]))
                temp_reading = self.SMU_DRAIN.query_ascii_values(":READ?")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
                
                temp = np.array([i, float(i*self.wait_time), temp_reading[5], temp_reading[1], np.log10(np.abs(temp_reading[1]))])
                
                self.signal.emit(temp)
                time.sleep(self.wait_time)
                
            else:
                break;
        self.stop() 