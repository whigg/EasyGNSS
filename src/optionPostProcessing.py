#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:47:54 2019

@author: pc-apple
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QLabel

class OptionPostProcessing(QWidget):
    '''
    Panel where the user can decide the Input parameters of the acquisition
    Has default parameters
    Inherits from QWidget
    
    Attributes:
        public QComboBox port_list
        public QComboBox bitrate_list
        public QComboBox bytesize_list
        public QComboBox parity_list
        public QComboBox stopbits_list
        public QComboBox flowcontrol_list
        
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        # Possible values for Input stream configuration
        input_mode = (["Static", "Kinematic"])
        input_format = (["XYZ", "llh"])
        
        # Default Input stream configuration
        input_index_mode = 0
        input_index_format = 0

        # Setting the elements on the layout
        self.mode_list=QComboBox(self)
        self.mode_list.addItems(input_mode)
        self.mode_list.setCurrentIndex(input_index_mode)

        self.format_list=QComboBox(self)
        self.format_list.addItems(input_format)
        self.format_list.setCurrentIndex(input_index_format)

        #Setting the Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Calculus mode'))
        layout.addWidget(self.mode_list)
        layout.addWidget(QLabel('Output format'))
        layout.addWidget(self.format_list)
        self.setLayout(layout)