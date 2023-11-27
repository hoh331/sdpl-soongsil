# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:20:47 2022

@author: Hongseok Oh
"""

# For Qt layout (GUI)
from PyQt5.QtWidgets import (QLineEdit, QComboBox, QTextEdit, QGroupBox, QGridLayout)
from PyQt5.QtWidgets import (QPushButton, QRadioButton, QLabel)
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame)
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QFont, QColor
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)


# For dialog
import tkinter as tk # for the dialog of opening file
from tkinter import filedialog # for the dialog of opening file
import os
from datetime import datetime

# For VISA control
import pyvisa as visa
import numpy as np
      
class CreateConnectionControlBox:
    def __init__(self, title='Connection Control Box', num_equipment=3):
        self.groupbox = QGroupBox(title)
        self.grid = QGridLayout()
        self.rm = visa.ResourceManager()   
              
        self.lbl_list = [None]*num_equipment
        self.cb_list = [None]*num_equipment
        self.btn_list = [None]*num_equipment
        self.lbl_status_list = [None]*num_equipment
        self.num_equipment = num_equipment
        self.SMU_list = [None]*num_equipment
        
        self.flag = 0
        
        for i in range (num_equipment):
            self.lbl_list[i] = QLabel('%s%d%s' %('SMU',i,':'))
            self.cb_list[i] = QComboBox()
            self.btn_list[i] = QPushButton('Check')
            self.lbl_status_list[i] = QLabel('-')
      
            self.grid.addWidget(self.lbl_list[i],2*(i),0)
            self.grid.addWidget(self.cb_list[i],2*(i),1,1,2)
            self.grid.addWidget(self.btn_list[i],2*(i),3)
            self.grid.addWidget(self.lbl_status_list[i],2*(i)+1,0,1,4)
         
        self.btn_refresh = QPushButton('Refresh')
        self.grid.addWidget(self.btn_refresh,2*(num_equipment),3,1,1)
         
        self.groupbox.setLayout(self.grid)
        self.connection_refresh()

        self.btn_refresh.clicked.connect(self.connection_refresh)
        for i in range (num_equipment):
            self.btn_list[i].clicked.connect(self.makeFunc(i))
        # self.btn_list[0].clicked.connect(lambda: self.check_connection(0))
        # self.btn_list[1].clicked.connect(lambda: self.check_connection(1))
        # self.btn_list[2].clicked.connect(lambda: self.check_connection(2))
        
    
        
    def makeFunc(self, x):
        return (lambda: self.check_connection(x)) #Ref: https://stackoverflow.com/questions/19837486/lambda-in-a-loop

    def set_item(self, index, name):
        self.lbl_list[index].setText(name)
        
    def set_connections_list(self, itemlist):
        for i in range (self.num_equipment):
            self.cb_list[i].clear()
            self.cb_list[i].addItems(itemlist)
            
    def get_value(self, index):
        return(self.cb_list[index].currentText())
    
    def update_status(self, index, status):
        self.lbl_status_list[index].setText(status)
        
    def check_connection(self, index):
        print(index)
        self.SMU_list[index] = self.rm.open_resource(self.cb_list[index].currentText())
        print(self.SMU_list[index])
        text_update = self.SMU_list[index].query("*IDN?")
        self.update_status(index, text_update[0:50])
        keyword = 'DMM4020'        
        if keyword in text_update:
            print(self.SMU_list[index].read())
    
    def connection_refresh(self): #""" Refresh the connection with SMUs (Find available GPIB signals)"""
        # Clear the current items
        self.Conn_list = self.rm.list_resources()
        self.set_connections_list(self.Conn_list)
        for i in range(self.num_equipment):
            self.update_status(i, '-')
        # Add items available
        # Leave a log
        #self.update_log('Find available connections...\n')

    def get_SMU_list(self):
        for i in range (self.num_equipment):
            self.SMU_list[i] = self.rm.open_resource(self.cb_list[i].currentText())
        
        print(self.SMU_list)            
        return(self.SMU_list)
    
    def get_SMU_list_selectedonly(self, array):
        for i in array:
            self.SMU_list[i] = self.rm.open_resource(self.cb_list[i].currentText())        
        print(self.SMU_list)            
        return(self.SMU_list)
            
class CreateParameterSettingsBox:
    def __init__(self, title = 'Parameter Settings Box', num_parameter = 5):
        self.groupbox = QGroupBox(title)
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
                   
        self.lbl_param_list = [None]*num_parameter
        self.le_list = [None]*num_parameter
        self.lbl_unit_list = [None]*num_parameter
        self.hbox_list = [None]*num_parameter
        
        
        for i in range (num_parameter):
            self.lbl_param_list[i] = QLabel('%s%d%s' %('Parameter',i,':'))
            self.le_list[i] = QLineEdit('0')
            self.le_list[i].setAlignment(QtCore.Qt.AlignRight)
            self.lbl_unit_list[i] = QLabel('%s%d' %('Unit',i))
            
            self.hbox_list[i] = QHBoxLayout()
            self.hbox_list[i].addWidget(self.lbl_param_list[i])
            self.hbox_list[i].addWidget(self.le_list[i])
            self.hbox_list[i].addWidget(self.lbl_unit_list[i])
            self.vbox.addLayout(self.hbox_list[i])
            
        self.groupbox.setLayout(self.vbox)
        
    def set_item(self, index, name, value, unit):
        self.lbl_param_list[index].setText(name)
        self.le_list[index].setText(value)
        self.lbl_unit_list[index].setText(unit)
        
    def get_value(self, index):
        return(self.le_list[index].text())
    
    def show_only_name(self, index):
        self.hbox_list[index].removeWidget(self.le_list[index])
        self.hbox_list[index].removeWidget(self.lbl_unit_list[index])
        self.le_list[index].setHidden(True)
        self.lbl_unit_list[index].setHidden(True)
        
class CreateParameterSettingsBoxWithToggle:
    def __init__(self, title = 'Parameter Settings Box', num_parameter = 5, num_toggle = 2, **kwargs):
        self.groupbox = QGroupBox(title)
        self.rbtn_layout = kwargs.get("layout")
        if self.rbtn_layout == "vertical":
            self.hbox_toggle = QVBoxLayout()
        else:
            self.hbox_toggle = QHBoxLayout()

        self.vbox = QVBoxLayout()        
        
        self.rbtn_list = [None]*num_toggle
        for i in range (num_toggle):
            self.rbtn_list[i] = QRadioButton('%s%d' %('Item', i))
            self.rbtn_list[i].setChecked(False)
            self.hbox_toggle.addWidget(self.rbtn_list[i])
            
                    
        self.lbl_param_list = [None]*num_parameter
        self.le_list = [None]*num_parameter
        self.lbl_unit_list = [None]*num_parameter
        self.hbox_list = [None]*num_parameter
        
        self.vbox.addLayout(self.hbox_toggle)
        
        for i in range (num_parameter):
            self.lbl_param_list[i] = QLabel('%s%d%s' %('Parameter',i,':'))
            self.le_list[i] = QLineEdit('0')
            self.le_list[i].setAlignment(QtCore.Qt.AlignRight)
            self.lbl_unit_list[i] = QLabel('%s%d' %('Unit',i))
            
            self.hbox_list[i] = QHBoxLayout()
            self.hbox_list[i].addWidget(self.lbl_param_list[i])
            self.hbox_list[i].addWidget(self.le_list[i])
            self.hbox_list[i].addWidget(self.lbl_unit_list[i])
            
            self.vbox.addLayout(self.hbox_list[i])
            
        self.groupbox.setLayout(self.vbox)
        
        
        
    def set_item(self, index, name, value, unit):
        self.lbl_param_list[index].setText(name)
        self.le_list[index].setText(value)
        self.lbl_unit_list[index].setText(unit)
        
    def set_toggle_item(self, index, name, checked):
        self.rbtn_list[index].setText(name)
        self.rbtn_list[index].setChecked(checked)
        
    def get_value(self, index):
        return(self.le_list[index].text())
    
    def show_only_name(self, index):
        self.hbox_list[index].removeWidget(self.le_list[index])
        self.hbox_list[index].removeWidget(self.lbl_unit_list[index])
        self.le_list[index].setHidden(True)
        self.lbl_unit_list[index].setHidden(True)
        
class CreateGraphBox():
    def __init__(self, title = 'Graph plots', num_graph = 2):
        # Setup the plot screen
        self.groupbox = QGroupBox(title)
        self.hbox_plot = QHBoxLayout()
        self.canvas = []
        self.plot = []
        self.subplot_container = []
        self.num_graph = num_graph
        for i in range (num_graph):
            self.canvas.append(pg.GraphicsLayoutWidget())
            self.plot.append(self.canvas[i].addPlot())
            self.hbox_plot.addWidget(self.canvas[i])
                            
            self.plot[i].setTitle("%s%d" %('Graph',i), color='k', bold = True)
            self.plot[i].setLabel('left', "%s%d%s" %('Y-Axis',i,'(Unit)'))
            self.plot[i].setLabel('bottom', "%s%d%s" %('X-Axis',i,'(Unit)'))
            
            self.subplot_container.append([])
        
        # Setup background color and axis
        # Set grey color
        color_grey = [230,230,230]
        for i in range (num_graph):     
            self.canvas[i].setBackground(color_grey)
            self.plot[i].getAxis('left').setTextPen('k')
            self.plot[i].getAxis('right').setTextPen('k')
            self.plot[i].getAxis('bottom').setTextPen('k')
            self.plot[i].getAxis('top').setTextPen('k')
            self.plot[i].showAxis('right')
            self.plot[i].showAxis('top')
        

        self.groupbox.setLayout(self.hbox_plot)         
        
    def update_plot(self, index, x_data, y_data, graph_num = 9999):
        if graph_num == 9999:
            self.subplot_container[index][-1].setData(x_data, y_data)
        else:
            self.subplot_container[index][-(1+graph_num)].setData(x_data, y_data)
        
    def clear_plot(self, index):
        self.plot[index].clear()
        
    def addnew_plot(self, index, **kwargs):
        self.graph_type = kwargs.get("type")
        if self.graph_type == "symbol":
            self.subplot_container[index].append(self.plot[index].plot(pen = 'b', symbol='o', symbolPen='r'))
            if len(self.subplot_container[index])>1:
                self.subplot_container[index][-2].setPen('k')
                self.subplot_container[index][-2].setSymbolBrush(QColor(10, 130, 3))
        else:
            self.subplot_container[index].append(self.plot[index].plot(pen = pg.mkPen('r', width = 3)))
            if len(self.subplot_container[index])>1:
                self.subplot_container[index][-2].setPen('b')
            

        
            
    
        
    def reset_plot(self):
        for i in range(self.num_graph):
            self.plot[i].clear()
            self.subplot_container[i] = []

            
    def set_titles(self, index, title_name, x_axis_label, y_axis_label):
        self.plot[index].setTitle(title_name)
        self.plot[index].setLabel('left', y_axis_label)
        self.plot[index].setLabel('bottom', x_axis_label)
        

        
        
        
class CreateLiveValueBox(): # Execute the measurement 
    def __init__(self, title = 'Live Values', num_values = 3):
        self.num_values = num_values
        self.groupbox = QGroupBox('Live status') # Object to be returned
        # Outline layouts
        self.grid = QGridLayout() 
        self.lbl_status_value = QLabel('Idle')
        self.lbl_status_value.setStyleSheet("background-color: lightgreen;"
                                            "color: black;"
                                            "font: bold 12px")
        self.lbl_status_value.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grid.addWidget(self.lbl_status_value, 0,0,2,1)
        self.lbl_title_list = [None]*num_values
        self.lbl_value_list = [None]*num_values
        for i in range (num_values):
            self.lbl_title_list[i] = QLabel('%s%d' %('Value',i))
            self.lbl_title_list[i].setStyleSheet("color: black;"
                                                 "font: bold 12px")
            self.lbl_title_list[i].setAlignment(QtCore.Qt.AlignCenter)
            self.lbl_value_list[i] = QLabel('%d %s' %(0,'Unit'))
            self.lbl_value_list[i].setStyleSheet("background-color: black;"
                                                 "color: lightgreen;"
                                                 "font: bold 12px")
            self.lbl_value_list[i].setAlignment(QtCore.Qt.AlignCenter)
            self.grid.addWidget(self.lbl_title_list[i],0,i+1)
            self.grid.addWidget(self.lbl_value_list[i],1,i+1)
            
        self.groupbox.setLayout(self.grid)
        
    def set_titles(self, title_list):
        for i in range(self.num_values):
            self.lbl_title_list[i].setText(title_list[i])
            
    def set_values(self, value_list):
        for i in range(self.num_values):
            self.lbl_value_list[i].setText(value_list[i])
            
    def set_status_idle(self):
        self.lbl_status_value.setText('Idle')
        self.lbl_status_value.setStyleSheet("background-color: lightgreen;"
                                            "color: black;"
                                            "font: bold 12px")
        
    def set_status_run(self):
        self.lbl_status_value.setText('Running...')
        self.lbl_status_value.setStyleSheet("background-color: blue;"
                                            "color: white;"
                                            "font: bold 12px")
        
    def set_status_abort(self):
        self.lbl_status_value.setText('Abort')
        self.lbl_status_value.setStyleSheet("background-color: yellow;"
                                            "color: black;"
                                            "font: bold 12px")
    
        


class CreateDataSettingsBox:
    def __init__(self):
            # Settings for raw data save, folder and filename settings
        self.groupbox = QGroupBox('Data location and filename') # Object to be returned
        # Outline layouts
        self.vbox_settings = QVBoxLayout()
        self.hbox_settings_subbox_folder = QHBoxLayout()
        self.hbox_settings_subbox_filename = QHBoxLayout()
        
        # Widgets
        self.lbl_location = QLabel('Location:')
        self.le_location = QLineEdit('D:/Data')
        self.btn_location = QPushButton('Select folder')
        
        self.lbl_filename = QLabel('Filename:')
        self.le_filename = QLineEdit('noname')
                
        self.vbox_settings.addLayout(self.hbox_settings_subbox_folder)
        self.vbox_settings.addLayout(self.hbox_settings_subbox_filename)
        
        self.hbox_settings_subbox_folder.addWidget(self.lbl_location)
        self.hbox_settings_subbox_folder.addWidget(self.le_location)
        self.hbox_settings_subbox_folder.addWidget(self.btn_location)
        
        self.hbox_settings_subbox_filename.addWidget(self.lbl_filename)
        self.hbox_settings_subbox_filename.addWidget(self.le_filename)
    
        self.groupbox.setLayout(self.vbox_settings)
        
        self.btn_location.clicked.connect(self.select_folder)
        
        self.root = tk.Tk() # For folderpath selection window
        self.root.withdraw() # Don't show TK window
        self.root.dirName = 'D:/Data'
        
        
    def select_folder(self): # Select folder
        self.root.dirName = filedialog.askdirectory()
        self.le_location.setText(self.root.dirName)
        
    def file_name_check(self, folderpath, filename): # Check if the filename exists
        uniq = 1
        outputpath = '%s%s%s%s' %(folderpath, '/', filename, '.dat')
        newfilename = filename
        if os.path.exists(outputpath):
            newfilename = '%s(%d)' % (filename, uniq)
            outputpath = '%s%s%s%s' %(folderpath, '/', newfilename, '.dat')
            uniq += 1
            while os.path.exists(outputpath):
                newfilename = '%s(%d)' % (filename, uniq)
                outputpath = '%s%s%s%s' %(folderpath, '/', newfilename, '.dat')
                uniq += 1

        return newfilename
   
    def save_recording(self, data): # Save the recording to the dat file
        self.newfilename = self.file_name_check(self.root.dirName, self.le_filename.text())
        outputpath = '%s%s%s%s' %(self.root.dirName, '/', self.newfilename, '.dat')
        np.savetxt(outputpath, data, fmt = '%.6E', delimiter = ',', newline = '\n')
        

    
    
class CreateRunBox(): # Execute the measurement 
    def __init__(self):        
        self.groupbox = QGroupBox('Measurement') # Object to be returned
        # Outline layouts
        self.vbox_run = QVBoxLayout() 
        
        # Widgets
        self.btn_run = QPushButton('RUN')
        self.btn_abort = QPushButton('ABORT')
        # Draw widgets and layouts
        self.vbox_run.addWidget(self.btn_run)
        self.vbox_run.addWidget(self.btn_abort)
    
        self.groupbox.setLayout(self.vbox_run)
        


class CreateLogBox(): # Execute the measurement 
    def __init__(self):
        self.groupbox = QGroupBox('System log') # Object to be returned
        # Outline layouts
        self.vbox_status = QVBoxLayout() 
        
        # Widgets
        self.te_status_panel = QTextEdit()
        
        # Draw widgets and layouts
        self.vbox_status.addWidget(self.te_status_panel)
    
        self.groupbox.setLayout(self.vbox_status)
        
    def update_log(self, update_text):
        now = datetime.now()
        dt_string = now.strftime("[%Y-%m-%d %H:%M:%S]")
        self.te_status_panel.append('%s %s' %(dt_string, update_text))
        
    def remove_last_sentence(self):
        self.te_status_panel.undo()
        
class CreateSWInfoBox():
    def __init__(self, sw_text = None, date_text = None, name_text = None, aff_text = None, contact_text = None):
        self.groupbox = QGroupBox('SW Information')
        self.vbox = QVBoxLayout()
        self.lbl_sw = QLabel(sw_text)
        self.lbl_sw.setAlignment(QtCore.Qt.AlignCenter)
        # self.lbl_date = QLabel(date_text)
        # self.lbl_date.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_name = QLabel(name_text)
        self.lbl_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_aff= QLabel(aff_text)
        self.lbl_aff.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_contact = QLabel(contact_text)
        self.lbl_contact.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_sw)
        # self.vbox.addWidget(self.lbl_date)
        self.vbox.addWidget(self.lbl_name)
        self.vbox.addWidget(self.lbl_aff)
        self.vbox.addWidget(self.lbl_contact)
        self.groupbox.setLayout(self.vbox)
        
class TimeDisplayBox():
    def __init__(self):        
        font = QFont('Arial', 12, QFont.Bold)
        font_medium = QFont('Arial', 12, QFont.Bold)
        self.groupbox = QGroupBox('Time Display:')
        self.hbox_time_display = QHBoxLayout()
        self.vbox_current_time = QVBoxLayout()
        self.vbox_recording_time = QVBoxLayout()
        self.lbl_current_time_label = QLabel('Current date & time')
        self.lbl_current_time = QLabel('00:00:00')
        self.lbl_recording_time_label = QLabel('Time elapsed for the current measurment:')
        self.lbl_recording_time = QLabel('00:00:00.00')
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(100)
        self.vbox_current_time.addWidget(self.lbl_current_time_label)
        self.vbox_current_time.addWidget(self.lbl_current_time)
        self.vbox_recording_time.addWidget(self.lbl_recording_time_label)
        self.vbox_recording_time.addWidget(self.lbl_recording_time)
        self.hbox_time_display.addLayout(self.vbox_current_time)
        self.hbox_time_display.addLayout(self.vbox_recording_time)
        self.groupbox.setLayout(self.hbox_time_display)
        self.lbl_current_time.setFont(font_medium)
        self.lbl_recording_time.setFont(font_medium)
        self.lbl_current_time_label.setAlignment(Qt.AlignCenter)
        self.lbl_current_time.setAlignment(Qt.AlignCenter)
        self.lbl_recording_time_label.setAlignment(Qt.AlignCenter)
        self.lbl_recording_time.setAlignment(Qt.AlignCenter)
        
        
    def refresh(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_date = current_date.toString('yyyy/MM/dd')
        label_time = current_time.toString('hh:mm:ss')
        label = ('%s %s' %(label_date, label_time))
        self.lbl_current_time.setText(label)
        
    def update_time_elapsed(self):
        self.current_time = time.time()
        self.time_elapsed = self.current_time - self.start_time
        self.lbl_recording_time.setText(self.convert_time(self.time_elapsed))
        
    def convert_time(self, time_second):
        hours = time_second // 3600.0
        time_second = time_second - hours*3600.0
        minutes = time_second // 60.0
        time_second = time_second - minutes*60.0
        
        return('%02.0f:%02.0f:%05.2f'%(hours, minutes, time_second))
    def check_start_time(self):
        self.start_time = time.time()
        
        
    