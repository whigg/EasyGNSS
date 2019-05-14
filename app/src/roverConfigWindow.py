#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:52:22 2019

@author: edgar
"""

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QDialog, QSizePolicy, QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QFont

from correctionConfig import CorrectionConfig
from inputConfig import InputConfig
from solConfig import SolConfig
from logConfig import LogConfig
from calculusConfig import CalculusConfig
from basePosConfig_Rover import BasePosConfig_Rover
from confConfig import ConfConfig


class RoverConfigWindow:
    '''
    Class RoverConfigWindow is a QDialog subwindow that opens when TabRover.__confi_b is clicked
    It contains all the changeable parameters for the acquisition sorted by type
    
    Attributes:
        private QDialog window : the window created by the class
        private ConnectionToModel rover_model : accessor to the Rover Model
        private InputConfig tab_input : to change input parameters (see InputConfig)
        private CorrectionConfig tab_corr : to change input2 parameters (see CorrectionConfig)
        private SolConfig tab_sol : to change solution parameters (see SolConfig)
        private LogConfig tab_log : to change log parameters (see LogConfig)
        private BasePosConfig_Rover tab_basepos : to change Base position parameters (see BasePosConfig_Rover)
        private QPushButton apply_b : apply and save the modified parameters
        private QPushButton close_b : close the config window
    '''
    def __init__(self, parent=None):
        
        self.__window = QDialog(parent)
        self.__parent = parent
        

        self.__window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.__window.setGeometry(0, 0, 1100, 600)
        self.__window.setStyleSheet("background-color: rgb(245, 190, 35); font: 25pt 'Helvetica';")

        self.__rover_model = None
        
        
        
        ######  CONFIGURATION PART  ######
        tabs = QTabWidget()

        self.__tab_conf=ConfConfig()
        self.__tab_calculus=CalculusConfig()
        self.__tab_input=InputConfig()
        self.__tab_corr=CorrectionConfig()
        self.__tab_sol=SolConfig()
        self.__tab_log=LogConfig()
        self.__tab_basepos=BasePosConfig_Rover()
       
        tabs.addTab(self.__tab_conf,"Conf file")
        tabs.addTab(self.__tab_calculus,"Calculus")
        tabs.addTab(self.__tab_basepos,"BasePos")
        tabs.addTab(self.__tab_sol,"Solution")
        tabs.addTab(self.__tab_log,"Log")
        tabs.addTab(self.__tab_input,"Input 1")
        tabs.addTab(self.__tab_corr,"Input 2")
        
        
        
        
        ######  BUTTONS  ######

        self.__apply_button= QPushButton('Apply')
        self.__apply_button.clicked.connect(self.applyParam)
        self.__close_button= QPushButton('Close')
        self.__close_button.clicked.connect(self.__window.close)
    
        hbox = QHBoxLayout()
        hbox.addWidget(self.__apply_button)
        hbox.addWidget(self.__close_button)
        
        ######  SETTING GLOBAL LAYOUT ######
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        layout.addLayout(hbox)

        self.__window.setLayout(layout)
        
        
        
    def show(self):
        '''
        Show RoverConfigWindow on screen
        '''
        self.__window.exec_()
        
    def setModel(self, model):
        '''
        Setter of the model attribute
        '''
        self.__rover_model = model
        
    def applyParam(self):
        '''
        Apply the chosen parameters to the model
        
        The getOptions method for each classes returns the values of each option
        It is hard coded so obviously not incredible but I could not return a list of values as I'd like
        cause Python encodes the list
        This might be interessting to find another way round for future developpments
        '''
        
        options = []
        
        (a, b, c, d) = self.__tab_conf.getOptions()
        options.append([a, b, c, d])
        
        (a, b, c, d, e, f, g) = self.__tab_calculus.getOptions()
        options.append([a, b, c, d, e, f, g])

        (a, b, c, d, e, f) = self.__tab_input.getOptions()
        options.append([a, b, c, d, e, f])

        (a, b, c, d, e, f,g ,h) = self.__tab_corr.getOptions()
        options.append([a, b, c, d, e, f, g ,h])

        (a, b, c, d) = self.__tab_sol.getOptions()
        options.append([a, b, c, d])

        (a, b) = self.__tab_log.getOptions()
        options.append([a, b])

        (a, b, c, d, e) = self.__tab_basepos.getOptions()
        options.append([a, b, c, d, e])
      
               
        real_rover_model = self.__rover_model.getInstanceRover()
        real_rover_model.setOptions(options)
        
        self.confirmApply()
        
        
    def confirmApply(self):
        '''
        Shows a small subwindow to confirm that parameters have been applied 
        It exits both config window and subwindow when 'OK' is pressed
        '''

        d = QDialog()
        d.setGeometry(400,300,200,200)
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