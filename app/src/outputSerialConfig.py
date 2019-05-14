#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:45:39 2019

@author: edgar
"""


from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel


class OutputSerialConfig(QWidget):
    '''
    Panel where the user can decide the Output Serial parameters of acquisition
    Has default parameters
    Inherits from QWidget
    
    Parameters:
        private QCheckBox output2_b
        private QComboBox port_list
        private QComboBox bitrate_list
        private QComboBox bytesize_list
        private QComboBox parity_list
        private QComboBox stopbits_list
        private QComboBox flowcontrol_list

    '''
    
    def __init__(self,parent=None):
        super().__init__()

        
        # Possible values for tthe OutputSerial stream configuration
        output2_flag = False
        output2_port = (['serial0','serial1','ttyACM0','ttyACM1','ttyUSB0','ttyUSB1'])
        output2_bitrate = (['300','600','1200','2400','4800','9600','19200','38400','57600','115200','230400'])
        output2_bytesize = (['7 bits','8 bits'])   #[7 8]
        output2_parity = (['None','Even','Odd'])   #[n e o]
        output2_stopbits = (['1 bit','2 bits'])    #[1 2]
        output2_flowcontrol = (['None','RTS/CTS']) #[off rtscts]
        
        
        # Default Output(Serial) stream configration
        output2_index_port=4
        output2_index_bitrate = 9
        output2_index_bytesize = 1
        output2_index_parity = 0
        output2_index_stopbits = 0
        output2_index_flowcontrol = 0
        

        # Setting the elements on the layout
        self.__output2_b = QCheckBox("Enable",self)
        self.__output2_b.setChecked(output2_flag)

        self.__port_list=QComboBox(self)
        self.__port_list.addItems(output2_port)
        self.__port_list.setCurrentIndex(output2_index_port)

        self.__bitrate_list=QComboBox(self)
        self.__bitrate_list.addItems(output2_bitrate)
        self.__bitrate_list.setCurrentIndex(output2_index_bitrate)

        self.__bytesize_list=QComboBox(self)
        self.__bytesize_list.addItems(output2_bytesize)
        self.__bytesize_list.setCurrentIndex(output2_index_bytesize)

        self.__parity_list=QComboBox(self)
        self.__parity_list.addItems(output2_parity)
        self.__parity_list.setCurrentIndex(output2_index_parity)

        self.__stopbits_list=QComboBox(self)
        self.__stopbits_list.addItems(output2_stopbits)
        self.__stopbits_list.setCurrentIndex(output2_index_stopbits)

        self.__flowcontrol_list=QComboBox(self)
        self.__flowcontrol_list.addItems(output2_flowcontrol)
        self.__flowcontrol_list.setCurrentIndex(output2_index_flowcontrol)
        

        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(self.__output2_b,0,0)
        grid.addWidget(QLabel('Port'),1,0)
        grid.addWidget(self.__port_list,1,1)
        grid.addWidget(QLabel('Bit Rate'),1,2)
        grid.addWidget(self.__bitrate_list,1,3)
        grid.addWidget(QLabel('Byte Size'),2,0)
        grid.addWidget(self.__bytesize_list,2,1)
        grid.addWidget(QLabel('Parity'),2,2)
        grid.addWidget(self.__parity_list,2,3)
        grid.addWidget(QLabel('Stop Bits'),3,0)
        grid.addWidget(self.__stopbits_list,3,1)
        grid.addWidget(QLabel('Flow Control'),3,2)
        grid.addWidget(self.__flowcontrol_list,3,3)
        self.setLayout(grid)