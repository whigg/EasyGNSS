#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:41:10 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel

class InputConfig(QWidget):
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
        input_port = (['serial0','serial1','ttyACM0','ttyACM1','ttyUSB0','ttyUSB1'])
        input_bitrate = (['300','600','1200','2400','4800','9600','19200','38400','57600','115200','230400'])
        input_bytesize = (['7 bits','8 bits'])   #[7 8]
        input_parity = (['None','Even','Odd'])   #[n e o]
        input_stopbits = (['1 bit','2 bits'])    #[1 2]
        input_flowcontrol = (['None','RTS/CTS']) #[off rtscts]
        
        # Default Input stream configuration
        input_index_port=2
        input_index_bitrate = 9
        input_index_bytesize = 1
        input_index_parity = 0
        input_index_stopbits = 0
        input_index_flowcontrol = 0

        # Setting the elements on the layout
        self.port_list=QComboBox(self)
        self.port_list.addItems(input_port)
        self.port_list.setCurrentIndex(input_index_port)

        self.bitrate_list=QComboBox(self)
        self.bitrate_list.addItems(input_bitrate)
        self.bitrate_list.setCurrentIndex(input_index_bitrate)

        self.bytesize_list=QComboBox(self)
        self.bytesize_list.addItems(input_bytesize)
        self.bytesize_list.setCurrentIndex(input_index_bytesize)

        self.parity_list=QComboBox(self)
        self.parity_list.addItems(input_parity)
        self.parity_list.setCurrentIndex(input_index_parity)

        self.stopbits_list=QComboBox(self)
        self.stopbits_list.addItems(input_stopbits)
        self.stopbits_list.setCurrentIndex(input_index_stopbits)

        self.flowcontrol_list=QComboBox(self)
        self.flowcontrol_list.addItems(input_flowcontrol)
        self.flowcontrol_list.setCurrentIndex(input_index_flowcontrol)

        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(QLabel('Port'),0,0)
        grid.addWidget(self.port_list,0,1)
        grid.addWidget(QLabel('Bit Rate'),0,2)
        grid.addWidget(self.bitrate_list,0,3)
        grid.addWidget(QLabel('Byte Size'),1,0)
        grid.addWidget(self.bytesize_list,1,1)
        grid.addWidget(QLabel('Parity'),1,2)
        grid.addWidget(self.parity_list,1,3)
        grid.addWidget(QLabel('Stop Bits'),2,0)
        grid.addWidget(self.stopbits_list,2,1)
        grid.addWidget(QLabel('Flow Control'),2,2)
        grid.addWidget(self.flowcontrol_list,2,3)
        self.setLayout(grid)