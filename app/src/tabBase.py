#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:06:16 2019

@author: edgar
"""

import os

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore

from baseConfigWindow import BaseConfigWindow
from chronometer import Chronometer
from connectionToModel import ConnectionToModel

class TabBase(QWidget):
    '''
    Class TabBase is the sub widget that contains the base launch and 
    configuration access button
    Inherits from QWidget
    Divided into a Right Part and a Left Part
    
    Attributes:
        private path dirtrs : directory of the script
        private ConnectionToModel base_model : connector to the Base Model
        private QTimer base_timer : timer of the widget
        private QPushButton start_b : button that launchs the acquisition
        private QPushButton config_b : button that opens the Config Window
        private QLabel icon : base image
        private Chronometer chrono_base : chronometer taht appears on the UI for the base
        private QLabel stream_status : shows the status of the stream
        
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        
        #Setting font
        self.setFont(QFont('Helvetica',25))
        # Get path to the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        #Connection to the Base model
        self.__base_model = ConnectionToModel()
        #timer
        self.__base_timer = QtCore.QTimer(self)
        self.__base_timer.timeout.connect(self.updateBase) 
         
        
        ######  RIGHT PART OF THE WIDGET  ######
        
        # Start Button
        self.__start_b = QPushButton('Start', self)
        self.__start_b.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.__start_b.setCheckable(True)
        self.__start_b.toggled.connect(self.startBase) 
        
        # Config Button
        self.__config_b = QPushButton('Config', self)
        self.__config_b.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.__config_b.clicked.connect(self.openConfig)
        
        # horizontal layout for the buttons
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.__start_b)
        right_layout.addWidget(self.__config_b)
        
        
        ###### LEFT PART OF THE WIDGET  ######
        
        # Base image
        fig=QPixmap(self.__dirtrs +'/img/base.png')  
        self.__icon=QLabel(self)
        self.__icon.setPixmap(fig)
        
        # Chrono
        self.__chrono_base = Chronometer()
        
        # Setting left part layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.__icon)
        left_layout.addWidget(self.__chrono_base)
        
        ####### LOWER PART OF THE WIDGET ######
        status = QLabel('Stream Status:')
        status.setAlignment(QtCore.Qt.AlignLeft)
        self.__status_base = QLabel('Not Started')
        self.__status_base.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        
        lower_layout = QHBoxLayout()
        lower_layout.addWidget(status)
        lower_layout.addWidget(self.__status_base)
        
        ##### SETTING THE GLOBAL LAYOUT  ######
        
        base_layout = QHBoxLayout()
        base_layout.addLayout(left_layout)
        base_layout.addLayout(right_layout)
        
        base_layout2 = QVBoxLayout()
        base_layout2.addLayout(base_layout)
        base_layout2.addLayout(lower_layout)
         
        self.setLayout(base_layout2)
        
        
        ###########  FUNCTIONS  ##################
        
    def openConfig(self):
        '''
        Opens the BaseConfig subwindow
        '''
        try:
            # disabling buttons to prevent multi opennings and launchings
            self.__config_b.setDisabled(True)
            self.__start_b.setDisabled(True)
            
            subWindow=BaseConfigWindow(self)
            subWindow.setModel(self.__base_model)
            subWindow.show()
            
        except Exception as e:
            print(e)
        
        # enabling buttons back
        self.__config_b.setDisabled(False)
        self.__start_b.setDisabled(False)
        
            
    def startBase(self):
        '''
        Launches the acquisition
        Notifies the Model
        Modifies the UI
        '''
        if self.__start_b.isChecked():   # if the acquisition is started   
            
            try:
                # Notifying the model
                real_base_model = self.__base_model.getInstanceBase()
                real_base_model.startBase()

                # modifying the UI
                self.__start_b.setText('Stop')
                self.__config_b.setDisabled(True)
                
                self.__chrono_base.start()
                self.__base_timer.start(1000)
                
            except Exception as e:
                print(e)

        else:       # if the acquisition is stopped
            
            try:
                self.__base_timer.stop()
                
                # Notifying the model
                real_base_model = self.__base_model.getInstanceBase()
                real_base_model.stopBase()
                
                # modifying the UI
                self.__start_b.setText('Start')
                self.__config_b.setDisabled(False)
                self.__chrono_base.stop()
        
            except Exception as e:
                print(e)
                
                
    def updateBase(self):        
        '''
        Access the Raws from the model and displays information on screen
        Displays the the calculus mode, the calculated position and the stream status 
        '''
        
        real_base_model = self.__base_model.getInstanceBase()
        rawstream = real_base_model.getRaw() 
        
        if (rawstream=='stream server start error'):
            self.__status_base.setText('stream server start error\n')

        streams=rawstream.split()
        print(streams)
        if len(streams)==9:
            self.__status_base.setText(streams[0]+' '+streams[1]+' '+streams[5]+'bps '+streams[8])
        if len(streams)>=10:
            self.__status_base.setText(streams[0]+' '+streams[1]+' '+streams[5]+'bps '+streams[8]+' '+streams[10])
