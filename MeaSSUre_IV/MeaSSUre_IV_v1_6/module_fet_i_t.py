# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):        
    def tab_setup(self):
        self.tab = QWidget()   
        self.scan_type = "I-t"
        
        """I-t Tab Setup"""
        self.it_SMU_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Select number of SMU', 0, 2)
        self.it_SMU_ParamBox.set_toggle_item(0, "Single SMU", 1)
        self.it_SMU_ParamBox.set_toggle_item(1, "Two SMUs", 0)
            
        self.it_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain bias setup', 9)
        self.it_Drain_ParamBox.set_item(0, 'Vds', '1', 'V')
        self.it_Drain_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.it_Drain_ParamBox.show_only_name(1)
        self.it_Drain_ParamBox.set_item(2, 'Drain Auto Zero', '0', '0: OFF/1: ON')
        self.it_Drain_ParamBox.set_item(3, 'Drain Voltage source range', '20', 'V')        
        self.it_Drain_ParamBox.set_item(4, 'Drain Current sensing range', '100E-6', 'A')        
        self.it_Drain_ParamBox.set_item(5, 'Drain trigger delay', '0.0', 's')
        self.it_Drain_ParamBox.set_item(6, 'Drain source delay', '0.0', 's')
        self.it_Drain_ParamBox.set_item(7, 'Drain NPLC', '0.1', 'number')
        self.it_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.it_Gate_ParamBox = ui.CreateParameterSettingsBox('Gate bias setup', 9)
        self.it_Gate_ParamBox.set_item(0, 'Vgs', '0', 'V')
        self.it_Gate_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.it_Gate_ParamBox.show_only_name(1)
        self.it_Gate_ParamBox.set_item(2, 'Gate Auto Zero', '0', '0: OFF/1: ON')
        self.it_Gate_ParamBox.set_item(3, 'Gate Voltage source range', '20', 'V')        
        self.it_Gate_ParamBox.set_item(4, 'Gate Current sensing range', '100E-6', 'A')   
        self.it_Gate_ParamBox.set_item(5, 'Gate trigger delay', '0.0', 's')
        self.it_Gate_ParamBox.set_item(6, 'Gate source delay', '0.0', 's')
        self.it_Gate_ParamBox.set_item(7, 'Gate NPLC', '0.1', 'number')
        self.it_Gate_ParamBox.set_item(8, 'Current compliance', '100E-3', 'A')
        
        self.it_Time_ParamBox = ui.CreateParameterSettingsBox('Measurement speed setup', 3)
        self.it_Time_ParamBox.set_item(0, 'Measurement time', '10', 's')
        self.it_Time_ParamBox.set_item(1, 'Delay between each data point', '50', 'ms')
        self.it_Time_ParamBox.set_item(2, 'Delay before sweep starts', '0', 's')
        
        self.Time_GraphBox = ui.CreateGraphBox('I-t characteristics', 2)
        self.Time_GraphBox.set_titles(0, 'I-t curves (Ids-Vds)', 'Time (s)', 'Ids (A)')        
        self.Time_GraphBox.set_titles(1, 'I-t curves (leakage) (Igs-Vds)', 'Time (s)', 'Igs (A)')
        
        
        # tab setup
        self.tab_hbox = QHBoxLayout()  
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox.addWidget(self.it_SMU_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.it_Drain_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.it_Gate_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.it_Time_ParamBox.groupbox)
        self.tab_vbox.addStretch(1)
        self.tab_hbox.addLayout(self.tab_vbox)
        self.tab_hbox.addWidget(self.Time_GraphBox.groupbox)
        self.tab_hbox.setStretch(0,1)
        self.tab_hbox.setStretch(1,4)
        self.tab.setLayout(self.tab_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("I-t module loaded")
      
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.Time_GraphBox.addnew_plot(0)
                self.Time_GraphBox.addnew_plot(1)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                if self.it_SMU_ParamBox.rbtn_list[0].isChecked():
                    self.Time_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                else:
                    self.Time_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                    self.Time_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,4])
                # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                if self.it_SMU_ParamBox.rbtn_list[0].isChecked():
                    self.main.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[2], 'A'), '%.4e%s' %(0.0, 'V'), '%.4e%s' %(0.0, 'A')])
                else:
                    self.main.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[2], 'A'), '%.4e%s' %(array[3], 'V'), '%.4e%s' %(array[4], 'A')])
   
                
    #Override the method in parent class 
    def run_measurement(self):        
        self.measurement_timer = QTimer()
        self.measurement_timer.setInterval(TIMER_INTERVAL)
        self.main.TimeDisplayBox.check_start_time()
        self.measurement_timer.timeout.connect(self.main.TimeDisplayBox.update_time_elapsed)
        self.measurement_timer.start(TIMER_INTERVAL)
        
        if self.it_SMU_ParamBox.rbtn_list[0].isChecked():
            print("Single SMU mode")
            self.SMU_list = self.main.ConnectionControlBox.get_SMU_list_selectedonly([0])
        else:
            print("Dual SMU mode")
            self.SMU_list = self.main.ConnectionControlBox.get_SMU_list()

        print("Run Measurement: %s" %(self.scan_type))
        self.main.LogBox.update_log("Run Measurement: %s" %(self.scan_type))
        
        for i in range(self.main.tabtotalnum):
            if i != self.main.tabs.currentIndex():
                self.main.tabs.setTabEnabled(i, False)
                
        print("Preparing tables of biasing values...")        
        self.run_measurement_start()

    def run_measurement_start(self):      
        # Calculate sweep points
        self.vds_list = []
        self.vgs_list = []      
        

        vds_start = round(float(self.it_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
        self.vds_list.append(vds_start)
             
        vgs_start = round(float(self.it_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
        self.vgs_list.append(vgs_start)

        print ("Table prepared")
       
        print ("Preparing bias parameters")
        if self.it_SMU_ParamBox.rbtn_list[0].isChecked():
            self.SMU_init_params = [[]]
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))         
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
            print ("Bias parameters:")
            print (self.SMU_init_params[0])
        else:
            self.SMU_init_params = [[],[]]
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
            self.SMU_init_params[0].append(round(float(self.it_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
            
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-7].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-6].text()), ROUNDNUM))
            self.SMU_init_params[1].append(round(float(self.it_Gate_ParamBox.le_list[-5].text()), ROUNDNUM))
            print ("Bias parameters:")
            print (self.SMU_init_params[0])
            print (self.SMU_init_params[1])
        
        self.stress_time_list = round(float(self.it_Time_ParamBox.le_list[0].text()), ROUNDNUM)
        self.pulse_width = int(round(float(self.it_Time_ParamBox.le_list[1].text()), ROUNDNUM))
        self.wait_time = round(float(self.it_Time_ParamBox.le_list[2].text()), ROUNDNUM)
        
        self.tot_num_measure_points = int(self.stress_time_list*1000.0/self.pulse_width)+10000
        
        print ("Prepare measurement...")
        # Prepare data array for save
        if self.it_SMU_ParamBox.rbtn_list[0].isChecked():
            self.result_data = np.empty((self.tot_num_measure_points, 3))
        else:
            self.result_data = np.empty((self.tot_num_measure_points, 5))
        self.result_data[:] = np.NaN
        self.N = 0
        self.start = 0
        
        #Reset graph
        self.Time_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   wait_time = self.wait_time,
                                   pulse_width = self.pulse_width,
                                   stress_time_list = self.stress_time_list)
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
                    if self.num_SMU == 1:
                        CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1]  
                        temp = np.array([CURRENT_TIME, vds, CURRENT_DRAIN])
                        self.signal.emit(temp)
                    else:
                        CURRENT_DRAIN = (self.SMU_DRAIN.query_ascii_values(":READ?"))[1]  
                        CURRENT_GATE = (self.SMU_GATE.query_ascii_values(":READ?"))[1]
                        temp = np.array([CURRENT_TIME, vds, CURRENT_DRAIN, vgs, CURRENT_GATE])
                        self.signal.emit(temp)
            else:
                timer.stop()
                self.stop()  
            
        print("Scan type: %s" %(self.scan_type))   
        self.num_SMU = len(self.SMU_init_params)
        # print("Number of SMUs: %d" %(len(self.SMU_init_params)))
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        if len(self.SMU_init_params)==2:
            self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])

        self.SMU_DRAIN = self.SMU_list[0]
        if len(self.SMU_init_params)==2:
            self.SMU_GATE = self.SMU_list[1]
        
        """ Special for high-speed measurement """
        self.SMU_DRAIN.write(":SYST:AZER:STAT ", str(self.SMU_init_params[0][4])) #Disable autozero
        if len(self.SMU_init_params)==2:
            self.SMU_GATE.write(":SYST:AZER:STAT ", str(self.SMU_init_params[1][4])) #Disable autozero
        
        # Fix source & measure range
        self.SMU_DRAIN.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[0][5]))
        self.SMU_DRAIN.write(":SENS:CURR:RANG ", str(self.SMU_init_params[0][6]))     
        if len(self.SMU_init_params)==2:
            self.SMU_GATE.write(":SOUR:VOLT:RANG ", str(self.SMU_init_params[1][5]))
            self.SMU_GATE.write(":SENS:CURR:RANG ", str(self.SMU_init_params[1][6]))
        
        vds = self.vds_list[0]
        vgs = self.vgs_list[0]
        
        timer = QTimer()
        timer.setTimerType(QtCore.Qt.PreciseTimer)
        timer.timeout.connect(repeating_measurement)
        
        new_curve = np.empty(5)
        new_curve[:] = np.NaN
        self.signal.emit(new_curve)
        
        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
        self.SMU_DRAIN.write(":OUTP ON")        
        if len(self.SMU_init_params)==2:
            self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
            self.SMU_GATE.write(":OUTP ON")

        time.sleep(self.wait_time)
        self.start_time = time.time()
        timer.start(self.pulse_width)
        self.exec_()
        
    def stop(self):  
        self.signal.emit([99999999,99999999,99999999,99999999,99999999,99999999])  

        print("IO_Thread stop called") 
        self.SMU_DRAIN.write("OUTP OFF")
        if len(self.SMU_init_params)==2:
            self.SMU_GATE.write("OUTP OFF")
            
        self.quit()
            
        