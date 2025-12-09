# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):
    def tab_setup(self):
        self.tabIV = QWidget()
        self.tab = self.tabIV
        self.scan_type = "I-V"
        """I-V Tab Setup"""
       
        self.IV_Drain_ParamBox =  ui.CreateParameterSettingsBoxWithToggle('Drain bias setup', 10, 3, layout = "vertical")
        self.IV_Drain_ParamBox.set_toggle_item(0, 'Single sweep', True)
        self.IV_Drain_ParamBox.set_toggle_item(1, 'Double sweep', False)
        self.IV_Drain_ParamBox.set_toggle_item(2, 'Cycle sweep', False)
        self.IV_Drain_ParamBox.set_item(0, 'Vds start (Neg. Lim. cycle sweep)', '0', 'V')
        self.IV_Drain_ParamBox.set_item(1, 'Vds stop (Pos. Lim. cycle sweep)', '1', 'V')
        self.IV_Drain_ParamBox.set_item(2, 'Vds step', '0.02', 'V')
        self.IV_Drain_ParamBox.set_item(3, 'Number of sweeps', '1', 'cycle(s)')
        self.IV_Drain_ParamBox.set_item(4, 'Delay before sweep', '1', 's')
        self.IV_Drain_ParamBox.set_item(5, '<Measurement settings>', '0', '0')
        self.IV_Drain_ParamBox.show_only_name(5)
        self.IV_Drain_ParamBox.set_item(6, 'Drain trigger delay', '0.01', 's')
        self.IV_Drain_ParamBox.set_item(7, 'Drain source delay', '0.01', 's')
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
        
        #main ui communication test
        self.main.LogBox.update_log("I/V loaded")
     
    def update_plot(self, array):     
        print(array)
        if array[0] == 99999999:
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
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A'), '- V', ' -A'])     
                    
    def run_measurement_start(self):
        # Calculate sweep points
        self.vds_list = []
        self.wait_time = round(float(self.IV_Drain_ParamBox.le_list[4].text()), ROUNDNUM)
        
        # Calculate list for drain biases
        vds_start = round(float(self.IV_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
        vds_stop =  round(float(self.IV_Drain_ParamBox.le_list[1].text()), ROUNDNUM)
        vds_step =  round(float(self.IV_Drain_ParamBox.le_list[2].text()), ROUNDNUM)
        self.repeat_num = int(self.IV_Drain_ParamBox.le_list[3].text())
        
        if self.IV_Drain_ParamBox.rbtn_list[2].isChecked():
            temp = 0.0
            while (temp <= vds_stop):
                self.vds_list.append(temp)
                temp = round((temp + vds_step), ROUNDNUM)
            
            temp = round((temp - vds_step), ROUNDNUM)
            while (temp >= vds_start):
                self.vds_list.append(temp)
                temp = round((temp - vds_step), ROUNDNUM)
            
            temp = round((temp + vds_step), ROUNDNUM)                   
            while (temp <= 0.0):
                self.vds_list.append(temp)
                temp = round((temp + vds_step), ROUNDNUM)               

        else:
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
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   repeat_num = self.repeat_num,
                                   wait_time = self.wait_time)
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()     
        
class IO_Thread(IO_Thread_Super):        
    def run(self):
        print("Scan type: %s" %(self.scan_type))
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        
        self.SMU_DRAIN = self.SMU_list[0]
        
        new_curve = np.empty(3)
        new_curve[:] = np.NaN
        self.signal.emit(new_curve)
        
        for i in range(self.repeat_num):
            if self.flag == 1:
                self.signal.emit(new_curve) #Notify main function to draw a new curve
                time.sleep(self.wait_time)
            else:
                break;
            for vds in self.vds_list:
                if self.flag == 1:
                    self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(vds))
                    self.SMU_DRAIN.write(":OUTP ON")
                    CURRENT_DRAIN = self.SMU_DRAIN.query_ascii_values(":READ?")
                    CURRENT_DRAIN = CURRENT_DRAIN[1]

                    temp = np.array([vds, CURRENT_DRAIN, np.log10(np.abs(CURRENT_DRAIN))])

                    self.signal.emit(temp)
                else:
                    break;

        self.stop()     

    def stop(self):  
        self.signal.emit([99999999,99999999,99999999])  

        print("IO_Thread stop called") 
        self.SMU_DRAIN.write("OUTP OFF")    
        self.quit()
        