#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:21:20 2019

@author: edgar
"""

import sys
import os

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPixmap

from tabRover import TabRover
from tabBase import TabBase
from tabPostProcessing import TabPostProcessing          

class MainWidget(QWidget):
    '''
    Class MainWidget is the main window of the application
    Inherits from QWidget
    Divided into a Upper Part and a Central Part
    
    Attributes : 
        private QPushButton quit_b
        private QPushButton shutdown_b
        private QLabel logo
        private TabRover tabRover
        private TabBase tabBase
        
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        
        #Setting font
        self.setFont(QFont('Helvetica',18))
        # Get path to the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        
        
        ######  UPPER PART OF THE WIDGET  #####
        
        # Quit Button
        self.__quit_b = QPushButton('Quit')
        self.__quit_b.resize(70,49)
        self.__quit_b.setMinimumSize(70, 49)
        self.__quit_b.clicked.connect(self.closeEvent)
        
        # Shutdown Button
        self.__shutdown_b = QPushButton('Shutdown')
        self.__shutdown_b.resize(70,49)
        self.__shutdown_b.setMinimumSize(70, 49)
        self.__shutdown_b.clicked.connect(self.shutdown)
        
        # Logo
        fig=QPixmap(self.__dirtrs + '/img/logo2.png')  
        self.__logo=QLabel(self)
        fig = fig.scaledToHeight(70)
        self.__logo.setPixmap(fig)
        
        #Setting upper part layout
        upper_part = QHBoxLayout()
        upper_part.addWidget(self.__logo)
        upper_part.addWidget(self.__quit_b)
        upper_part.addWidget(self.__shutdown_b)
        
        
        
        
        ######  CENTRAL PART OF THE WIDGET  ######
        
        central_part = QTabWidget()
        
        self.__tabRover = TabRover()
        self.__tabBase = TabBase()
        self.__tabPostProcessing = TabPostProcessing()
        
        central_part.addTab(self.__tabRover,'Rover')
        central_part.addTab(self.__tabBase,'Base')
        central_part.addTab(self.__tabPostProcessing,'Post-processing')
 
        ##### SETTING THE GLOBAL LAYOUT  ######
        
        global_layout = QVBoxLayout()
        
        global_layout.addLayout(upper_part)
        global_layout.addWidget(central_part)
        
        self.setLayout(global_layout)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.show()
        
        
        
    ##############  FUNCTIONS  ######################
        
    def closeEvent(self):
        '''
        Closes the application
        '''
        sys.exit(0)
        
    def shutdown(self):
        '''
        Shuts down the GNSS
        '''
        os.system("shutdown now -h")