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
from PyQt5.QtGui import QPixmap

from tabRover import TabRover
from tabBase import TabBase
from tabSatellites import TabSatellites
from tabPostProcessing import TabPostProcessing

class MainWidget(QWidget):
    '''
    Class MainWidget is the main window of the application
    Inherits from QWidget
    Divided into a Upper Part and a Central Part
    
    Attributes : 
        private QPushButton quit_b : button to quit EasyGNSS
        private QPushButton shutdown_b : button to shutdown the GNSS
        private QLabel bannar : EasyGNSS bannar 
        private TabRover tabRover : UI part corresponding to the rover
        private TabBase tabBase : UI part corresponding to the base
        private TabPostProcessing tabPostProcessing : UI part corresponding to the post processing
        private TabSatellites tabSatellites : UI part corresponding to the Satellites information
        private path dirtrs : directory of the script
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        #Setting style
        string = "background-color: rgb(161,183,36); font: 25pt 'Helvetica';"
        self.setStyleSheet(string)

        
        # Get path to the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        
        
        ######  UPPER PART OF THE WIDGET  #####
        
        # Quit Button
        self.__quit_b = QPushButton('Quit')
        self.__quit_b.resize(70,49)
        self.__quit_b.setMinimumSize(70, 49)
        self.__quit_b.clicked.connect(self.closeEvent)
        self.__quit_b.setStyleSheet("background-color: rgb(255, 203, 45);")
        
        # Shutdown Button
        self.__shutdown_b = QPushButton('Shutdown')
        self.__shutdown_b.resize(70,49)
        self.__shutdown_b.setMinimumSize(70, 49)
        self.__shutdown_b.clicked.connect(self.shutdown)
        self.__shutdown_b.setStyleSheet("background-color: rgb(255, 203, 45);")
        
        # Bannar
        fig=QPixmap(self.__dirtrs +'/img/logo2.png')  
        self.__bannar=QLabel(self)
        fig = fig.scaledToHeight(70)
        self.__bannar.setPixmap(fig)

        
        
        #Setting upper part layout
        upper_part = QHBoxLayout()
        upper_part.addWidget(self.__bannar)
        upper_part.addWidget(self.__quit_b)
        upper_part.addWidget(self.__shutdown_b)
        
        
        
        
        ######  CENTRAL PART OF THE WIDGET  ######
        
        central_part = QTabWidget()
        
        self.__tabRover = TabRover()
        self.__tabBase = TabBase()
        self.__tabPostProcessing = TabPostProcessing()
        self.__tabSatellites = TabSatellites()
        
        central_part.addTab(self.__tabRover,'Rover')
        central_part.addTab(self.__tabBase,'Base')   
        central_part.addTab(self.__tabPostProcessing,'Post Processing')
        
 
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
