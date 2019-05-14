#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:46:17 2019

@author: pc-apple
"""

import os

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore

from chronometer import Chronometer
from postProcessingConfigWindow import PostProcessingConfigWindow

class TabPostProcessing(QWidget):
    '''
    Class TabRover is the sub widget that contains the rover launch, calculus mode,
    configuration and results for the rover
    Inherits from QWidget
    Divided into a Right Part, a Left Part, a Upper Part and a Lower Part
    
    Attributes:
        private path dirtrs
        private QPushButton start_b
        private QPushButton config_b
        private QLabel icon
        private Chronometer chrono_rover
        private QLabel lSol
        private QLabel lLong
        private QLabel lLat
        private QLabel lAlt
    
    !!!!!!! still need to implement upper part !!!!!!
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        
        #Setting font
        self.setFont(QFont('Helvetica',18))
        # Get path to the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        
        
        ######  RIGHT PART OF THE WIDGET  ######
        
        # Start Button
        self.__start_b = QPushButton('Start', self)
        self.__start_b.setCheckable(True)
        self.__start_b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.__start_b.toggled.connect(self.startRoverToggled) #à connecter correctement
        #self.__quit_b.clicked.connect(self.closeEvent)  # peut etre a virer
        
        # Config Button
        self.__config_b = QPushButton('Config', self)
        self.__config_b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.__config_b.clicked.connect(self.openConfig)
        
        
        # Setting right part layout
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.__start_b)
        right_layout.addWidget(self.__config_b)
        
        
        ######  LEFT PART OF THE WIDGET  ######
        
        # Rover image
        fig=QPixmap(self.__dirtrs +'/img/postProcessing.png')  
        self.__icon=QLabel(self)
        self.__icon.setPixmap(fig)
        
        # Chrono
        self.__chrono_rover = Chronometer()
        
        
        # Setting left part layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.__icon)
        left_layout.addWidget(self.__chrono_rover)
        
        
        ######  LOWER PART OF THE WIDGET  ######
        
        # Position indicators
        Sol_=QLabel('Sol:')
        Sol_.setAlignment(QtCore.Qt.AlignRight)
        Lat_=QLabel('Lat:')
        Lat_.setAlignment(QtCore.Qt.AlignRight)
        Lon_=QLabel('Lon:')
        Lon_.setAlignment(QtCore.Qt.AlignRight)
        Alt_=QLabel('Alt:')
        Alt_.setAlignment(QtCore.Qt.AlignRight)
       
        # Calculated Position
        self.__lSol=QLabel('')       
        self.__lLat=QLabel('')      
        self.__lLon=QLabel('')       
        self.__lAlt=QLabel('')
        
        # Setting lower part layout
        lower_layout = QHBoxLayout()
        
        lower_layout.addWidget(Sol_)
        lower_layout.addWidget(self.__lSol)
        lower_layout.addWidget(Lat_)
        lower_layout.addWidget(self.__lLat)
        lower_layout.addWidget(Lon_)
        lower_layout.addWidget(self.__lLon)
        lower_layout.addWidget(Alt_)
        lower_layout.addWidget(self.__lAlt)
        
        
        ###### UPPER PART OF THE WIDGET  ######
        
        
        # ajouter modes de calcul!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        ##### SETTING THE GLOBAL LAYOUT  ######
        
        rover_layout1 = QHBoxLayout()
        rover_layout1.addLayout(left_layout)
        rover_layout1.addLayout(right_layout)  
        
        rover_layout = QVBoxLayout()
        rover_layout.addLayout(rover_layout1)
        rover_layout.addLayout(lower_layout)
        self.setLayout(rover_layout)
        
        
        #################  FUNCTIONS  #########################
        
        
    def openConfig(self):
        '''
        Opens the RoverConfig subwindow
        '''
        try:
            print("a")
            subWindow = PostProcessingConfigWindow(self)
            subWindow.show()
        except Exception as e:
            print(e)