#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:06:16 2019

@author: edgar
"""

import os

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap

from baseConfigWindow import BaseConfigWindow
from chronometer import Chronometer

class TabBase(QWidget):
    '''
    Class TabBase is the sub widget that contains the base launch and 
    configuration access button
    Inherits from QWidget
    Divided into a Right Part and a Left Part
    
    Attributes:
        private path dirtrs
        private QPushButton start_b
        private QPushButton config_b
        private QLabel icon
        private Chronometer chrono_base
        
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
        self.__start_b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.__start_b.setCheckable(True)
        #self.__start_b.toggled.connect(self.startRoverToggled) #à connecter correctement
        #self.__quit_b.clicked.connect(self.closeEvent)  # peut etre a virer
        
        # Config Button
        self.__config_b = QPushButton('Config', self)
        self.__config_b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
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
        
        
        
        ##### SETTING THE GLOBAL LAYOUT  ######
        
        base_layout = QHBoxLayout()
        base_layout.addLayout(left_layout)
        base_layout.addLayout(right_layout)
         
        self.setLayout(base_layout)
        
        
        ###########  FUNCTIONS  ##################
        
    def openConfig(self):
        '''
        Opens the BaseConfig subwindow
        '''
        try:
            print("a")
            subWindow=BaseConfigWindow(self)
            subWindow.show()
        except Exception as e:
            print(e)