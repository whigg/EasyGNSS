#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:41:10 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel

class InputConfig(QWidget):
    '''
    Panel where the user can decide the Input parameters of the acquisition, how and through where
    does the data from the antenna is transmitted to RTKLIB
    !!!! For base corrections sent through radio, the rover shall have exact same parameters (except for the port) as
    the OutputSerial of the base
    Has default parameters
    Inherits from QWidget
    
    Attributes:
        Core :
            private list input_port : through wich serial port shall data pass
            private list input_bitrate : at wich bitrate shall it be sent
            private list input_bytesize : at wich bytesize (for octet shall be 8)
            private list input_parity : 
            private list input_stopbits : 
            private list input_flowcontrol : 
            
            private int input_index_port
            private int input_index_bitrate
            private int input_index_bytesize
            private int input_index_parity
            private int input_index_stopbits
            private int input_index_flowcontrol
        UI : 
            private QComboBox port_list
            private QComboBox bitrate_list
            private QComboBox bytesize_list
            private QComboBox  parity_list
            private QComboBox  stopbits_list
            private QComboBox flowcontrol_list
        
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        # Possible values for Input stream configuration
        self.__input_port = (['serial0','serial1','ttyACM0','ttyACM1','ttyUSB0','ttyUSB1'])
        self.__input_bitrate = (['300','600','1200','2400','4800','9600','19200','38400','57600','115200','230400'])
        self.__input_bytesize = (['7','8'])   #[7 8]
        self.__input_parity = (['n','e','o'])   #[n e o]
        self.__input_stopbits = (['1','2'])    #[1 2]
        self.__input_flowcontrol = (['off','rtscts']) #[off rtscts]
        
        # Default Input stream configuration
        self.__input_index_port=2
        self.__input_index_bitrate = 9
        self.__input_index_bytesize = 1
        self.__input_index_parity = 0
        self.__input_index_stopbits = 0
        self.__input_index_flowcontrol = 0
        

        # Setting the elements on the layout
        self.__port_list=QComboBox(self)
        self.__port_list.addItems(self.__input_port)
        self.__port_list.setCurrentIndex(self.__input_index_port)

        self.__bitrate_list=QComboBox(self)
        self.__bitrate_list.addItems(self.__input_bitrate)
        self.__bitrate_list.setCurrentIndex(self.__input_index_bitrate)

        self.__bytesize_list=QComboBox(self)
        self.__bytesize_list.addItems(['7 bits','8 bits'])
        self.__bytesize_list.setCurrentIndex(self.__input_index_bytesize)

        self.__parity_list=QComboBox(self)
        self.__parity_list.addItems(['None','Even','Odd'])
        self.__parity_list.setCurrentIndex(self.__input_index_parity)

        self.__stopbits_list=QComboBox(self)
        self.__stopbits_list.addItems(['1 bit','2 bits'])
        self.__stopbits_list.setCurrentIndex(self.__input_index_stopbits)

        self.__flowcontrol_list=QComboBox(self)
        self.__flowcontrol_list.addItems(['None','RTS/CTS'])
        self.__flowcontrol_list.setCurrentIndex(self.__input_index_flowcontrol)

        #Setting the Layout
        grid=QGridLayout()
        
        grid.addWidget(QLabel('Port'),0,0)
        grid.addWidget(self.__port_list,0,1)
        grid.addWidget(QLabel('Bit Rate'),0,2)
        grid.addWidget(self.__bitrate_list,0,3)
        
        grid.addWidget(QLabel('Byte Size'),1,0)
        grid.addWidget(self.__bytesize_list,1,1)
        grid.addWidget(QLabel('Parity'),1,2)
        grid.addWidget(self.__parity_list,1,3)
        
        grid.addWidget(QLabel('Stop Bits'),2,0)
        grid.addWidget(self.__stopbits_list,2,1)
        grid.addWidget(QLabel('Flow Control'),2,2)
        grid.addWidget(self.__flowcontrol_list,2,3)
        
        self.setLayout(grid)
        
        
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''        
        self.__input_index_port = self.__port_list.currentIndex()
        self.__input_index_index_bitrate = self.__bitrate_list.currentIndex()
        self.__input_index_bytesize = self.__bytesize_list.currentIndex()
        self.__input_index_parity = self.__parity_list.currentIndex()
        self.__input_index_stopbits = self.__stopbits_list.currentIndex()
        self.__input_index_flowcontrol = self.__flowcontrol_list.currentIndex()
        
        
    def getOptions(self):
        '''
        Returns Input options in a list
        '''
        
        self.apply()
        
        
        return (self.__input_port[self.__input_index_port],
                   self.__input_bitrate[self.__input_index_bitrate],
                   self.__input_bytesize[self.__input_index_bytesize],
                   self.__input_parity[self.__input_index_parity],
                   self.__input_stopbits[self.__input_index_stopbits],
                   self.__input_flowcontrol[self.__input_index_flowcontrol])
    
        