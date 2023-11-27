# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):
    def tab_setup(self):
        self.tabMemory_Endurance = QWidget()
        self.tab = self.tabMemory_Endurance
        self.scan_type = "Memory endurance"
        
        """Memory_Endurance Tab Setup"""
        self.Memory_Endurance_Program_ParamBox = ui.CreateParameterSettingsBox('Program setup', 3)
        self.Memory_Endurance_Program_ParamBox.set_item(0, 'Program gate bias', '-10', 'V')
        self.Memory_Endurance_Program_ParamBox.set_item(1, 'Program drain bias', '10', 'V')
        self.Memory_Endurance_Program_ParamBox.set_item(2, 'Program pulse width', '200', 'ms')
        
        self.Memory_Endurance_Erase_ParamBox = ui.CreateParameterSettingsBox('Erase setup', 3)
        self.Memory_Endurance_Erase_ParamBox.set_item(0, 'Erase gate bias', '10', 'V')
        self.Memory_Endurance_Erase_ParamBox.set_item(1, 'Erase drain bias', '10', 'V')
        self.Memory_Endurance_Erase_ParamBox.set_item(2, 'Erase pulse width', '200', 'ms')
        
        self.Memory_Endurance_Read_ParamBox = ui.CreateParameterSettingsBox('Read setup', 3)
        self.Memory_Endurance_Read_ParamBox.set_item(0, 'Read gate bias', '0', 'V')
        self.Memory_Endurance_Read_ParamBox.set_item(1, 'Read drain bias', '1', 'V')
        self.Memory_Endurance_Read_ParamBox.set_item(2, 'Read pulse width', '200', 'ms')
        
        self.Memory_Endurance_Sequence_ParamBox = ui.CreateParameterSettingsBox('Sequence setup', 2)
        self.Memory_Endurance_Sequence_ParamBox.set_item(0, 'Delay between sequences', '200', 'ms')
        self.Memory_Endurance_Sequence_ParamBox.set_item(1, 'Total number of cycles', '100', '#')
        
        self.Memory_Endurance_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain SMU setup', 4)
        self.Memory_Endurance_Drain_ParamBox.set_item(0, 'Drain Trigger delay', '0', 'ms')
        self.Memory_Endurance_Drain_ParamBox.set_item(1, 'Drain Source delay', '0', 'ms')
        self.Memory_Endurance_Drain_ParamBox.set_item(2, 'Drain NPLC', '0.1', 'number')
        self.Memory_Endurance_Drain_ParamBox.set_item(3, 'Current compliance', '1E-3', 'A')
        
        self.Memory_Endurance_Gate_ParamBox = ui.CreateParameterSettingsBox('Gate SMU setup', 4)
        self.Memory_Endurance_Gate_ParamBox.set_item(0, 'Gate Trigger delay', '0', 'ms')
        self.Memory_Endurance_Gate_ParamBox.set_item(1, 'Gate Source delay', '0', 'ms')
        self.Memory_Endurance_Gate_ParamBox.set_item(2, 'Gate NPLC', '0.1', 'number')
        self.Memory_Endurance_Gate_ParamBox.set_item(3, 'Gate compliance', '1E-3', 'A')       
      
        self.Memory_Endurance_GraphBox = ui.CreateGraphBox('Memory Endurances', 1)
        self.Memory_Endurance_GraphBox.set_titles(0, 'Memory Endurance recording (Program/Erase)', 'Cycle (#)', 'Ids (A)')        

        # Memory_Endurance tab setup
        self.tabMemory_Endurance_hbox = QHBoxLayout()  
        self.tabMemory_Endurance_vbox = QVBoxLayout()
        self.tabMemory_Endurance_vbox.addWidget(self.Memory_Endurance_Program_ParamBox.groupbox)
        self.tabMemory_Endurance_vbox.addWidget(self.Memory_Endurance_Erase_ParamBox.groupbox)
        self.tabMemory_Endurance_vbox.addWidget(self.Memory_Endurance_Read_ParamBox.groupbox)
        self.tabMemory_Endurance_vbox.addWidget(self.Memory_Endurance_Sequence_ParamBox.groupbox)
        self.tabMemory_Endurance_vbox.addStretch(1)
        self.tabMemory_Endurance_vbox.addWidget(self.Memory_Endurance_Drain_ParamBox.groupbox)
        self.tabMemory_Endurance_vbox.addWidget(self.Memory_Endurance_Gate_ParamBox.groupbox)
        
        self.tabMemory_Endurance_vbox.addStretch(1)
        self.tabMemory_Endurance_hbox.addLayout(self.tabMemory_Endurance_vbox)
        self.tabMemory_Endurance_hbox.addWidget(self.Memory_Endurance_GraphBox.groupbox)
        self.tabMemory_Endurance_hbox.setStretch(0,1)
        self.tabMemory_Endurance_hbox.setStretch(1,4)
        self.tabMemory_Endurance.setLayout(self.tabMemory_Endurance_hbox)        
        
        #main ui communication test
        self.main.LogBox.update_log("Memory endurance module loaded")
    
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.Memory_Endurance_GraphBox.addnew_plot(0, type = "symbol")
                self.Memory_Endurance_GraphBox.addnew_plot(0, type = "symbol")
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.Memory_Endurance_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,1], graph_num=0)
                self.Memory_Endurance_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,4], graph_num=1)
                 # Update the plot
    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[0], 'V'), '%.4e%s' %(array[1], 'A'), '%.4e%s' %(array[2], 'V'), '%.4e%s' %(array[3], 'uA')])
                
                    
    def run_measurement_start(self):                
        # Calculate sweep points
        self.vds_list = []
        self.vgs_list = []
        
        # Calculate list for gate and drain biases
        vgs_program = round(float(self.Memory_Endurance_Program_ParamBox.le_list[0].text()), ROUNDNUM)
        vgs_erase =  round(float(self.Memory_Endurance_Erase_ParamBox.le_list[0].text()), ROUNDNUM)
        vgs_read =  round(float(self.Memory_Endurance_Read_ParamBox.le_list[0].text()), ROUNDNUM)
        
        vds_program = round(float(self.Memory_Endurance_Program_ParamBox.le_list[1].text()), ROUNDNUM)
        vds_erase = round(float(self.Memory_Endurance_Erase_ParamBox.le_list[1].text()), ROUNDNUM)
        vds_read =  round(float(self.Memory_Endurance_Read_ParamBox.le_list[1].text()), ROUNDNUM)
        
        self.pulse_width_program = round(float(self.Memory_Endurance_Program_ParamBox.le_list[2].text())/1000.0, ROUNDNUM)
        self.pulse_width_erase = round(float(self.Memory_Endurance_Erase_ParamBox.le_list[2].text())/1000.0, ROUNDNUM)      
        self.pulse_width_read = round(float(self.Memory_Endurance_Read_ParamBox.le_list[2].text())/1000.0, ROUNDNUM)
                
        self.wait_time = round(float(self.Memory_Endurance_Sequence_ParamBox.le_list[0].text())/1000.0, ROUNDNUM)
        self.repeat_num = int(self.Memory_Endurance_Sequence_ParamBox.le_list[1].text())
        
        self.vgs_list.append(vgs_program)
        self.vgs_list.append(vgs_erase)
        self.vgs_list.append(vgs_read)
        
        self.vds_list.append(vds_program)
        self.vds_list.append(vds_erase)
        self.vds_list.append(vds_read)
                                       
        self.tot_num_measure_points = self.repeat_num
                
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[]]
        self.SMU_init_params[0].append(round(float(self.Memory_Endurance_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Memory_Endurance_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Memory_Endurance_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.Memory_Endurance_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.Memory_Endurance_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Memory_Endurance_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Memory_Endurance_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.Memory_Endurance_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
        
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
        self.Memory_Endurance_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   wait_time = self.wait_time,
                                   pulse_width_program = self.pulse_width_program,
                                   pulse_width_erase = self.pulse_width_erase,
                                   pulse_width_read = self.pulse_width_read,
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
        print(self.vds_list[0])
        print(self.vds_list[1])
        print(self.vds_list[2])
        time.sleep(0.1)
        print("Initiallized SMUs")
        self.init_SMU(self.SMU_list[0], self.SMU_init_params[0])
        self.init_SMU(self.SMU_list[1], self.SMU_init_params[1])
        
        self.SMU_DRAIN = self.SMU_list[0]
        self.SMU_GATE = self.SMU_list[1]
        
        new_curve = np.empty(6)
        new_curve[:] = np.NaN
        time.sleep(0.1)
        print("Go to initial biasing points")
        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
        self.SMU_GATE.write(":OUTP ON")
        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
        self.SMU_DRAIN.write(":OUTP ON")
        
        self.signal.emit(new_curve)
        print("Memory_endurance measurement start") 
        print("Repeat number: %d" %(self.repeat_num))
        print("Pulse width for program: %.3f" %(self.pulse_width_program))
        print("Pulse width for erase: %.3f" %(self.pulse_width_erase))
        print("Pulse width for read: %.3f" %(self.pulse_width_read))
        print("Wait time: %.3f" %(self.wait_time))
        
        self.wait_time = self.take_positive(self.wait_time - self.OFFSET_TIME)
        self.pulse_width_program = self.take_positive(self.pulse_width_program - self.OFFSET_TIME)
        self.pulse_width_erase = self.take_positive(self.pulse_width_erase - self.OFFSET_TIME)
        self.pulse_width_read = self.take_positive(self.pulse_width_read - self.OFFSET_TIME)
        
        print("Adjusted wait time: %.3f" %(self.wait_time))
        print("Adjusted pulse width for program: %.3f" %(self.pulse_width_program))
        print("Adjusted pulse width for erase: %.3f" %(self.pulse_width_erase))
        print("Adjusted pulse width for read: %.3f" %(self.pulse_width_read))
        
        for i in range(self.repeat_num):
            if self.flag == 1:
                # Programming
                time.sleep(self.wait_time)
                print("Program")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs_list[0]))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds_list[0]))
                time.sleep(0.001)
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")
                time.sleep(self.pulse_width_program)
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")
                
                # Reading programmed state
                time.sleep(self.wait_time)
                print("Read programmed state")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs_list[2]))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds_list[2]))
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")
                time.sleep(self.pulse_width_read)
                temp_program = self.SMU_DRAIN.query_ascii_values(":READ?")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))  
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")               
                
                # Erasing
                time.sleep(self.wait_time)
                print("Erase")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs_list[1]))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds_list[1]))
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")
                time.sleep(self.pulse_width_erase)
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")
                
                # Reading erased state
                time.sleep(self.wait_time)
                print("Read erased state")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs_list[2]))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds_list[2]))
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")
                time.sleep(self.pulse_width_read)
                temp_erase = self.SMU_DRAIN.query_ascii_values(":READ?")
                self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))  
                self.SMU_GATE.query_ascii_values(":READ?")
                self.SMU_DRAIN.query_ascii_values(":READ?")   
                
                print("Update programmed/erased state: current levels")
                temp = np.array([i, temp_program[1], np.log10(np.abs(temp_program[1])), i, temp_erase[1], np.log10(np.abs(temp_erase[1]))])
                
                self.signal.emit(temp)                
            else:
                break;

        self.stop()     