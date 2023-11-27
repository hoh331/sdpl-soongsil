# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:05:31 2023

@author: Hongseok
"""

from module_common import *

class CreateClass(CreateClass_Super):        
    def tab_setup(self):
        self.tab = QWidget()   
        self.scan_type = "PD"
        
        """PD Tab Setup"""            
        self.PD_General_ParamBox = ui.CreateParameterSettingsBoxWithToggle('PD General Parameters', 3, 2, layout = "vertical")
        self.PD_General_ParamBox.set_toggle_item(0, "Drain (Memristor/Memtransistor)", 1)
        self.PD_General_ParamBox.set_toggle_item(1, "Gate (Synaptic Transistor)", 0)
        self.PD_General_ParamBox.set_item(0, 'Total # of cycles', '3', 'cycles')
        self.PD_General_ParamBox.set_item(1, 'Internal trigger refresh time', '50', 'ms')
        self.PD_General_ParamBox.set_item(2, 'Delay before start', '1', 's')
        
        self.PD_Pot_Pulse_ParamBox = ui.CreateParameterSettingsBox('Potentiation Pulse Parameters', 3)
        self.PD_Pot_Pulse_ParamBox.set_item(0, 'Number of pulses', '100', 'times')
        self.PD_Pot_Pulse_ParamBox.set_item(1, 'Pulse amplitude', '-5', 'V')
        self.PD_Pot_Pulse_ParamBox.set_item(2, 'Pulse width', '100', 'ms')
        
        self.PD_Neg_Pulse_ParamBox = ui.CreateParameterSettingsBox('Depression Pulse Parameters', 3)
        self.PD_Neg_Pulse_ParamBox.set_item(0, 'Number of pulses', '100', 'times')
        self.PD_Neg_Pulse_ParamBox.set_item(1, 'Pulse amplitude', '5', 'V')
        self.PD_Neg_Pulse_ParamBox.set_item(2, 'Pulse width', '100', 'ms')

        self.PD_Read_ParamBox = ui.CreateParameterSettingsBox('PD Read Parameters', 5)
        self.PD_Read_ParamBox.set_item(0, 'Read Drain bias', '1', 'V')
        self.PD_Read_ParamBox.set_item(1, 'Read Gate bias', '1', 'V')
        self.PD_Read_ParamBox.set_item(2, 'Before-read delay', '250', 'ms')
        self.PD_Read_ParamBox.set_item(3, 'After-read delay', '250', 'ms')
        self.PD_Read_ParamBox.set_item(4, 'Turn off bias while waiting', '0', '0:OFF/1:ON')       
       
        self.PD_Drain_ParamBox = ui.CreateParameterSettingsBox('Drain SMU setup', 7)
        self.PD_Drain_ParamBox.set_item(0, 'Drain Auto Zero', '0', '0: OFF/1: ON')
        self.PD_Drain_ParamBox.set_item(1, 'Drain Voltage source range', '20', 'V')        
        self.PD_Drain_ParamBox.set_item(2, 'Drain Current sensing range', '100E-6', 'A')        
        self.PD_Drain_ParamBox.set_item(3, 'Drain trigger delay', '0.0', 's')
        self.PD_Drain_ParamBox.set_item(4, 'Drain source delay', '0.0', 's')
        self.PD_Drain_ParamBox.set_item(5, 'Drain NPLC', '1', 'number')
        self.PD_Drain_ParamBox.set_item(6, 'Current compliance', '10E-3', 'A')
        
        self.PD_Gate_ParamBox = ui.CreateParameterSettingsBox('Gate SMU setup', 7)
        self.PD_Gate_ParamBox.set_item(0, 'Gate Auto Zero', '0', '0: OFF/1: ON')
        self.PD_Gate_ParamBox.set_item(1, 'Gate Voltage source range', '20', 'V')        
        self.PD_Gate_ParamBox.set_item(2, 'Gate Current sensing range', '100E-6', 'A')   
        self.PD_Gate_ParamBox.set_item(3, 'Gate trigger delay', '0.0', 's')
        self.PD_Gate_ParamBox.set_item(4, 'Gate source delay', '0.0', 's')
        self.PD_Gate_ParamBox.set_item(5, 'Gate NPLC', '1', 'number')
        self.PD_Gate_ParamBox.set_item(6, 'Current compliance', '100E-3', 'A')                
        
        self.PD_GraphBox = ui.CreateGraphBox('PD characteristics', 1)
        self.PD_GraphBox.set_titles(0, 'PD Curves', 'Pulse number (#)', 'Ids (A)')        
        
        
        # tab setup
        self.tab_hbox = QHBoxLayout()  
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox2 = QVBoxLayout()
        self.tab_vbox.addWidget(self.PD_Pot_Pulse_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.PD_Neg_Pulse_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.PD_Read_ParamBox.groupbox)
        self.tab_vbox.addWidget(self.PD_General_ParamBox.groupbox)
        self.tab_vbox.addStretch(1)
        
        self.tab_vbox2.addWidget(self.PD_Drain_ParamBox.groupbox)
        self.tab_vbox2.addWidget(self.PD_Gate_ParamBox.groupbox)       
        self.tab_vbox2.addStretch(1)

        self.tab_hbox.addLayout(self.tab_vbox)
        self.tab_hbox.addLayout(self.tab_vbox2)
        self.tab_hbox.addWidget(self.PD_GraphBox.groupbox)
        self.tab_hbox.setStretch(0,1)
        self.tab_hbox.setStretch(1,1)
        self.tab_hbox.setStretch(2,3)
        self.tab.setLayout(self.tab_hbox)
        
        #main ui communication test
        self.main.LogBox.update_log("PD module loaded")
      
    def update_plot(self, array):
        print(array)
        if array[0] == 99999999:
            self.measurement_done_flag = True
            self.stop_measurement()
        else:
            if np.isnan(array)[0] == True:
                self.PD_GraphBox.addnew_plot(0, type = "symbol")
                self.count = 1
                self.start = self.N
    
            else:
                self.result_data[self.N] = array
                self.PD_GraphBox.update_plot(0, self.result_data[self.start:self.start+self.count,0], self.result_data[self.start:self.start+self.count,2])
                
                # Update the plot    
                self.N = self.N+1
                self.count = self.count + 1
                
                self.main.LiveBox.set_status_run()
                self.main.LiveBox.set_values(['%.4e%s' %(array[1], 'V'), '%.4e%s' %(array[2], 'A'), '%.4e%s' %(array[3], 'V'), '%.4e%s' %(array[4], 'A')])

    def run_measurement_start(self):      
        # Calculate sweep points  
        
        print ("Table prepared")
        
        print ("Preparing bias parameters")
        self.SMU_init_params = [[],[]]
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[0].append(round(float(self.PD_Drain_ParamBox.le_list[-5].text()), ROUNDNUM))
        
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-4].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-3].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-2].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-1].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-7].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-6].text()), ROUNDNUM))
        self.SMU_init_params[1].append(round(float(self.PD_Gate_ParamBox.le_list[-5].text()), ROUNDNUM))
        print ("Bias parameters:")
        print (self.SMU_init_params[0])
        print (self.SMU_init_params[1])
        
        self.vds_list = []
        self.vgs_list = []
        
        # Calculate list for drain biases
        self.pulse_target = self.PD_General_ParamBox.rbtn_list[0].isChecked()
        self.total_num_cycles = round(float(self.PD_General_ParamBox.le_list[0].text()), ROUNDNUM)
        self.time_step = round(float(self.PD_General_ParamBox.le_list[1].text()), ROUNDNUM)       
        self.start_delay = round(float(self.PD_General_ParamBox.le_list[2].text()), ROUNDNUM)      
        self.wait_time = self.start_delay
        
        self.pot_pulse_num = round(float(self.PD_Pot_Pulse_ParamBox.le_list[0].text()), ROUNDNUM)
        self.pot_pulse_amp = round(float(self.PD_Pot_Pulse_ParamBox.le_list[1].text()), ROUNDNUM)
        self.pot_pulse_width = round(float(self.PD_Pot_Pulse_ParamBox.le_list[2].text()), ROUNDNUM)
        
        self.neg_pulse_num = round(float(self.PD_Neg_Pulse_ParamBox.le_list[0].text()), ROUNDNUM)
        self.neg_pulse_amp = round(float(self.PD_Neg_Pulse_ParamBox.le_list[1].text()), ROUNDNUM)
        self.neg_pulse_width = round(float(self.PD_Neg_Pulse_ParamBox.le_list[2].text()), ROUNDNUM)
                
        self.vds_list.append(round(float(self.PD_Read_ParamBox.le_list[0].text()), ROUNDNUM))
        self.vgs_list.append(round(float(self.PD_Read_ParamBox.le_list[1].text()), ROUNDNUM))
        self.before_read_delay = round(float(self.PD_Read_ParamBox.le_list[2].text()), ROUNDNUM)
        self.after_read_delay = round(float(self.PD_Read_ParamBox.le_list[3].text()), ROUNDNUM)
        self.read_bias_off = round(float(self.PD_Read_ParamBox.le_list[4].text()), ROUNDNUM)       
                
        print ("Prepare measurement...")
        self.tot_num_measure_points = (int(self.pot_pulse_num) + int(self.neg_pulse_num))*int(self.total_num_cycles)
        # Prepare data array for save
        self.result_data = np.empty((self.tot_num_measure_points, 5))
        self.result_data[:] = np.NaN
        self.N = 0
        self.start = 0
        
        #Reset graph
        self.PD_GraphBox.reset_plot()   
        
        # Initiate IO_Thread thread
        self.main.LogBox.update_log("SMU_list: %s" %(self.SMU_list))
        self.IO_Thread = IO_Thread(self.SMU_list, self.SMU_init_params, 
                                   scan_type = self.scan_type, 
                                   pulse_target = self.pulse_target,
                                   time_step = self.time_step,
                                   pot_pulse_num = self.pot_pulse_num,
                                   pot_pulse_amp = self.pot_pulse_amp,
                                   pot_pulse_width = self.pot_pulse_width,
                                   neg_pulse_num = self.neg_pulse_num,
                                   neg_pulse_amp = self.neg_pulse_amp,
                                   neg_pulse_width = self.neg_pulse_width,
                                   vds_list = self.vds_list, 
                                   vgs_list = self.vgs_list,
                                   before_read_delay = self.before_read_delay,
                                   after_read_delay = self.after_read_delay,
                                   read_bias_off = self.read_bias_off,
                                   start_delay = self.start_delay,
                                   total_num_cycles = self.total_num_cycles,
                                   wait_time = self.wait_time
                                   ) 
        self.IO_Thread.signal.connect(self.update_plot)
        self.main.LogBox.update_log("Measurement start!")
        self.IO_Thread.start()  

class IO_Thread(IO_Thread_Super):  
    def __init__(self, SMU_list, SMU_init_params, scan_type = None,
                 wait_time = None, vds_list = None, vgs_list = None, 
                 repeat_num = None, pulse_width = None, stress_time_list = None,
                 stress_vgs = None, stress_vds = None, parent = None, 
                 pulse_width_program = None, pulse_width_erase = None,
                 pulse_width_read = None, pulse_start = None, pulse_amp = None,
                 pulse_target = None, time_step = None, pulse_to_pulse_delay = None,
                 num_pulses = None, **kwargs):
        
        QtCore.QThread.__init__(self, parent)
        print("IO Thread start")
        
        self.SMU_list = SMU_list
        self.SMU_init_params = SMU_init_params
        self.scan_type = scan_type
        self.wait_time = wait_time
        self.pulse_target = pulse_target
        self.time_step = time_step
        self.vds_list = vds_list
        self.vgs_list = vgs_list
        self.pot_pulse_num = kwargs.get("pot_pulse_num")
        self.pot_pulse_amp = kwargs.get("pot_pulse_amp")
        self.pot_pulse_width = kwargs.get("pot_pulse_width")
        
        self.neg_pulse_num = kwargs.get("neg_pulse_num")
        self.neg_pulse_amp = kwargs.get("neg_pulse_amp")
        self.neg_pulse_width = kwargs.get("neg_pulse_width")
        
        self.before_read_delay = kwargs.get("before_read_delay")
        self.after_read_delay = kwargs.get("after_read_delay")
        self.read_bias_off = kwargs.get("read_bias_off")  
        self.start_delay = kwargs.get("start_delay")
        self.total_num_cycles = kwargs.get("total_num_cycles")
        
        self.flag = 1 # If measurment is done (or aborted)
        self.flag_pot_neg = 1 # 1: potentiation, 0: depression
        self.cycle_count = 1 # current cycle 
        self.pd_cycle_count = 1
        self.flag_status = 1 # current pulsation stage
        self.cycle_count_abs = 1
    
    def is_pulse_rightnow(self, current_time, time_seg_01, time_seg_02, time_seg_03):
       if current_time < time_seg_01:
           return 1
       elif current_time >= time_seg_01 and current_time < time_seg_02:
           return 2
       elif current_time >= time_seg_02 and current_time < time_seg_03:
           return 3
       else:
           return 4
                
    def run(self):
        def repeating_measurement():
            if self.flag == 1:
                CURRENT_TIME = time.time()-self.start_time
                flag_status = self.is_pulse_rightnow(CURRENT_TIME, self.time_seg_01, self.time_seg_02, self.time_seg_03)
                print("Current pulse number: %d" %(self.cycle_count))
                if flag_status == 1:
                    print("Time seg 01: Current: after read delay")
                    if self.read_bias_off == 1:
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
                        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                        self.SMU_GATE.query_ascii_values(":READ?")
                        self.SMU_DRAIN.query_ascii_values(":READ?")                        
                    else:
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds))
                        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs))
                        self.SMU_GATE.query_ascii_values(":READ?")
                        self.SMU_DRAIN.query_ascii_values(":READ?")
                elif flag_status == 2:
                    print("Time seg 02: Apply pulse")
                    self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vdsamp))
                    self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgsamp))
                    print((self.SMU_GATE.query_ascii_values(":READ?")))
                    print((self.SMU_DRAIN.query_ascii_values(":READ?"))) 
                elif flag_status == 3:
                    print("Time seg 03: Turn off pulse")
                    if self.read_bias_off == 1:
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(0))
                        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(0))
                        self.SMU_GATE.query_ascii_values(":READ?")
                        self.SMU_DRAIN.query_ascii_values(":READ?")                        
                    else:
                        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds))
                        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs))
                        self.SMU_GATE.query_ascii_values(":READ?")
                        self.SMU_DRAIN.query_ascii_values(":READ?")
                else:
                    print("Time seg 04: read")
                    self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds))
                    self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs))
                    CURRENT_GATE = (self.SMU_DRAIN.query_ascii_values(":READ?"))
                    CURRENT_DRAIN = (self.SMU_GATE.query_ascii_values(":READ?"))
                    print(CURRENT_GATE)
                    print(CURRENT_DRAIN)
                    temp = np.array([self.cycle_count_abs, CURRENT_DRAIN[0], CURRENT_DRAIN[1], CURRENT_GATE[0], CURRENT_GATE[1]])
                    self.signal.emit(temp)  
                    print("Pulse cycle done")
                    self.start_time = time.time() #reset start time
                    self.cycle_count = self.cycle_count + 1
                    self.cycle_count_abs = self.cycle_count_abs + 1
                    if self.cycle_count > self.cycle_count_max:
                        if self.flag_pot_neg == 1: # transition from potentiation to depression
                            print("Transition from potentiation to depression")
                            self.flag_pot_neg = 0
                            self.cycle_count = 1
                            self.cycle_count_max = self.neg_pulse_num
                            if self.pulse_target == 1:
                                self.vdsamp = self.vds + self.neg_pulse_amp
                            else:
                                self.vgsamp = self.vgs + self.neg_pulse_amp
                        else: # a cycle is done
                            self.pd_cycle_count = self.pd_cycle_count + 1
                            if self.pd_cycle_count <= self.total_num_cycles: # start next pd cycle
                                print("Start new PD cycle, transition from depression to potentiation")
                                self.flag_pot_neg = 1
                                self.cycle_count = 1
                                self.cycle_count_max = self.pot_pulse_num
                                if self.pulse_target == 1:
                                    self.vdsamp = self.vds + self.pot_pulse_amp
                                else:
                                    self.vgsamp = self.vgs + self.pot_pulse_amp
                            else: # measurment is done
                                print("All PD cycle is done")
                                self.flag = 0  
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
        
        self.time_seg_01 = self.after_read_delay/1000.0
        if self.flag_pot_neg == 1:
            self.time_seg_02 = round(float((self.after_read_delay+self.pot_pulse_width)/1000.0), ROUNDNUM)
        else:
            self.time_seg_02 = round(float((self.after_read_delay+self.neg_pulse_width)/1000.0), ROUNDNUM)            
        self.time_seg_03 = round(float(self.time_seg_02 + self.before_read_delay/1000.0), ROUNDNUM)
        self.cycle_count_max = self.pot_pulse_num
           
        self.vds = self.vds_list[0]
        self.vgs = self.vgs_list[0]

        self.vgsamp = self.vgs
        self.vdsamp = self.vds
        
        if self.pulse_target == 1:
            self.vdsamp = self.vds + self.pot_pulse_amp
        else:
            self.vgsamp = self.vgs + self.pot_pulse_amp
        
        timer = QTimer()
        timer.setTimerType(QtCore.Qt.PreciseTimer)
        timer.timeout.connect(repeating_measurement)
        
        new_curve = np.empty(5)
        new_curve[:] = np.NaN
        self.time_step = int(self.time_step)
        self.signal.emit(new_curve)
        
        self.SMU_GATE.write(":SOUR:VOLT:LEV ", str(self.vgs))
        self.SMU_GATE.write(":OUTP ON")
        
        self.SMU_DRAIN.write(":SOUR:VOLT:LEV ", str(self.vds))
        self.SMU_DRAIN.write(":OUTP ON")        

        time.sleep(self.wait_time)
        self.start_time = time.time()
        timer.start(self.time_step)
        self.exec_()
            
   
        