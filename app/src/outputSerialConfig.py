#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:45:39 2019

@author: edgar
"""


from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel
from functools import partial


class OutputSerialConfig(QWidget):
    '''
    Panel where the user can decide if he wants the output of the base acquisition to be sent to the radio for 
    transmission to the rover
    If yes set the details of the sending to the radio
    Has default parameters
    Inherits from QWidget
    
    Parameters:
        Core : 
            private Boolean output2_flag : wether output shall be transmitted to the radio
            private list output2_format : wich format shall be applied (rtcm or ubx)
            private int output2_index_format
            private list output2_port : through wich serial port output shall pass to the radio
            private int output2_index_port
            private list output2_bitrate : at wich bit rate shall it be sent
            private int output2_index_bitrate
            private list output2_bytesize : what would be the bytesize (for octet shall be 8)
            private int output2_index_bytesize
            private list output2_parity : 
            private int output2_index_parity
            private list output2_stopbits : 
            private int output2_index_stopbits
            private list output2_flowcontrol : 
            private int output2_index_flowcontrol
        UI : 
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
        self.__output2_flag = False
        self.__output2_format=(['ubx','rtcm3'])
        self.__output2_port = (['serial0','serial1','ttyACM0','ttyACM1','ttyUSB0','ttyUSB1'])
        self.__output2_bitrate = (['300','600','1200','2400','4800','9600','19200','38400','57600','115200','230400'])
        self.__output2_bytesize = (['7','8'])   #[7 8]
        self.__output2_parity = (['n','e','o'])   #[n e o]
        self.__output2_stopbits = (['1','2'])    #[1 2]
        self.__output2_flowcontrol = (['off','rtscts']) #[off rtscts]
        
        
        # Default Output(Serial) stream configration
        self.__output2_index_format = 0
        self.__output2_index_port=4
        self.__output2_index_bitrate = 9
        self.__output2_index_bytesize = 1
        self.__output2_index_parity = 0
        self.__output2_index_stopbits = 0
        self.__output2_index_flowcontrol = 0
        

        # Setting the elements on the layout
        self.__output2_b = QCheckBox("Enable",self)
        self.__output2_b.setChecked(self.__output2_flag)
        
        self.__format_list=QComboBox(self)
        self.__format_list.addItems(['UBX','RTCM3'])
        self.__format_list.setCurrentIndex(self.__output2_index_format)

        self.__port_list=QComboBox(self)
        self.__port_list.addItems(self.__output2_port)
        self.__port_list.setCurrentIndex(self.__output2_index_port)

        self.__bitrate_list=QComboBox(self)
        self.__bitrate_list.addItems(self.__output2_bitrate)
        self.__bitrate_list.setCurrentIndex(self.__output2_index_bitrate)

        self.__bytesize_list=QComboBox(self)
        self.__bytesize_list.addItems(['7 bits','8 bits'])
        self.__bytesize_list.setCurrentIndex(self.__output2_index_bytesize)

        self.__parity_list=QComboBox(self)
        self.__parity_list.addItems(['None','Even','Odd'])
        self.__parity_list.setCurrentIndex(self.__output2_index_parity)

        self.__stopbits_list=QComboBox(self)
        self.__stopbits_list.addItems(['1 bit','2 bits'])
        self.__stopbits_list.setCurrentIndex(self.__output2_index_stopbits)

        self.__flowcontrol_list=QComboBox(self)
        self.__flowcontrol_list.addItems(['None','RTS/CTS'])
        self.__flowcontrol_list.setCurrentIndex(self.__output2_index_flowcontrol)
        
        
        # default activated parameters
        self.typeChanged()
        self.__output2_b.stateChanged.connect(partial(self.typeChanged))
        

        #Setting the Layout
        grid=QGridLayout()
        
        grid.addWidget(self.__output2_b,0,0)
        grid.addWidget(QLabel('Format'),0,2)
        grid.addWidget(self.__format_list,0,3)
        
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
      
        
    def typeChanged(self):
        '''
        Check wether the output is enabled and edit the UI
        '''
        
        if self.__output2_b.isChecked() == True: 
            
            self.__format_list.setDisabled(False)
            self.__port_list.setDisabled(False)
            self.__bitrate_list.setDisabled(False)
            self.__bytesize_list.setDisabled(False)
            self.__parity_list.setDisabled(False)
            self.__stopbits_list.setDisabled(False)
            self.__flowcontrol_list.setDisabled(False)
            
        else:
            
            self.__format_list.setDisabled(True)
            self.__port_list.setDisabled(True)
            self.__bitrate_list.setDisabled(True)
            self.__bytesize_list.setDisabled(True)
            self.__parity_list.setDisabled(True)
            self.__stopbits_list.setDisabled(True)
            self.__flowcontrol_list.setDisabled(True)
            
    
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''

        self.__output2_flag = self.__output2_b.isChecked()
        self.__output2_index_format = self.__format_list.currentIndex()
        self.__output2_index_port = self.__port_list.currentIndex()
        self.__output2_index_index_bitrate = self.__bitrate_list.currentIndex()
        self.__output2_index_bytesize = self.__bytesize_list.currentIndex()
        self.__output2_index_parity = self.__parity_list.currentIndex()
        self.__output2_index_stopbits = self.__stopbits_list.currentIndex()
        self.__output2_index_flowcontrol = self.__flowcontrol_list.currentIndex()
        
        
    def getOptions(self):
        '''
        Returns Logs options 
        '''
        
        self.apply()       
        
        return (self.__output2_flag,
                self.__output2_format[self.__output2_index_format],
                self.__output2_port[self.__output2_index_port],
               self.__output2_bitrate[self.__output2_index_bitrate],
               self.__output2_bytesize[self.__output2_index_bytesize],
               self.__output2_parity[self.__output2_index_parity],
               self.__output2_stopbits[self.__output2_index_stopbits],
               self.__output2_flowcontrol[self.__output2_index_flowcontrol])