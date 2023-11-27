# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):
    def tab_setup(self):
        self.tabCollector = QWidget()
        self.tab = self.tabCollector
        self.scan_type = "Collector"
        
        """Collector Tab Setup"""
        self.Collector_Drain_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Collector bias setup', 9, 2)
        self.Collector_Drain_ParamBox.set_toggle_item(0, 'Single sweep', True)
        self.Collector_Drain_ParamBox.set_toggle_item(1, 'Double sweep', False)
        self.Collector_Drain_ParamBox.set_item(0, 'Vc start', '0', 'V')
        self.Collector_Drain_ParamBox.set_item(1, 'Vc stop', '1', 'V')
        self.Collector_Drain_ParamBox.set_item(2, 'Vc step', '0.02', 'V')
        self.Collector_Drain_ParamBox.set_item(3, 'Delay before sweep', '1', 's')
        self.Collector_Drain_ParamBox.set_item(4, '<Measurement settings>', '0', '0')
        self.Collector_Drain_ParamBox.show_only_name(4)
        self.Collector_Drain_ParamBox.set_item(5, 'Collector trigger delay', '0.01', 's')
        self.Collector_Drain_ParamBox.set_item(6, 'Collector source delay', '0.01', 's')
        self.Collector_Drain_ParamBox.set_item(7, 'Collector NPLC', '1', 'number')
        self.Collector_Drain_ParamBox.set_item(8, 'Current compliance', '10E-3', 'A')
        
        self.Collector_Gate_ParamBox = ui.CreateParameterSettingsBoxWithToggle('Base current setup', 8, 2)
        self.Collector_Gate_ParamBox.set_toggle_item(0, 'Linear steps', False)
        self.Collector_Gate_ParamBox.set_toggle_item(1, 'Custom steps', True)
        self.Collector_Gate_ParamBox.set_item(0, 'Ib (start)', '5, 10, 20, 30', 'uA')
        self.Collector_Gate_ParamBox.set_item(1, 'Ib stop', '10', 'uA')
        self.Collector_Gate_ParamBox.set_item(2, 'Ib step', '10', 'uA')
        self.Collector_Gate_ParamBox.set_item(3, '<Measurement settings>', '0', '0')
        self.Collector_Gate_ParamBox.show_only_name(3)
        self.Collector_Gate_ParamBox.set_item(4, 'Base trigger delay', '0.01', 's')
        self.Collector_Gate_ParamBox.set_item(5, 'Base source delay', '0.01', 's')
        self.Collector_Gate_ParamBox.set_item(6, 'Base NPLC', '1', 'number')
        self.Collector_Gate_ParamBox.set_item(7, 'Voltage compliance', '25', 'V')
        
        self.Collector_GraphBox = ui.CreateGraphBox('Collector characteristics', 1)
        self.Collector_GraphBox.set_titles(0, 'Collector characteristic curves (Ic-Vc)', 'Vc (V)', 'Ic (A)')
        
 
        # Collector tab setup
        self.tabCollector_hbox = QHBoxLayout()  
        self.tabCollector_vbox = QVBoxLayout()
        self.tabCollector_vbox.addWidget(self.Collector_Drain_ParamBox.groupbox)
        self.tabCollector_vbox.addWidget(self.Collector_Gate_ParamBox.groupbox)
        self.tabCollector_vbox.addStretch(1)
        self.tabCollector_hbox.addLayout(self.tabCollector_vbox)
        self.tabCollector_hbox.addWidget(self.Collector_GraphBox.groupbox)
        self.tabCollector_hbox.setStretch(0,1)
        self.tabCollector_hbox.setStretch(1,4)
        self.tabCollector.setLayout(self.tabCollector_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("BJT Collector module loaded")
     
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.Collector_GraphBox.addnew_plot(0)
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.Collector_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,1], self.result_data[self.start:self.start+self.count,3])
                 # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[3], 'A'), '%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[0], 'uA')])
     
                    
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
        self.wait_time = round(float(self.Collector_Drain_ParamBox.le_list[3].text()), ROUNDNUM)
        
        # Calculate list for drain biases
        vds_start = round(float(self.Collector_Drain_ParamBox.le_list[0].text()), ROUNDNUM)
        vds_stop =  round(float(self.Collector_Drain_ParamBox.le_list[1].text()), ROUNDNUM)
        vds_step =  round(float(self.Collector_Drain_ParamBox.le_list[2].text()), ROUNDNUM)
        
        temp = vds_start
        while (temp <= vds_stop):
            self.vds_list.append(temp)
            temp = round((temp + vds_step), ROUNDNUM)
            
        if self.Collector_Drain_ParamBox.rbtn_list[1].isChecked():
            self.vds_list = np.concatenate([self.vds_list, np.flip(self.vds_list)])
            
        # calculate list for gate biases
        if self.Collector_Gate_ParamBox.rbtn_list[1].isChecked():
            text = self.Collector_Gate_ParamBox.le_list[0].text()
            self.vgs_list = [float(x) for x in text.split(',')]
            
        else:                
            vgs_start = round(float(self.Collector_Gate_ParamBox.le_list[0].text()), ROUNDNUM)
            vgs_stop =  round(float(self.Collector_Gate_ParamBox.le_list[1].text()), ROUNDNUM)
            vgs_step =  round(float(self.Collector_Gate_ParamBox.le_list[2].text()), ROUNDNUM)     
            
            temp = vgs_start
            while (temp <= vgs_stop):
                self.vgs_list.append(temp)
                temp = round((temp + vgs_step), ROUNDNUM)   

        self.tot_num_measure_points = len(self.vds_list)*len(self.vgs_list)
        
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[]]
        self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Collector_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Collector_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
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
        self.Collector_GraphBox.reset_plot()   
        
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
        self.init_SMU_Curr(self.SMU_list[1], self.SMU_init_params[1])
        
        self.SMU_COLLECTOR = self.SMU_list[0]
        self.SMU_BASE = self.SMU_list[1]
        
        new_curve = np.empty(6)
        new_curve[:] = np.NaN
        self.signal.emit(new_curve)
        
        # self.vgs_list = np.multiply(self.vgs_list, 1.0E-6)
        
        for vgs in self.vgs_list:
            if self.flag == 1:
                vgs_str = str(vgs)+str("E-6")
                print("Vgs value:")
                print(vgs_str)
                self.SMU_BASE.write(":SOUR:CURR:LEV ", vgs_str)
                self.SMU_BASE.write(":OUTP ON")
                self.signal.emit(new_curve) #Notify main function to draw a new curve
            else:
                break;
            for vds in self.vds_list:
                if self.flag == 1:
                    if vds == self.vds_list:
                        time.sleep(self.wait_time)
                    self.SMU_COLLECTOR.write(":SOUR:VOLT:LEV ", str(vds))
                    self.SMU_COLLECTOR.write(":OUTP ON")
                    CURRENT_GATE = self.SMU_BASE.query_ascii_values(":READ?")
                    CURRENT_DRAIN = self.SMU_COLLECTOR.query_ascii_values(":READ?")
                    print("gate reading")
                    print(CURRENT_GATE)
                    VOLTAGE_GATE = CURRENT_GATE[0]
                    CURRENT_GATE = CURRENT_GATE[1]
                    CURRENT_DRAIN = CURRENT_DRAIN[1]

                    temp = np.array([vgs, vds, VOLTAGE_GATE, CURRENT_DRAIN, np.log10(np.abs(CURRENT_GATE)), np.log10(np.abs(CURRENT_DRAIN))])

                    self.signal.emit(temp)
                else:
                    break;
        self.stop()     