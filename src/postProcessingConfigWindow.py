#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:50:24 2019

@author: pc-apple
"""

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QFont

from optionPostProcessing import OptionPostProcessing
from stationPostProcessing import StationPostProcessing

class PostProcessingConfigWindow:
    '''
    Class RoverConfigWindow is a QDialog subwindow that opens when TabRover.__confi_b is clicked
    It contains all the changeable parameters for the acquisition sorted by type
    
    Attributtes:
        private QDialog window 
        private InputConfig tab_input
        private CorrectionConfig tab_corr
        private SolConfig tab_sol
        private LogConfig tab_log
        private BasePosConfig_Rover tab_basepos
    '''
    def __init__(self, parent=None):
        
        self.__window = QDialog(parent)
        self.__parent = parent
        self.__window.setFont(QFont('Helvetica',18))

        self.__window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.__window.setGeometry(0, 0, 700, 500)

        
        ######  CONFIGURATION PART  ######
        tabs = QTabWidget()

        self.__tab_option = OptionPostProcessing()
        self.__tab_station = StationPostProcessing()
        
        tabs.addTab(self.__tab_option,"Options")
        tabs.addTab(self.__tab_station, "Stations")
        
        ######  BUTTONS  ######

        self.__apply_button= QPushButton('Apply')
#        self.__apply_button.clicked.connect(self.applyParam)
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