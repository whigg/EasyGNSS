#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:42:52 2019

@author: edgar
"""

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QDialog, QDesktopWidget, QLabel, QSizePolicy
from PyQt5 import QtCore
from PyQt5.QtGui import QFont

from outputConfig import OutputConfig
from inputConfig import InputConfig
from outputSerialConfig import OutputSerialConfig
from logConfig import LogConfig
from basePosConfig_Base import BasePosConfig_Base



class BaseConfigWindow:
    '''
    Class BaseConfigWindow is a QDialog subwindow that opens when TabBase.__confi_b is clicked
    It contains all the changeable parameters for the acquisition sorted by type
    
    Attributes:       
        private QDialog window : the window created by the class
        private ConnectionToModel rover_model : accessor to the Rover Model
        private InputConfig tab_input : to change input parameters (see InputConfig)
        private OutputConfig tab_output : to change output parameters (see OutputConfig)
        private OutputSerialConfig tab_output_serial : to change output2 parameters (see OutputSerialConfig)
        private LogConfig tab_log : to change log parameters (see LogConfig)
        private BaseposConfig_Base tab_basepos : to change Base position parameters (see BasePosConfig_Rover)
        private QPushButton apply_b : apply and save the modified parameters
        private QPushButton close_b : close the config window
    '''
    
    def __init__(self, parent=None):
        
        self.__window = QDialog(parent)
        self.__parent = parent

        self.__window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        screenShape = QDesktopWidget().screenGeometry()

        self.__window.setGeometry(0, 0, int(screenShape.width()*1100/1366), int(screenShape.height()*500/768))
        string = "background-color: rgb(245, 190, 35); font: 25pt 'Helvetica';"
        self.__window.setStyleSheet(string)

        self.__base_model = None
        
        
        ######  CONFIGURATION PART  ######
        tabs = QTabWidget()

        self.__tab_input = InputConfig()

        self.__tab_output = OutputConfig()

        self.__tab_output_serial = OutputSerialConfig()

        self.__tab_log = LogConfig()

        self.__tab_basepos = BasePosConfig_Base()
        
        tabs.addTab(self.__tab_basepos,"BasePos")
        tabs.addTab(self.__tab_log,"Log")        
        tabs.addTab(self.__tab_input,"Input")
        tabs.addTab(self.__tab_output_serial,"Output 1")
        tabs.addTab(self.__tab_output,"Output 2")
        

        
        ######  BUTTONS  ######

        self.__apply_button= QPushButton('Apply')
        self.__apply_button.clicked.connect(self.applyParam)
        self.__close_button= QPushButton('Close')
        self.__close_button.clicked.connect(self.__window.close)

        layout = QVBoxLayout()
        layout.addWidget(tabs)

        hbox = QHBoxLayout()
        hbox.addWidget(self.__apply_button,1)
        hbox.addWidget(self.__close_button,1)
        layout.addLayout(hbox)

        self.__window.setLayout(layout)
        
        
    def show(self):
        '''
        Displays BaseConfigWindow on screen 
        '''
        self.__window.exec_()
     
        
    def setModel(self, model):
        '''
        Setter of the model attribute
        '''
        self.__base_model = model
        
    def applyParam(self):
        '''
        Apply the chosen parameters to the model
        
        The getOptions method for each classes returns the values of each option
        It is hard coded so obviously not incredible but I could not return a list of values as I'd like
        cause Python encodes the list
        This might be interessting to find another way round for future developpments
        '''
        
        options = []

        (a, b, c, d) = self.__tab_basepos.getOptions()
        options.append([a, b, c, d])

        (a, b) = self.__tab_log.getOptions()
        options.append([a, b])

        (a, b, c, d, e, f) = self.__tab_input.getOptions()
        options.append([a, b, c, d, e, f])

        (a, b, c, d, e, f, g, h) = self.__tab_output.getOptions()
        options.append([a, b, c, d, e, f, g ,h])

        (a, b, c, d, e, f, g, h) = self.__tab_output_serial.getOptions()
        options.append([a, b, c, d, e, f, g, h])

    
        real_base_model = self.__base_model.getInstanceBase()
        real_base_model.setOptions(options)
        
        self.confirmApply()
        
        
    def confirmApply(self):
        '''
        Shows a small subwindow to confirm that parameters have been applied 
        '''

        d = QDialog()
        screenShape = QDesktopWidget().screenGeometry()
        d.setGeometry(int(screenShape.width()*400/1366), int(screenShape.height()*300/768),int(screenShape.width()*200/1366), int(screenShape.height()*200/768))
        d.setWindowTitle('Parameters')
        d.setFont(QFont('Helvetica',18))
        
        label = QLabel('Parameters saved')
        
        b1 = QPushButton("ok",d)
        b1.clicked.connect(self.__window.close)
        b1.clicked.connect(d.close)
        b1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(b1)
        d.setLayout(layout)
        d.setStyleSheet("background-color: rgb(161,183,36); font: 24pt 'Helvetica'; ")
        
        d.exec_()
