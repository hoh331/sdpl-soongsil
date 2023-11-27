# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):
    def tab_setup(self):
        self.tabPBSNBS = QWidget()
        self.tab = self.tabPBSNBS
        self.scan_type = "PBS and NBS"
        """PBSNBS Tab Setup"""
       
        self.PBSNBS_Stress_ParamBox =  ui.CreateParameterSettingsBox('Bias stress setup', 3)
        self.PBSNBS_Stress_ParamBox.set_item(0, 'Stress bias (Gate)', '10', 'V')
        self.PBSNBS_Stress_ParamBox.set_item(1, 'Stress bias (Drain)', '1', 'V')
        self.PBSNBS_Stress_ParamBox.set_item(2, 'Time seq.', '0, 1, 10, 100', 's')
        
        self.PBSNBS_Gate_ParamBox =  ui.CreateParameterSettingsBoxWithToggle('Gate bias setup', 8, 2)
        self.PBSNBS_Gate_ParamBox.set_toggle_item(0, 'Single sweep', False)
        self.PBSNBS_Gate_ParamBox.set_toggle_item(1, 'Double sweep', True)
        self.PBSNBS_Gate_ParamBox.set_item(0, 'Vgs start', '0', 'V')
        self.PBSNBS_Gate_ParamBox.set_item(1, 'Vgs stop', '10', 'V')
        self.PBSNBS_Gate_ParamBox.set_item(2, 'Vgs step', '0.1', 'V')
        self.PBSNBS_Gate_ParamBox.set_item(3, '<Measurement settings>', '0', '0')
        self.PBSNBS_Gate_ParamBox.show_only_name(3)
        self.PBSNBS_Gate_ParamBox.set_item(4, 'Gate trigger delay', '0.01', 's')
        self.PBSNBS_Gate_ParamBox.set_item(5, 'Gate source delay', '0.01', 's')
        self.PBSNBS_Gate_ParamBox.set_item(6, 'Gate NPLC', '1', 'number')
        self.PBSNBS_Gate_ParamBox.set_item(7, 'Current compliance', '100E-3', 'A')
        
        self.PBSNBS_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain bias setup', 6)
        self.PBSNBS_Drain_ParamBox.set_item(0, 'Vds', '1', 'V')
        self.PBSNBS_Drain_ParamBox.set_item(1, '<Measurement settings>', '0', '0')
        self.PBSNBS_Drain_ParamBox.show_only_name(1)
        self.PBSNBS_Drain_ParamBox.set_item(2, 'Drain trigger delay', '0.01', 's')
        self.PBSNBS_Drain_ParamBox.set_item(3, 'Drain source delay', '0.01', 's')
        self.PBSNBS_Drain_ParamBox.set_item(4, 'Drain NPLC', '1', 'number')
        self.PBSNBS_Drain_ParamBox.set_item(5, 'Current compliance', '10E-3', 'A')
        
        self.PBSNBS_GraphBox = ui.CreateGraphBox('PBS/NBS characteristics', 2)
        self.PBSNBS_GraphBox.set_titles(0, 'PBS/NBS transfer curves (Ids-Vgs)', 'Vgs (V)', 'Ids (A)')
        self.PBSNBS_GraphBox.set_titles(1, 'Gate leakage curves (Igs-Vgs)', 'Vgs (V)', 'Igs (A)')
        
        # PBSNBS tab setup
        self.tabPBSNBS_hbox = QHBoxLayout()  
        self.tabPBSNBS_vbox = QVBoxLayout()
        self.tabPBSNBS_vbox.addWidget(self.PBSNBS_Stress_ParamBox.groupbox)
        self.tabPBSNBS_vbox.addWidget(self.PBSNBS_Gate_ParamBox.groupbox)
        self.tabPBSNBS_vbox.addWidget(self.PBSNBS_Drain_ParamBox.groupbox)
        self.tabPBSNBS_vbox.addStretch(1)
        self.tabPBSNBS_hbox.addLayout(self.tabPBSNBS_vbox)
        self.tabPBSNBS_hbox.addWidget(self.PBSNBS_GraphBox.groupbox)
        self.tabPBSNBS_hbox.setStretch(0,1)
        self.tabPBSNBS_hbox.setStretch(1,4)
        self.tabPBSNBS.setLayout(self.tabPBSNBS_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("PBS/NPS loaded")
    
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        elif array[0] == 99999998:
            self.main.LogBox.update_log("Applying bias stress for %d seconds" %(array[1]))
            self.main.LogBox.update_log("Remaining time: %d" %(array[1]))
        elif array[0] == 99999997:
            self.main.LogBox.remove_last_sentence()
            self.main.LogBox.update_log("Remaining time: %d" %(array[1]))
        else:
            if np.isnan(array)[0] == True:
                self.PBSNBS_GraphBox.addnew_plot(0)
                self.PBSNBS_GraphBox.addnew_plot(1)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.PBSNBS_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,5])
                self.PBSNBS_GraphBox.update_plot(1, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,4])
                # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'A'), '%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A')])
     
    def run_measurement_start(self):        
        # Calculate sweep points
        self.stress_time_list = []
        self.vds_list = []
        self.vgs_list = []
        
        # Calculate list for gate bias
        vgs_start = round(float(self.PBSNBS_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
        vgs_stop =  round(float(self.PBSNBS_Gate_ParamBox.le_list[1].text()), ROUNDNUM)
        vgs_step =  round(float(self.PBSNBS_Gate_ParamBox.le_list[2].text()), ROUNDNUM)
        
        temp = vgs_start
        while (temp <= vgs_stop):
            self.vgs_list.append(temp)
            temp = round((temp + vgs_step), ROUNDNUM)
            
        if self.PBSNBS_Gate_ParamBox.rbtn_list[1].isChecked():
            self.vgs_list = np.concatenate([self.vgs_list, np.flip(self.vgs_list)])
            
        # calculate list for drain bias (single)
        self.vds_list.append(round(float(self.PBSNBS_Drain_ParamBox.le_list[0].text()), ROUNDNUM))
        
        # calculate list for stress times
        text = self.PBSNBS_Stress_ParamBox.le_list[2].text()
        self.stress_time_list = [float(x) for x in text.split(',')]
        
        self.tot_num_measure_points = len(self.stress_time_list)*len(self.vgs_list)
        
        self.stress_vgs = round(float(self.PBSNBS_Stress_ParamBox.le_list[0].text()), ROUNDNUM)
        self.stress_vds = round(float(self.PBSNBS_Stress_ParamBox.le_list[1].text()), ROUNDNUM)
                
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[]]
        self.SMU_init_params[0].append(round(float(self.PBSNBS_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PBSNBS_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PBSNBS_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PBSNBS_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.PBSNBS_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PBSNBS_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PBSNBS_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PBSNBS_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        print ("Bias parameters:")
        print (self.SMU_init_params[0])
        print (self.SMU_init_params[1])
        
        print ("Prepare measurement...")
        
        # Prepare data array for save
        self.result_data = np.empty((self.tot_num_measure_points, 7))
        self.result_data[:] = np.NaN
        self.N = 0
        self.start = 0
        
        #Reset graph
        self.PBSNBS_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   stress_time_list = self.stress_time_list,
                                   stress_vgs = self.stress_vgs,
                                   stress_vds = self.stress_vds)
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
        
        new_curve = np.empty(7)
        new_curve[:] = np.NaN
        self.signal.emit(new_curve)
        
        for stress_time in self.stress_time_list:
            if self.flag == 1:
                self.signal.emit([99999998,stress_time])
                self.signal.emit(new_curve) #Notify main function to draw a new curve
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.stress_vds))
                self.SMU_DRAIN.write(":OUTP ON")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.stress_vgs))
                self.SMU_GATE.write(":OUTP ON")                  
                
            else:
                break;
            self.stress_start_time = time.time()
            self.stress_finish_time = self.stress_start_time + stress_time    
            
            if self.flag == 1:
                while time.time()<self.stress_finish_time:
                    time.sleep(0.01)
                    self.signal.emit([99999997, int(self.stress_finish_time - time.time())])

            for vds in self.vds_list:
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                self.SMU_DRAIN.write(":OUTP ON")
                for vgs in self.vgs_list:
                    if self.flag == 1:
                        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(vgs))
                        self.SMU_GATE.write(":OUTP ON")
                        CURRENT_GATE = self.SMU_GATE.query_ascii_values(":READ?")
                        CURRENT_DRAIN = self.SMU_DRAIN.query_ascii_values(":READ?")
                        CURRENT_GATE = CURRENT_GATE[1]
                        CURRENT_DRAIN = CURRENT_DRAIN[1]
    
                        temp = np.array([vgs, vds, CURRENT_GATE, CURRENT_DRAIN, np.log10(np.abs(CURRENT_GATE)), np.log10(np.abs(CURRENT_DRAIN)), stress_time])

                        self.signal.emit(temp)
                    else:
                        break;
                        
        self.stop()     