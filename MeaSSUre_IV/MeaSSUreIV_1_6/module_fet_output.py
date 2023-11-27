# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):        
    def tab_setup(self):
        self.tabOutput = QWidget()
        self.tab = self.tabOutput        
        self.scan_type = "Output"
        
        """Output Tab Setup"""
        self.Output_Drain_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Drain bias setup', 9, 2)
        self.Output_Drain_ParamBox.set_toggle_item(0, 'Single sweep', True)
        self.Output_Drain_ParamBox.set_toggle_item(1, 'Double sweep', False)
        self.Output_Drain_ParamBox.set_item(0, 'Vds start', '0', 'V')
        self.Output_Drain_ParamBox.set_item(1, 'Vds stop', '10', 'V')
        self.Output_Drain_ParamBox.set_item(2, 'Vds step', '0.1', 'V')
        self.Output_Drain_ParamBox.set_item(3, 'Delay before sweep', '1', 's')
        self.Output_Drain_ParamBox.set_item(4, '<Measurement settings>', '0', '0')
        self.Output_Drain_ParamBox.show_only_name(4)
        self.Output_Drain_ParamBox.set_item(5, 'Drain trigger delay', '0.01', 's')
        self.Output_Drain_ParamBox.set_item(6, 'Drain source delay', '0.01', 's')
        self.Output_Drain_ParamBox.set_item(7, 'Drain NPLC', '1', 'number')
        self.Output_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.Output_Gate_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Gate bias setup', 8, 2)
        self.Output_Gate_ParamBox.set_toggle_item(0, 'Linear steps', False)
        self.Output_Gate_ParamBox.set_toggle_item(1, 'Custom steps', True)
        self.Output_Gate_ParamBox.set_item(0, 'Vgs (start)', '5, 10, 20, 30', 'V')
        self.Output_Gate_ParamBox.set_item(1, 'Vgs stop', '10', 'V')
        self.Output_Gate_ParamBox.set_item(2, 'Vgs step', '10', 'V')
        self.Output_Gate_ParamBox.set_item(3, '<Measurement settings>', '0', '0')
        self.Output_Gate_ParamBox.show_only_name(3)
        self.Output_Gate_ParamBox.set_item(4, 'Gate trigger delay', '0.01', 's')
        self.Output_Gate_ParamBox.set_item(5, 'Gate source delay', '0.01', 's')
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
        self.tabOutput_vbox.addStretch(1)
        self.tabOutput_hbox.addLayout(self.tabOutput_vbox)
        self.tabOutput_hbox.addWidget(self.Output_GraphBox.groupbox)
        self.tabOutput_hbox.setStretch(0,1)
        self.tabOutput_hbox.setStretch(1,4)
        self.tabOutput.setLayout(self.tabOutput_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("FET:Output loaded")
      
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
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
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'A'), '%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A')])

    def run_measurement_start(self):      
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
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   wait_time = self.wait_time)
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()  

class IO_Thread(IO_Thread_Super):        
    def run(self):
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
                    
        self.stop()